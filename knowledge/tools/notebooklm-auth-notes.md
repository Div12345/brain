# NotebookLM Auth Notes

## Port Conflict Issue (2026-02-03)

**Problem:** When Claude Desktop is running with `--remote-debugging-port=9222`, the NotebookLM auth tool (`notebooklm-mcp-auth`) fails because it also tries to use port 9222 for Chrome debugging.

**Error:**
```
Connected to Chrome debugger
Failed to create page: status=500
ERROR: Failed to find or create NotebookLM page
```

**Root Cause:** Both tools expect exclusive access to port 9222.

## Potential Solutions

1. **Run auth before launching Claude Desktop in debug mode**
   - Auth first, then launch Claude Desktop with debug flags
   - Drawback: Auth expires every 10-30 min

2. **Use different ports**
   - Configure one tool to use 9223 instead
   - Needs changes to MCP configs

3. **Run NotebookLM MCP from Windows Claude Desktop**
   - Per brain-zpd resolution, Windows has headless Chrome
   - Claude Desktop on Windows could handle NotebookLM tasks

4. **Schedule auth refresh**
   - Have a script that refreshes auth when Claude Desktop isn't in debug mode

## Current Workaround

For now, don't run Claude Desktop in debug mode when needing NotebookLM access, or vice versa.

## Related Beads
- brain-zpd (closed): WSL Cookie Bridge solution
- brain-qms: NotebookLM Library Pipeline (blocked by this)
