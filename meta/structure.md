# System Structure

> Self-documentation. Agents update this when they create new directories/patterns.

## Directory Tree

```
brain/
├── CLAUDE.md              # Agent bootstrap (read first always)
├── context/               # Current state (agents read + write)
│   └── priorities.md      # What to focus on now
├── knowledge/             # Discovered insights (append-only)
│   └── README.md          # Structure guide
├── logs/                  # Agent activity logs (append-only)
│   └── README.md          # Format guide
├── agents/                # Agent-specific instructions
│   └── overnight.md       # Overnight runner
├── meta/                  # Self-documentation
│   ├── structure.md       # This file
│   └── improvements.md    # System improvement ideas
└── archive/               # Superseded content
```

## Design Principles

| Principle | Reason |
|-----------|--------|
| **Flat over deep** | Max 2 levels - easier for agents to navigate |
| **Markdown only** | Human + AI readable, git-friendly |
| **Frontmatter required** | Structured metadata for querying |
| **Append over edit** | Preserves history, avoids conflicts |
| **Links are first-class** | `[[wikilinks]]` enable knowledge graph |

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Knowledge | `topic-YYYY-MM-DD.md` | `vault-analysis-2026-01-31.md` |
| Log | `YYYY-MM-DD-HHMM-agent.md` | `2026-01-31-0230-overnight.md` |
| Context | `topic.md` | `priorities.md` |

## Evolution Protocol

When creating new structure:
1. Create the new file/folder
2. Update this document
3. Update CLAUDE.md if it affects agent workflow
4. Log the change in `meta/improvements.md`
