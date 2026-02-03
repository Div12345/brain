# CC Scheduler - Design Document

> A thin coordination layer for scheduled Claude Code execution, integrated with the brain system.

## Philosophy

**From brain repo core principles:**
- Low friction above all
- File-based coordination (blackboard pattern)
- Structured logging for accessibility
- Self-improving through iteration
- Simple > clever

**Applied to scheduler:**
- Minimal moving parts
- Uses existing brain structure (tasks/, logs/, context/)
- Everything is a readable file (no opaque databases)
- Easy to understand, modify, extend
- Command center for orchestration, not a complex system

---

## Core Loop

```
┌─────────────────────────────────────────────────────────────┐
│                     THE SCHEDULING LOOP                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   YOU (planning)                                            │
│     │                                                       │
│     ▼                                                       │
│   tasks/pending/*.md  ◄──── Create task files               │
│     │                                                       │
│     ▼                                                       │
│   ccq run (triggered)  ◄──── Manual / Scheduled / On-reset  │
│     │                                                       │
│     ├─► Check capacity (ccusage)                            │
│     │     └─► No capacity? Wait/retry/abort                 │
│     │                                                       │
│     ├─► Load task + agent + rules                           │
│     │                                                       │
│     ├─► Move: pending/ → active/                            │
│     │     └─► Update context/active-agents.md               │
│     │                                                       │
│     ├─► Execute claude with full context                    │
│     │     └─► Working dir, MCPs, timeout                    │
│     │                                                       │
│     ├─► Capture output                                      │
│     │                                                       │
│     ├─► Move: active/ → completed/ or failed/               │
│     │                                                       │
│     ├─► Log to logs/scheduler/                              │
│     │                                                       │
│     └─► Next task (if queue not empty)                      │
│                                                             │
│   YOU (reviewing)                                           │
│     │                                                       │
│     ▼                                                       │
│   Review: logs/, knowledge/, prompts/pending/               │
│     │                                                       │
│     ▼                                                       │
│   Iterate: adjust tasks, priorities, rules                  │
│     │                                                       │
│     └─────────────────────► (loop continues)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Integration Map

```
EXISTING (brain repo)              SCHEDULER (new)
─────────────────────              ────────────────
tasks/
├── pending/       ◄─────────────── ccq reads queue from here
├── active/        ◄─────────────── ccq moves task here during execution
├── completed/     ◄─────────────── ccq moves successful tasks here
└── failed/        ◄─────────────── ccq moves failed tasks here

agents/
├── overnight.md   ◄─────────────── ccq loads agent persona
└── rules.md       ◄─────────────── ccq loads safety rules (NEW)

context/
├── priorities.md  ◄─────────────── ccq injects into task context
├── active-agents.md ◄───────────── ccq updates when task starts/ends
└── session-handoff.md ◄─────────── ccq can inject for continuity

logs/
└── scheduler/     ◄─────────────── ccq writes execution logs (NEW)
    ├── YYYY-MM-DD-HH-MM-taskname.md
    └── index.jsonl                  (append-only run index)

prompts/
└── pending/       ◄─────────────── tasks can generate questions for you

tools/
└── cc-scheduler/  ◄─────────────── scheduler code lives here (NEW)
    ├── DESIGN.md                    (this file)
    ├── ccq                          (main script)
    ├── lib/                         (modules)
    └── config.yaml                  (scheduler settings)
