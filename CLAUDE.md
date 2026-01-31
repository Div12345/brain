# CLAUDE.md - Agent Bootstrap

> This file is read FIRST by any AI agent. It bootstraps context and defines behavior.

## What This Repo Is

A **self-recursive knowledge base** - every agent run improves the next run.

## Core Principles

1. **Every action leaves artifacts** - Write discoveries to `knowledge/`
2. **Read before write** - Check `logs/` and `context/` before acting
3. **Update context for next agent** - Your successor reads what you write
4. **Structure emerges from use** - Create files/folders as needed, document in `meta/`
5. **No deletions without archiving** - Move to `archive/` instead

## Directory Purpose

| Directory | Read/Write | Purpose |
|-----------|------------|----------|
| `context/` | RW | Current state - priorities, projects, patterns |
| `knowledge/` | RW | Discovered insights, synthesized understanding |
| `logs/` | Append | What you did and why |
| `agents/` | R | Instructions for specific agent types |
| `meta/` | RW | Self-documentation of this system |
| `archive/` | W | Superseded content (never delete, archive) |

## Agent Workflow

```
1. Read CLAUDE.md (this file)
2. Read context/priorities.md
3. Read logs/ (last 3 entries)
4. Do your task
5. Write to knowledge/ (discoveries)
6. Update context/ (state changes)
7. Append to logs/ (what you did)
```

## Linked Resources

- **Obsidian Vault**: Available via Obsidian MCP
- **Zotero**: Available via Zotero MCP
- **This Repo**: For agent-accessible, version-controlled knowledge

## Current Focus

See `context/priorities.md`
