---
title: "Obsidian One-Note-Per-Entity Migration Pattern"
date: 2026-02-11
category: system-design
tags: [obsidian, dataview, migration, cooking, self-service]
severity: pattern
module: personal-systems
symptoms:
  - prose lists that can't be queried
  - hand-curated command centers that go stale
  - agent-dependent workflows for simple lookups
---

# Obsidian One-Note-Per-Entity Migration Pattern

## Problem
Prose inventory lists (75 items in one file) can't answer "what can I make?" without agent analysis. Hand-curated Command Centers go stale the moment reality changes.

## Root Cause
Storing queryable data as prose instead of structured frontmatter properties. Obsidian's Dataview can only query note-level properties, not inline text.

## Solution: 5-Layer Architecture

```
VIEW (Dataview queries in Command Center) — computed, never hand-written
  ↑
RULES (recipe.ingredients links to ingredient notes)
  ↑
REGISTRY (one note per entity with typed properties)
  ↑
CAPTURE (Templater templates, < 30 sec)
  ↑
FEEDBACK (toggle properties on use → views auto-update)
```

### Implementation Pattern

1. **Parse source data** into structured records (name, properties)
2. **Write Python script** to batch-create notes on filesystem (WAY faster than MCP one-by-one)
3. **Use Obsidian Properties panel** for user interaction (checkbox toggles, not markdown editing)
4. **Dataview queries** in Command Center compute views from properties
5. **Templates** pre-fill schema for new entries

### Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Data model | One note per entity | Properties UI, backlinks, Dataview native |
| File creation | Python script on filesystem | 82 files in 1 second vs 82 MCP calls |
| Property types | YAML frontmatter | Obsidian Properties panel renders checkboxes, dropdowns |
| View layer | Dataview queries | Auto-updates, no maintenance |
| Naming | kebab-case slugs | URL-safe, link-friendly |

### Gotchas

1. **Vault path on WSL**: The Obsidian vault is at `/mnt/c/Users/din18/OneDrive/Apps/remotely-save/OneVault/`, NOT at `/mnt/c/Users/din18/brain/` (that's the brain repo which also has .obsidian but is a different vault)
2. **Boolean properties**: Use `have: true` / `have: false` (not quoted strings) for Dataview boolean queries to work
3. **Link syntax in frontmatter**: Use `"[[slug]]"` (quoted) in YAML lists for Obsidian to recognize as links
4. **Dataview recipe matching**: `WHERE all(ingredients, (i) => default(i.have, false) = true)` — need `default()` because unresolved links return null
5. **Always-stock items not in inventory**: Create notes with `have: false` so the restock query catches them immediately

### Migration Script Location
`brain/tools/scripts/migrate-cooking.py` — reusable pattern for future domain migrations

## Applies To
- Any Obsidian domain with enumerable entities (ingredients, experiments, tasks)
- Any "what matches?" query (recipe→ingredients, task→energy, experiment→target)
- Any hand-curated list that could be computed from structured data

## References
- Plan: `docs/plans/2026-02-11-refactor-lean-self-service-personal-system-plan.md`
- Prior: `docs/solutions/2026-02-10-claude-desktop-delegation-patterns.md`
