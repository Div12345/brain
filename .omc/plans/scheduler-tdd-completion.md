# CC-Scheduler TDD Completion Plan

**Created:** 2026-02-03
**Budget:** 45% session remaining (~225k tokens)
**Methodology:** TDD (Red→Green→Refactor) + Ecomode (haiku-first)

---

## Budget Allocation

| Module | Est. Tokens | Agent Tier | Running Total |
|--------|-------------|------------|---------------|
| M1: Task Schema | 15k | haiku | 15k (7%) |
| M2: Executor Routing | 20k | haiku | 35k (16%) |
| M3: Validate Command | 15k | haiku | 50k (22%) |
| M4: Integration Tests | 20k | sonnet | 70k (31%) |
| M5: Smoke Test | 5k | haiku | 75k (33%) |
| **Buffer** | 50k | - | 125k (55%) |

**Remaining after plan:** ~100k tokens (45%) for your actual work today.

---

## Module 1: Task Schema Extension

### 1.1 Test File (Write First)
**File:** `tools/cc-scheduler/tests/test_tasks.py`

```python
"""TDD tests for extended task schema."""
import pytest
from pathlib import Path
import tempfile
from lib.tasks import Task, parse_task_file

class TestTaskSchema:
    """Test extended task schema parsing."""

    def test_parses_skill_field(self):
        """RED: Task should parse skill field."""
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
        """RED: Task should parse model_hint field."""
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
        """RED: Missing skill should default to None."""
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
        """RED: Missing model_hint should default to sonnet."""
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
        """RED: Task should parse mcps_required list."""
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
        """RED: Invalid skill should raise error."""
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
            with pytest.raises(ValueError, match="Invalid skill"):
                parse_task_file(Path(f.name))

    def test_validates_model_hint_values(self):
        """RED: Invalid model_hint should raise error."""
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
            with pytest.raises(ValueError, match="Invalid model_hint"):
                parse_task_file(Path(f.name))
```

### 1.2 Implementation (Make Tests Pass)
**File:** `tools/cc-scheduler/lib/tasks.py` - Add to Task dataclass:

```python
# Add to imports
from typing import Optional, List

# Valid values
VALID_SKILLS = [None, "autopilot", "ralph", "ultrawork", "ecomode", "plan", "analyze", "deepsearch", "tdd"]
VALID_MODEL_HINTS = ["haiku", "sonnet", "opus"]

@dataclass
class Task:
    """Task definition with extended schema."""
    name: str
    priority: int
    timeout: str
    path: Path
    body: str
    mode: str = "autonomous"
    estimated_tokens: int = 10000
    tags: list = None
    depends_on: list = None
    deadline: datetime = None
    project: str = None
    # NEW FIELDS
    skill: Optional[str] = None
    model_hint: str = "sonnet"
    mcps_required: List[str] = None
    inject_capabilities: bool = False

# Add validation in parse_task_file():
def parse_task_file(path: Path) -> Task:
    """Parse task file with validation."""
    # ... existing parsing code ...

    # Extract new fields
    skill = frontmatter.get("skill")
    model_hint = frontmatter.get("model_hint", "sonnet")
    mcps_required = frontmatter.get("mcps_required", [])
    inject_capabilities = frontmatter.get("inject_capabilities", False)

    # Validate
    if skill is not None and skill not in VALID_SKILLS:
        raise ValueError(f"Invalid skill: {skill}. Valid: {VALID_SKILLS}")
    if model_hint not in VALID_MODEL_HINTS:
        raise ValueError(f"Invalid model_hint: {model_hint}. Valid: {VALID_MODEL_HINTS}")

    return Task(
        # ... existing fields ...
        skill=skill,
        model_hint=model_hint,
        mcps_required=mcps_required or [],
        inject_capabilities=inject_capabilities,
    )
```

### 1.3 Validation Command
```bash
cd tools/cc-scheduler && python -m pytest tests/test_tasks.py -v
```

