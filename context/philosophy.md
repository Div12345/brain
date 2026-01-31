# User Philosophy & Patterns

> Extracted from vault meta-documentation. The agent should embody these principles.

## Core Philosophy

**Source: `99 - Meta/Task Management System - Overview.md`**

| Principle | What It Means | Agent Implication |
|-----------|---------------|-------------------|
| **Minimal viable structure** | Start simple, add complexity only when pain points emerge | Don't over-engineer outputs |
| **Match your brain** | Use patterns already present, don't force new habits | Learn existing tags, formats, rhythms |
| **Low friction** | If it feels like work, the system has failed | Outputs should slot into existing flow |
| **Iterate based on use** | Version 1.0 mindset. Adjust based on what helps | Propose small changes, not redesigns |

## Behavioral Patterns

### How You Think About Tasks

| Pattern | Description |
|---------|-------------|
| **Energy states** | Reflective mood ≠ productive action-taking mindset |
| **Time windows** | Frame work as "shouldn't take more than a few hours" |
| **Urgency vs eventually** | Some have hard deadlines, others float |
| **Context switching cost** | Research vs admin vs personal need different headspaces |
| **Blocking factors** | Weather, waiting on others, need to call someone |

### Task Capture Patterns

You naturally write tasks in multiple formats:
- Narrative text: "I want to make amazon returns before I buy anything more"
- Bracket notation: `[!credit card closing]` or `[yoga]`
- Highlighted urgency: `==tracker==` with `!!!!!!!!!`
- Numbered lists with sub-tasks
- Mixed with reflective writing and planning

### What Falls Through Cracks

"Tasks scattered across daily notes with no persistence - things like 'Amazon returns' mentioned for months without completion."

## Existing Systems That Work

| System | Status | Notes |
|--------|--------|-------|
| Daily note template | Working | Has structure but often unfilled sections |
| Priority markers `!` `!!` `!!!` | Working | Natural, fast to type |
| Dataview dashboard | Partial | Installed but may not be checked daily |
| Zotero integration | Working | Paper search and reference |
| `[[wikilinks]]` | Working | Cross-references actively used |

## What Doesn't Work / Known Gaps

| Gap | Why It Matters |
|-----|----------------|
| No due dates | Urgency-based, not deadline-based thinking |
| Flat lists overwhelming | Hard to pick what to work on |
| No context categorization | Admin, research, personal all mixed |
| No energy/time metadata | Can't filter by "quick wins" vs "deep work" |
| Wellbeing metrics unfilled | Template has them but rarely used |

## Vault Structure Preferences

**From CLAUDE.md in vault:**
- Two-level hierarchy max
- YAML frontmatter with tags
- Tag system: `#type/`, `#context/`, `#theme/`, `#status/`
- Links auto-update when files move
- New files default to `01 - Personal/Fleeting`

## Anti-Patterns to Avoid

Based on documented preferences, the agent should NEVER:

| Don't | Why |
|-------|-----|
| Suggest emoji-based systems | "Explicitly rejected emojis" |
| Propose complex date syntax | "Adds cognitive load" |
| Create overwhelming dashboards | "Low friction" principle |
| Add many new habits/routines | "Avoid draining spirals of setup" |
| Ignore existing working systems | "Match your brain" |

## Success Metrics

A good recommendation should:
1. Use existing patterns (exclamation marks, wikilinks, current folders)
2. Require zero new habits to maintain
3. Be testable in one day
4. Fail gracefully if ignored

---
*Last updated: 2026-01-31 (extracted from vault meta-documentation)*
