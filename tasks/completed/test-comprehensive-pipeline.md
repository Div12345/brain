---
title: Comprehensive Pipeline Validation
priority: 1
estimate: 10m
backend: desktop
skill: none
tags: [test, validation, pipeline]
---

# Comprehensive Pipeline Validation

## CRITICAL REMINDERS

**YOUR tools** (Gemini MCP - call directly):
- `claude_desktop_new`, `claude_desktop_send`, `claude_desktop_read`
- `claude_desktop_list_connectors`, `claude_desktop_toggle_connector`, `claude_desktop_reload_mcp`

**DESKTOP's tools** (tell Desktop to use these via send):
- Desktop Commander: `execute_command`, `read_file`, `write_file`, `list_directory`
- Obsidian: `obsidian_list_notes`, `obsidian_read_note`
- Memory: `create_entities`, `search_nodes`

**NEVER** send your tool names to Desktop. Desktop doesn't have `claude_desktop_*` tools.

---

## Test Protocol - 5 Scenarios

### Scenario 1: Multi-Turn Context Retention

1. `claude_desktop_new()` - fresh start
2. `claude_desktop_send("My name is TestBot and my favorite number is 42. Remember this.")`
3. `claude_desktop_send("What is my name and favorite number?")` - verify Desktop remembers
4. Report: `S1_CONTEXT: [PASS if Desktop remembered, FAIL otherwise]`

### Scenario 2: Desktop Commander File Access

1. `claude_desktop_send("Use your Desktop Commander tool to list the contents of C:\\Users\\din18\\brain\\tasks\\completed - just show the first 5 files")`
2. Verify Desktop used `list_directory` or `execute_command`, NOT asked you to do it
3. Report: `S2_DC_ACCESS: [PASS if Desktop used its tools, FAIL if it asked you]`

### Scenario 3: MCP Connector Dynamic Enable

1. `claude_desktop_list_connectors()` - find a disabled connector (zotero or paper-search)
2. `claude_desktop_toggle_connector(connector_name="zotero", enable=true)`
3. `claude_desktop_reload_mcp()` then `claude_desktop_new()`
4. `claude_desktop_send("Do you have zotero tools available? List your zotero-related tools if any.")`
5. Report: `S3_DYNAMIC_MCP: [PASS if Desktop has zotero tools, FAIL otherwise]`
6. Cleanup: `claude_desktop_toggle_connector(connector_name="zotero", enable=false)`

### Scenario 4: Extended Analysis Task

1. `claude_desktop_send("Analyze the structure of C:\\Users\\din18\\brain directory using Desktop Commander. Tell me: 1) How many top-level folders exist, 2) Which folder has the most files, 3) Any .md files in the root. Be thorough but concise.")`
2. Wait for full response
3. Evaluate: Did Desktop provide all 3 requested pieces of information?
4. Report: `S4_ANALYSIS: [PASS if complete, PARTIAL if some missing, FAIL if inadequate]`

### Scenario 5: Error Recovery

1. `claude_desktop_send("Use your nonexistent_fake_tool to do something")` - intentionally trigger error
2. `claude_desktop_read()` - check how Desktop handles the error
3. Did Desktop gracefully explain the tool doesn't exist?
4. Report: `S5_ERROR_HANDLING: [PASS if graceful, FAIL if crashed/confused]`

---

## Final Summary

```
SCENARIO_1_CONTEXT: [PASS|FAIL]
SCENARIO_2_DC_ACCESS: [PASS|FAIL]
SCENARIO_3_DYNAMIC_MCP: [PASS|FAIL]
SCENARIO_4_ANALYSIS: [PASS|PARTIAL|FAIL]
SCENARIO_5_ERROR_HANDLING: [PASS|FAIL]
OVERALL: [X/5 passed]
```

TASK COMPLETE
What was done: [detailed steps for each scenario]
What was learned: [key insights about pipeline reliability]
What remains: [any issues that need fixing]