### 1.4 Expected Output
```
tests/test_tasks.py::TestTaskSchema::test_parses_skill_field PASSED
tests/test_tasks.py::TestTaskSchema::test_parses_model_hint PASSED
tests/test_tasks.py::TestTaskSchema::test_skill_defaults_to_none PASSED
tests/test_tasks.py::TestTaskSchema::test_model_hint_defaults_to_sonnet PASSED
tests/test_tasks.py::TestTaskSchema::test_parses_mcps_required PASSED
tests/test_tasks.py::TestTaskSchema::test_validates_skill_values PASSED
tests/test_tasks.py::TestTaskSchema::test_validates_model_hint_values PASSED

7 passed
```

---

## Module 2: Executor Routing

### 2.1 Test File (Write First)
**File:** `tools/cc-scheduler/tests/test_executor.py`

```python
"""TDD tests for executor routing."""
import pytest
from unittest.mock import Mock, patch
from lib.executor import build_command, build_prompt_with_skill
from lib.tasks import Task
from pathlib import Path
from datetime import datetime

def make_task(**kwargs) -> Task:
    """Factory for test tasks."""
    defaults = {
        "name": "test-task",
        "priority": 1,
        "timeout": "30m",
        "path": Path("/tmp/test.md"),
        "body": "Test body",
        "mode": "autonomous",
        "skill": None,
        "model_hint": "sonnet",
        "mcps_required": [],
    }
    defaults.update(kwargs)
    return Task(**defaults)

class TestBuildCommand:
    """Test command building with routing."""

    def test_basic_command_structure(self):
        """RED: Basic command should have claude -p structure."""
        task = make_task()
        cmd = build_command(task)

        assert cmd[0] == "claude"
        assert "-p" in cmd
        assert "--verbose" in cmd
        assert "--dangerously-skip-permissions" in cmd

    def test_skill_prefix_added(self):
        """RED: Skill should be prefixed to prompt."""
        task = make_task(skill="autopilot", body="Do something")
        cmd = build_command(task)

        prompt_idx = cmd.index("-p") + 1
        prompt = cmd[prompt_idx]
        assert prompt.startswith("/oh-my-claudecode:autopilot")
        assert "Do something" in prompt

    def test_no_skill_prefix_when_none(self):
        """RED: No prefix when skill is None."""
        task = make_task(skill=None, body="Do something")
        cmd = build_command(task)

        prompt_idx = cmd.index("-p") + 1
        prompt = cmd[prompt_idx]
        assert not prompt.startswith("/oh-my-claudecode:")
        assert prompt == "Do something"

    def test_haiku_model_flag(self):
        """RED: Haiku hint should add model flag."""
        task = make_task(model_hint="haiku")
        cmd = build_command(task)

        assert "--model" in cmd
        model_idx = cmd.index("--model") + 1
        assert "haiku" in cmd[model_idx]

    def test_opus_model_flag(self):
        """RED: Opus hint should add model flag."""
        task = make_task(model_hint="opus")
        cmd = build_command(task)

        assert "--model" in cmd
        model_idx = cmd.index("--model") + 1
        assert "opus" in cmd[model_idx]

    def test_sonnet_no_model_flag(self):
        """RED: Sonnet (default) should not add model flag."""
        task = make_task(model_hint="sonnet")
        cmd = build_command(task)

        assert "--model" not in cmd

    def test_readonly_tool_restrictions(self):
        """RED: Read-only mode should restrict tools."""
        task = make_task(mode="read-only")
        cmd = build_command(task)

        assert "--allowedTools" in cmd
        tools_idx = cmd.index("--allowedTools") + 1
        assert "Read" in cmd[tools_idx]
        assert "Write" not in cmd[tools_idx]

class TestPromptWithCapabilities:
    """Test capability injection into prompts."""

    def test_injects_capabilities_when_enabled(self):
        """RED: Should inject capability list when enabled."""
        task = make_task(inject_capabilities=True, body="Original body")
        prompt = build_prompt_with_skill(task)

        assert "## Available Capabilities" in prompt
        assert "autopilot" in prompt.lower()
        assert "Original body" in prompt

    def test_no_injection_when_disabled(self):
        """RED: Should not inject when disabled."""
        task = make_task(inject_capabilities=False, body="Original body")
        prompt = build_prompt_with_skill(task)

        assert "## Available Capabilities" not in prompt
```

