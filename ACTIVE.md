---
created: 2026-01-31
tags:
  - coordination
  - active-work
  - status
status: active
updated: 2026-01-31T10:50
aliases:
  - active work
  - current tasks
---

# Active Work Coordination

> Agents check this file to avoid duplicating work.

## Currently Running

| Agent | Task | Started | Status |
|-------|------|---------|--------|
| claude-code-web | Hooks + messaging + orchestration | 2026-01-31 09:20 | ✅ Complete |
| overnight-A (Desktop) | Research + infrastructure | 2026-01-31T09:30 | ✅ Complete |

## Recent Commits This Session

### claude-code-web
1. CC hooks setup (.claude/settings.json)
2. Obsidian frontmatter conversion (all files)
3. Linux overnight runner + systemd configs
4. Inter-agent messaging system (messages/)
5. Auto-continuation orchestration

### overnight-A (Desktop)
1. Research: Recursive self-improvement patterns
2. Self-improvement: Add metrics and retrospective tracking
3. Research: Proactive assistant patterns
4. Proactive: Generate predictions for tomorrow
5. Research: Context window management
6. Pattern: Multi-agent coordination via GitHub blackboard

## Task Ownership

| Area | Owner | Notes |
|------|-------|-------|
| knowledge/research/ | overnight-A | Research docs |
| context/ | overnight-A | Infrastructure |
| .claude/ | claude-code-web | CC hooks |
| messages/ | claude-code-web | Inter-agent messaging |
| tools/orchestration/ | claude-code-web | Auto-continuation |
| prompts/ | Both | Questions |
| logs/ | Both | Activity logs |

## Coordination Rules

1. Check [[context/active-agents]] before starting
2. Log to [[logs/]]
3. Check [[context/off-limits]] before modifications
4. Commit frequently
5. Generate questions → [[prompts/pending]]

## See Also
- [[context/active-agents]] - Detailed agent tracking
- [[context/session-state]] - Recovery state
- [[context/handoff]] - Handoff protocol
- [[messages/README]] - Inter-agent messaging

---

*Last updated: 2026-01-31T10:50 by merge (claude-code-web + overnight-A)*
