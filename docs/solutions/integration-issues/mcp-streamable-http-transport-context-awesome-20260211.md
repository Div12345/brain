---
module: System
date: 2026-02-11
problem_type: integration_issue
component: tooling
symptoms:
  - "MCP server returns 406 Not Acceptable via HTTP transport"
  - "MCP server fails to connect via SSE transport"
  - "npx package does not exist on npm (E404)"
root_cause: config_error
resolution_type: environment_setup
severity: medium
tags: [mcp, streamable-http, stdio, context-awesome, vercel, transport-protocol]
---

# Troubleshooting: MCP Server Using Streamable HTTP Transport Fails in Claude Code

## Problem
Remote MCP servers deployed on Vercel/Next.js using the newer "Streamable HTTP" transport protocol return 406 Not Acceptable when Claude Code tries to connect via HTTP or SSE transport modes. The package may also not be published to npm, blocking the npx approach.

## Environment
- Module: System (MCP infrastructure)
- Platform: Claude Code on WSL2 / Linux
- Affected Component: MCP server connectivity
- Date: 2026-02-11

## Symptoms
- `claude mcp add --transport http` → 406 Not Acceptable from server
- `claude mcp add --transport sse` → Failed to connect
- `npx -y context-awesome-mcp` → npm E404, package not found
- Server's `/api/mcp` endpoint works fine via direct `curl` POST with JSON body

## What Didn't Work

**Attempted Solution 1:** HTTP transport via Claude Code
- **Why it failed:** Server uses Streamable HTTP protocol (newer MCP transport). Claude Code's HTTP client sends different headers/negotiation than what the server expects. Vercel deployment returns 406.

**Attempted Solution 2:** SSE transport
- **Why it failed:** The server's SSE endpoint exists in source code but the Vercel deployment only exposes `/api/mcp`, not `/sse`.

**Attempted Solution 3:** npx from npm
- **Why it failed:** Package `context-awesome-mcp` was never published to npm registry.

## Solution

Clone the repo locally, build from source, run via stdio transport:

```bash
# Clone
git clone https://github.com/bh-rat/context-awesome.git ~/.local/share/context-awesome/

# Build
cd ~/.local/share/context-awesome && npm install && npm run build

# Add to Claude Code as local stdio MCP
claude mcp add context-awesome -- node ~/.local/share/context-awesome/build/index.js
```

The MCP server is a thin client that calls the backend API at `api.context-awesome.com` — the backend works fine, it's only the hosted MCP endpoint that has the transport mismatch.

## Why This Works

1. **Root cause:** Vercel/Next.js deployments using the MCP SDK's Streamable HTTP transport speak a newer protocol that Claude Code's HTTP/SSE client can't negotiate. The server returns 406 because it can't agree on a content type.
2. **stdio bypasses the problem:** Running locally via stdio means no HTTP negotiation at all — Claude Code spawns the process directly and communicates via stdin/stdout.
3. **The server source is just a thin API client:** The actual intelligence lives on the remote backend (`api.context-awesome.com`). The MCP server just wraps it with tool definitions. So running locally loses nothing.

## Prevention

- When an MCP server's hosted endpoint fails with 406 or transport errors, check if it's using Streamable HTTP (common on Vercel/Next.js deployments)
- Always check if the repo can be cloned and run locally via stdio as a fallback
- Verify the npm package actually exists before trying npx (`npm search <name>`)
- stdio transport is the most reliable — prefer it for any MCP server that can run locally

## Related Issues

No related issues documented yet.
