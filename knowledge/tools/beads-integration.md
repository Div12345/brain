---
created: 2026-01-31
tags:
  - knowledge
  - tools
  - beads
  - memory
  - task-tracking
updated: 2026-01-31T10:35
agent: claude-code-web
---

# Beads (bd) Integration

> Git-backed issue tracker for AI coding agents by Steve Yegge.

## Why Beads?

Solves the "50 First Dates" problem - agents wake up with no memory of yesterday's work. Beads gives agents:
- Addressable work items with IDs
- Dependency tracking
- Priority management
- Git-backed persistence (survives compaction)

## Installation

```bash
# Quick install
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash

# Or via npm
npm install -g @beads/bd

# Or via Homebrew
brew install beads
```

## Setup for Brain Repo

```bash
cd /path/to/brain
bd init
```

This creates `.beads/` directory with:
- `beads.jsonl` - Task data
- `config.json` - Settings

## Essential Commands

| Command | Purpose |
|---------|---------|
| `bd ready` | Show tasks ready to work (no blockers) |
| `bd create "Title" -p 0` | Create priority-0 (highest) task |
| `bd show <id>` | View task details |
| `bd update <id> -s done` | Mark task complete |
| `bd dep add <child> <parent>` | Add dependency |
| `bd archive` | Clean up done tasks |

## Agent Integration

Add to [[CLAUDE.md]] or create `AGENTS.md`:

```markdown
## Task Management

Use `bd` (Beads) for task tracking:
- `bd ready` to see what to work on
- `bd create "task" -p N` to add tasks
- `bd update <id> -s done` when complete

Before starting: `bd ready`
After completing work: `bd update <id> -s done`
```

## Benefits for Brain System

| Current Approach | With Beads |
|-----------------|------------|
| Files in tasks/ | Structured JSON with IDs |
| Manual priority | Numeric priority + dependencies |
| No dependencies | Explicit dependency graph |
| Context loss on compaction | Git-backed, survives compaction |

## Integration with Messages

Beads can complement our messaging system:
- Use Beads for **task tracking**
- Use messages/ for **agent-to-agent communication**
- Use context/ for **shared state**

## MCP Server Available

For Claude Desktop without CLI access:
```
https://playbooks.com/mcp/steveyegge-beads
```

## Related

- [[inspirations/multi-agent-tools]] - Orchestration tools
- [[tasks/README]] - Current task queue (to migrate)
- [[context/session-state]] - Session recovery

## Sources

- [GitHub: steveyegge/beads](https://github.com/steveyegge/beads)
- [Medium: Introducing Beads](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a)
- [Beads MCP Server](https://playbooks.com/mcp/steveyegge-beads)
