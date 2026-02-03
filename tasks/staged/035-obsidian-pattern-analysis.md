---
name: obsidian-note-pattern-analysis
bead_id: brain-4aq
priority: 2
estimated_tokens: 15000
mode: autonomous
timeout: 60m
skill: analyze
model_hint: sonnet
tags: [analysis, obsidian]
depends_on: []
---

# Obsidian Note Pattern Analysis

## Goal
Analyze daily note usage patterns to propose data-driven template optimization.

## Environment Constraints
- **Execution env:** WSL2 Claude Code
- **MCP tools needed:** obsidian-mcp
- **Working dir:** ~/brain
- **Vault location:** User's Obsidian vault (01 - Personal/Daily)

## Analysis Scope
- Daily notes (last 30-60 days)
- arterial_analysis project logs
- Recurring note patterns

## Questions to Answer

| Question | Method |
|----------|--------|
| Which template sections have >50% fill rate? | Parse all daily notes, count non-empty sections |
| What do users actually write? | Categorize content types |
| How do arterial logs differ from daily notes? | Compare structure/content |
| Are there temporal patterns? | Check morning vs evening entries |
| Implicit sections that should be explicit? | Find recurring ad-hoc patterns |

## Deliverables
- `knowledge/analysis/daily-note-patterns.md` - Pattern findings with data
- `knowledge/proposals/optimized-daily-template.md` - New template proposal

## Success Criteria
- [ ] Analyzed 30+ daily notes
- [ ] Documented fill rates by section
- [ ] Identified unused sections to remove
- [ ] Proposed specific template changes with rationale