### 2.2 Implementation (Make Tests Pass)
**File:** `tools/cc-scheduler/lib/executor.py` - Add functions:

```python
# Capability documentation for injection
CAPABILITIES_TEMPLATE = '''
## Available Capabilities

### OMC Skills
- autopilot: Full autonomous execution
- ralph: Must-complete persistence loop
- ultrawork: Maximum parallelism
- ecomode: Token-efficient parallel
- plan: Strategic planning
- analyze: Deep investigation
- deepsearch: Codebase search
- tdd: Test-driven development

### Model Routing
- haiku: Fast, cheap ($0.25/M) - simple tasks
- sonnet: Balanced ($3/M) - standard work
- opus: Powerful ($15/M) - complex reasoning

### Available MCPs
- memory: Persist learnings
- obsidian: Research vault
- github: Repo operations
- paper-search: Academic research

'''

def build_prompt_with_skill(task: Task) -> str:
    """Build prompt with optional skill prefix and capability injection."""
    prompt = task.body

    # Inject capabilities if requested
    if getattr(task, 'inject_capabilities', False):
        prompt = CAPABILITIES_TEMPLATE + "\n## Task\n" + prompt

    # Add skill prefix
    skill = getattr(task, 'skill', None)
    if skill:
        prompt = f"/oh-my-claudecode:{skill} {prompt}"

    # Add mode instruction
    if task.mode == "read-only":
        prompt = f"[READ-ONLY MODE - Do not modify any files]\n\n{prompt}"
    elif task.mode == "plan-first":
        prompt = f"[PLAN-FIRST MODE - Create a plan before executing]\n\n{prompt}"

    return prompt


def build_command(task: Task) -> list[str]:
    """Build claude CLI command with routing."""
    prompt = build_prompt_with_skill(task)

    cmd = ["claude", "-p", prompt, "--verbose", "--dangerously-skip-permissions"]

    # Model routing
    model_hint = getattr(task, 'model_hint', 'sonnet')
    if model_hint == "haiku":
        cmd.extend(["--model", "claude-haiku-3"])
    elif model_hint == "opus":
        cmd.extend(["--model", "claude-opus-4"])
    # sonnet is default, no flag needed

    # Tool restrictions for read-only
    if task.mode == "read-only":
        cmd.extend(["--allowedTools", "Read,Glob,Grep,WebSearch,WebFetch"])

    return cmd
```

### 2.3 Update execute_task to use build_command
```python
# In execute_task(), replace the cmd building with:
cmd = build_command(task)
```

### 2.4 Validation Command
```bash
cd tools/cc-scheduler && python -m pytest tests/test_executor.py -v
```

### 2.5 Expected Output
```
tests/test_executor.py::TestBuildCommand::test_basic_command_structure PASSED
tests/test_executor.py::TestBuildCommand::test_skill_prefix_added PASSED
tests/test_executor.py::TestBuildCommand::test_no_skill_prefix_when_none PASSED
tests/test_executor.py::TestBuildCommand::test_haiku_model_flag PASSED
tests/test_executor.py::TestBuildCommand::test_opus_model_flag PASSED
tests/test_executor.py::TestBuildCommand::test_sonnet_no_model_flag PASSED
tests/test_executor.py::TestBuildCommand::test_readonly_tool_restrictions PASSED
tests/test_executor.py::TestPromptWithCapabilities::test_injects_capabilities_when_enabled PASSED
tests/test_executor.py::TestPromptWithCapabilities::test_no_injection_when_disabled PASSED

9 passed
```

---

## Module 3: Validate Command

### 3.1 Test File (Write First)
**File:** `tools/cc-scheduler/tests/test_validate.py`

