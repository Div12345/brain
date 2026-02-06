import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from lib.executor import move_task
from lib.tasks import Task


class TestMoveTask(unittest.TestCase):

    def test_move_task_normal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            from_dir = tmpdir / "pending"
            to_dir = tmpdir / "active"
            from_dir.mkdir(parents=True, exist_ok=True)
            to_dir.mkdir(parents=True, exist_ok=True)

            task_file = from_dir / "test_task.md"
            task_file.write_text("# Test Task")

            task = Task(name="test_task", path=task_file)

            with patch("lib.executor.TASKS_DIR", tmpdir):
                result = move_task(task, "pending", "active")

            assert result == to_dir / "test_task.md"
            assert result.exists()
            assert not task_file.exists()

    def test_move_task_idempotent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            from_dir = tmpdir / "pending"
            to_dir = tmpdir / "active"
            from_dir.mkdir(parents=True, exist_ok=True)
            to_dir.mkdir(parents=True, exist_ok=True)

            task_file = from_dir / "test_task.md"
            task_file.write_text("# Test Task")

            dest_file = to_dir / "test_task.md"
            dest_file.write_text("# Test Task")

            task_file.unlink()

            task = Task(name="test_task", path=task_file)

            with patch("lib.executor.TASKS_DIR", tmpdir):
                result = move_task(task, "pending", "active")

            assert result == dest_file
            assert dest_file.exists()

    def test_move_task_missing_both(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            from_dir = tmpdir / "pending"
            to_dir = tmpdir / "active"
            from_dir.mkdir(parents=True, exist_ok=True)
            to_dir.mkdir(parents=True, exist_ok=True)

            task_file = from_dir / "test_task.md"

            task = Task(name="test_task", path=task_file)

            with patch("lib.executor.TASKS_DIR", tmpdir):
                with self.assertRaises(Exception):
                    move_task(task, "pending", "active")


if __name__ == "__main__":
    unittest.main()
