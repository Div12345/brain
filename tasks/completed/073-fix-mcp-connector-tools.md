---
name: fix-mcp-connector-tools
priority: 10
estimated_tokens: 40000
mode: autonomous
timeout: 30m
backend: desktop
model_hint: sonnet
tags: [mcp, fix, urgent]
depends_on: []
ce_aware: true
---

# Fix MCP Connector Management Tools

## Goal
The `list_connectors`, `toggle_connector`, and `reload_mcp` tools in the Claude Desktop MCP server are broken. The DOM selectors don't match the current Desktop UI. Fix them.

## Context
- MCP server location: `C:\Users\din18\brain\tools\mcps\claude-desktop-mcp\server.py` (Windows path)
- Or via WSL: `\\wsl$\Ubuntu\home\div\brain\tools\mcps\claude-desktop-mcp\server.py`
- The tools use CDP to evaluate JavaScript in Desktop's renderer process

## Current Problem
The `list_connectors` function at line 416 tries to:
1. Click `button[aria-label="Toggle menu"]`
2. Find `[role="menuitem"]` with text "Connectors"
3. Extract connector list

But it returns empty - the selectors don't match current Desktop UI.

## What You Need To Do

### Step 1: Probe Desktop's DOM
Using your Developer Tools or by inspecting your own UI, find:
1. How to open the menu that contains "Connectors"
2. What selector opens the connectors panel/dropdown
3. What the connector items look like (enabled/disabled state)

### Step 2: Document the Correct Selectors
List the working CSS selectors for:
- Menu button to click
- Connectors menu item
- Individual connector toggles
- Enabled/disabled state indicators

### Step 3: Write the Fix
Provide the corrected JavaScript code for `list_connectors()` and `toggle_connector()` functions.

## Output Format
```
WORKING SELECTORS:
- Menu button: [selector]
- Connectors item: [selector]
- Connector toggle: [selector]
- Enabled state: [how to detect]

FIXED CODE:
[Updated list_connectors function]
[Updated toggle_connector function]

TASK COMPLETE
What was done: [bullets]
What was learned: [bullets]
What remains: [bullets]
```
