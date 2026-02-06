---
name: desktop-mcp-core-fixes
priority: 8
estimated_tokens: 35000
mode: autonomous
timeout: 30m
skill: null
model_hint: sonnet
tags: [mcp, claude-desktop, refactor]
depends_on: [desktop-mcp-test-suite]
---

# Fix and Upgrade Claude Desktop MCP Core Tools

## Goal
Fix 3 existing MCP tools and add 3 new tools in `tools/mcps/claude-desktop-mcp/server.py`. This is the critical upgrade that makes Desktop reliable enough for autonomous use.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain/tools/mcps/claude-desktop-mcp
- **Python venv:** `~/brain/tools/mcps/claude-desktop-mcp/.venv/`
- **Desktop must be running** on port 9229

## Plan Reference
Full plan at `docs/plans/2026-02-05-feat-claude-desktop-compute-leverage-plan.md` — Phase 4.

## What This Task Must Produce

### Fix 1: HTML Escaping in `send_message()` (server.py:245-280)
**Problem:** Message text is injected raw into innerHTML via `'<p>' + escaped + '</p>'`. If message contains `<`, `>`, `&`, or quotes, it creates broken HTML or injection.
**Fix:** Add HTML entity escaping before innerHTML insertion. Either escape in Python before sending, or use `textContent` instead of `innerHTML` in the JS. Prefer `textContent` approach as it's simpler.

### Fix 2: Replace `wait_for_response()` (server.py:282-302)
**Problem:** Hash-based stability detection is fragile — fails on long responses where hash keeps changing, and can false-positive on pauses during thinking.
**Fix:** Replace with stop-button polling:
```
GENERATING = document.querySelector('button[aria-label="Stop response"]') !== null
DONE = stop button absent AND last message role is 'assistant'
```
Poll every 2s. When stop button disappears and last message is from assistant, response is complete. Return the last assistant message text.

### Fix 3: Migrate CSS Selectors to `data-testid`
**Problem:** CSS class selectors like `.flex-1.flex.flex-col.px-4.max-w-3xl` break on UI updates.
**Fix:** Replace with `data-testid` selectors where available:
- Message container: use `[data-testid="user-message"]` for role detection (already partially done)
- Model: `[data-testid="model-selector-dropdown"]`
- Keep ProseMirror and aria-label selectors where no testid exists (these are also stable)

### Fix 4: Enhance `claude_desktop_info`
Add to the info response:
- `model`: current model name from `[data-testid="model-selector-dropdown"]` text
- `message_count`: number of messages in conversation
- `is_generating`: boolean from stop-button check

### New Tool 1: `claude_desktop_status`
Lightweight status check (no side effects):
- `is_generating`: boolean (stop button present?)
- `model`: current model name
- `message_count`: number of messages
- `send_button_state`: present/disabled/enabled
- `url`: current page URL

### New Tool 2: `claude_desktop_stop`
Click the stop button to halt generation:
- Check if stop button exists
- Click it
- Return success/failure (fail if not generating)

### New Tool 3: `claude_desktop_read_interim`
Read partial response while still generating:
- Get the last assistant message text even if generation is ongoing
- Return `{text, is_complete: false, char_count}` if still generating
- Return `{text, is_complete: true, char_count}` if done

## Success Criteria
- [ ] `send_message("test <b>bold</b> & stuff")` sends literal text, not HTML
- [ ] `wait_for_response()` uses stop-button detection, not hash-based
- [ ] `claude_desktop_info` returns model name and generating state
- [ ] `claude_desktop_status` tool registered and returns correct state
- [ ] `claude_desktop_stop` tool registered and can halt generation
- [ ] `claude_desktop_read_interim` tool registered and returns partial text
- [ ] All existing tests in `tests/` still pass
- [ ] Run `cd ~/brain/tools/mcps/claude-desktop-mcp && .venv/bin/python -m pytest tests/ -v` green

## Overnight Agent Instructions
1. Read the plan at `docs/plans/2026-02-05-feat-claude-desktop-compute-leverage-plan.md`
2. Read current `server.py` (536 lines) fully
3. Read `tests/` directory to understand existing test expectations
4. Fix `send_message()` — use textContent instead of innerHTML
5. Replace `wait_for_response()` with stop-button polling implementation
6. Audit all querySelector calls and migrate to data-testid where possible
7. Enhance `claude_desktop_info` handler to include model/count/generating
8. Add `claude_desktop_status` tool (list_tools + call_tool handler)
9. Add `claude_desktop_stop` tool
10. Add `claude_desktop_read_interim` tool
11. Run tests: `.venv/bin/python -m pytest tests/ -v`
12. If tests fail, fix until green