```python
"""TDD tests for validate command."""
import pytest
from pathlib import Path
import tempfile
import os
from lib.validate import validate_task, validate_all_pending, ValidationResult

class TestValidateTask:
    """Test single task validation."""

    def test_valid_task_passes(self):
        """RED: Valid task should pass validation."""
        content = '''---
name: valid-task
priority: 1
timeout: 30m
skill: autopilot
model_hint: sonnet
---
Do something useful
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            result = validate_task(Path(f.name))

        assert result.valid is True
        assert len(result.errors) == 0

    def test_missing_required_field_fails(self):
        """RED: Missing name should fail."""
        content = '''---
priority: 1
timeout: 30m
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            result = validate_task(Path(f.name))

        assert result.valid is False
        assert any("name" in e.lower() for e in result.errors)

    def test_invalid_skill_fails(self):
        """RED: Invalid skill should fail."""
        content = '''---
name: test
priority: 1
timeout: 30m
skill: not_a_real_skill
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            result = validate_task(Path(f.name))

        assert result.valid is False
        assert any("skill" in e.lower() for e in result.errors)

    def test_empty_body_warns(self):
        """RED: Empty body should warn."""
        content = '''---
name: test
priority: 1
timeout: 30m
---

'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            result = validate_task(Path(f.name))

        assert len(result.warnings) > 0
        assert any("empty" in w.lower() for w in result.warnings)

    def test_reports_estimated_tokens(self):
        """RED: Should report estimated tokens."""
        content = '''---
name: test
priority: 1
timeout: 30m
estimated_tokens: 15000
---
Body
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            result = validate_task(Path(f.name))

        assert result.estimated_tokens == 15000

class TestValidateAll:
    """Test batch validation."""

    def test_returns_summary(self):
        """RED: Should return valid/invalid counts."""
        # This test needs a temp directory with task files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create valid task
            valid = Path(tmpdir) / "valid.md"
            valid.write_text('''---
name: valid
priority: 1
timeout: 30m
---
Body
''')
            # Create invalid task
            invalid = Path(tmpdir) / "invalid.md"
            invalid.write_text('''---
priority: 1
---
Body
''')

            summary = validate_all_pending(Path(tmpdir))

        assert summary["total"] == 2
        assert summary["valid"] == 1
        assert summary["invalid"] == 1
```

### 3.2 Implementation (Make Tests Pass)
**File:** `tools/cc-scheduler/lib/validate.py`

```python
"""Task validation module."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import yaml

from .tasks import VALID_SKILLS, VALID_MODEL_HINTS

@dataclass
class ValidationResult:
    """Result of validating a single task."""
    path: Path
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    estimated_tokens: int = 0
    skill: Optional[str] = None
    model_hint: str = "sonnet"


def validate_task(path: Path) -> ValidationResult:
    """Validate a single task file."""
    result = ValidationResult(path=path, valid=True)

    try:
        content = path.read_text()
    except Exception as e:
        result.valid = False
        result.errors.append(f"Cannot read file: {e}")
        return result

    # Split frontmatter and body
    if not content.startswith("---"):
        result.valid = False
        result.errors.append("Missing YAML frontmatter (must start with ---)")
        return result

    parts = content.split("---", 2)
    if len(parts) < 3:
        result.valid = False
        result.errors.append("Invalid frontmatter format")
        return result

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        result.valid = False
        result.errors.append(f"Invalid YAML: {e}")
        return result

    body = parts[2].strip()

    # Required fields
    if not frontmatter.get("name"):
        result.valid = False
        result.errors.append("Missing required field: name")

    if not frontmatter.get("priority"):
        result.valid = False
        result.errors.append("Missing required field: priority")

    if not frontmatter.get("timeout"):
        result.valid = False
        result.errors.append("Missing required field: timeout")

    # Validate skill
    skill = frontmatter.get("skill")
    if skill is not None and skill not in VALID_SKILLS:
        result.valid = False
        result.errors.append(f"Invalid skill: {skill}. Valid: {VALID_SKILLS}")
    result.skill = skill

    # Validate model_hint
    model_hint = frontmatter.get("model_hint", "sonnet")
    if model_hint not in VALID_MODEL_HINTS:
        result.valid = False
        result.errors.append(f"Invalid model_hint: {model_hint}. Valid: {VALID_MODEL_HINTS}")
    result.model_hint = model_hint

    # Warnings
    if not body:
        result.warnings.append("Task body is empty")

    if len(body) < 20:
        result.warnings.append("Task body is very short - may lack context")

    # Extract tokens
    result.estimated_tokens = frontmatter.get("estimated_tokens", 10000)

    return result


def validate_all_pending(pending_dir: Path) -> dict:
    """Validate all pending tasks."""
    results = []

    for task_file in pending_dir.glob("*.md"):
        results.append(validate_task(task_file))

    valid_count = sum(1 for r in results if r.valid)
    invalid_count = sum(1 for r in results if not r.valid)
    total_tokens = sum(r.estimated_tokens for r in results if r.valid)

    return {
        "total": len(results),
        "valid": valid_count,
        "invalid": invalid_count,
        "total_tokens": total_tokens,
        "results": results,
    }


def format_validation_report(summary: dict) -> str:
    """Format validation results for display."""
    lines = [f"Validating {summary['total']} pending tasks...\n"]

    for result in summary["results"]:
        status = "✓" if result.valid else "✗"
        lines.append(f"{status} {result.path.name}")

        if result.valid:
            lines.append(f"  - Skill: {result.skill or 'none'}")
            lines.append(f"  - Model: {result.model_hint}")
            lines.append(f"  - Tokens: {result.estimated_tokens:,}")

        for err in result.errors:
            lines.append(f"  - ERROR: {err}")

        for warn in result.warnings:
            lines.append(f"  - WARN: {warn}")

        lines.append("")

    lines.append(f"Summary: {summary['valid']} valid, {summary['invalid']} invalid")
    lines.append(f"Total tokens (valid tasks): {summary['total_tokens']:,}")

    return "\n".join(lines)
```