```

---

## Data Structures

### Task File (`tasks/pending/*.md`)

```markdown
---
name: zotero-weekly-digest
agent: overnight           # loads agents/overnight.md (optional, defaults to none)
mode: autonomous           # read-only | plan-first | autonomous
timeout: 30m               # max execution time
working_dir: ~/brain       # where claude runs (optional, defaults to ~/brain)
priority: 1                # lower = runs first (optional, defaults to 100)
tags: [research, weekly]   # for filtering/searching (optional)
created: 2026-02-03
---

## Task

Summarize papers added to Zotero in the last 7 days.
Focus on papers related to:
- Arterial compliance / blood pressure modeling
- Transfer functions in physiological systems
- Machine learning for biomedical signals

## Output

- Save digest to `knowledge/research/zotero-weekly-YYYY-MM-DD.md`
- If anything urgent or highly relevant found, note in `context/priorities.md`
- Questions for me → `prompts/pending/`

## Success Criteria

- Digest file exists with paper summaries
- Each paper has: title, authors, relevance score, key findings
```

**Minimal task (just a prompt):**

```markdown
---
name: quick-scan
timeout: 10m
---

List all TODO comments in ~/research/arterial-compliance/src/
```

### Agent Definition (`agents/overnight.md`)

Already exists. Key sections scheduler uses:
- Identity/persona (injected as system context)
- Capabilities (what it can do)
- Restrictions (what it cannot do)
- Output formats (how to structure output)

### Rules File (`agents/rules.md`) - NEW

```markdown
---
name: scheduler-rules
applies_to: all-scheduled-tasks
---

# Safety Rules for Scheduled Execution

## File Safety
- NEVER delete files without backup
- NEVER modify outside working_dir without explicit instruction
- NEVER touch: .env*, *.key, .ssh/*, ~/.config/*

## Git Safety
- NEVER force push
- NEVER commit to main directly (use branches)
- Commits need descriptive messages

## Brain Conventions
- Research output → knowledge/
- Logs → logs/
- Questions → prompts/pending/
- Follow Obsidian link conventions [[like-this]]

## Execution Limits
- Respect timeout
- If stuck > 5 minutes on one thing, log and move on
- Max 100 tool calls per task

## On Error
- Log full error with context
- Don't retry automatically
- Exit gracefully
```

### Log Entry (`logs/scheduler/YYYY-MM-DD-HH-MM-taskname.md`)

```markdown
---
task: zotero-weekly-digest
started: 2026-02-03T00:05:12
ended: 2026-02-03T00:18:45
duration: 13m 33s
status: completed          # completed | failed | timeout | interrupted
agent: overnight
mode: autonomous
working_dir: ~/brain
---

# Execution Log: zotero-weekly-digest

## Summary
Successfully generated weekly Zotero digest with 7 papers.

## Output Files Created
- knowledge/research/zotero-weekly-2026-02-03.md

## Context Updates
- None

## Questions Generated
- None

## Errors
- None

## Token Usage
- Prompt: ~2,400 tokens
- Response: ~8,200 tokens
- Total: ~10,600 tokens

## Full Transcript

<details>
<summary>Click to expand</summary>

[Full claude output here, collapsed by default]

</details>
```

### Run Index (`logs/scheduler/index.jsonl`)

Append-only, one JSON object per line:

```jsonl
{"id":"run-001","task":"zotero-weekly-digest","started":"2026-02-03T00:05:12","ended":"2026-02-03T00:18:45","status":"completed","duration_sec":813,"log_file":"2026-02-03-00-05-zotero-weekly-digest.md"}
{"id":"run-002","task":"arterial-todos","started":"2026-02-03T00:19:01","ended":"2026-02-03T00:24:33","status":"completed","duration_sec":332,"log_file":"2026-02-03-00-19-arterial-todos.md"}
{"id":"run-003","task":"overnight-research","started":"2026-02-03T00:25:00","ended":"2026-02-03T00:47:22","status":"failed","duration_sec":1342,"log_file":"2026-02-03-00-25-overnight-research.md","error":"timeout"}
```

### Scheduler Config (`tools/cc-scheduler/config.yaml`)

```yaml
# CC Scheduler Configuration

# Paths (relative to brain repo root)
paths:
  tasks_pending: tasks/pending
  tasks_active: tasks/active
  tasks_completed: tasks/completed
  tasks_failed: tasks/failed
  agents: agents
  rules: agents/rules.md
  logs: logs/scheduler
  context_priorities: context/priorities.md
  context_agents: context/active-agents.md

# Execution defaults
defaults:
  agent: null                    # no agent persona by default
  mode: read-only                # safe default
  timeout: 30m
  working_dir: ~/brain

# Scheduling
schedule:
  enabled: false
  time: "00:05"                  # 12:05 AM
  check_capacity: true           # check ccusage before running
  retry_if_no_capacity: true
  retry_interval: 15m
  max_retries: 4

# Capacity checking
capacity:
  min_tokens: 1000000            # 1M tokens minimum to start queue
  min_time: 30m                  # 30 min minimum remaining

# Notifications (future)
notify:
  enabled: false
  method: null                   # ntfy | telegram | none
```

---

## Commands

### `ccq status`

Shows current state at a glance.

```
$ ccq status

┌─ Usage ─────────────────────────────────────────────────────┐
│ Block: 7:00 PM → 12:00 AM                                   │
│ Used:  42.1% (25.7M / 61M)   Remaining: 1h 23m             │
╰─────────────────────────────────────────────────────────────╯

┌─ Queue ─────────────────────────────────────────────────────┐
│ pending:   3    active: 0    today: 2 ✓  1 ✗               │
│                                                             │
│ Next: zotero-weekly-digest (autonomous, 30m)               │
╰─────────────────────────────────────────────────────────────╯

┌─ Schedule ──────────────────────────────────────────────────┐
│ Armed: 12:05 AM daily    Last: 2026-02-02 00:05 (3 tasks)  │
╰─────────────────────────────────────────────────────────────╯
```

### `ccq list`

Shows task queue with details.

```
$ ccq list

PENDING (3)
  1. zotero-weekly-digest     autonomous  30m   p:1
  2. arterial-todos           read-only   10m   p:2
  3. overnight-research       autonomous  60m   p:3

ACTIVE (0)

COMPLETED TODAY (2)
  ✓ project-scan              00:05  12m
  ✓ inbox-triage              00:18  8m

FAILED TODAY (1)
  ✗ web-research              00:27  timeout after 30m
```

### `ccq add`

Add a task to the queue.

```bash
# Quick add (minimal task)
ccq add "Summarize recent papers on transfer functions"

# Add from file
ccq add -f my-task.md

# Interactive add
ccq add -i
```

### `ccq edit <task>`

Open task in $EDITOR.

```bash
ccq edit zotero-weekly-digest
# Opens tasks/pending/001-zotero-weekly-digest.md in $EDITOR
```

### `ccq run`

Execute tasks.

```bash
# Run next pending task
ccq run

# Run all pending tasks
ccq run --all

# Run specific task
ccq run zotero-weekly-digest

# Dry run (show what would happen)
ccq run --dry

# Run only if capacity available
ccq run --if-available

# Force run even if low capacity
ccq run --force
```

### `ccq logs`

View execution history.

```bash
# Recent runs
ccq logs

# Specific run
ccq logs zotero-weekly-digest

# Today's runs
ccq logs --today

# Follow mode (for active runs)
ccq logs -f
```

### `ccq schedule`

Manage automatic scheduling.

```bash
# Show schedule status
ccq schedule

# Enable daily at 12:05 AM
ccq schedule set 00:05

# Disable
ccq schedule disable

# Test trigger (runs scheduler logic without executing)
ccq schedule test
```

### `ccq` (no args)

TUI dashboard (future, module 8).

---

## Execution Detail

### What happens when `ccq run` executes a task:

```python
def run_task(task_path):
    # 1. Load task
    task = parse_task_file(task_path)
    
    # 2. Check capacity (unless --force)
    if not check_capacity():
        return Result.NO_CAPACITY
    
    # 3. Load agent (if specified)
    agent_context = ""
    if task.agent:
        agent_context = load_file(f"agents/{task.agent}.md")
    
    # 4. Load rules
    rules = load_file("agents/rules.md")
    
    # 5. Load current priorities (for context)
    priorities = load_file("context/priorities.md")
    
    # 6. Build prompt
    prompt = f"""
{agent_context}

## Safety Rules
{rules}

## Current Priorities
{priorities}

## Your Task
{task.prompt}
"""
    
    # 7. Move to active
    move_file(task_path, f"tasks/active/{task.filename}")
    update_active_agents(task.name, "running")
    
    # 8. Execute
    result = execute_claude(
        prompt=prompt,
        working_dir=task.working_dir,
        timeout=task.timeout,
        mode=task.mode  # affects --dangerously-skip-permissions
    )
    
    # 9. Move to completed/failed
    dest = "completed" if result.success else "failed"
    move_file(f"tasks/active/{task.filename}", f"tasks/{dest}/{task.filename}")
    update_active_agents(task.name, "done")
    
    # 10. Log
    write_log(task, result)
    append_to_index(task, result)
    
    return result
```

### Claude invocation modes

| Mode | Command | Use Case |
|------|---------|----------|
| `read-only` | `claude -p "prompt"` | Safe queries, no file changes |
| `plan-first` | `claude -p "prompt" --allowedTools Read,Grep,Glob` | Can read, plan, but not modify |
| `autonomous` | `claude -p "prompt" --dangerously-skip-permissions` | Full autonomous execution |

---

## Future Considerations

### Phase 1 (Now)
- [x] Design document
- [ ] `ccq status` - usage + queue overview
- [ ] `ccq list` - show tasks
- [ ] `ccq run` - execute single task
- [ ] `ccq logs` - view results
- [ ] Basic logging

### Phase 2 (Soon)
- [ ] `ccq add` - create tasks
- [ ] `ccq edit` - modify tasks
- [ ] `ccq schedule` - Windows Task Scheduler integration
- [ ] Retry logic for capacity issues

### Phase 3 (Later)
- [ ] TUI dashboard
- [ ] Phone access (Termux SSH or simple web UI)
- [ ] Notifications (ntfy.sh)
- [ ] omc integration (boulder state updates)

### Phase 4 (Future)
- [ ] Multi-task parallelism (if multiple usage blocks)
- [ ] Task dependencies (run B after A)
- [ ] Recurring tasks (daily, weekly)
- [ ] Usage analytics / predictions

---

## Open Questions (To Resolve As We Build)

1. **Task naming**: Auto-generate IDs (001-, 002-) or use slugified names?

2. **Priority handling**: Sort by priority field, or by filename order?

3. **Timeout enforcement**: Hard kill, or graceful shutdown signal?

4. **Context injection**: How much of brain context to include? Just priorities, or more?

5. **MCP access**: All MCPs available always, or per-task declaration?

6. **Git integration**: Auto-commit after each run, or leave for manual commit?

7. **Multiple active tasks**: Allow parallel execution, or strict single-task?

---

## Implementation Notes

### Language Choice: Python

Reasons:
- Easy YAML/Markdown parsing (frontmatter, etc.)
- subprocess for claude CLI
- Rich ecosystem for TUI (textual, rich)
- Already in your env (conda)
- Readable and maintainable

### File Structure

```
tools/cc-scheduler/
├── DESIGN.md              # This document
├── ccq                    # Main entry point (executable)
├── config.yaml            # Settings
├── lib/
│   ├── __init__.py
│   ├── capacity.py        # ccusage integration
│   ├── tasks.py           # Task parsing and management
│   ├── executor.py        # Claude execution
│   ├── logging.py         # Log management
│   └── ui.py              # Output formatting
└── tests/
    └── ...
```

### Dependencies

```
# Minimal
pyyaml          # Config/task parsing
python-frontmatter  # Markdown frontmatter parsing

# For TUI (later)
rich            # Pretty terminal output
textual         # TUI framework (if we go that route)
```

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-03 | Use existing tasks/ structure | Don't reinvent, integrate |
| 2026-02-03 | Python for implementation | Best balance of simplicity and capability |
| 2026-02-03 | Standalone first, omc integration later | Start simple, add complexity as needed |
| 2026-02-03 | File-based everything | Matches brain philosophy, easy to inspect/debug |

---

## References

- [brain repo CLAUDE.md](../../../CLAUDE.md)
- [overnight agent](../../agents/overnight.md)
- [ClaudeNightsWatch](https://github.com/aniketkarne/ClaudeNightsWatch)
- [overnight tool](https://github.com/yail259/overnight)
- [ccusage](https://github.com/ryoppippi/ccusage)
