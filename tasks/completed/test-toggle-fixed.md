---
title: Test Toggle Fixed
priority: 1
estimate: 3m
backend: desktop
skill: none
tags: [test, mcp]
---

# Test Toggle Fixed

## YOUR MCP Tools (call directly)
- `claude_desktop_list_connectors()`
- `claude_desktop_toggle_connector(connector_name, enable)`

## Steps

1. Call `claude_desktop_list_connectors()` - report count and list
2. Pick `context7` (should be disabled) or any disabled connector
3. Call `claude_desktop_toggle_connector(connector_name="context7", enable=true)`
4. Call `claude_desktop_list_connectors()` - verify context7 is now enabled
5. Call `claude_desktop_toggle_connector(connector_name="context7", enable=false)` - toggle back
6. Call `claude_desktop_list_connectors()` - verify context7 is disabled again

## Report
```
LIST_1: [count] connectors found
TOGGLE_ON: [success|error]
VERIFY_ON: context7 enabled=[true|false]
TOGGLE_OFF: [success|error]
VERIFY_OFF: context7 enabled=[true|false]
TEST: [PASS if both toggles worked, FAIL otherwise]
```

TASK COMPLETE
What was done: [list steps completed]
What was learned: [any insights]
What remains: None
