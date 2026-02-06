---
kanban-plugin: basic
tags:
  - dashboard
  - kanban
---

# CE Pipeline Board

## Backlog
- [ ] Antigravity/OC evaluation
- [ ] NotebookLM integration for lit review
- [ ] OneVault ↔ brain vault linking decision

## Brainstorm
- [ ] [[docs/brainstorms/2026-02-05-unified-workflow-framework-brainstorm|Workflow Framework]] #active

## Plan
- [ ] Cardiac output CV analysis plan
- [ ] Arterial analysis code review plan

## Work
- [ ] Multi-model quota fallback (executor.py)
- [ ] Morning briefing generation

## Review


## Compound


## Done
- [x] State.md created
- [x] Session-note template created
- [x] CE+OMC hybrid architecture documented

---

## Quick Links

- **Current State:** [[context/State.md]]
- **Priorities:** [[context/priorities.md]]
- **Recent Solutions:** [[docs/solutions/]]

---

## Dataview: Recent Sessions

```dataview
TABLE date, interface, project, ce_stage
FROM "sessions"
SORT date DESC
LIMIT 10
```

## Dataview: Pending Tasks

```dataview
TABLE priority, skill, estimated_tokens
FROM "tasks/pending"
SORT priority ASC
```
