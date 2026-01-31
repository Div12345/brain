---
created: 2026-01-31
tags:
  - design
  - orchestration
  - architecture
updated: 2026-01-31T09:45
agent: desktop-architect
aliases:
  - orchestration design
  - task queue design
---

# Orchestration Layer Design

> Practical design for coordinating Claude Desktop + Claude Code via this repo.

## Design Philosophy

**Simple first, scale later.** Start with file-based coordination that any interface can read/write. Add complexity only when proven necessary.

---

## Architecture

```
┌─────────────────── BRAIN REPO (GitHub) ───────────────────┐
│                                                           │
│   tasks/pending/     ←── Agents pick up work here        │
│   tasks/active/      ←── Mark what you're doing          │
│   tasks/completed/   ←── Drop finished work              │
│   context/           ←── Shared state                    │
│   logs/              ←── Activity records                │
│                                                           │
└─────────────────────────────────────────────────────────────┘
           ↑                    ↑                    ↑
           │                    │                    │
    ┌──────┴──────┐     ┌──────┴──────┐     ┌──────┴──────┐
    │   Desktop   │     │ Claude Code │     │  Scheduled  │
    │   (Opus)    │     │  (Terminal) │     │    Jobs     │
    └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Task Queue Format

### Location: `tasks/pending/`

Each task is a markdown file with YAML frontmatter:

```markdown
---
id: task-2026-01-31-001
created: 2026-01-31T02:30:00Z
priority: medium
requires:
  - code_execution
  - file_access
preferred_interface: claude-code
timeout: 60m
status: pending
---

# Task: Analyze vault folder structure

## Input
Obsidian vault at `D:\Obsidian\main-vault`

## Expected Output
- Folder tree analysis in `knowledge/insights/vault-structure.md`
- Recommended reorganization plan

## Context
- See `context/priorities.md` for why this matters
- User wants to consolidate scattered notes
```

### Lifecycle

1. **pending/** — Waiting for pickup
2. **active/** — Agent renames file to include their ID: `task-001.claude-code.md`
3. **completed/** — Moved here with results appended
4. **failed/** — Moved here with error info

---

## Agent Claiming Protocol

When an agent starts:

1. Read `tasks/pending/` for available tasks
2. Check `tasks/active/` — don't duplicate work
3. Claim by moving file to `tasks/active/` with agent suffix
4. Update `context/active-agent.md`

```markdown
<!-- context/active-agent.md -->
---
agent: claude-code
started: 2026-01-31T02:30:00Z
task: task-2026-01-31-001
expected_completion: 2026-01-31T03:30:00Z
---
```

---

## Desktop ↔ Claude Code Coordination

### Communication Channels

| From | To | Method |
|------|-----|--------|
| Desktop | CC | Write task to `tasks/pending/` |
| CC | Desktop | Write to `context/handoff.md` |
| Either | User | Write to `prompts/pending.md` |
| User | Either | Write to `prompts/answered.md` |

### Handoff Protocol

When Desktop creates work for CC:

```markdown
<!-- context/handoff.md -->
## For Claude Code

### Task
Run overnight vault analysis

### Files Modified
- Created `tasks/pending/task-2026-01-31-001.md`

### Notes
- Use AIM memory MCP if available
- Write insights to knowledge/insights/
- Commit frequently

### Blocking Issues
None currently
```

---

## Scheduling Design (Windows)

### Option A: Windows Task Scheduler (Recommended)

**Trigger:** Daily at 2:00 AM  
**Action:** PowerShell script → Claude Code

```powershell
# overnight-brain.ps1
$logFile = "C:\brain\logs\$(Get-Date -Format 'yyyy-MM-dd')-overnight.log"
Set-Location C:\brain

# Check for pending tasks
$pendingTasks = Get-ChildItem -Path ".\tasks\pending\*.md"

if ($pendingTasks.Count -gt 0) {
    "Starting overnight run at $(Get-Date)" | Out-File $logFile
    
    # Run Claude Code with the overnight prompt
    claude --dangerously-skip-permissions -p (Get-Content ".\agents\overnight.md" -Raw) 2>&1 | Out-File $logFile -Append
    
    "Completed at $(Get-Date)" | Out-File $logFile -Append
}
```

### Option B: WSL + cron

```bash
# Edit with: wsl crontab -e
0 2 * * * cd /mnt/c/brain && bash ./scripts/overnight.sh >> /mnt/c/brain/logs/cron.log 2>&1
```

---

## CC Hookify Rule (Draft)

For Claude Code to auto-check tasks on startup:

```markdown
<!-- ~/.claude/CLAUDE.md or project CLAUDE.md -->

## On Session Start

1. Check `tasks/pending/` for assigned work
2. If tasks exist matching my capabilities:
   - Claim the highest priority one
   - Update `context/active-agent.md`
3. If no tasks, proceed with user's request
4. Before finishing, check if anything needs handoff to Desktop
```

**Note:** Hookify integration TBD — need to test if hooks can run on session start.

---

## Usage Tracking Integration

### Option 1: Manual Logging

Agents append to `context/usage.md`:

```yaml
# context/usage.md
last_updated: 2026-01-31T03:00:00Z

claude_code:
  sessions_today: 3
  estimated_tokens: ~50000
  last_session: 2026-01-31T02:30:00Z

claude_desktop:
  messages_today: 12
  last_message: 2026-01-31T01:15:00Z
```

### Option 2: Automated (Future)

Integrate `tosage` or `claude-pulse` to auto-update metrics.

---

## Safety Mechanisms

1. **Claim locks** — Only one agent works a task
2. **Timeout detection** — If `active-agent.md` stale >2 hours, task can be reclaimed
3. **No delete without archive** — Failed tasks go to `tasks/failed/`, not deleted
4. **Commit frequently** — Progress survives crashes
5. **Human gates** — Some tasks require `prompts/pending.md` approval first

---

## Implementation Phases

### Phase 1: Basic Coordination (This Week)
- [x] Research complete
- [x] Create `tasks/` directory structure
- [x] Write first overnight task (hooks setup)
- [ ] Test Windows Task Scheduler

### Phase 2: Automated Scheduling (Next)
- [ ] Deploy PowerShell scheduled job
- [x] Add CC startup hook (SessionStart in `.claude/settings.json`)
- [ ] Test full overnight run

### Phase 3: Usage Awareness
- [ ] Integrate tosage or claude-pulse
- [ ] Add limit warnings to context

### Phase 4: Multi-Agent (If Needed)
- [ ] Evaluate claude-flow
- [ ] Consider parallel execution modes

---

## Open Questions (→ prompts/pending.md)

1. What's your overnight availability preference? (daily? weekdays only?)
2. Should failed tasks notify you immediately or batch for morning review?
3. Any tasks that should NEVER run unattended?
4. Where is your Obsidian vault located exactly?

---

*Design by Desktop Orchestration Architect Agent — 2026-01-31*
