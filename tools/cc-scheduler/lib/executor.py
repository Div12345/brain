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

import requests

from .tasks import Task, TASKS_DIR

DESKTOP_CHECK_URL = "http://127.0.0.1:9229/json"

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


def check_desktop_availability() -> bool:
    """Check if Claude Desktop is available via debug port."""
    try:
        response = requests.get(DESKTOP_CHECK_URL, timeout=1)
        return response.status_code == 200
    except requests.RequestException:
        return False


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


def build_prompt(task: Task, backend: str = "code") -> str:
    """Build execution prompt from task with skill prefix."""
    prompt = task.body

    # Add mode-specific instructions
    if task.mode == "read-only":
        prompt = f"[READ-ONLY MODE - Do not modify any files]\n\n{prompt}"
    elif task.mode == "plan-first":
        prompt = f"[PLAN-FIRST MODE - Create a plan before executing]\n\n{prompt}"

    # Prefix with skill invocation if specified
    skill = getattr(task, 'skill', None)
    if skill:
        prompt = f"/oh-my-claudecode:{skill} {prompt}"

    # Append CE post-execution protocol if enabled
    ce_aware = getattr(task, 'ce_aware', False)
    if ce_aware:
        template_path = Path(__file__).parent.parent / "templates" / "ce-aware-task.md"
        if template_path.exists():
            ce_template = template_path.read_text().strip()
            prompt = f"{prompt}\n\n{ce_template}"

    # Wrap prompt for Desktop backend (Gemini→Claude Desktop pipeline)
    if backend == "desktop":
        desktop_wrapper = (
            "You have claude_desktop MCP tools. Use them to complete this task via Claude Desktop.\n"
            "Do NOT use delegate_to_agent — call claude_desktop_* tools directly.\n\n"
            "PROTOCOL:\n"
            "1. Call claude_desktop_new to start a fresh conversation\n"
            "2. Call claude_desktop_send with the task below as the message, wait_for_response=true\n"
            "3. Call claude_desktop_read to get the response\n"
            "4. Evaluate the response quality. If incomplete, send follow-up.\n"
            "5. When satisfied, output the result.\n\n"
            "TASK FOR DESKTOP:\n"
        )
        prompt = desktop_wrapper + prompt

    return prompt


def build_command(task: Task, prompt: str, backend: str = "code") -> list[str]:
    """Build CLI command with model routing."""
    
    if backend == "desktop":
        # Gemini wrapper for Desktop
        # Read model and flags from config
        import yaml
        config_path = Path(__file__).parent.parent / "config.yaml"
        gemini_model = "gemini-3-flash-preview"  # Default to latest flash
        gemini_flags = ["--yolo", "--allowed-mcp-server-names", "claude-desktop"]

        if config_path.exists():
            with open(config_path) as f:
                cfg = yaml.safe_load(f) or {}
            desktop_cfg = cfg.get("backends", {}).get("desktop", {})
            gemini_model = desktop_cfg.get("gemini_model", gemini_model)
            gemini_flags = desktop_cfg.get("gemini_flags", gemini_flags)

        cmd = ["gemini", "-p", prompt, "--model", gemini_model]
        cmd.extend(gemini_flags)
        return cmd

    # Default: Claude Code CLI
    cmd = ["claude", "-p", prompt, "--verbose", "--dangerously-skip-permissions"]

    # Model routing based on task.model_hint
    model_hint = getattr(task, 'model_hint', 'sonnet')
    if model_hint == "haiku":
        cmd.extend(["--model", "haiku"])
    elif model_hint == "opus":
        cmd.extend(["--model", "opus"])
    # sonnet is default, no flag needed

    # Tool restrictions for read-only mode
    if task.mode == "read-only":
        cmd.extend(["--allowedTools", "Read,Glob,Grep,WebSearch,WebFetch"])

    return cmd


def move_task(task: Task, from_status: str, to_status: str) -> Path:
    """Move task file between status directories."""
    from_dir = TASKS_DIR / from_status
    to_dir = TASKS_DIR / to_status
    to_dir.mkdir(parents=True, exist_ok=True)

    new_path = to_dir / task.path.name

    # Idempotency: if source is already gone but destination exists, treat as success
    if not task.path.exists() and new_path.exists():
        return new_path

    shutil.move(str(task.path), str(new_path))
    return new_path


