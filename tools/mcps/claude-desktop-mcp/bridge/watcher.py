"""
Hybrid file watching system for the Claude Desktop Bridge.

Combines inotify (when available) with polling fallback for WSL2 reliability.
Includes concurrency control and health monitoring.
"""

import json
import logging
import threading
import time
from pathlib import Path
from typing import Callable, Optional, Set

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .config import BridgeConfig
from .processor import ResponseWriter, archive_task, expire_task
from .schema import Response, ResponseError, Task

logger = logging.getLogger(__name__)


class ConcurrencyController:
    """Controls concurrent task processing with atomic file-based claiming.

    Uses atomic file moves to ensure only one worker processes a task.
    Tracks active tasks and enforces max concurrency limits.
    """

    def __init__(self, max_concurrent: int, processing_dir: Path):
        """Initialize concurrency controller.

        Args:
            max_concurrent: Maximum number of concurrent tasks allowed
            processing_dir: Directory for in-flight task files
        """
        self.max_concurrent = max_concurrent
        self.processing_dir = processing_dir
        self._lock = threading.Lock()

    def count_active_tasks(self) -> int:
        """Count currently active tasks by scanning processing directory.

        Returns:
            Number of .json files in processing directory
        """
        try:
            return len(list(self.processing_dir.glob("*.json")))
        except Exception as e:
            logger.error(f"Failed to count active tasks: {e}")
            return 0

    def can_claim_task(self) -> bool:
        """Check if we can claim another task without exceeding limits.

        Returns:
            True if under concurrency limit, False otherwise
        """
        return self.count_active_tasks() < self.max_concurrent

    def claim_task(self, task_file: Path) -> Optional[Path]:
        """Atomically claim a task by moving it to processing directory.

        Uses atomic file move to ensure only one worker claims the task.

        Args:
            task_file: Path to task file in queue directory

        Returns:
            Path to claimed file in processing directory, or None if claim failed
        """
        with self._lock:
            # Check concurrency limit
            if not self.can_claim_task():
                logger.debug(f"Cannot claim task, at concurrency limit ({self.max_concurrent})")
                return None

            # Atomic move to processing directory
            dest = self.processing_dir / task_file.name
            try:
                task_file.rename(dest)
                logger.debug(f"Claimed task: {task_file.name}")
                return dest
            except FileNotFoundError:
                # Another worker claimed it first
                logger.debug(f"Task already claimed: {task_file.name}")
                return None
            except Exception as e:
                logger.error(f"Failed to claim task {task_file.name}: {e}")
                return None


class TaskFileHandler(FileSystemEventHandler):
    """Handles file system events for task files.

    Filters for .json files and invokes callback on creation.
    """

    def __init__(self, callback: Callable[[Path], None]):
        """Initialize handler with callback.

        Args:
            callback: Function to call when new task file detected
        """
        self.callback = callback

    def on_created(self, event):
        """Handle file creation events.

        Args:
            event: watchdog FileCreatedEvent
        """
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process .json files
        if file_path.suffix == ".json":
            logger.debug(f"Inotify detected new file: {file_path.name}")
            self.callback(file_path)


