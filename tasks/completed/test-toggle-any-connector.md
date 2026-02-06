---
title: Test Toggle Any Connector
priority: 1
estimate: 5m
backend: desktop
skill: none
tags: [test, mcp, pipeline]
---

# Test Toggle Any Connector

## REMEMBER: These are YOUR MCP tools, not Desktop's

You (Gemini) call these directly:
- `claude_desktop_list_connectors()`
- `claude_desktop_toggle_connector(connector_name, enable)`
- `claude_desktop_reload_mcp()`

## Test Protocol

### Step 1: List all connectors
```
YOUR TOOL CALL: claude_desktop_list_connectors()
```
Report: `CONNECTORS: [list names and enabled states]`

### Step 2: Pick a test connector
- If ANY connector is DISABLED, pick one to enable (prefer: context7, filesystem, github)
- If ALL are enabled, pick one to disable temporarily

Report: `TARGET: [name] currently [enabled|disabled], will [enable|disable]`

### Step 3: Toggle the connector
```
YOUR TOOL CALL: claude_desktop_toggle_connector(connector_name="<target>", enable=<opposite of current>)
```
Report: `TOGGLE_1: [result]`

### Step 4: Verify toggle worked
```
YOUR TOOL CALL: claude_desktop_list_connectors()
```
Check if target connector's state changed.
Report: `VERIFY_1: [changed|unchanged] - [target] now [enabled|disabled]`

### Step 5: Toggle back to original state
```
YOUR TOOL CALL: claude_desktop_toggle_connector(connector_name="<target>", enable=<original state>)
```
Report: `TOGGLE_2: [result]`

### Step 6: Final verification
```
YOUR TOOL CALL: claude_desktop_list_connectors()
```
Report: `VERIFY_2: [target] back to [original state]`

## Final Report
```
TEST_RESULT: [PASS if toggle worked both directions, FAIL otherwise]
DETAILS: [summary of what happened]
```

TASK COMPLETE
What was done: [bullets]
What was learned: [bullets]
What remains: [bullets or None]