### 3.3 Add to ccq CLI
**File:** `tools/cc-scheduler/ccq` - Add command:

```python
# Add import
from lib.validate import validate_all_pending, format_validation_report

# Add command function
def cmd_validate(args):
    """Validate all pending tasks."""
    pending_dir = TASKS_DIR / "pending"

    if not pending_dir.exists():
        print("No pending directory found.")
        return 0

    summary = validate_all_pending(pending_dir)
    print(format_validation_report(summary))

    return 0 if summary["invalid"] == 0 else 1

# Add to subparsers
subparsers.add_parser("validate", help="Validate all pending tasks")

# Add to main dispatch
elif args.command == "validate":
    return cmd_validate(args)
```

### 3.4 Validation Command
```bash
cd tools/cc-scheduler && python -m pytest tests/test_validate.py -v
```

### 3.5 Expected Output
```
tests/test_validate.py::TestValidateTask::test_valid_task_passes PASSED
tests/test_validate.py::TestValidateTask::test_missing_required_field_fails PASSED
tests/test_validate.py::TestValidateTask::test_invalid_skill_fails PASSED
tests/test_validate.py::TestValidateTask::test_empty_body_warns PASSED
tests/test_validate.py::TestValidateTask::test_reports_estimated_tokens PASSED
tests/test_validate.py::TestValidateAll::test_returns_summary PASSED

6 passed
```

---

## Module 4: Integration Test

### 4.1 Test File
**File:** `tools/cc-scheduler/tests/test_integration.py`

```python
"""Integration tests for full scheduler flow."""
import pytest
from pathlib import Path
import tempfile
import shutil

from lib.tasks import parse_task_file, load_pending_tasks, TASKS_DIR
from lib.executor import build_command, execute_task
from lib.validate import validate_task
from lib.log_utils import get_history_stats

class TestFullFlow:
    """Test complete task lifecycle."""

    def test_task_parse_validate_build_command(self):
        """Integration: Parse → Validate → Build Command."""
        content = '''---
name: integration-test
priority: 1
timeout: 5m
skill: ecomode
model_hint: haiku
estimated_tokens: 1000
---
List files in current directory
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        # Parse
        task = parse_task_file(path)
        assert task.name == "integration-test"
        assert task.skill == "ecomode"

        # Validate
        result = validate_task(path)
        assert result.valid is True

        # Build command
        cmd = build_command(task)
        assert "claude" in cmd
        assert "/oh-my-claudecode:ecomode" in cmd[cmd.index("-p") + 1]
        assert "--model" in cmd
        assert "haiku" in cmd[cmd.index("--model") + 1]

    def test_dry_run_does_not_execute(self):
        """Integration: Dry run returns without subprocess."""
        content = '''---
name: dry-run-test
priority: 1
timeout: 5m
---
This should not execute
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            task = parse_task_file(Path(f.name))

        result = execute_task(task, dry_run=True)

        assert result.success is True
        assert "[DRY RUN]" in result.output
        assert result.duration_seconds == 0
```

