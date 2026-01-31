---
created: 2026-01-31
tags:
  - research
  - obsidian
  - mcp
  - tools
status: active
agent: overnight
---

# Obsidian MCP Server Options

Researched 2026-01-31 for brain vault integration.

## Top Options

### 1. @mauricio.wolff/mcp-obsidian (RECOMMENDED)
**GitHub:** [bitbonsai/mcp-obsidian](https://github.com/bitbonsai/mcp-obsidian)  
**Website:** [mcp-obsidian.org](https://mcp-obsidian.org)

**Pros:**
- No Obsidian plugin needed - direct file access
- Simple npx install: `npx @mauricio.wolff/mcp-obsidian@latest /path/to/vault`
- Works with Claude Desktop, CC, ChatGPT+, Cursor
- Safe frontmatter parsing (gray-matter)
- 11 methods: read, write, patch, search, tags, frontmatter

**Config:**
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["@mauricio.wolff/mcp-obsidian@latest", "/path/to/vault"]
    }
  }
}
```

### 2. jacksteamdev/obsidian-mcp-tools
**GitHub:** [jacksteamdev/obsidian-mcp-tools](https://github.com/jacksteamdev/obsidian-mcp-tools)

**Pros:**
- Obsidian plugin with semantic search
- Templater integration
- Most feature-rich

**Cons:**
- Requires Obsidian plugin installation
- More complex setup

### 3. iansinnott/obsidian-claude-code-mcp
**GitHub:** [iansinnott/obsidian-claude-code-mcp](https://github.com/iansinnott/obsidian-claude-code-mcp)

**Pros:**
- Specifically designed for Claude Code
- WebSocket + HTTP/SSE dual transport
- Auto-discovery by CC

**Cons:**
- Requires Obsidian plugin
- Newer, less tested

### 4. MarkusPfundstein/mcp-obsidian
**GitHub:** [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)

**Pros:**
- Python-based (uvx)
- Uses Obsidian REST API plugin

**Cons:**
- Requires Obsidian Local REST API plugin running
- Additional dependency

### 5. cyanheads/obsidian-mcp-server
**GitHub:** [cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server)

**Pros:**
- Most comprehensive features
- Built on mcp-ts-template
- HTTP transport option

**Cons:**
- Requires Obsidian Local REST API plugin
- More complex

## Recommendation

For brain vault: **@mauricio.wolff/mcp-obsidian**
- Simplest setup (no Obsidian plugin)
- Works with brain repo directly
- npx = no install needed
- Safe frontmatter handling

## Setup Task

Create [[tasks/pending/task-obs-001-mcp-setup]] for:
1. Get user's main Obsidian vault path ([[prompts/pending#Q-2026-01-31-02]])
2. Configure MCP in Claude Desktop
3. Test read/write operations
4. Integrate with [[agents/overnight]] for vault analysis

## Related
- [[inspirations/claude-code-ecosystem]] - CC tools
- [[context/capabilities]] - System capabilities
- [[prompts/pending]] - Vault path question
