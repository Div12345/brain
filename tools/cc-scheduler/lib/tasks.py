#!/usr/bin/env python3
"""
Task file parser for cc-scheduler.

Reads task files from brain/tasks/pending/ with YAML frontmatter.
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

# Default paths (can be overridden)
BRAIN_ROOT = Path.home() / "brain"
TASKS_DIR = BRAIN_ROOT / "tasks"

# Valid values for schema validation
VALID_SKILLS = [None, "autopilot", "ralph", "ultrawork", "ecomode", "plan", "analyze", "deepsearch", "tdd"]
VALID_MODEL_HINTS = ["haiku", "sonnet", "opus"]


@dataclass
class Task:
    """A scheduled task parsed from markdown file."""
    name: str
    path: Path
    priority: int = 5  # 1-10, lower = higher priority
    estimated_tokens: int = 50000  # Default estimate
    mode: str = "autonomous"  # autonomous | plan-first | read-only
    timeout: str = "30m"
    tags: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    deadline: Optional[datetime] = None
    body: str = ""  # Task content after frontmatter
    project: str = ""  # Project name (set by queue)
    project_boost: int = 0  # Priority boost from project config
    # Extended schema for routing
    skill: Optional[str] = None  # OMC skill to use
    model_hint: str = "sonnet"  # haiku | sonnet | opus
    mcps_required: List[str] = field(default_factory=list)
    inject_capabilities: bool = False

    @property
    def is_runnable(self) -> bool:
        """Check if task has no unmet dependencies."""
        # Basic check - queue.py does full dependency resolution
        return True


PRIORITY_MAP = {"low": 7, "medium": 5, "high": 3, "critical": 1}

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    frontmatter_str, body = match.groups()

    # Simple YAML parsing (handles both inline and multiline lists)
    frontmatter = {}
    current_key = None
    current_list = None

    for line in frontmatter_str.strip().split('\n'):
        # Check for list item continuation
        if line.strip().startswith('- ') and current_key:
            if current_list is None:
                current_list = []
            current_list.append(line.strip()[2:].strip())
            continue
        elif current_key and current_list is not None:
            frontmatter[current_key] = current_list
            current_list = None
            current_key = None

        if ':' in line and not line.strip().startswith('-'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Empty value might indicate multiline list follows
            if not value:
                current_key = key
                current_list = []
                continue

            # Handle inline lists [a, b, c]
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
            # Handle numbers
            elif value.isdigit():
                value = int(value)
            # Handle string priorities
            elif key == 'priority' and value.lower() in PRIORITY_MAP:
                value = PRIORITY_MAP[value.lower()]
            # Handle booleans
            elif value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            # Strip quotes
            elif value.startswith('"') or value.startswith("'"):
                value = value[1:-1]

            frontmatter[key] = value

    # Handle trailing list
    if current_key and current_list is not None:
        frontmatter[current_key] = current_list

    return frontmatter, body.strip()


def parse_task_file(path: Path) -> Optional[Task]:
    """Parse a single task file."""
    try:
        content = path.read_text()
        meta, body = parse_frontmatter(content)

        # Parse deadline if present
        deadline = None
        if 'deadline' in meta:
            try:
                deadline = datetime.fromisoformat(str(meta['deadline']))
            except ValueError:
                pass

        # Extract and validate new fields
        skill = meta.get('skill')
        if skill is not None and skill not in VALID_SKILLS:
            raise ValueError(f"Invalid skill: {skill}. Valid: {VALID_SKILLS}")

        model_hint = meta.get('model_hint', 'sonnet')
        if model_hint not in VALID_MODEL_HINTS:
            raise ValueError(f"Invalid model_hint: {model_hint}. Valid: {VALID_MODEL_HINTS}")

        mcps_required = meta.get('mcps_required', [])
        inject_capabilities = meta.get('inject_capabilities', False)

        return Task(
            name=meta.get('name', path.stem),
            path=path,
            priority=meta.get('priority', 5),
            estimated_tokens=meta.get('estimated_tokens', 50000),
            mode=meta.get('mode', 'autonomous'),
            timeout=meta.get('timeout', '30m'),
            tags=meta.get('tags', []),
            depends_on=meta.get('depends_on', []),
            deadline=deadline,
            body=body,
            skill=skill,
            model_hint=model_hint,
            mcps_required=mcps_required if isinstance(mcps_required, list) else [],
            inject_capabilities=inject_capabilities,
        )
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        return None


def load_pending_tasks(tasks_dir: Path = None) -> List[Task]:
    """Load all pending tasks, sorted by priority."""
    if tasks_dir is None:
        tasks_dir = TASKS_DIR

    pending_dir = tasks_dir / "pending"
    if not pending_dir.exists():
        return []

    tasks = []
    for path in pending_dir.glob("*.md"):
        task = parse_task_file(path)
        if task:
            tasks.append(task)

    # Sort by: priority (asc), deadline (nulls last), estimated_tokens (asc)
    def sort_key(t: Task):
        deadline_ts = t.deadline.timestamp() if t.deadline else float('inf')
        return (t.priority, deadline_ts, t.estimated_tokens)

    return sorted(tasks, key=sort_key)


def get_runnable_tasks(tasks: List[Task], available_tokens: int) -> List[Task]:
    """Filter tasks that fit within available capacity."""
    return [t for t in tasks if t.is_runnable and t.estimated_tokens <= available_tokens]


if __name__ == "__main__":
    tasks = load_pending_tasks()
    print(f"Found {len(tasks)} pending tasks:\n")
    for t in tasks:
        deadline = t.deadline.strftime("%Y-%m-%d") if t.deadline else "none"
        print(f"  [{t.priority}] {t.name} ({t.estimated_tokens:,} tokens, deadline: {deadline})")
        print(f"      mode: {t.mode}, timeout: {t.timeout}")
        if t.tags:
            print(f"      tags: {', '.join(t.tags)}")
