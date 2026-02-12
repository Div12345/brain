---
name: daily-inbox-triage
priority: 1
estimated_tokens: 15000
mode: autonomous
timeout: 30m
skill: analyze
model_hint: haiku
tags: [recurring, vault, inbox]
depends_on: []
bead_id: brain-080
---

# Daily Inbox Triage

## Goal
Process new Inbox captures overnight — categorize and move to appropriate Spaces.

## Environment Constraints
- **Execution env:** WSL2 (overnight agent via Gemini→Desktop pipeline)
- **Working dir:** ~/brain
- **MCP tools needed:** Obsidian MCP (obsidian_list_notes, obsidian_read_note, obsidian_update_note, obsidian_delete_note)
- **Depends on:** None

## What This Task Must Produce

### 1. Moved Notes
New Inbox captures moved to correct Space, Knowledge, or Archive folder.

### 2. Morning Briefing Update
Append processing results to Dashboard/Morning Briefing.md

## Known Blockers
- Obsidian must be running for MCP tools
- Some notes may need user decision (→ leave in Inbox, add to review list)

## Success Criteria
- [ ] All new Inbox notes since last run are categorized
- [ ] Notes with clear destinations are moved
- [ ] Ambiguous notes left in Inbox with suggested destination comment
- [ ] Morning Briefing updated with what was processed

## Fallback
Leave notes in Inbox with a suggested destination tag. User processes during morning review.

## Overnight Agent Instructions
1. List Inbox/ notes, filter to those created since last triage
2. For each note: read content, determine disposition using these rules:
   - Active interest with depth → Projects/{space}/
   - Belongs to active project → Projects/{project}/
   - Reusable concept → Knowledge/
   - Sensitive/private → Personal/
   - Stale/one-off → Archive/
   - Ambiguous → Leave in Inbox, append suggested destination
3. Move notes via read→create→delete pattern
4. Update Dashboard/Morning Briefing.md with results
5. Verify: obsidian_list_notes on Inbox/ to confirm reduction

## Output
- Moved notes in their destination folders
- Dashboard/Morning Briefing.md (updated)

## Schedule
- **Frequency:** Daily
- **Trigger:** BrainOvernightGemini task (3:30 AM)
- **Via:** Gemini→Desktop pipeline or OpenCode
