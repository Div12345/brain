---
created: 2026-01-31
tags:
  - research
  - mcp
  - pkm
  - tools
status: active
agent: overnight
---

# PKM MCP Servers

MCP servers for personal knowledge management integration.

## Obsidian (Recommended for Brain)
See [[knowledge/research/obsidian-mcp-options]] for detailed comparison.

**Top pick:** `@mauricio.wolff/mcp-obsidian`

## Other PKM MCPs

### Logseq MCP
- **Repo:** apw124/logseq-mcp
- **Features:** Create pages, search, block operations
- **Pattern:** Local-first, outliner-focused

### Bear Notes MCP
- **Repo:** Junpei Kawamoto's implementation
- **Features:** Semantic search via embeddings, read/write
- **Pattern:** RAG-powered, macOS-only

### Apple Notes MCP  
- **Repo:** sirmews/apple-notes-mcp
- **Features:** Read/write, LanceDB embeddings
- **macOS only** via JXA

### SiYuan MCP
- **Repo:** onigeya/siyuan-mcp-server
- **Features:** Block-based, SQL queries
- **Self-hosted**, privacy-first

### TriliumNext MCP
- **Repo:** TypeScript prototype
- **Features:** Hierarchical notes, graph links
- **Status:** Prototype

## Common Patterns

1. **Semantic Search** - Vector embeddings for "find notes about X"
2. **Block Operations** - Create, update, link content
3. **Local-First** - Data stays on machine
4. **RAG Integration** - Notes as context for LLM

## For Brain System

Since brain uses GitHub + Obsidian:
1. Primary: Obsidian MCP for vault operations
2. Secondary: GitHub MCP (already have) for coordination
3. Future: Custom MCP for brain-specific operations

## Workflow Ideas

```
User: "What do I know about multi-agent coordination?"
→ Obsidian MCP: semantic search brain vault
→ Return: [[knowledge/research/multi-agent-coordination]] + related notes
→ Claude: synthesize into answer with citations
```

## Related
- [[knowledge/research/obsidian-mcp-options]]
- [[knowledge/research/ai-memory-systems]]
