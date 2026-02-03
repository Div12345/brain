#!/usr/bin/env python3
"""
Task executor for cc-scheduler.

Wraps omc/claude invocation with timeout handling and output capture.
Delegates actual execution to claude CLI or omc skills.
"""

import subprocess
import shutil
import os
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .tasks import Task, TASKS_DIR

@dataclass
class ExecutionResult:
    """Result of task execution."""
    task_name: str
    success: bool
    exit_code: int
    output: str
    started_at: datetime
    ended_at: datetime
    duration_seconds: float
    error: Optional[str] = None


def parse_timeout(timeout_str: str) -> int:
    """Parse timeout string like '30m' or '2h' to seconds."""
    if timeout_str.endswith('m'):
        return int(timeout_str[:-1]) * 60
    elif timeout_str.endswith('h'):
        return int(timeout_str[:-1]) * 3600
    elif timeout_str.endswith('s'):
        return int(timeout_str[:-1])
    else:
        return int(timeout_str)


def build_prompt(task: Task) -> str:
    """Build execution prompt from task."""
    # Include task body as the main prompt
    prompt = task.body

    # Add mode-specific instructions
    if task.mode == "read-only":
        prompt = f"[READ-ONLY MODE - Do not modify any files]\n\n{prompt}"
    elif task.mode == "plan-first":
        prompt = f"[PLAN-FIRST MODE - Create a plan before executing]\n\n{prompt}"

    return prompt


def move_task(task: Task, from_status: str, to_status: str) -> Path:
    """Move task file between status directories."""
    from_dir = TASKS_DIR / from_status
    to_dir = TASKS_DIR / to_status
    to_dir.mkdir(parents=True, exist_ok=True)

    new_path = to_dir / task.path.name
    shutil.move(str(task.path), str(new_path))
    return new_path


def execute_task(task: Task, dry_run: bool = False) -> ExecutionResult:
    """
    Execute a task using claude CLI.

    Execution modes:
    - autonomous: claude -p "prompt" --allowedTools ...
    - plan-first: claude -p "prompt" (with planning instruction)
    - read-only: claude -p "prompt" --allowedTools Read,Glob,Grep,WebSearch
    """
    started_at = datetime.now()
    timeout_secs = parse_timeout(task.timeout)
    prompt = build_prompt(task)

    if dry_run:
        return ExecutionResult(
            task_name=task.name,
            success=True,
            exit_code=0,
            output=f"[DRY RUN] Would execute: {task.name}\nPrompt: {prompt[:200]}...",
            started_at=started_at,
            ended_at=datetime.now(),
            duration_seconds=0,
        )

    # Move task to active
    try:
        move_task(task, "pending", "active")
    except Exception as e:
        return ExecutionResult(
            task_name=task.name,
            success=False,
            exit_code=-1,
            output="",
            started_at=started_at,
            ended_at=datetime.now(),
            duration_seconds=0,
            error=f"Failed to move task to active: {e}"
        )

    # Build claude command
    cmd = ["claude", "-p", prompt, "--verbose"]

    # Add tool restrictions based on mode
    if task.mode == "read-only":
        cmd.extend(["--allowedTools", "Read,Glob,Grep,WebSearch,WebFetch"])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_secs,
            cwd=str(Path.home() / "brain"),  # Run from brain repo
            env={**os.environ, "CLAUDE_CODE_ENTRYPOINT": "ccq-scheduler"}
        )

        ended_at = datetime.now()
        success = result.returncode == 0
        output = result.stdout + ("\n" + result.stderr if result.stderr else "")

        # Move to completed or failed
        final_status = "completed" if success else "failed"
        task.path = TASKS_DIR / "active" / task.path.name
        move_task(task, "active", final_status)

        return ExecutionResult(
            task_name=task.name,
            success=success,
            exit_code=result.returncode,
            output=output,
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=(ended_at - started_at).total_seconds(),
        )

    except subprocess.TimeoutExpired as e:
        ended_at = datetime.now()
        task.path = TASKS_DIR / "active" / task.path.name
        move_task(task, "active", "failed")

        return ExecutionResult(
            task_name=task.name,
            success=False,
            exit_code=-1,
            output=e.stdout.decode() if e.stdout else "",
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=(ended_at - started_at).total_seconds(),
            error=f"Task timed out after {timeout_secs}s"
        )

    except Exception as e:
        ended_at = datetime.now()
        try:
            task.path = TASKS_DIR / "active" / task.path.name
            move_task(task, "active", "failed")
        except:
            pass

        return ExecutionResult(
            task_name=task.name,
            success=False,
            exit_code=-1,
            output="",
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=(ended_at - started_at).total_seconds(),
            error=str(e)
        )


if __name__ == "__main__":
    from .tasks import load_pending_tasks

    tasks = load_pending_tasks()
    if not tasks:
        print("No pending tasks")
    else:
        print(f"Would execute: {tasks[0].name}")
        print(f"Prompt preview:\n{build_prompt(tasks[0])[:500]}...")
