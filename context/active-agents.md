---
created: 2026-01-31
tags:
  - context
  - coordination
  - agents
updated: 2026-02-11T17:30
---

# Active Agents

> Coordination file for multi-agent work. Check before starting.

## Currently Active

| Agent | Interface | Working On | Since | Status |
|-------|-----------|------------|-------|--------|
| code-main | Claude Code | Task triage, question resolution | 2026-02-01 | Active |
| desktop-new | Claude Desktop | OneNote inventory (Task 083) | 2026-02-11 | Pending pickup |

## Claimed Work Areas

| Area | Agent | Notes |
|------|-------|-------|
| `knowledge/research/multi-agent*` | overnight-A | Coordination patterns |
| `knowledge/research/obsidian*` | overnight-B | MCP options |
| `prompts/` | overnight-B | Questions setup |
| `tasks/pending/083-windows-onenote-inventory.md` | desktop-new | Windows location scan |

## Recent Handoffs

| Time | From | To | Topic |
|------|------|----|-------|
| 17:30 | code-main | desktop-new | OneNote inventory task created |
| 09:05 | overnight-B | any | Completed Obsidian MCP research |

## Task Status

### Task 083: Windows OneNote Inventory
- **Status:** Pending pickup (ready to start)
- **Assigned To:** Claude Desktop / Overnight Agent
- **Target:** `C:\Users\din18\` (all OneNote locations)
- **Output:** `Projects/Mining Results/onenote-inventory.md` (Obsidian)
- **Priority:** HIGH (Pitt backup from Sept 2023)
- **Message:** `messages/outbox/MSG-20260211-claude-code-to-desktop-onenote-inventory.md`

## Coordination Rules

1. **Check this file** before starting work
2. **Update claiming** when starting new area
3. **Clear claim** when done with area
4. **Don't duplicate** - if claimed, work elsewhere
5. **Commit frequently** - every 5-10 min for visibility

## Agent Registration

New agents should:
1. Add themselves to "Currently Active"
2. Check claimed areas
3. Pick unclaimed work
4. Update this file

## Related
- [[context/session-state]] - Compaction-resilient state
- [[knowledge/research/multi-agent-coordination]] - Patterns
- [[context/handoff]] - Handoff protocol
