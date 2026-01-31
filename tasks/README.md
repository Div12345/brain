# Task Queue System

> Async coordination between agents via file-based tasks.

## Directories

| Directory | Purpose |
|-----------|---------|
| `pending/` | Tasks waiting to be claimed |
| `active/` | Tasks currently being worked |
| `completed/` | Successfully finished tasks |
| `failed/` | Tasks that errored |

## Task Lifecycle

```
pending/ → active/ → completed/
                  ↘ failed/
```

## Creating a Task

Drop a `.md` file in `pending/` with this format:

```markdown
---
id: task-YYYY-MM-DD-NNN
created: ISO timestamp
priority: high | medium | low
requires:
  - capability1
  - capability2
preferred_interface: claude-code | claude-desktop | any
timeout: 30m
---

# Task: [Title]

## Input
[What the task needs to work with]

## Expected Output
[What success looks like]

## Context
[Links to relevant files]
```

## Claiming a Task

1. Move file from `pending/` to `active/`
2. Rename to include agent ID: `task-001.claude-code.md`
3. Update `context/active-agent.md`

## Completing a Task

1. Append results to the task file
2. Move to `completed/`
3. Clear `context/active-agent.md`
4. Commit changes

## Failure Handling

1. Append error details to task file
2. Move to `failed/`
3. Clear `context/active-agent.md`
4. Log error