### 4.2 Validation Command
```bash
cd tools/cc-scheduler && python -m pytest tests/test_integration.py -v
```

---

## Module 5: Smoke Test Task

### 5.1 Create Smoke Test Task
**File:** `tasks/pending/000-smoke-test.md`

```markdown
---
name: smoke-test
priority: 1
timeout: 5m
estimated_tokens: 1000
skill: null
model_hint: haiku
mode: read-only
inject_capabilities: false
tags: [test, smoke]
---

# Scheduler Smoke Test

Execute these steps to verify the scheduler is working:

1. Report the current date and time
2. List files in `tasks/pending/`
3. Read `logs/scheduler/history.jsonl` and report entry count
4. Output exactly: "SMOKE TEST PASSED at {timestamp}"

This is a read-only verification task. Do not create or modify any files.
```

### 5.2 Validation Sequence
```bash
# 1. Validate the task
./ccq validate

# 2. Dry run to see command
./ccq run --dry

# 3. Actually run (only if validation passed)
./ccq run --force

# 4. Check logs
./ccq logs -n 1

# 5. Verify history entry
tail -1 logs/scheduler/history.jsonl | jq .
```

### 5.3 Expected Final State
```
✓ Task in tasks/completed/000-smoke-test.md
✓ Log in logs/scheduler/2026-02-03-HHMM-smoke-test.md
✓ Entry in logs/scheduler/history.jsonl with success=true
✓ Output contains "SMOKE TEST PASSED"
```

---

## Execution Sequence

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Create Tests (RED)                                 │
│ ├─ tests/test_tasks.py         → 7 failing tests           │
│ ├─ tests/test_executor.py      → 9 failing tests           │
│ └─ tests/test_validate.py      → 6 failing tests           │
│                                                             │
│ Validation: pytest --collect-only (22 tests collected)     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Implement (GREEN)                                  │
│ ├─ lib/tasks.py               → Add schema fields          │
│ ├─ lib/executor.py            → Add routing functions      │
│ └─ lib/validate.py            → Create validation module   │
│                                                             │
│ Validation: pytest -v (22 tests passed)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: Wire Up CLI                                        │
│ └─ ccq                        → Add validate command       │
│                                                             │
│ Validation: ./ccq validate (runs without error)            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: Integration + Smoke Test                           │
│ ├─ tests/test_integration.py  → 2 tests pass               │
│ └─ tasks/pending/000-smoke-test.md → Real execution        │
│                                                             │
│ Validation: ./ccq run → "SMOKE TEST PASSED"                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ ✓ SYSTEM READY                                              │
│                                                             │
│ You can now:                                                │
│ 1. Write tasks using capability-aware schema               │
│ 2. ./ccq validate → catches errors before running          │
│ 3. ./ccq run → routes to correct skill/model               │
│ 4. ./ccq logs → verify results                             │
│ 5. Focus on your actual work!                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Approval Gates

| Gate | After | Approve If | Command to Verify |
|------|-------|------------|-------------------|
| **G1** | Phase 1 | Tests collected without syntax errors | `pytest --collect-only` |
| **G2** | Phase 2 | All 22 tests pass | `pytest -v` |
| **G3** | Phase 3 | CLI runs validation | `./ccq validate` |
| **G4** | Phase 4 | Smoke test passes | `./ccq run` + check logs |

---

**STATUS: PLAN COMPLETE - AWAITING APPROVAL**

Reply with:
- "Approve all" → Execute all phases sequentially
- "Approve G1" → Execute Phase 1 only, checkpoint
- "Skip to G3" → Assume tests exist, implement directly
- "Modify X" → Request changes to plan
