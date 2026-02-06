---
name: test-obsidian-mcp-enabled
priority: 10
estimated_tokens: 15000
mode: autonomous
timeout: 10m
backend: desktop
model_hint: sonnet
tags: [test, obsidian, mcp]
depends_on: []
ce_aware: false
---

# Test: Verify Obsidian MCP is Working

## Goal
Quick test to verify that Obsidian MCP connector is now available and working in Desktop after being enabled.

## What To Do

1. Check if you have `obsidian_*` tools available (obsidian_list_notes, obsidian_read_note, etc.)
2. If yes: use `obsidian_list_notes` to list 5 notes from the vault
3. If no: report which tools you DO have available

## Expected Output
```
OBSIDIAN_MCP_STATUS: [available/unavailable]
TOOLS_FOUND: [list of obsidian tools if any]
SAMPLE_NOTES: [5 note names if available]

TASK COMPLETE
What was done: [bullets]
What was learned: [bullets]
What remains: [bullets]
```
