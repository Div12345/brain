"""Task processor for the Claude Desktop Bridge.

Handles task processing, command execution, and response generation.
"""

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from .config import BridgeConfig
from .schema import Response, ResponseError, Task, TaskType

logger = logging.getLogger(__name__)


class TaskProcessor:
    """Process tasks from the queue with type-specific handlers."""

    def __init__(self, config: BridgeConfig):
        """Initialize the task processor.

        Args:
            config: Bridge configuration
        """
        self.config = config
        self.handlers: dict[TaskType, Callable[[Task], Response]] = {
            TaskType.MESSAGE: self._handle_message,
            TaskType.COMMAND: self._handle_command,
            TaskType.QUERY: self._handle_query,
            TaskType.DELEGATE: self._handle_delegate,
        }

    def process(self, task: Task) -> Response:
        """Process a task and return a response.

        Args:
            task: Task to process

        Returns:
            Response object with result or error
        """
        start_time = datetime.now(timezone.utc)

        try:
            handler = self.handlers.get(task.type)
            if not handler:
                return Response(
                    task_id=task.id,
                    status="error",
                    error=ResponseError(
                        code="UNKNOWN_TASK_TYPE",
                        message=f"Unknown task type: {task.type}",
                    ),
                )

            response = handler(task)

            # Calculate processing time
            end_time = datetime.now(timezone.utc)
            processing_ms = int((end_time - start_time).total_seconds() * 1000)
            response.processing_ms = processing_ms

            return response

        except Exception as e:
            logger.exception(f"Error processing task {task.id}")
            return Response(
                task_id=task.id,
                status="error",
                error=ResponseError(
                    code="PROCESSING_ERROR",
                    message="An error occurred while processing the task",
                    details={"type": type(e).__name__},
                ),
            )

    def _handle_message(self, task: Task) -> Response:
        """Handle MESSAGE task by writing to context.

        Args:
            task: Task with message payload

        Returns:
            Response with acknowledgment
        """
        context_file = self.config.queue_path / "context" / f"{task.id}.json"

        try:
            context_data = {
                "task_id": task.id,
                "message": task.payload.message,
                "context": task.payload.context,
                "source": task.source.model_dump(),
                "created_at": task.created_at.isoformat(),
            }

            with open(context_file, "w") as f:
                json.dump(context_data, f, indent=2)

            return Response(
                task_id=task.id,
                status="success",
                result={
                    "acknowledged": True,
                    "context_file": str(context_file),
                },
            )

        except Exception as e:
            logger.exception(f"Error writing context for task {task.id}")
            return Response(
                task_id=task.id,
                status="error",
                error=ResponseError(
                    code="CONTEXT_WRITE_ERROR",
                    message="Failed to write context",
                ),
            )

    def _handle_command(self, task: Task) -> Response:
        """Handle COMMAND task by executing predefined commands.

        Args:
            task: Task with command payload

        Returns:
            Response with command result
        """
        command = task.payload.message.lower()

        command_map = {
            "status": self._cmd_status,
            "read_file": self._cmd_read_file,
            "list_tasks": self._cmd_list_tasks,
        }

        handler = command_map.get(command)
        if not handler:
            return Response(
                task_id=task.id,
                status="error",
                error=ResponseError(
                    code="UNKNOWN_COMMAND",
                    message=f"Unknown command: {command}",
                    details={"available_commands": list(command_map.keys())},
                ),
            )

        try:
            result = handler(task.payload)
            return Response(
                task_id=task.id,
                status="success",
                result=result,
            )
        except Exception as e:
            logger.exception(f"Error executing command {command}")
            return Response(
                task_id=task.id,
                status="error",
                error=ResponseError(
                    code="COMMAND_ERROR",
                    message="Command execution failed",
                ),
            )

    def _handle_query(self, task: Task) -> Response:
        """Handle QUERY task by returning state data.

        Args:
            task: Task with query payload

        Returns:
            Response with requested state data
        """
        query_type = task.payload.message.lower()

        try:
            if query_type == "active_tasks":
                processing_dir = self.config.queue_path / "processing"
                tasks = [f.name for f in processing_dir.glob("*.json")]
                return Response(
                    task_id=task.id,
                    status="success",
                    result={"active_tasks": tasks},
                )

            elif query_type == "config":
                return Response(
                    task_id=task.id,
                    status="success",
                    result={"config": self.config.to_safe_dict()},
                )

            else:
                return Response(
                    task_id=task.id,
                    status="error",
                    error=ResponseError(
                        code="UNKNOWN_QUERY",
                        message=f"Unknown query type: {query_type}",
                        details={"available_queries": ["active_tasks", "config"]},
                    ),
                )

        except Exception as e:
            logger.exception(f"Error handling query {query_type}")
            return Response(
                task_id=task.id,
                status="error",
                error=ResponseError(
                    code="QUERY_ERROR",
                    message="Query execution failed",
                ),
            )

    def _handle_delegate(self, task: Task) -> Response:
        """Handle DELEGATE task by checking chain length and re-queuing.

        Args:
            task: Task to delegate

        Returns:
            Response indicating delegation status
        """
        max_chain_length = 3

        if len(task.delegation_chain) >= max_chain_length:
            return Response(
                task_id=task.id,
                status="rejected",
                error=ResponseError(
                    code="MAX_DELEGATION_DEPTH",
                    message=f"Maximum delegation chain length ({max_chain_length}) reached",
                    details={"chain": task.delegation_chain},
                ),
            )

        try:
            # Update delegation chain
            task.delegation_chain.append(task.source.agent)

            # Write back to queue
            queue_file = self.config.queue_path / "queue" / f"{task.id}.json"
            with open(queue_file, "w") as f:
                f.write(task.to_json())

            return Response(
                task_id=task.id,
                status="success",
                result={
                    "delegated": True,
                    "chain_length": len(task.delegation_chain),
                },
            )

        except Exception as e:
            logger.exception(f"Error delegating task {task.id}")
            return Response(
                task_id=task.id,
                status="error",
                error=ResponseError(
                    code="DELEGATION_ERROR",
                    message="Task delegation failed",
                ),
            )

    def _cmd_status(self, payload) -> dict:
        """Return system status.

        Args:
            payload: Task payload (unused)

        Returns:
            Dictionary with system status
        """
        queue_dir = self.config.queue_path / "queue"
        processing_dir = self.config.queue_path / "processing"
        responses_dir = self.config.queue_path / "responses"
        dead_letter_dir = self.config.queue_path / "dead-letter"

        return {
            "status": "running",
            "queue_size": len(list(queue_dir.glob("*.json"))),
            "processing": len(list(processing_dir.glob("*.json"))),
            "responses": len(list(responses_dir.glob("*.json"))),
            "dead_letter": len(list(dead_letter_dir.glob("*.json"))),
            "config": self.config.to_safe_dict(),
        }

    def _cmd_read_file(self, payload) -> dict:
        """Read file with safety checks.

        Args:
            payload: Task payload with file path in args[0]

        Returns:
            Dictionary with file contents

        Raises:
            ValueError: If file path not provided or invalid
        """
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

        if not payload.args or len(payload.args) == 0:
            raise ValueError("File path required in args[0]")

        file_path = Path(payload.args[0])

        # Security: Check for symlinks BEFORE resolve (resolve follows symlinks)
        if file_path.is_symlink():
            raise ValueError("Symlinks are not allowed")

        # Safety check: must be within queue_path
        try:
            file_path = file_path.resolve()
            queue_path = self.config.queue_path.resolve()

            # Fix PATH TRAVERSAL: Use is_relative_to instead of startswith
            if not file_path.is_relative_to(queue_path):
                raise ValueError("File path must be within queue directory")
        except Exception:
            raise ValueError("Invalid file path")

        if not file_path.exists():
            raise ValueError("File not found")

        if not file_path.is_file():
            raise ValueError("Path is not a file")

        # Security: Check file size limit
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"File exceeds size limit")

        # Read file
        with open(file_path, "r") as f:
            content = f.read()

        return {
            "file_path": str(file_path.relative_to(queue_path)),  # Sanitize path in response
            "content": content,
            "size_bytes": file_size,
        }

    def _cmd_list_tasks(self, payload) -> dict:
        """List tasks in processing directory.

        Args:
            payload: Task payload (unused)

        Returns:
            Dictionary with task list
        """
        processing_dir = self.config.queue_path / "processing"
        tasks = []

        for task_file in processing_dir.glob("*.json"):
            try:
                with open(task_file, "r") as f:
                    task_data = json.load(f)
                    tasks.append({
                        "id": task_data.get("id"),
                        "type": task_data.get("type"),
                        "created_at": task_data.get("created_at"),
                        "file": task_file.name,
                    })
            except Exception as e:
                logger.warning(f"Error reading task file {task_file}: {e}")

        return {
            "tasks": tasks,
            "count": len(tasks),
        }


