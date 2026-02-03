#!/usr/bin/env python3
"""
Structured logging for cc-scheduler.

Writes execution logs to brain/logs/scheduler/ in Obsidian-style markdown.
Maintains an index.jsonl for machine-readable queries.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import asdict

# Import locally to avoid circular
# from .executor import ExecutionResult
# from .capacity import Capacity

BRAIN_ROOT = Path.home() / "brain"
LOGS_DIR = BRAIN_ROOT / "logs" / "scheduler"


def ensure_logs_dir():
    """Create logs directory if needed."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def generate_run_id() -> str:
    """Generate unique run ID."""
    return datetime.now().strftime("run-%Y-%m-%d-%H%M%S")


def log_execution(
    task_name: str,
    run_id: str,
    success: bool,
    exit_code: int,
    output: str,
    started_at: datetime,
    ended_at: datetime,
    duration_seconds: float,
    capacity_before: Optional[dict] = None,
    capacity_after: Optional[dict] = None,
    error: Optional[str] = None,
) -> Path:
    """
    Write execution log as markdown with YAML frontmatter.

    Returns path to log file.
    """
    ensure_logs_dir()

    # Generate filename
    timestamp = started_at.strftime("%Y-%m-%d-%H%M")
    filename = f"{timestamp}-{task_name}.md"
    log_path = LOGS_DIR / filename

    # Build frontmatter
    frontmatter = {
        "task": task_name,
        "run_id": run_id,
        "started": started_at.isoformat(),
        "ended": ended_at.isoformat(),
        "duration_seconds": round(duration_seconds, 2),
        "status": "completed" if success else "failed",
        "exit_code": exit_code,
    }

    if capacity_before:
        frontmatter["capacity_before_5h"] = capacity_before.get("five_hour_percent", 0)
        frontmatter["capacity_before_7d"] = capacity_before.get("weekly_percent", 0)

    if capacity_after:
        frontmatter["capacity_after_5h"] = capacity_after.get("five_hour_percent", 0)
        frontmatter["capacity_after_7d"] = capacity_after.get("weekly_percent", 0)

    if error:
        frontmatter["error"] = error

    # Build markdown content
    content = "---\n"
    for key, value in frontmatter.items():
        content += f"{key}: {value}\n"
    content += "---\n\n"

    content += f"# Execution Log: {task_name}\n\n"
    content += f"**Run ID:** {run_id}\n"
    content += f"**Status:** {'✓ Completed' if success else '✗ Failed'}\n"
    content += f"**Duration:** {duration_seconds:.1f}s\n\n"

    if error:
        content += f"## Error\n\n```\n{error}\n```\n\n"

    content += "## Output\n\n"
    content += "```\n"
    # Truncate very long outputs
    if len(output) > 50000:
        content += output[:25000]
        content += "\n\n... [truncated] ...\n\n"
        content += output[-25000:]
    else:
        content += output
    content += "\n```\n"

    # Write log file
    log_path.write_text(content)

    # Append to index
    append_to_index(frontmatter)

    return log_path


def append_to_index(entry: dict):
    """Append entry to index.jsonl for machine queries."""
    index_path = LOGS_DIR / "index.jsonl"
    with open(index_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def classify_error(success: bool, error: Optional[str], exit_code: int) -> Optional[str]:
    """Classify error type for feedback loop analysis."""
    if success:
        return None
    if error:
        error_lower = error.lower()
        if "timeout" in error_lower or "timed out" in error_lower:
            return "timeout"
    if exit_code != 0:
        return "exit_error"
    return "exception"


def estimate_tokens(output: str) -> int:
    """Rough token estimate from output length (~4 chars per token)."""
    return len(output) // 4


def append_to_history(
    task_id: str,
    success: bool,
    error_type: Optional[str],
    tokens: int,
    duration_s: float,
    log_file: str,
    timestamp: Optional[str] = None,
) -> None:
    """
    Append minimal 6-field entry to history.jsonl for feedback loop.

    This is separate from index.jsonl - history.jsonl is specifically
    designed for self-improvement analysis with minimal fields:
    - task_id, success, error_type, tokens, duration_s, log_file
    """
    ensure_logs_dir()
    history_path = LOGS_DIR / "history.jsonl"

    entry = {
        "task_id": task_id,
        "success": success,
        "error_type": error_type,
        "tokens": tokens,
        "duration_s": round(duration_s, 2),
        "log_file": log_file,
        "timestamp": timestamp or datetime.now().isoformat(),
    }

    with open(history_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_history_stats(n: int = 100) -> dict:
    """Get feedback loop statistics from history.jsonl."""
    history_path = LOGS_DIR / "history.jsonl"
    if not history_path.exists():
        return {"total": 0, "success_rate": 0, "avg_tokens": 0, "avg_duration": 0, "error_types": {}}

    entries = []
    with open(history_path) as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))

    entries = entries[-n:]  # Last n entries
    if not entries:
        return {"total": 0, "success_rate": 0, "avg_tokens": 0, "avg_duration": 0, "error_types": {}}

    total = len(entries)
    successes = sum(1 for e in entries if e.get("success"))
    tokens = [e.get("tokens", 0) for e in entries]
    durations = [e.get("duration_s", 0) for e in entries]

    # Count error types
    error_types = {}
    for e in entries:
        et = e.get("error_type")
        if et:
            error_types[et] = error_types.get(et, 0) + 1

    return {
        "total": total,
        "successes": successes,
        "failures": total - successes,
        "success_rate": round(successes / total * 100, 1) if total else 0,
        "avg_tokens": round(sum(tokens) / len(tokens)) if tokens else 0,
        "avg_duration": round(sum(durations) / len(durations), 1) if durations else 0,
        "error_types": error_types,
    }


def get_recent_logs(n: int = 10) -> list[dict]:
    """Read recent log entries from index."""
    index_path = LOGS_DIR / "index.jsonl"
    if not index_path.exists():
        return []

    entries = []
    with open(index_path) as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))

    return entries[-n:]


def get_stats() -> dict:
    """Get execution statistics."""
    entries = get_recent_logs(100)
    if not entries:
        return {"total": 0, "success_rate": 0, "avg_duration": 0}

    total = len(entries)
    successes = sum(1 for e in entries if e.get("status") == "completed")
    durations = [e.get("duration_seconds", 0) for e in entries]

    return {
        "total": total,
        "successes": successes,
        "failures": total - successes,
        "success_rate": round(successes / total * 100, 1) if total else 0,
        "avg_duration": round(sum(durations) / len(durations), 1) if durations else 0,
    }


def format_recent_logs(n: int = 5) -> str:
    """Format recent logs for display."""
    logs = get_recent_logs(n)
    if not logs:
        return "No execution logs yet."

    lines = []
    for log in reversed(logs):
        status = "✓" if log.get("status") == "completed" else "✗"
        task = log.get("task", "unknown")
        duration = log.get("duration_seconds", 0)
        started = log.get("started", "")[:16]
        lines.append(f"  {status} {started} {task} ({duration:.0f}s)")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Recent execution logs:")
    print(format_recent_logs())
    print()
    stats = get_stats()
    print(f"Stats: {stats['total']} runs, {stats['success_rate']}% success, avg {stats['avg_duration']}s")
