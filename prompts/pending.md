---
created: 2026-01-31
tags:
  - prompts
  - questions
  - status/pending
updated: 2026-01-31T08:56
---

# Pending Questions

> Questions from agents awaiting user response.

## Q-2026-01-31-01: Overnight Schedule
**Priority:** Medium  
**From:** overnight agent  
**Blocks:** Automated scheduling

When should overnight runs happen?
- Specific time (e.g., 2am-6am)?
- On-demand only?
- When you say "goodnight"?

---

## Q-2026-01-31-02: Obsidian Vault Path
**Priority:** High  
**From:** overnight agent  
**Blocks:** Vault sync, MCP integration

What's the full path to your main Obsidian vault?  
Needed for:
- Obsidian MCP configuration
- claude-obsidian-sync hooks
- Vault analysis

---

## Q-2026-01-31-03: Failed Task Notification
**Priority:** Low  
**From:** overnight agent  
**Blocks:** Error handling design

How should I notify you of failed tasks?
- Leave in [[prompts/pending]]?
- Email (if Gmail MCP added)?
- Just log to [[logs/]]?

---

## Q-2026-01-31-04: Off-Limits Tasks
**Priority:** Medium  
**From:** overnight agent  
**Blocks:** [[context/off-limits]] completion

Any specific tasks/domains I should never touch autonomously?
- Specific repos?
- Financial data?
- Work vs personal boundaries?

---

## Q-2026-01-31-05: Brain Repo Local Path
**Priority:** Low  
**From:** overnight agent  
**Blocks:** CC local integration

Confirm local path:  
`C:\Users\din18\OneDrive - University of Pittsburgh\Work\Github\brain`

Is this correct for CC hooks?

---

## How to Answer

1. Reply in conversation OR
2. Edit this file directly and move to [[prompts/answered]]

Agents check this file at session start.
