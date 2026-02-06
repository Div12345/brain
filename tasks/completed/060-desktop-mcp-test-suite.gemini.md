---
name: desktop-mcp-test-suite
priority: 8
estimated_tokens: 25000
mode: autonomous
timeout: 25m
skill: null
model_hint: sonnet
tags: [mcp, testing, tdd, claude-desktop]
depends_on: []
---

# Create Test Suite for Claude Desktop MCP

## Goal
Build a pytest test suite for `tools/mcps/claude-desktop-mcp/` that validates DOM selectors and MCP tool behavior against the live Claude Desktop instance. This is TDD foundation — tests must exist BEFORE the MCP refactor in task 061.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain/tools/mcps/claude-desktop-mcp
- **Desktop must be running** with Main Process Debugger enabled on port 9229
- **Python venv:** `~/brain/tools/mcps/claude-desktop-mcp/.venv/`

## Context
DOM probing scripts at `/tmp/probe-desktop.py`, `/tmp/probe-generating.py`, `/tmp/probe-cdp-file.py`, `/tmp/probe-fileupload.py` contain working CDP connection code and discovered DOM structure. Use these as reference for what selectors exist and how to connect.

Key findings from probing:
- 18 stable `data-testid` attributes in Desktop DOM
- Stop button `button[aria-label="Stop response"]` appears during generation, disappears when done
- Send button `button[aria-label="Send message"]` present when idle
- ProseMirror editor at `.ProseMirror` for text input
- Model shown in `[data-testid="model-selector-dropdown"]`
- File input at `#chat-input-file-upload-bottom`

## What This Task Must Produce

### `tests/conftest.py`
Shared pytest fixtures:
- `ws_connection` — connects to Desktop via port 9229, yields websocket, closes on teardown
- `eval_renderer(ws, js_expr)` — evaluates JS in renderer via main process proxy (copy pattern from probe scripts)
- Skip markers for when Desktop is unavailable

### `tests/test_selectors.py`
Assert that all DOM selectors the MCP depends on exist:
- `data-testid="model-selector-dropdown"` exists
- `data-testid="user-message"` exists (in conversations with messages)
- `button[aria-label="Send message"]` exists when idle
- `.ProseMirror` editor exists
- `#chat-input-file-upload-bottom` file input exists
- Sidebar conversation links `a[href*="/chat/"]` exist

### `tests/test_status.py`
Test generation state detection:
- When idle: no stop button, send button present
- (Optional/manual) When generating: stop button appears — this requires sending a message first, so mark as integration test

### `tests/test_send_read.py`
Integration test for the core send→read cycle:
- Send a simple message ("What is 2+2?")
- Wait for response (using stop-button polling, NOT hash-based)
- Read messages and verify response contains "4"
- Verify message count increased

### `pyproject.toml` or `pytest.ini`
Test configuration with markers for:
- `@pytest.mark.integration` — requires live Desktop
- `@pytest.mark.slow` — tests that wait for generation

## Success Criteria
- [ ] `pytest tests/test_selectors.py` passes against live Desktop
- [ ] `pytest tests/test_send_read.py -m integration` completes a full send→read cycle
- [ ] Tests are importable and discoverable by pytest
- [ ] conftest fixtures handle Desktop-unavailable gracefully (skip, don't crash)

## Overnight Agent Instructions
1. Read the existing `server.py` to understand current tool implementations
2. Read `/tmp/probe-desktop.py` for CDP connection pattern and discovered selectors
3. Read `/tmp/probe-generating.py` for generation state detection pattern
4. Create `tests/` directory structure
5. Write `conftest.py` with ws_connection fixture using the probe script's connect pattern
6. Write `test_selectors.py` — each selector as a separate test function
7. Write `test_status.py` — idle state assertions
8. Write `test_send_read.py` — full integration test
9. Add pytest config to `pyproject.toml`
10. Run `cd ~/brain/tools/mcps/claude-desktop-mcp && .venv/bin/python -m pytest tests/ -v` to verify
11. If Desktop is unavailable, ensure tests skip gracefully rather than error
