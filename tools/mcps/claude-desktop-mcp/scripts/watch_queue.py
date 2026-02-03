#!/usr/bin/env python3
"""
Bridge Queue Watcher - Monitors queue for tasks from Claude Desktop.

Usage:
    python scripts/watch_queue.py [--config PATH]

Or after pip install:
    watch-queue [--config PATH]
"""

import argparse
import logging
import signal
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bridge.config import BridgeConfig
from bridge.processor import TaskProcessor
from bridge.watcher import QueueWatcher


def setup_logging(level: str):
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Bridge Queue Watcher")
    parser.add_argument("--config", type=Path, help="Path to config.json")
    args = parser.parse_args()

    # Load config
    config = BridgeConfig.load_config(args.config)

    # Setup logging
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)

    # Ensure directories exist
    config.ensure_directories()
    logger.info(f"Queue path: {config.queue_path}")

    # Write default config if missing
    config.write_default_config()

    # Create processor and watcher
    processor = TaskProcessor(config)
    watcher = QueueWatcher(config, processor)

    # Handle shutdown signals
    def shutdown(signum, frame):
        logger.info("Shutting down...")
        watcher.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Start watching (blocking)
    logger.info("Starting queue watcher...")
    logger.info(f"Watching: {config.queue_path / 'queue'}")
    logger.info(f"Max concurrent tasks: {config.max_concurrent_tasks}")

    try:
        watcher.start()
    except KeyboardInterrupt:
        logger.info("Interrupted")
    finally:
        watcher.stop()


if __name__ == "__main__":
    main()
