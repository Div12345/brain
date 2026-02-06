---
title: Test Connector Tools Become Available
priority: 1
estimate: 5m
backend: desktop
skill: none
tags: [test, mcp]
---

# Test Connector Tools Become Available

## Objective
Verify that after enabling a connector, its tools actually become available in Desktop.

## YOUR MCP Tools (call directly)
- `claude_desktop_list_connectors()`
- `claude_desktop_toggle_connector(connector_name, enable)`
- `claude_desktop_reload_mcp()`
- `claude_desktop_new()`
- `claude_desktop_send(message, wait_for_response)`

## Test Protocol

### Step 1: Find a disabled connector with verifiable tools
Call `claude_desktop_list_connectors()` and pick one:
- `context7` → has `resolve-library-id`, `query-docs` tools
- `zotero` → has `zotero_search`, `zotero_get_item` tools
- `paper-search` → has `search_papers` tool

Report: `TARGET: [name] is currently disabled`

### Step 2: Enable the connector
```
claude_desktop_toggle_connector(connector_name="<target>", enable=true)
claude_desktop_reload_mcp()
claude_desktop_new()
```

### Step 3: Ask Desktop to use a tool from that connector
Send to Desktop:
- If context7: "Do you have the resolve-library-id or query-docs tool? Try calling it with any library name."
- If zotero: "Do you have zotero_search tool? Try searching for 'test'."
- If paper-search: "Do you have search_papers tool? Try searching for 'machine learning'."

Report: `TOOLS_AVAILABLE: [yes, Desktop used the tool | no, Desktop said tool not found]`

### Step 4: Disable the connector (cleanup)
```
claude_desktop_toggle_connector(connector_name="<target>", enable=false)
```

## Final Report
```
CONNECTOR_TESTED: [name]
TOGGLE_SUCCESS: [yes|no]
TOOLS_BECAME_AVAILABLE: [yes|no]
TEST_RESULT: [PASS if tools became available after toggle, FAIL otherwise]
```

TASK COMPLETE
What was done: [steps]
What was learned: [insights about whether toggle actually enables tools]
What remains: [any follow-up needed]
