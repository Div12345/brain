---
created: 2026-01-31
tags:
  - patterns
  - compaction
  - recovery
status: active
agent: overnight
---

# Compaction Recovery Pattern

Pattern for surviving Claude context compaction.

## Problem
Long sessions get compacted, losing context. Agent needs to resume seamlessly.

## Solution

Maintain recovery state in committed files:

**Tier 1: Always Read First**
- context/session-state.md - Current task, what's done
- context/active-agents.md - Who's working on what
- Recent commits (last 5-10)

**Tier 2: As Needed**
- context/predictions.md - What was planned
- prompts/pending.md - Unanswered questions
- logs/YYYY-MM-DD-agent.md - Full session history

## Recovery Protocol

```
1. Check commits: gh api repos/{owner}/{repo}/commits --jq '.[0:5]'
2. Read session-state.md
3. Read active-agents.md
4. Review what other agents completed
5. Pick unclaimed work
6. Continue
```

## Key Properties

- **Idempotent** - Can recover multiple times
- **Append-only** - Updates don't lose history
- **Self-documenting** - State files explain themselves

## When to Update

- After significant work (3-5 changes)
- Before potentially long operations
- At session end

## Related
- [[context/session-state]]
- [[knowledge/research/context-window-management]]
