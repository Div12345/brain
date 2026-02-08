---
status: idea
created: 2026-02-05
priority: medium
tags: [mcp, claude-desktop, development, tooling]
---

# MCP Plugin Restructure for Claude Desktop

## Problem
Developing an MCP server/plugin for Claude Desktop but not using a proper SDK or framework. The current implementation may not follow MCP protocol standards, making it fragile and hard to extend.

## Options to Evaluate

### Official MCP SDK
- `@modelcontextprotocol/sdk` (TypeScript)
- `mcp` Python package (official Python SDK)
- Pros: Protocol-compliant, maintained by Anthropic
- Cons: May be more boilerplate

### FastMCP
- Higher-level Python framework for building MCP servers
- Pros: Less boilerplate, decorator-based, fast iteration
- Cons: Third-party, may lag behind protocol changes

### Other
- Need to research what's current in 2026 for MCP development
- Check if there are newer frameworks or if the ecosystem has consolidated

## Tasks When Ready
1. Research current MCP SDK landscape (what's standard in Feb 2026)
2. Audit existing plugin code — what does it do, what's the interface
3. Choose framework and restructure
4. Add proper tool definitions, resource handling, notification support
5. Test with Claude Desktop DevTools (depends on DevTools access fix)

## Context
- The plugin needs to support the async notification use case (see desktop-compute-leverage idea)
- DevTools/Node debugger access is currently broken — blocks development iteration
- Plugin runs as MCP server that Claude Desktop connects to
