---
created: 2026-02-01
tags:
  - context
  - meta
  - workflow
  - observations
updated: 2026-02-01
---

# Workflow Observations

> Running log of patterns, friction points, and improvement opportunities.

## Format

```markdown
### [DATE] - [Category]
**Observed:** What happened
**Pattern:** Why it matters
**Suggestion:** Potential improvement
**Status:** noted | proposed | implemented | rejected
```

---

## Observations

### 2026-02-01 - Daily vs Project Notes
**Observed:** 357 daily notes with 9-section template, only "Today's Focus" used (stream-of-consciousness). But arterial_analysis Command Center is rich, structured, actively maintained.
**Pattern:** Template mismatch - daily template doesn't fit actual work style. Project notes work better.
**Suggestion:** Replace daily template with project-centric format. Daily note = "What I worked on" + links to project notes.
**Status:** proposed

### 2026-02-01 - arterial_analysis Maturity
**Observed:** Sophisticated Hamilton pipeline (L1-L6), rigorous methodology (in-fold filtering per Vabalas 2019), clear open questions about feature selection validation.
**Pattern:** This is production-quality research infrastructure. Open questions map directly to "ML pipeline coverage" completion criteria.
**Suggestion:** The 4 open questions in Command Center ARE the completion checklist.
**Status:** noted

### 2026-02-01 - Tool Integration
**Observed:** Claude Desktop ↔ Code bridge built to enable cross-interface communication
**Pattern:** User works across multiple Claude interfaces, needs coordination
**Suggestion:** Use bridge for context handoffs, overnight summaries
**Status:** implemented

### 2026-02-01 - Daily Notes
**Observed:** 8+ sections in template, only 2 used. Tomorrow's Intent disconnected from next day.
**Pattern:** Template friction → abandonment of features
**Suggestion:** Pattern analysis task created to find what's actually useful
**Status:** noted (task pending)

### 2026-02-01 - Code Verification
**Observed:** User runs many unstructured cross-verifications on Claude code
**Pattern:** Lack of confidence → excessive manual checking
**Suggestion:** Structured verification workflow with learning component
**Status:** noted (task pending)

### 2026-02-01 - Work Schedule
**Observed:** User says they work "all the time" - no clear off-hours
**Pattern:** May indicate overwork or irregular schedule
**Suggestion:** Track actual work times to find natural breaks
**Status:** noted

---

### 2026-02-01 - Multi-Tool Research Sessions
**Observed:** User running Gemini session for Taiwan group literature completeness check while working in Claude Code. Session file at `/home/div/gemini-conversation-1769976946402.json` - untracked until now.
**Pattern:** Parallel research across multiple AI tools, no unified tracking
**Suggestion:** Track parallel sessions in `current-focus.md`, periodic sync
**Status:** implemented (added tracking table)

### 2026-02-01 - Cross-Tool Research Insight
**Observed:** Gemini session (2468 lines) identified "bridge dataset" - user has unique data combining Tonometry + PVR + Mortality that spans engineering and epidemiology paper domains. Potential novel research question.
**Pattern:** Deep research sessions in one tool produce insights that should propagate to project documentation
**Suggestion:** Capture key findings from parallel sessions into current-focus.md and project notes
**Status:** implemented (finding captured)

## Friction Log

| Date | Tool | Friction | Impact | Fix? |
|------|------|----------|--------|------|
| 2026-02-01 | Daily notes | Unused sections add guilt | Low adoption | ✅ Fixed (minimal template) |
| 2026-02-01 | Claude Code | Unstructured verification | Time sink | Pending workflow |
| 2026-02-01 | Multi-tool | Parallel sessions untracked | Lost context | ✅ Fixed (tracking table) |

## Automation Candidates

| Pattern | Frequency | Effort to Automate | Value |
|---------|-----------|-------------------|-------|
| Context handoff Desktop↔Code | Daily | Done (MCP bridge) | High |
| Daily note template fill | Daily | Medium | Medium |
| Literature gap checking | Weekly | High | High |

