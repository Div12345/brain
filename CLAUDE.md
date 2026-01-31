---
created: 2026-01-31
tags:
  - meta
  - claude-code
  - entry-point
status: active
aliases:
  - Claude entry
  - CC entry
---

# Brain - Self-Evolving AI Assistant System

## Quick Facts
- **Purpose:** Multi-interface Claude coordination for anticipatory assistance
- **Interfaces:** Desktop Claude, Claude Code, Overnight Agent
- **Coordination:** File-based via GitHub (blackboard pattern)

## Key Commands
```bash
# Check state
cat context/session-state.md
cat context/active-agents.md
ls tasks/pending/

# Commit work
git add -A && git commit -m "[type]: description"
```

## Directory Map
| Dir | Purpose |
|-----|---------|
| [[context/]] | Shared state, priorities, predictions |
| [[tasks/]] | Task queue (pending→active→completed) |
| [[knowledge/]] | Learned patterns, research |
| [[agents/]] | Agent definitions |
| [[tools/]] | Configs, scripts |
| [[prompts/]] | User Q&A |

## Critical Rules
1. Check [[context/active-agents]] before starting
2. Log to [[logs/]]
3. Check [[context/off-limits]] before modifications
4. Commit frequently for coordination
5. Generate questions → [[prompts/pending]]
6. Follow [[meta/contribution-workflow]] for PRs

## Task Claiming
1. Check [[tasks/pending/]]
2. Move to tasks/active/ with agent suffix
3. Update [[context/active-agents]]
4. Work
5. Move to completed/ or failed/

## Coordination
- **State:** [[context/session-state]] - Recovery state
- **Agents:** [[context/active-agents]] - Who's working on what
- **Handoffs:** [[context/handoff]] - Agent transitions
- **Questions:** [[prompts/pending]] / [[prompts/answered]]

## Git Workflow

```bash
# Start: create branch from main
git checkout -b claude/<task>-<session-suffix> origin/main

# Work: commit and push frequently
git add -A && git commit -m "[type]: description"
git push -u origin claude/<branch>

# Coordinate: send messages to other agents
echo "..." > messages/outbox/MSG-<timestamp>-<from>-<to>.md

# Finish: create PR or request merge
# See [[meta/contribution-workflow]] for details
```

## See Also
- [[meta/contribution-workflow]] - Full PR/contribution guide
- [[messages/README]] - Inter-agent messaging
- [[agents/overnight]] - Overnight agent definition
- [[HOME]] - Obsidian home page
