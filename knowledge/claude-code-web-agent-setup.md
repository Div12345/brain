---
created: 2026-01-31
tags:
  - knowledge
  - claude-code
  - hooks
  - web-agent
  - configuration
updated: 2026-01-31T09:30
agent: claude-code-web
---

# Claude Code Web Agent Setup

Documentation for running brain orchestration via remote Claude Code web agents.

## Environment

| Property | Value |
|----------|-------|
| User | root |
| Shell | /bin/bash |
| Node | /opt/node22/bin/node |
| Python | /usr/local/bin/python3 |
| Git | /usr/bin/git |

## Configuration Files

### Project-Level: `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "type": "command",
          "command": "head -25 \"$CLAUDE_PROJECT_DIR/context/priorities.md\" | tail -n +10",
          "timeout": 5,
          "statusMessage": "Loading brain context..."
        }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "cat \"$CLAUDE_PROJECT_DIR/context/active-agent.md\" 2>/dev/null || true",
          "timeout": 3
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "echo \"$(date -Iseconds) | Session stop\" >> \"$CLAUDE_PROJECT_DIR/logs/cc-sessions.log\"",
          "timeout": 5,
          "async": true
        }]
      }
    ]
  }
}
```

### User-Level: `~/.claude/settings.json`

Pre-configured with:
- Stop hook for git commit/push verification
- Skill permission enabled

### Hook Scripts

Located in `.claude/hooks/`:
- `session-log.sh` - Structured session logging

## Hook Events Reference

| Event | Purpose | Our Usage |
|-------|---------|-----------|
| `SessionStart` | On session begin | Load priorities context |
| `UserPromptSubmit` | Before processing prompt | Show active agent |
| `Stop` | When Claude stops responding | Log session activity |

## Capabilities Available

### Tools
- Full filesystem access
- Git operations
- Node.js (v22)
- Python 3
- Standard Unix tools

### Plugins
- Official Claude plugins marketplace available at `~/.claude/plugins/marketplaces/`

### Not Available
- MCP servers (no .mcp.json configured)
- Browser automation (no Playwright)
- External API access may be limited

## Workflow

1. **On Session Start**: Automatically see current priorities
2. **On Each Prompt**: See active agent status (prevents conflicts)
3. **On Session End**: Automatically logs to `logs/cc-sessions.log`

## Files Created

| File | Purpose |
|------|---------|
| `.claude/settings.json` | Hooks configuration |
| `.claude/hooks/session-log.sh` | Session logging script |
| `context/active-agent.md` | Coordination tracking |

## Testing Hooks

```bash
export CLAUDE_PROJECT_DIR="/home/user/brain"

# Test SessionStart
head -25 "$CLAUDE_PROJECT_DIR/context/priorities.md" | tail -n +10

# Test UserPromptSubmit
cat "$CLAUDE_PROJECT_DIR/context/active-agent.md"

# Test Stop
echo "$(date -Iseconds) | Test" >> "$CLAUDE_PROJECT_DIR/logs/cc-sessions.log"
```

## Related

- [[tasks/pending/task-cc-001-hooks-setup]] - Original task
- [[inspirations/claude-code-ecosystem]] - Ecosystem research
- [[.claude/skills/brain-system/SKILL]] - Brain system skill

---

*Generated: 2026-01-31 by claude-code-web*
