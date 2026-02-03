#!/usr/bin/env python3
"""
Multi-project task queue for cc-scheduler.

Loads tasks from multiple project directories, resolves dependencies,
and provides runnable task filtering.
"""

from pathlib import Path
from typing import List, Optional, Set
from dataclasses import dataclass

from .tasks import Task, parse_task_file, load_pending_tasks, TASKS_DIR


@dataclass
class ProjectConfig:
    """Configuration for a project's task directory."""
    path: Path
    boost: int = 0  # Priority boost for this project
    name: str = ""  # Project identifier

    def __post_init__(self):
        if not self.name:
            self.name = self.path.parent.name if self.path.name == "tasks" else self.path.name


class TaskQueue:
    """
    Multi-project task queue with dependency tracking.
    """

    def __init__(self, projects: List[ProjectConfig] = None):
        self.projects = projects or [ProjectConfig(path=TASKS_DIR)]
        self._tasks: List[Task] = []
        self._completed_names: Set[str] = set()

    def load_all(self) -> List[Task]:
        """Load tasks from all configured projects."""
        self._tasks = []
        self._completed_names = set()

        for project in self.projects:
            pending_dir = project.path / "pending" if project.path.name != "pending" else project.path
            completed_dir = project.path / "completed" if project.path.name != "pending" else project.path.parent / "completed"

            # Load completed task names for dependency checking
            if completed_dir.exists():
                for path in completed_dir.glob("*.md"):
                    task = parse_task_file(path)
                    if task:
                        self._completed_names.add(task.name)

            # Load pending tasks
            if pending_dir.exists():
                for path in pending_dir.glob("*.md"):
                    task = parse_task_file(path)
                    if task:
                        # Attach project info
                        task.project = project.name
                        task.project_boost = project.boost
                        self._tasks.append(task)

        return self._tasks

    def check_dependencies(self, task: Task) -> bool:
        """
        Check if all dependencies are satisfied.

        A dependency is satisfied if:
        - The task name is in completed tasks, OR
        - No task with that name exists (external dependency assumed met)
        """
        if not task.depends_on:
            return True

        pending_names = {t.name for t in self._tasks}

        for dep in task.depends_on:
            # If dependency is in pending, it's not satisfied
            if dep in pending_names:
                return False
            # If dependency is completed, it's satisfied
            # If dependency doesn't exist anywhere, assume external and satisfied

        return True

    def get_blocked_tasks(self) -> List[Task]:
        """Get tasks that are blocked by dependencies."""
        return [t for t in self._tasks if not self.check_dependencies(t)]

    def get_runnable_tasks(self, max_tokens: int = None) -> List[Task]:
        """
        Get tasks that can be run now.

        Filters by:
        - Dependencies satisfied
        - Token estimate within budget (if max_tokens provided)
        """
        runnable = []

        for task in self._tasks:
            if not self.check_dependencies(task):
                continue

            if max_tokens and task.estimated_tokens > max_tokens:
                continue

            runnable.append(task)

        return runnable

    def get_by_name(self, name: str) -> Optional[Task]:
        """Get a task by name."""
        for task in self._tasks:
            if task.name == name:
                return task
        return None

    def get_by_tag(self, tag: str) -> List[Task]:
        """Get all tasks with a specific tag."""
        return [t for t in self._tasks if tag in t.tags]

    def get_by_project(self, project: str) -> List[Task]:
        """Get all tasks for a specific project."""
        return [t for t in self._tasks if getattr(t, 'project', None) == project]

    def summary(self) -> dict:
        """Get queue summary statistics."""
        blocked = self.get_blocked_tasks()
        runnable = self.get_runnable_tasks()

        total_tokens = sum(t.estimated_tokens for t in self._tasks)
        runnable_tokens = sum(t.estimated_tokens for t in runnable)

        # Group by project
        by_project = {}
        for task in self._tasks:
            proj = getattr(task, 'project', 'default')
            if proj not in by_project:
                by_project[proj] = []
            by_project[proj].append(task.name)

        return {
            "total": len(self._tasks),
            "runnable": len(runnable),
            "blocked": len(blocked),
            "total_tokens": total_tokens,
            "runnable_tokens": runnable_tokens,
            "by_project": by_project,
            "completed_count": len(self._completed_names),
        }


def load_projects_from_config(config: dict) -> List[ProjectConfig]:
    """Load project configurations from YAML config."""
    projects = []

    for proj in config.get("projects", []):
        path = Path(proj["path"]).expanduser()
        boost = proj.get("boost", 0)
        name = proj.get("name", "")

        projects.append(ProjectConfig(
            path=path,
            boost=boost,
            name=name
        ))

    # Default to brain tasks if no projects configured
    if not projects:
        projects.append(ProjectConfig(path=TASKS_DIR))

    return projects


def format_queue_status(queue: TaskQueue) -> str:
    """Format queue status for display."""
    summary = queue.summary()

    lines = [
        f"Task Queue Summary:",
        f"  Total tasks:    {summary['total']}",
        f"  Runnable:       {summary['runnable']}",
        f"  Blocked:        {summary['blocked']}",
        f"  Completed:      {summary['completed_count']}",
        f"",
        f"Token estimates:",
        f"  Total:          {summary['total_tokens']:,}",
        f"  Runnable:       {summary['runnable_tokens']:,}",
    ]

    if summary['by_project']:
        lines.append("")
        lines.append("By project:")
        for proj, tasks in summary['by_project'].items():
            lines.append(f"  {proj}: {len(tasks)} tasks")

    return "\n".join(lines)


if __name__ == "__main__":
    queue = TaskQueue()
    queue.load_all()
    print(format_queue_status(queue))
