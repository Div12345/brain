# Brain - Self-Evolving AI Assistant System

## Quick Facts
- **Purpose:** Multi-interface Claude coordination for anticipatory assistance
- **Interfaces:** Desktop Claude, Claude Code, Overnight Agent
- **Coordination:** File-based task queue via GitHub

## Key Commands
```bash
# Check state
cat context/priorities.md
cat context/active-agent.md
ls tasks/pending/

# Commit work
git add -A && git commit -m "[type]: description"
```

## Directory Map
| Dir | Purpose |
|-----|---------|
| `context/` | Shared state, priorities |
| `tasks/` | Task queue (pending→active→completed) |
| `knowledge/` | Learned patterns |
| `agents/` | Agent definitions |
| `tools/` | Configs, scripts |
| `prompts/` | User Q&A |

## Critical Rules
1. Check `context/active-agent.md` before starting
2. Log everything to `logs/`
3. Never modify without checking `context/off-limits.md`
4. Keep commits atomic
5. Generate questions for ambiguity → `prompts/pending.md`

## Task Claiming
1. Check `tasks/pending/`
2. Move to `tasks/active/` with suffix: `task.claude-code.md`
3. Update `context/active-agent.md`
4. Work
5. Move to `completed/` or `failed/`
6. Clear active-agent

## Coordination
- **Handoffs:** Write to `context/handoff.md`
- **Questions:** Write to `prompts/pending.md`
- **Answers:** Read from `prompts/answered.md`

## See Also
- `.claude/skills/brain-system/SKILL.md` - Full skill reference
- `agents/overnight.md` - Overnight agent definition
- `tools/orchestration/DESIGN.md` - Architecture design
