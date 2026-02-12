---
name: weekly-vault-health
priority: 2
estimated_tokens: 20000
mode: autonomous
timeout: 30m
skill: analyze
model_hint: sonnet
tags: [recurring, vault, health]
depends_on: []
bead_id: brain-081
---

# Weekly Vault Health Check

## Goal
Ensure vault stays healthy — no orphans, broken links, or forgotten notes.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain
- **MCP tools needed:** Obsidian MCP
- **Depends on:** None

## What This Task Must Produce

### 1. Health Report
Dashboard/Vault Health.md with current metrics.

### 2. Fixes Applied
Broken links repaired, orphan notes linked or archived.

## Known Blockers
- Large vault may need pagination for full scans

## Success Criteria
- [ ] Orphan notes identified (notes with no inlinks or outlinks)
- [ ] Broken links identified and fixed where possible
- [ ] Aging notes (>30 days untouched outside Archive) flagged
- [ ] Space CCs have working dataview queries
- [ ] Health report updated

## Fallback
Generate report only, flag issues for manual fix.

## Overnight Agent Instructions
1. Search for broken links: `obsidian_global_search` for `[[` patterns, cross-reference with file list
2. Find orphan notes: notes not linked from any CC or other note
3. Find aging notes: notes untouched >30 days outside Archive/
4. Check each Space CC: verify dataview queries render (no syntax errors)
5. Write results to Dashboard/Vault Health.md
6. Auto-fix: link orphans to relevant CC, archive stale captures

## Output
- Dashboard/Vault Health.md (created/updated)
- Fixed broken links
- Archived or linked orphan notes

## Schedule
- **Frequency:** Weekly (Sunday night)
- **Trigger:** BrainOvernightGemini task
- **Via:** Gemini→Desktop pipeline
