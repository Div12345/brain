---
title: Test MCP Connector Tools v2
priority: 1
estimate: 5m
backend: desktop
skill: none
tags: [test, mcp, pipeline]
---

# Test MCP Connector Tools v2

## Objective
Verify that `list_connectors` and `toggle_connector` tools work correctly via Gemini→Desktop pipeline.

## Test Steps

1. Call `claude_desktop_list_connectors()` - report all connectors found
2. If obsidian is disabled, call `claude_desktop_toggle_connector(connector_name="obsidian", enable=true)`
3. Call `claude_desktop_reload_mcp()`
4. Call `claude_desktop_new()` to start fresh conversation
5. Ask Desktop: "Do you have obsidian_list_notes tool available? Just answer yes or no."
6. Report results

## Required Output Markers

```
CONNECTORS_LIST: [json list of connectors]
TOGGLE_RESULT: [success|skipped|error: reason]
OBSIDIAN_AVAILABLE: [yes|no]
TEST_RESULT: [PASS|FAIL]
```

## Success Criteria
- list_connectors returns valid JSON with connector names
- toggle_connector succeeds (or is skipped if already enabled)
- Fresh conversation has access to Obsidian tools
