"""
Configuration management for the Claude Desktop Bridge.

Handles configuration loading, directory setup, and validation.
"""

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class BridgeConfig(BaseModel):
    """Configuration for the Claude Desktop Bridge.

    This configuration controls all aspects of the bridge behavior including
    polling intervals, concurrency limits, and file retention policies.
    """

    queue_path: Path = Field(
        default=Path("/mnt/c/Users/din18/.claude-bridge"),
        description="Root directory for all bridge operations"
    )
    poll_interval_ms: int = Field(
        default=500,
        description="Polling interval in milliseconds when inotify unavailable",
        ge=100,
        le=10000
    )
    inotify_enabled: bool = Field(
        default=True,
        description="Whether to use inotify for file watching (Linux only)"
    )
    inotify_fallback_poll_ms: int = Field(
        default=2000,
        description="Polling interval when inotify is enabled but no events occur",
        ge=500,
        le=30000
    )
    inotify_health_check_interval: int = Field(
        default=10,
        description="Seconds between inotify health checks",
        ge=5,
        le=300
    )
    max_concurrent_tasks: int = Field(
        default=5,
        description="Maximum number of tasks to process concurrently",
        ge=1,
        le=50
    )
    default_ttl_seconds: int = Field(
        default=300,
        description="Default time-to-live for tasks in seconds",
        ge=10,
        le=3600
    )
    archive_retention_days: int = Field(
        default=7,
        description="Days to retain archived task files",
        ge=1,
        le=365
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("queue_path", mode="before")
    @classmethod
    def validate_queue_path(cls, v):
        """Ensure queue_path is a Path object."""
        if isinstance(v, str):
            return Path(v)
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Ensure log_level is valid."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()

    def ensure_directories(self) -> None:
        """Create all required bridge directories if they don't exist.

        Creates the following directory structure:
        - queue/: Incoming task files
        - processing/: Tasks currently being processed
        - responses/: Completed task responses
        - dead-letter/: Failed tasks that couldn't be processed
        - archive/: Historical tasks (cleaned up after retention period)
        - logs/: Bridge operation logs
        - context/: Shared context files
        """
        subdirs = [
            "queue",
            "processing",
            "responses",
            "dead-letter",
            "archive",
            "logs",
            "context",
        ]

        # Create root directory
        self.queue_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        for subdir in subdirs:
            (self.queue_path / subdir).mkdir(exist_ok=True)

    def write_default_config(self) -> None:
        """Write default configuration to config.json if it doesn't exist.

        This creates a user-editable config file at {queue_path}/config.json
        with the current configuration values.
        """
        config_file = self.queue_path / "config.json"

        if config_file.exists():
            return

        # Ensure directory exists
        self.queue_path.mkdir(parents=True, exist_ok=True)

        # Write config
        with open(config_file, "w") as f:
            json.dump(self.to_safe_dict(), f, indent=2)

    def to_safe_dict(self) -> dict:
        """Convert configuration to a dictionary suitable for serialization.

        Returns:
            Dictionary with all config values, Paths converted to strings
        """
        data = self.model_dump()
        # Convert Path to string for JSON serialization
        data["queue_path"] = str(data["queue_path"])
        return data

    @classmethod
    def load_config(cls, path: Optional[Path] = None) -> "BridgeConfig":
        """Load configuration from file or use defaults.

        Args:
            path: Optional path to config.json. If None, uses default location
                  at {queue_path}/config.json

        Returns:
            BridgeConfig instance with loaded or default values
        """
        # If no path provided, use default
        if path is None:
            default_config = cls()
            path = default_config.queue_path / "config.json"

        # If config file doesn't exist, return defaults
        if not path.exists():
            return cls()

        # Load from file
        with open(path) as f:
            data = json.load(f)

        return cls(**data)
