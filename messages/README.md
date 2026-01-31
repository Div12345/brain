---
created: 2026-01-31
tags:
  - messages
  - coordination
  - inter-agent
updated: 2026-01-31T10:20
---

# Inter-Agent Messaging

> File-based messaging for coordinating agents across worktrees/checkouts.

## Philosophy

Git is the message bus. Each agent pushes messages, pulls to receive.

## Directory Structure

```
messages/
├── inbox/          # Messages TO check (pull before reading)
├── outbox/         # Messages FROM this agent (push after writing)
└── archive/        # Processed messages
```

## Message Format

Filename: `MSG-[timestamp]-[from]-[to].md`

Example: `MSG-2026-01-31T10-30-00-claude-code-desktop.md`

```markdown
---
from: claude-code-web
to: claude-desktop | claude-code | overnight | all
timestamp: 2026-01-31T10:30:00Z
priority: high | normal | low
type: request | response | notification | sync
expires: 2026-01-31T23:59:59Z  # optional
---

# Subject Line

## Message

[Content]

## Context

[Links to relevant files]

## Action Required

- [ ] [Specific action]

## Response To

[MSG-id if this is a response]
```

## Protocol

### Sending a Message

1. Create message file in `messages/outbox/`
2. `git add messages/outbox/`
3. `git commit -m "MSG: [brief description]"`
4. `git push`

### Receiving Messages

1. `git pull` (or `git fetch && git merge`)
2. Check `messages/inbox/` for new messages addressed to you
3. Process message
4. Move to `messages/archive/` with response appended
5. Commit and push

### Force Alignment (Urgent)

For urgent coordination:

1. Write to `messages/outbox/` with `priority: high`
2. Also update `context/handoff.md` with sync request
3. Push immediately
4. Other agent should check on next iteration

## Message Types

| Type | When to Use |
|------|-------------|
| `request` | Ask another agent to do something |
| `response` | Reply to a request |
| `notification` | FYI, no action needed |
| `sync` | Request state synchronization |

## Example Messages

### Request Task Handoff
```markdown
---
from: claude-code-web
to: claude-desktop
priority: normal
type: request
---

# Task Handoff: Review overnight runner

## Message

I've created the Linux overnight runner. Please review and test.

## Action Required

- [ ] Review tools/configs/overnight-brain.sh
- [ ] Test on actual Linux system
```

### Sync Request
```markdown
---
from: claude-code-web
to: all
priority: high
type: sync
---

# Sync: Pull latest changes

## Message

Major updates pushed. All agents should pull before continuing.

## Context

- CC hooks configured
- All files have Obsidian frontmatter
- Linux runner created
```

## Hooks Integration

The Stop hook can automatically check for urgent messages:

```bash
# In overnight-brain.sh
git fetch origin
URGENT=$(find messages/inbox -name "MSG-*-high-*.md" 2>/dev/null | wc -l)
if [ "$URGENT" -gt 0 ]; then
    echo "URGENT: $URGENT high-priority messages waiting"
fi
```

## Related

- [[context/handoff]] - Handoff protocol
- [[context/active-agent]] - Who's working
- [[tools/orchestration/DESIGN]] - Architecture