class ResponseWriter:
    """Write responses to the responses directory with atomic operations."""

    def __init__(self, config: BridgeConfig):
        """Initialize the response writer.

        Args:
            config: Bridge configuration
        """
        self.config = config

    def write_response(self, response: Response, notify: bool = True) -> Path:
        """Write response to file atomically.

        Args:
            response: Response to write
            notify: Whether to notify desktop (requires notify module)

        Returns:
            Path to written response file
        """
        responses_dir = self.config.queue_path / "responses"
        response_file = responses_dir / f"{response.task_id}.json"
        temp_file = responses_dir / f"{response.task_id}.tmp"

        try:
            # Write to temporary file
            with open(temp_file, "w") as f:
                json.dump(response.model_dump(), f, indent=2, default=str)

            # Atomic rename
            temp_file.rename(response_file)

            # Notify desktop if requested
            if notify:
                try:
                    # Import here to avoid circular dependency
                    from .notify import notify_desktop
                    notify_desktop(response)  # Only takes response, not config
                except ImportError:
                    logger.debug("Notify module not available yet")

            return response_file

        except Exception as e:
            logger.exception(f"Error writing response for task {response.task_id}")
            # Clean up temp file if it exists
            if temp_file.exists():
                temp_file.unlink()
            raise


def claim_task(task_file: Path, processing_dir: Path) -> Optional[Path]:
    """Claim a task by moving it to processing directory.

    Args:
        task_file: Path to task file in queue
        processing_dir: Path to processing directory

    Returns:
        Path to claimed task file in processing directory, or None if claim failed
    """
    try:
        dest_file = processing_dir / task_file.name
        shutil.move(str(task_file), str(dest_file))
        return dest_file
    except Exception as e:
        logger.warning(f"Failed to claim task {task_file}: {e}")
        return None


def archive_task(task_file: Path, archive_dir: Path) -> None:
    """Archive a completed task.

    Args:
        task_file: Path to task file in processing
        archive_dir: Path to archive directory
    """
    try:
        dest_file = archive_dir / task_file.name
        shutil.move(str(task_file), str(dest_file))
        logger.debug(f"Archived task {task_file.name}")
    except Exception as e:
        logger.error(f"Failed to archive task {task_file}: {e}")


def expire_task(task_file: Path, dead_letter_dir: Path) -> None:
    """Move expired task to dead-letter queue.

    Args:
        task_file: Path to expired task file
        dead_letter_dir: Path to dead-letter directory
    """
    try:
        dest_file = dead_letter_dir / task_file.name
        shutil.move(str(task_file), str(dest_file))
        logger.warning(f"Expired task moved to dead-letter: {task_file.name}")
    except Exception as e:
        logger.error(f"Failed to expire task {task_file}: {e}")
