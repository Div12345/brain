---
title: Claude Desktop MCP Server - Async Patterns & Truncation Fix
type: feat
date: 2026-02-11
status: complete
deepened: 2026-02-11
prior_plan: 2026-02-05-mcp-server-improvements-plan.md
---

## Enhancement Summary

**Deepened on:** 2026-02-11
**Research agents used:** best-practices-researcher (MCP async patterns), framework-docs-researcher (Python MCP SDK), learnings-researcher (institutional knowledge), repo-research-analyst (codebase patterns)

### Key Research Insights
1. **MCP has no hard TextContent size limits** — removing 4000 cap is safe per protocol spec
2. **`isError: true` flag** exists in `CallToolResult` — should use for error responses instead of just JSON `{"error": ...}`
3. **MCP experimental Tasks API** exists for fire-and-forget but is heavy — our separate `wait` tool approach is simpler and sufficient
4. **Progress notifications** via `ctx.report_progress()` exist but require high-level MCPServer API — our low-level Server API doesn't support them easily
5. **CDP ping timeout gotcha** — disable `ping_interval=None` on websocket connections to prevent 20s disconnects (not currently an issue since we use sync `websocket-client`, not `websockets`)
6. **Response size best practice** — for very large responses, return resource URIs instead of text blobs. But for our use case (message reading), direct text is correct

# Claude Desktop MCP Server - Async Patterns & Truncation Fix

## Overview

Improve the CD MCP server (`tools/mcps/claude-desktop-mcp/server.py`) to fix response truncation, add async send/wait decoupling, and improve response reading for long content. This builds on the existing Feb 5 MCP improvements plan (P0-P4) and incorporates learnings from real-world delegation sessions.

## Problem Statement

Three pain points discovered during real CD delegation sessions (Feb 10-11):

1. **Response truncation**: `get_messages()` hard-caps every message at 4000 chars via `text.substring(0, 4000)` in renderer JS (line 415). Long CD responses get silently cut off. Callers receive partial data with no indication of truncation.

2. **Blocking send-wait coupling**: `claude_desktop_send` with `wait_for_response=true` blocks the entire MCP call until CD finishes. CC can't do other work while waiting. The only alternative (`wait_for_response=false`) provides no way to later wait for completion.

3. **No chunked reading**: `read_interim` returns the entire in-progress response as one blob. For long responses, this means either truncation or massive payloads. No offset/limit support.

## Institutional Learnings Applied

From `docs/solutions/2026-02-10-claude-desktop-delegation-patterns.md`:
- **Block, don't poll** — one `send(wait=true, timeout=300)` is better than read loops
- **Signal truncation explicitly** — callers need `is_truncated` flag, not silent cutoff
- **Desktop is single resource** — CDP connection not thread-safe, serialize all access
- **Debounce stop-button** — 2 consecutive absent polls needed (already in code)

From `docs/solutions/2026-02-05-gemini-desktop-steering-pipeline.md`:
- Hash-based detection returns thinking blocks, not actual responses
- Stop button presence is the canonical generation signal
- Pipe mode can buffer MCP output — consider explicit flush markers

## Proposed Changes

### P0: Fix Response Truncation (Critical)

**Problem**: Line 415 in `get_messages()` JS: `text.substring(0, 4000)`

**Solution**:
- [x] Remove the 4000 char hard cap from `get_messages()` JS
- [x] Add `max_chars` parameter to `claude_desktop_read` tool (default: 0 = unlimited)
- [x] When `max_chars > 0`, truncate and add `is_truncated: true` to response metadata
- [x] Add `total_chars` to each message in response so callers know full size
- [x] Return `is_truncated` flag per message in the messages array

**Files**: `server.py` — `get_messages()` JS template, `claude_desktop_read` handler

**Acceptance**:
- Read a 15K+ char response without truncation
- `max_chars=500` returns truncated text with `is_truncated: true` and `total_chars: 15000`

### P1: Decouple Send from Wait

**Problem**: `claude_desktop_send(wait_for_response=true)` blocks until done. No way to send async then wait later.

**Solution**:
- [x] Add `claude_desktop_wait` tool — blocks until CD stops generating, returns the response
  - Parameters: `timeout` (int, default 120)
  - Returns: `{response: "...", waited_seconds: N, is_truncated: bool}`
  - Uses existing `wait_for_response()` logic internally
- [x] Modify `claude_desktop_send` default `wait_for_response` to remain `true` (backwards compat)
- [x] Document the async pattern: `send(wait=false)` → do other work → `wait(timeout=300)`

**Files**: `server.py` — new tool registration + handler, reuse `wait_for_response()` function

