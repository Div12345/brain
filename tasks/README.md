# Task Queue

> Async task management for multi-interface orchestration.

## How It Works

1. **Any interface** can create a task in `pending/`
2. **Orchestrator** routes task to best available interface
3. **Interface** moves task to `active/`, executes, writes result
4. **Completed** tasks go to `completed/` with output
5. **Failed** tasks go to `failed/` with error info

## Task Spec Format

```markdown
---
id: task-[timestamp]-[random]
created: 2026-01-31T02:00:00Z
priority: high | medium | low
requires:
  - code_execution    # needs Claude Code
  - web_search        # needs search capability
  - file_write        # needs file system access
preferred_interface: claude_code | claude_desktop | gemini | any
timeout: 30m
created_by: overnight | oracle | user | architect
---

# Task: [Short Description]

## Objective
[What needs to be accomplished]

## Input
[Data, files, or context needed]

## Expected Output
[What success looks like]

## Context
[Links to relevant brain files]

## Notes
[Any additional instructions]
```

## Directories

```
tasks/
├── pending/      # Waiting for pickup
├── active/       # Currently executing
├── completed/    # Successfully finished
└── failed/       # Errors or timeouts
```

## Task Lifecycle

```
CREATED → PENDING → ACTIVE → COMPLETED
                  ↘        ↗
                    FAILED
```

### State Transitions

| From | To | Trigger |
|------|-----|---------|
| - | pending | Task created |
| pending | active | Interface claims task |
| active | completed | Task succeeds |
| active | failed | Task errors or times out |
| failed | pending | Retry requested |

## Claiming a Task

When an interface picks up a task:

1. Move file from `pending/` to `active/`
2. Add to frontmatter:
   ```yaml
   claimed_by: [interface_name]
   claimed_at: [timestamp]
   ```
3. Execute task
4. Move to `completed/` or `failed/` with results

## Completed Task Format

Add to the original task file:

```markdown
---
# ... original frontmatter ...
completed_at: 2026-01-31T02:30:00Z
completed_by: claude_code
duration: 28m
---

# ... original task spec ...

---

## Result

### Output
[What was produced]

### Files Created
- [path/to/file1]
- [path/to/file2]

### Summary
[Brief description of what was done]
```

## Failed Task Format

```markdown
---
# ... original frontmatter ...
failed_at: 2026-01-31T02:30:00Z
failed_by: claude_code
error_type: timeout | error | cancelled
retries: 0
max_retries: 3
---

# ... original task spec ...

---

## Failure Info

### Error
[Error message or description]

### Partial Progress
[What was accomplished before failure]

### Suggested Fix
[How to resolve, if known]
```

## Priority Routing

| Priority | Max Wait | Escalation |
|----------|----------|------------|
| high | 5 min | Immediate notification |
| medium | 30 min | Batch with similar tasks |
| low | 4 hours | Run when idle |

## Example Task

```markdown
---
id: task-20260131-0200-abc123
created: 2026-01-31T02:00:00Z
priority: medium
requires:
  - vault_read
  - analysis
preferred_interface: any
timeout: 1h
created_by: overnight
---

# Task: Analyze January Daily Notes

## Objective
Extract patterns from January 2026 daily notes.

## Input
- Obsidian vault: `01 - Personal/Daily/2026-01-*.md`

## Expected Output
- Pattern summary in `knowledge/patterns/january-2026.md`
- Updated `context/patterns.md`

## Context
- See `agents/overnight.md` for analysis methodology
- Previous analysis: `knowledge/patterns/december-2025.md`
```

---

*Tasks are the unit of work. Small, specific, trackable.*
