---
name: weekly-connection-suggestions
priority: 3
estimated_tokens: 25000
mode: autonomous
timeout: 30m
skill: analyze
model_hint: sonnet
tags: [recurring, vault, anticipatory]
depends_on: []
bead_id: brain-082
---

# Weekly Connection Suggestions

## Goal
Update HOME.md "Connections You Might Miss" with fresh cross-space insights.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain
- **MCP tools needed:** Obsidian MCP
- **Depends on:** None

## What This Task Must Produce

### 1. Updated Connections Section
Fresh cross-pollination suggestions in Dashboard/HOME.md

### 2. Space CC Updates
New "Related Knowledge" entries where applicable

## Known Blockers
- Needs semantic understanding of note content (use smarter model)

## Success Criteria
- [ ] At least 3 new cross-space connections identified
- [ ] Connections are non-obvious (not just "both are about health")
- [ ] HOME.md connections section updated
- [ ] At least 2 Space CCs get new connection links

## Fallback
Generate suggestions in a temp note for user review instead of direct edits.

## Overnight Agent Instructions
1. Read all Space CCs to understand current focus areas
2. Read recent notes (modified in last 7 days) across all Spaces
3. Read Knowledge/ notes for cross-cutting concepts
4. Identify surprising connections:
   - Methodological parallels (e.g., tracking patterns in sim racing ↔ yoga)
   - Conceptual bridges (e.g., wave analysis ↔ music theory)
   - Emotional threads (e.g., writing about silence ↔ meditation practice)
5. Update HOME.md "Connections You Might Miss" section via obsidian_search_replace
6. Add relevant cross-links to 2-3 Space CCs

## Output
- Dashboard/HOME.md (updated connections section)
- Updated Space Command Centers (2-3)

## Schedule
- **Frequency:** Weekly (Wednesday night)
- **Trigger:** BrainOvernightGemini task
- **Via:** Gemini→Desktop pipeline
