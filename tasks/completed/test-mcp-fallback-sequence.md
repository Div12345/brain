---
title: Test MCP Fallback Sequence
priority: 1
estimate: 10m
backend: desktop
skill: none
tags: [test, mcp, pipeline]
---

# Test MCP Fallback Sequence

## Objective
Verify that Gemini correctly executes the MCP fallback sequence when Desktop reports tools unavailable.

## Test Protocol

1. **Create new Desktop conversation**
2. **Ask Desktop to list Obsidian notes** using obsidian_list_notes tool
3. **When Desktop says tools unavailable**, YOU MUST execute this sequence:
   - Call `claude_desktop_list_connectors()` - report what connectors exist
   - Call `claude_desktop_toggle_connector(connector_name="obsidian", enable=true)`
   - Call `claude_desktop_reload_mcp()`
   - Call `claude_desktop_new()` to start fresh conversation
   - Retry asking Desktop to list Obsidian notes
4. **Report results** with these markers:

```
MCP_FALLBACK_TEST: [PASS|FAIL]
SEQUENCE_EXECUTED: [list of tools called in order]
CONNECTORS_FOUND: [list from list_connectors]
TOGGLE_RESULT: [success|failure]
RELOAD_RESULT: [success|failure]
RETRY_RESULT: [tools available|still unavailable]
```

## Success Criteria
- All 5 fallback steps executed in order
- Final retry shows whether Obsidian tools became available

## CRITICAL
DO NOT just report "unavailable" without executing the full sequence first. The purpose of this test is to verify YOU execute the fallback tools, not just report what Desktop says.