**Acceptance**:
- `send(message, wait=false)` returns immediately with `{success: true, sent: message}`
- `wait(timeout=120)` blocks and returns full response when CD finishes
- Calling `wait` when CD isn't generating returns last assistant message immediately

### P2: Add Response Hash to Status

**Problem**: Callers can't detect "new response available" without reading the full message. Status only shows `is_generating` and `message_count`.

**Solution**:
- [x] Add `last_response_hash` (FNV-1a in JS, samples first 500 + last 500 chars) to `claude_desktop_status` output
- [x] Add `last_response_length` (char count of last assistant message)
- [x] Callers compare hash to detect change without reading full content

**Files**: `server.py` — `get_status()` function, `claude_desktop_status` handler

**Acceptance**:
- Status returns `{..., last_response_hash: "a1b2c3d4", last_response_length: 12500}`
- Hash changes when CD produces new response
- Hash stays same on repeated status calls with no new generation

### P3: Chunked Read for Long Content

**Problem**: Reading a 20K response as one JSON payload is unwieldy. No way to paginate.

**Solution**:
- [x] Add `offset` and `limit` params to `claude_desktop_read` tool
  - `offset`: character offset into the message text (default: 0)
  - `limit`: max characters to return (default: 0 = all)
- [x] Add same params to `claude_desktop_read_interim`
- [x] Response includes `total_chars`, `offset`, `has_more` for pagination

**Files**: `server.py` — `claude_desktop_read` and `claude_desktop_read_interim` handlers, `get_messages()` function

**Acceptance**:
- Read first 5000 chars: `read(last_n=1, offset=0, limit=5000)` → `{has_more: true, total_chars: 15000}`
- Read next chunk: `read(last_n=1, offset=5000, limit=5000)` → continues from where left off

## Architecture Constraints (Do NOT Violate)

1. **Single resource**: Desktop can only handle one controller. All CDP access must serialize. No concurrent requests.
2. **WebSocket per call**: Current pattern opens/closes WS per tool call. Preserve this — connection pooling is P1 from the older plan and has medium risk.
3. **stdio transport**: MCP server uses stdio. Don't add HTTP/SSE endpoints.
4. **Backwards compatibility**: Existing tool signatures must not break. New params have defaults matching old behavior.
5. **JSON response format**: All tools return `list[TextContent]` with `json.dumps()` result.
6. **Security**: Continue using `json.dumps()` for escaping expressions sent to renderer. Use `textContent` not `innerHTML`.

## Implementation Order

1. **P0 first** — Truncation fix. Highest impact, lowest risk. ~30 lines changed.
2. **P2 second** — Response hash in status. Quick win, enables smarter polling. ~20 lines.
3. **P1 third** — Wait tool. New tool, reuses existing logic. ~40 lines.
4. **P3 fourth** — Chunked read. Moderate complexity. ~50 lines.

## Risk Assessment

| Change | Risk | Mitigation |
|--------|------|------------|
| Remove 4000 char cap | Large responses may slow JSON serialization | Add optional `max_chars` param as escape valve |
| New `wait` tool | Caller might `wait` when nothing is generating | Return last assistant message immediately if idle |
| Response hash | Hash computation on every status call | md5 of first 1000 chars only (fast enough) |
| Chunked read | Off-by-one in offset math | Unit test with known-length strings |

## Test Strategy

- [ ] Update `tests/test_send_read.py` — verify no truncation on long responses
- [ ] New test: send long message, read back, assert full length preserved
- [ ] New test: `wait` tool returns response after generation completes
- [ ] New test: status includes `last_response_hash` and `last_response_length`
- [ ] New test: chunked read with offset/limit returns correct slices

## Files to Modify

| File | Changes |
|------|---------|
| `server.py:get_messages()` | Remove 4000 char cap, add total_chars tracking |
| `server.py:get_status()` | Add response hash + length |
| `server.py:list_tools()` | Add `claude_desktop_wait` tool, add new params to existing tools |
| `server.py:call_tool()` | Add `claude_desktop_wait` handler, update `read`/`read_interim` handlers |
| `tests/test_send_read.py` | Add truncation regression test |
| `tests/test_wait.py` (new) | Test wait tool behavior |

## References

- Prior plan: `docs/plans/2026-02-05-mcp-server-improvements-plan.md`
- Delegation patterns: `docs/solutions/2026-02-10-claude-desktop-delegation-patterns.md`
- Pipeline learnings: `docs/solutions/2026-02-05-gemini-desktop-steering-pipeline.md`
- Server source: `tools/mcps/claude-desktop-mcp/server.py` (1219 lines)
- Tests: `tools/mcps/claude-desktop-mcp/tests/`
