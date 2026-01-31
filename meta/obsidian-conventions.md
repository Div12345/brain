---
created: 2026-01-31
tags:
  - meta
  - conventions
aliases:
  - vault conventions
  - formatting rules
---

# Obsidian Conventions

This vault follows these conventions for consistency and graph navigation.

## Frontmatter (Required)

```yaml
---
created: YYYY-MM-DD
tags:
  - primary-category
  - secondary-tag
aliases:
  - alternate name
status: draft | active | complete | archived
agent: desktop | claude-code | overnight | user
---
```

## Tags Taxonomy

### Content Types
- `#research` - External findings
- `#knowledge` - Synthesized understanding  
- `#pattern` - Observed behavior patterns
- `#task` - Work items
- `#experiment` - Hypothesis testing
- `#log` - Session records
- `#agent` - Agent definitions
- `#tool` - Tool specs/configs

### Domains
- `#memory` - Memory systems
- `#orchestration` - Multi-agent coordination
- `#prediction` - Anticipatory patterns
- `#claude-code` - CC-specific
- `#obsidian` - Vault/PKM

### Status
- `#status/draft`
- `#status/active`
- `#status/complete`
- `#status/blocked`

## Backlinks

Use `[[note-name]]` liberally:
- Reference related concepts
- Link to source material
- Connect tasks to knowledge
- Thread agent handoffs

## Folder Structure

| Folder | Purpose | Primary Tags |
|--------|---------|-------------|
| `agents/` | Agent definitions | #agent |
| `context/` | Shared state | #context |
| `experiments/` | Hypotheses | #experiment |
| `inspirations/` | External research | #research |
| `knowledge/` | Synthesized insights | #knowledge |
| `logs/` | Session records | #log |
| `prompts/` | User Q&A | #prompt |
| `tasks/` | Work queue | #task |
| `tools/` | Configs & scripts | #tool |

## Naming

- Lowercase with hyphens: `ai-memory-systems.md`
- Tasks: `task-XXX-brief-name.md`
- Logs: `YYYY-MM-DD-session-type.md`
- Questions: `Q-YYYY-MM-DD-NN.md`

## Graph Tips

- Filter by tag to see clusters
- Color by folder for quick orientation
- Orphan notes = needs linking
- High-connection notes = core concepts