class HybridWatcher:
    """Hybrid file watcher using inotify + polling fallback.

    Uses watchdog Observer for inotify when available, with polling thread
    as fallback. Health check thread monitors inotify and switches to
    polling if events stop arriving.
    """

    def __init__(self, config: BridgeConfig, on_task: Callable[[Path], None]):
        """Initialize hybrid watcher.

        Args:
            config: Bridge configuration
            on_task: Callback for when task file detected
        """
        self.config = config
        self.on_task = on_task
        self.queue_dir = config.queue_path / "queue"

        # Tracking
        self._seen_files: Set[str] = set()
        self._last_inotify_event = time.time()
        self._stop_event = threading.Event()

        # Inotify setup
        self.observer: Optional[Observer] = None
        self._inotify_active = False

        # Threads
        self._polling_thread: Optional[threading.Thread] = None
        self._health_thread: Optional[threading.Thread] = None

    def start(self):
        """Start the hybrid watcher with inotify + polling."""
        logger.info("Starting hybrid watcher")

        # Try to start inotify
        if self.config.inotify_enabled:
            self._start_inotify()

        # Always start polling thread as fallback
        self._start_polling_thread()

        # Start health check thread if inotify is active
        if self._inotify_active:
            self._start_health_thread()

    def _start_inotify(self):
        """Start inotify-based watching."""
        try:
            self.observer = Observer()
            handler = TaskFileHandler(self._handle_task_file)
            self.observer.schedule(handler, str(self.queue_dir), recursive=False)
            self.observer.start()
            self._inotify_active = True
            self._last_inotify_event = time.time()
            logger.info("Inotify watcher started")
        except Exception as e:
            logger.warning(f"Failed to start inotify: {e}, using polling only")
            self._inotify_active = False

    def _start_polling_thread(self):
        """Start polling thread."""
        self._polling_thread = threading.Thread(
            target=self._polling_loop,
            name="PollingThread",
            daemon=True
        )
        self._polling_thread.start()
        logger.info(f"Polling thread started (interval: {self.config.poll_interval_ms}ms)")

    def _start_health_thread(self):
        """Start health check thread for inotify monitoring."""
        self._health_thread = threading.Thread(
            target=self._health_check_loop,
            name="HealthCheckThread",
            daemon=True
        )
        self._health_thread.start()
        logger.info("Health check thread started")

    def _handle_task_file(self, file_path: Path):
        """Handle detected task file.

        Tracks seen files to prevent duplicate processing.

        Args:
            file_path: Path to task file
        """
        # Update inotify timestamp
        self._last_inotify_event = time.time()

        # Prevent duplicate processing
        if file_path.name in self._seen_files:
            return

        self._seen_files.add(file_path.name)

        # Invoke callback
        try:
            self.on_task(file_path)
        except Exception as e:
            logger.error(f"Error processing task file {file_path.name}: {e}")

    def _polling_loop(self):
        """Polling loop that scans directory for new files.

        Uses different intervals based on inotify status:
        - If inotify active: slower polling as backup
        - If inotify inactive: faster polling as primary mechanism
        """
        while not self._stop_event.is_set():
            try:
                # Determine poll interval
                if self._inotify_active:
                    interval = self.config.inotify_fallback_poll_ms / 1000
                else:
                    interval = self.config.poll_interval_ms / 1000

                # Scan for files
                for task_file in self.queue_dir.glob("*.json"):
                    if task_file.name not in self._seen_files:
                        logger.debug(f"Polling detected new file: {task_file.name}")
                        self._handle_task_file(task_file)

                # Sleep
                self._stop_event.wait(interval)

            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                self._stop_event.wait(1)

    def _health_check_loop(self):
        """Health check loop that monitors inotify.

        If no inotify events for 30s but files exist in queue,
        assumes inotify is broken and logs warning.
        """
        while not self._stop_event.is_set():
            try:
                # Wait for check interval
                self._stop_event.wait(self.config.inotify_health_check_interval)

                if not self._inotify_active:
                    continue

                # Check if inotify is stale
                time_since_event = time.time() - self._last_inotify_event

                if time_since_event > 30:
                    # Check if there are pending files
                    pending_files = list(self.queue_dir.glob("*.json"))

                    if pending_files:
                        logger.warning(
                            f"Inotify health check FAILED: No events for {time_since_event:.1f}s "
                            f"but {len(pending_files)} files pending. Polling will handle them."
                        )

            except Exception as e:
                logger.error(f"Error in health check loop: {e}")

    def stop(self):
        """Stop all watcher threads cleanly."""
        logger.info("Stopping hybrid watcher")

        # Signal threads to stop
        self._stop_event.set()

        # Stop inotify observer
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=5)

        # Wait for threads
        if self._polling_thread:
            self._polling_thread.join(timeout=5)

        if self._health_thread:
            self._health_thread.join(timeout=5)

        logger.info("Hybrid watcher stopped")


class QueueWatcher:
    """High-level queue watcher that integrates HybridWatcher with TaskProcessor.

    Provides simple interface: start() and blocks until interrupted.
    """

    def __init__(self, config: BridgeConfig, processor):
        """Initialize queue watcher.

        Args:
            config: Bridge configuration
            processor: TaskProcessor instance to handle tasks
        """
        self.config = config
        self.processor = processor

        # Create concurrency controller
        processing_dir = config.queue_path / "processing"
        self.concurrency = ConcurrencyController(
            config.max_concurrent_tasks,
            processing_dir
        )

        # Create response writer
        self.response_writer = ResponseWriter(config)

        # Create hybrid watcher
        self.watcher = HybridWatcher(config, self._on_task_detected)

    def _on_task_detected(self, task_file: Path):
        """Handle detected task file.

        Attempts to claim task, then processes if successful.

        Args:
            task_file: Path to task file in queue directory
        """
        # Try to claim the task
        claimed_path = self.concurrency.claim_task(task_file)

        if claimed_path is None:
            # Either at concurrency limit or another worker claimed it
            return

        # Process the claimed task
        try:
            # Read task
            with open(claimed_path) as f:
                task_data = json.load(f)

            task = Task.model_validate(task_data)

            # Check TTL expiration before processing
            if task.is_expired():
                logger.warning(f"Task {task.id} has expired (TTL: {task.ttl_seconds}s)")
                dead_letter_dir = self.config.queue_path / "dead-letter"
                expire_task(claimed_path, dead_letter_dir)

                # Write timeout response if response required
                if task.response_required:
                    response = Response(
                        task_id=task.id,
                        status="timeout",
                        error=ResponseError(
                            code="TASK_EXPIRED",
                            message=f"Task expired after {task.ttl_seconds} seconds",
                        ),
                    )
                    self.response_writer.write_response(response, notify=True)
                return

            # Process via processor (correct method name)
            response = self.processor.process(task)

            # Write response if required
            if task.response_required:
                self.response_writer.write_response(response, notify=True)
                logger.info(f"Response written for task {task.id}: {response.status}")

            # Archive the task after successful processing
            archive_dir = self.config.queue_path / "archive"
            archive_task(claimed_path, archive_dir)

        except Exception as e:
            logger.error(f"Failed to process task {claimed_path.name}: {e}")

            # Move to dead-letter queue
            dead_letter_dir = self.config.queue_path / "dead-letter"

            try:
                claimed_path.rename(dead_letter_dir / claimed_path.name)
                logger.info(f"Moved failed task to dead-letter: {claimed_path.name}")
            except Exception as move_error:
                logger.error(f"Failed to move task to dead-letter: {move_error}")

    def start(self):
        """Start the queue watcher and block until interrupted.

        This is a blocking call that runs until KeyboardInterrupt or
        the watcher is stopped.
        """
        logger.info("Starting queue watcher")

        # Start the watcher
        self.watcher.start()

        # Block until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.watcher.stop()
