---
created: 2026-01-31
tags:
  - orchestration
  - auto-continue
  - documentation
updated: 2026-01-31T10:45
---

# Auto-Continuation Orchestration

> Patterns for keeping agents running after compaction/errors.

## Problem

Claude agents can stop mid-work due to:
- Context compaction (context window limit)
- Rate limits
- Errors/crashes
- User inactivity timeout

## Solution: Auto-Continue Script

`auto-continue.sh` checks for incomplete work and restarts agents.

### How It Works

```
┌─────────────────────────────────────┐
│           Scheduled Check           │
│   (cron, systemd timer, Task Sch)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   check_incomplete_work()           │
│   - session-state.md has [ ] items? │
│   - tasks/active/ not empty?        │
│   - messages/inbox has urgent?      │
└──────────────┬──────────────────────┘
               │
        Yes    │    No
      ┌────────┴────────┐
      ▼                 ▼
┌───────────┐     ┌───────────┐
│ Run Agent │     │   Done    │
│  (retry   │     │  (exit)   │
│   up to   │     └───────────┘
│  3 times) │
└─────┬─────┘
      │
      ▼
┌─────────────────────────────────────┐
│   git add && commit && push         │
└─────────────────────────────────────┘
```

### Usage

```bash
# Run once
./tools/orchestration/auto-continue.sh

# Run with cron (every 30 minutes)
# crontab -e
*/30 * * * * /path/to/brain/tools/orchestration/auto-continue.sh
```

## Desktop Agent Continuation

For Claude Desktop (not CLI), use these patterns:

### Pattern 1: Session State Prompt

At start of each Desktop session, paste:

```
Read context/session-state.md.
Check context/priorities.md.
Continue from where previous session left off.
```

### Pattern 2: GitHub MCP Polling

Desktop with GitHub MCP can:
1. Poll `context/session-state.md` for changes
2. Read new messages from `messages/inbox/`
3. React to high-priority items

### Pattern 3: Manual Trigger File

Create `context/trigger-continue.md`:
```markdown
---
trigger: true
for: claude-desktop
reason: Compaction recovery
---

Please continue work on [task].
```

Agent checks for this file and continues.

## Integration Points

### With Overnight Runner

```bash
# In overnight-brain.sh
# After main work, check for continuation needs
./tools/orchestration/auto-continue.sh
```

### With Hooks

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PreCompact": [{
      "hooks": [{
        "type": "command",
        "command": "cp context/session-state.md context/session-state.backup.md"
      }]
    }]
  }
}
```

### With Messages

Send continuation request via messaging:
```bash
# Create continuation request
cat > messages/outbox/MSG-$(date +%FT%T)-cc-desktop.md << 'EOF'
---
from: claude-code
to: claude-desktop
priority: high
type: request
---

# Continuation Request

Please continue work. See context/session-state.md for state.
EOF

git add messages/ && git commit -m "MSG: Continuation request" && git push
```

## Configuration

Environment variables:
- `BRAIN_PATH` - Path to brain repo (default: /home/user/brain)
- `MAX_RETRIES` - Retry attempts (default: 3)
- `RETRY_DELAY` - Seconds between retries (default: 30)

## Monitoring

Logs written to: `logs/auto-continue.log`

Check status:
```bash
tail -f logs/auto-continue.log
```

## Related

- [[tools/configs/overnight-brain.sh]] - Overnight runner
- [[context/session-state]] - State persistence
- [[messages/README]] - Inter-agent messaging
- [[knowledge/tools/task-management-comparison]] - Tool comparison
