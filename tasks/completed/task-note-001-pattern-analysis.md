---
created: 2026-02-01
tags:
  - task
  - analysis
  - obsidian
  - status/pending
priority: high
requires:
  - obsidian-mcp
preferred_interface: claude-code
timeout: 60m
---

# Task: Analyze Daily Note & Log Patterns

Analyze user's Obsidian notes to discover actual usage patterns and propose data-driven template optimization.

## Objective

1. Understand what sections/fields are actually used vs ignored
2. Find the "Tomorrow's Intent" → next day disconnect
3. Analyze arterial_analysis daily logs for patterns
4. Propose optimized templates based on real behavior

## Scope

- Daily notes (recent 30-60 days)
- arterial_analysis project logs
- Any recurring note patterns

## Analysis Questions

- [ ] Which template sections have >50% fill rate?
- [ ] What do users actually write in daily notes?
- [ ] How do arterial_analysis logs differ from daily notes?
- [ ] What temporal patterns exist (morning vs evening entries)?
- [ ] Are there implicit sections that should be explicit?

## Deliverables

1. `knowledge/analysis/daily-note-patterns.md` - Pattern findings
2. `knowledge/proposals/optimized-daily-template.md` - New template proposal
3. `knowledge/proposals/arterial-log-template.md` - Project log proposal (if needed)

## Acceptance Criteria

- [ ] Analyzed 30+ daily notes
- [ ] Analyzed arterial_analysis logs
- [ ] Documented fill rates by section
- [ ] Proposed specific template changes with rationale
- [ ] User can review and approve/modify

## Related

- [[prompts/answered#A-2026-02-01-01]]
- [[knowledge/research/pkm-mcp-servers]]