def execute_task(task: Task, dry_run: bool = False, run_id: str = None, log_file: str = None, force_backend: str = None) -> ExecutionResult:
    """
    Execute a task using claude CLI or Gemini Desktop wrapper.

    Execution modes:
    - autonomous: claude -p "prompt" --allowedTools ...
    - plan-first: claude -p "prompt" (with planning instruction)
    - read-only: claude -p "prompt" --allowedTools Read,Glob,Grep,WebSearch
    """
    started_at = datetime.now()
    timeout_secs = parse_timeout(task.timeout)

    # Determine backend
    backend = force_backend or getattr(task, 'backend', 'code')

    if backend == "auto":
        if check_desktop_availability():
            backend = "desktop"
        else:
            backend = "code"

    # Validation/Fallback for desktop
    if backend == "desktop" and not check_desktop_availability():
        print("Warning: Desktop backend requested but unavailable. Falling back to code.")
        backend = "code"

    prompt = build_prompt(task, backend=backend)

    if dry_run:
        cmd = build_command(task, prompt, backend)
        return ExecutionResult(
            task_name=task.name,
            success=True,
            exit_code=0,
            output=f"[DRY RUN] Would execute: {task.name}\nBackend: {backend}\nCommand: {' '.join(cmd[:6])}...\nSkill: {getattr(task, 'skill', None)}\nModel: {getattr(task, 'model_hint', 'sonnet')}\nPrompt: {prompt[:200]}...",
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

    # Build command with skill/model routing
    cmd = build_command(task, prompt, backend)

    try:
        tool_name = "gemini" if backend == "desktop" else "claude"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting {tool_name} process...")
        
        # Use Popen to stream output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr into stdout
            text=True,
            bufsize=1,  # Line buffered
            cwd=str(Path.home() / "brain"),
            env={
                **os.environ,
                "CLAUDE_CODE_ENTRYPOINT": "ccq-scheduler",
                # Context injection for scheduled tasks
                "CCQ_TASK_ID": task.name,
                "CCQ_RUN_ID": run_id or "",
                "CCQ_LOG_FILE": log_file or "",
                "CCQ_TASK_FILE": str(task.path),
            }
        )

        captured_output = []
        
        # Stream output while checking for timeout
        start_time = time.time()
        
        # Set stdout to non-blocking
        os.set_blocking(process.stdout.fileno(), False)
        
        while True:
            # Check for timeout
            if time.time() - start_time > timeout_secs:
                process.kill()
                raise subprocess.TimeoutExpired(cmd, timeout_secs, output="".join(captured_output).encode())
            
            # Check if process is still running
            retcode = process.poll()
            
            # Read available output
            try:
                # Read up to 1KB
                chunk = process.stdout.read(1024)
                if chunk:
                    print(chunk, end='', flush=True)
                    captured_output.append(chunk)
                elif retcode is not None:
                    # Process finished and no more output
                    break
                else:
                    # No output yet, sleep briefly
                    time.sleep(0.1)
            except Exception:
                # Should not happen with os.set_blocking, but safe fallback
                time.sleep(0.1)

        result_code = process.returncode
        ended_at = datetime.now()
        success = result_code == 0
        output = "".join(captured_output)

        # Detect Gemini quota exhaustion — fail fast, don't retry
        error_msg = None
        if backend == "desktop" and "TerminalQuotaError" in output:
            import re
            reset_match = re.search(r'reset after (\d+h\d+m)', output)
            reset_time = reset_match.group(1) if reset_match else "unknown"
            print(f"\n[QUOTA EXHAUSTED] Gemini quota exhausted. Resets in {reset_time}. Stopping further tasks.")
            success = False
            error_msg = f"Gemini quota exhausted. Resets in {reset_time}"

        # Move to completed or failed
        final_status = "completed" if success else "failed"
        task.path = TASKS_DIR / "active" / task.path.name
        move_task(task, "active", final_status)

        return ExecutionResult(
            task_name=task.name,
            success=success,
            exit_code=result_code,
            output=output,
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=(ended_at - started_at).total_seconds(),
            error=error_msg,
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
