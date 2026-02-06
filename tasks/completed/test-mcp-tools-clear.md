---
title: Test MCP Tools - Clear Instructions
priority: 1
estimate: 5m
backend: desktop
skill: none
tags: [test, mcp, pipeline]
---

# Test MCP Tools - Clear Instructions

## IMPORTANT: Who Does What

**YOU (Gemini)** have these MCP tools - call them directly as tool calls:
- `claude_desktop_list_connectors` - YOUR tool to query Desktop's connector state
- `claude_desktop_toggle_connector` - YOUR tool to toggle Desktop connectors
- `claude_desktop_reload_mcp` - YOUR tool to reload Desktop's MCP config
- `claude_desktop_new` - YOUR tool to create new Desktop conversation
- `claude_desktop_send` - YOUR tool to send messages to Desktop

**Claude Desktop** does NOT have these tools. Do NOT ask Desktop to call them.

## Test Protocol

### Step 1: YOU call your MCP tool
```
YOUR TOOL CALL: claude_desktop_list_connectors()
```
Report result as: `STEP1_RESULT: [json or error]`

### Step 2: If obsidian disabled, YOU toggle it
```
YOUR TOOL CALL: claude_desktop_toggle_connector(connector_name="obsidian", enable=true)
```
Report result as: `STEP2_RESULT: [success|skipped|error]`

### Step 3: YOU reload MCP
```
YOUR TOOL CALL: claude_desktop_reload_mcp()
```
Report result as: `STEP3_RESULT: [success|error]`

### Step 4: YOU create new conversation
```
YOUR TOOL CALL: claude_desktop_new()
```

### Step 5: YOU send message to Desktop
```
YOUR TOOL CALL: claude_desktop_send(message="List 3 notes from my Obsidian vault using your obsidian_list_notes tool.", wait_for_response=true)
```
Report Desktop's response as: `STEP5_RESULT: [response summary]`

## Final Report
```
OVERALL_TEST: [PASS if steps 1-3 succeeded and step 5 got notes, else FAIL]
```
