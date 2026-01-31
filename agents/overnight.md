# Overnight Agent Instructions

## Purpose

Run unattended overnight. Analyze vault, extract patterns, update knowledge base.

## Constraints

- **READ ONLY** on Obsidian vault (no edits to existing files)
- **WRITE** to this GitHub repo (knowledge/, logs/, context/)
- **NO** external API calls, emails, or irreversible actions
- **SELF-CONTINUING** - if context fills, summarize progress and continue

## Task Sequence

### Phase 1: Context Loading (5 min)
1. Read `CLAUDE.md` (done if you're reading this)
2. Read `context/priorities.md` for current focus
3. Read `logs/` last 3 entries for continuity

### Phase 2: Vault Analysis (30 min)
1. Use Obsidian MCP to read last 30 daily notes from `01 - Personal/Daily/`
2. Extract:
   - Recurring themes (what topics keep appearing?)
   - Incomplete tasks (what's started but not finished?)
   - Mood/energy patterns (if mentioned)
   - Friction points (what's complained about?)
3. Scan `03 - Projects/` - what's active vs stalled?
4. Check for orphan links (referenced but don't exist)

### Phase 3: Knowledge Synthesis (15 min)
1. Create `knowledge/vault-analysis-YYYY-MM-DD.md`
2. Structure findings with frontmatter
3. Identify top 3 actionable insights
4. Note confidence level for each finding

### Phase 4: Context Update (5 min)
1. Update `context/priorities.md` - new focus areas
2. Update `context/projects.md` - discovered status
3. Update `context/patterns.md` - behavioral observations

### Phase 5: Self-Improvement (5 min)
Before finishing, ask:
- What would make the next agent's job easier?
- What structure should exist that doesn't?
- What did I learn about analyzing this vault?

Write answers to `meta/improvements.md`

### Phase 6: Logging (2 min)
1. Create `logs/YYYY-MM-DD-HHMM-overnight.md`
2. Document: what done, what found, what next agent needs
3. Commit all changes to GitHub

## Output Format

All knowledge files use this template:

```markdown
---
created: YYYY-MM-DD
agent: overnight
sources: [list of files read]
confidence: high|medium|low
---

# Title

## Summary
(3 sentences max)

## Key Findings
| Finding | Evidence | Confidence |
|---------|----------|------------|
| ... | ... | ... |

## Patterns Discovered
(Structured, linkable)

## Open Questions
(For next agent to investigate)

## Recommendations
(Actionable next steps)
```

## Self-Recursion Hook

The system improves itself. Always ask:
1. What knowledge structure would help future agents?
2. What context was missing that I had to discover?
3. How can the CLAUDE.md be improved?

If you create new structures, document in `meta/structure.md`.
