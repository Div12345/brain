"""TDD tests for extended task schema."""
import pytest
from pathlib import Path
import tempfile
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tasks import Task, parse_task_file, VALID_SKILLS, VALID_MODEL_HINTS


class TestTaskSchema:
    """Test extended task schema parsing."""

    def test_parses_skill_field(self):
        """Task should parse skill field."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
skill: autopilot
---
Body here
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.skill == "autopilot"

    def test_parses_model_hint(self):
        """Task should parse model_hint field."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
model_hint: haiku
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.model_hint == "haiku"

    def test_skill_defaults_to_none(self):
        """Missing skill should default to None."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.skill is None

    def test_model_hint_defaults_to_sonnet(self):
        """Missing model_hint should default to sonnet."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.model_hint == "sonnet"

    def test_parses_mcps_required(self):
        """Task should parse mcps_required list."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
mcps_required: [memory, obsidian]
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.mcps_required == ["memory", "obsidian"]

    def test_validates_skill_values(self):
        """Invalid skill should set skill to None."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
skill: invalid_skill
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.skill is None

    def test_validates_model_hint_values(self):
        """Invalid model_hint should return None."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
model_hint: gpt4
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task is None

    def test_parses_backend(self):
        """Task should parse backend field."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
backend: desktop
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.backend == "desktop"

    def test_backend_defaults_to_code(self):
        """Missing backend should default to code."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task.backend == "code"

    def test_validates_backend_values(self):
        """Invalid backend should return None."""
        content = '''---
name: test-task
priority: 1
timeout: 30m
backend: cloud
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        assert task is None
