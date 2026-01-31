---
created: 2026-01-31
tags:
  - patterns
  - coordination
  - learned
status: active
agent: overnight
---

# Multi-Agent Coordination Pattern

Pattern learned from overnight session 2026-01-31.

## Pattern Name
GitHub Blackboard Coordination

## Problem
Multiple Claude instances need to work on same codebase without conflicts.

## Solution

Use GitHub repo as shared blackboard:
1. **Commits = Broadcast** - Commit messages signal work to other agents
2. **File-level locking** - Each agent works on different files
3. **Claim tracking** - context/active-agents.md shows who's doing what
4. **Recovery state** - context/session-state.md survives compaction

## Implementation

```
Before starting:
1. git pull / check recent commits
2. Read context/active-agents.md
3. Claim work area via commit
4. Update session-state.md

During work:
1. Commit frequently (every 3-5 changes)
2. Use prefixes: Research:, Coordination:, Task:, Obsidian:
3. Work on unclaimed file areas

After work:
1. Update session-state.md
2. Generate predictions.md
3. Update logs/
```

## When to Use
- Overnight parallel sessions
- Desktop + CC coordination
- Any multi-agent scenario

## Trade-offs
- Requires discipline to check before starting
- Merge conflicts still possible
- No real-time coordination (async only)

## Related
- [[knowledge/research/multi-agent-coordination]]
- [[context/active-agents]]
- [[context/session-state]]
