"""Pydantic schema models for the Desktop-Code bridge."""

from datetime import datetime, timezone
from enum import StrEnum
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskType(StrEnum):
    """Type of task being sent across the bridge."""

    MESSAGE = "message"
    COMMAND = "command"
    QUERY = "query"
    DELEGATE = "delegate"


class TaskSource(BaseModel):
    """Source information for a task."""

    agent: Literal["desktop", "code"]
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None


class TaskPayload(BaseModel):
    """Payload data for a task."""

    message: str
    context: Optional[str] = None
    args: Optional[list[str]] = None
    cwd: Optional[str] = None


class Task(BaseModel):
    """A task sent across the bridge."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: TaskType
    payload: TaskPayload
    source: TaskSource
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = 300
    priority: int = Field(default=5, ge=1, le=10)
    delegation_chain: list[str] = Field(default_factory=list)
    response_required: bool = True
    metadata: dict = Field(default_factory=dict)

    def is_expired(self) -> bool:
        """Check if the task has expired based on TTL."""
        now = datetime.now(timezone.utc)
        age_seconds = (now - self.created_at).total_seconds()
        return age_seconds > self.ttl_seconds

    def to_json(self) -> str:
        """Serialize task to JSON string."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, data: str) -> "Task":
        """Deserialize task from JSON string."""
        return cls.model_validate_json(data)


class ResponseError(BaseModel):
    """Error information in a response."""

    code: str
    message: str
    details: Optional[dict] = None


class Response(BaseModel):
    """Response to a task."""

    task_id: str
    status: Literal["success", "error", "timeout", "rejected"]
    result: Optional[dict] = None
    error: Optional[ResponseError] = None
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processing_ms: Optional[int] = None
