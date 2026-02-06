---
title: Claude Desktop MCP Server Improvements
type: improvement
date: 2026-02-05
source_task: 072-ce-plan-mcp-improvements
status: ready
---

# Claude Desktop MCP Server Improvements

## Problem Statement

The Claude Desktop MCP server works for basic steering but has reliability and performance gaps exposed by real-world Gemini pipeline usage:

1. **Response Truncation**: `claude_desktop_read` cuts off long responses mid-text
2. **Tool Call Latency**: Each CDP round-trip adds ~1-2s, complex scenarios (6+ calls) hit timeouts
3. **No Pagination**: Can't fetch full conversation history for long sessions
4. **Limited Error Context**: Connection failures return generic errors, hard to diagnose

## Proposed Changes (Priority Order)

### P0: Fix Response Truncation

**Impact**: High - Currently the #1 pain point

**Problem**: Long Desktop responses (>4K chars) get cut off in `get_messages()`. The DOM scraping extracts partial text.

**Solution**:
- [ ] Add `full_response` parameter to `claude_desktop_read` (default: false for backwards compat)
- [ ] When `full_response=true`, iterate through message blocks and concatenate
- [ ] Add chunked reading: `claude_desktop_read_chunk(message_index, chunk_start, chunk_size)`
- [ ] Return `is_truncated: bool` flag in response metadata

**Files**: `server.py:get_messages()`

**Acceptance**: Read a 10K+ char response without truncation

### P1: Reduce Tool Call Latency

**Impact**: High - Cumulative latency causes timeouts

**Problem**: Each tool call does full CDP handshake: find ws target → connect → enable Runtime → eval → disconnect

**Solution**:
- [ ] Connection pooling: keep WebSocket alive between calls within same session
- [ ] Add `_ws_pool` dict keyed by target URL with TTL (30s)
- [ ] Lazy cleanup: close stale connections on next call
- [ ] Add connection reuse metric to status output

**Files**: `server.py:get_renderer_ws()`, new `connection_pool.py` module

**Acceptance**: 3 sequential tool calls complete in <3s (vs current ~6s)

### P2: Add Pagination to Message Reading

**Impact**: Medium - Enables full conversation analysis

**Problem**: Long conversations (20+ messages) can't be fully retrieved

**Solution**:
- [ ] Add `offset` and `limit` params to `claude_desktop_read`
- [ ] Return `total_messages` count in response
- [ ] Add `claude_desktop_read_all` for full dump (with truncation warning)

**Files**: `server.py:get_messages()`

**Acceptance**: Retrieve all messages from a 50-message conversation

### P3: Improve Error Diagnostics

**Impact**: Medium - Reduces debugging time

**Problem**: "Connection error" doesn't say why (Desktop not running? Debugger disabled? Wrong port?)

**Solution**:
- [ ] Add structured error codes: `DESKTOP_NOT_RUNNING`, `DEBUGGER_DISABLED`, `RENDERER_NOT_FOUND`, `EVAL_FAILED`
- [ ] Include diagnostic hints in error messages
- [ ] Add `claude_desktop_diagnose` tool that runs full health check

**Files**: `server.py`, new `errors.py` module

**Acceptance**: Each failure mode has distinct error code and actionable message

### P4: Add Response Streaming (Future)

**Impact**: Low (nice-to-have) - Enables real-time monitoring

**Problem**: `read_interim` polls; no push notification when response completes

**Solution**:
- [ ] Investigate CDP Runtime.evaluate with awaitPromise for streaming
- [ ] Or: use MutationObserver in renderer to detect changes
- [ ] Add SSE-style streaming tool `claude_desktop_stream`

**Deferred**: Requires significant architecture change, low priority

## Risk Assessment

| Change | Risk | Mitigation |
|--------|------|------------|
| Connection pooling | Stale connections cause silent failures | TTL + explicit close on error |
| Full response reading | Memory blowup on huge responses | Add max_length param, default 100KB |
| New error module | Breaking changes to error handling | Keep old error strings as fallback |

## Complexity Estimates

| Change | Lines of Code | Test Cases | Risk |
|--------|--------------|------------|------|
| P0: Truncation fix | ~50 | 3 | Low |
| P1: Connection pooling | ~100 | 5 | Medium |
| P2: Pagination | ~30 | 3 | Low |
| P3: Error diagnostics | ~80 | 6 | Low |
| P4: Streaming | ~200 | 8 | High |

### P-1: Fix Connector Management Tools (URGENT)

**Impact**: High - Currently broken, blocks MCP auto-configuration

**Problem**: `list_connectors`, `toggle_connector`, `reload_mcp` return empty or fail silently. DOM selectors (`button[aria-label="Toggle menu"]`, `[role="menuitem"]` for "Connectors") don't match current Desktop UI.

**Solution**:
- [ ] Probe Desktop DOM to find correct selectors for menu and connectors
- [ ] Update `list_connectors()` with working selectors
- [ ] Update `toggle_connector()` to actually click the toggle
- [ ] Test: `list_connectors` should return actual connector list
- [ ] Test: `toggle_connector("obsidian", true)` should enable Obsidian MCP

**Files**: `server.py:416-470` (list_connectors, toggle_connector functions)

**Acceptance**: `claude_desktop_list_connectors` returns non-empty list of actual connectors

## Implementation Order

1. **P-1 first** - URGENT: Connector tools are broken
2. **P0 second** - Response truncation fix
3. **P3 third** - Helps debug P1 if issues arise
4. **P1 fourth** - Biggest performance impact
5. **P2 fifth** - Enables new use cases
6. **P4 deferred** - Only if streaming becomes necessary

## Test Strategy

- Unit tests: Mock CDP responses, verify parsing
- Integration tests: Real Desktop connection, verify round-trip
- Regression: Existing test suite must pass
- Performance: Benchmark 5-call sequence before/after P1

## Files to Modify

| File | Changes |
|------|---------|
| `server.py` | P0, P1, P2, P3 changes |
| `errors.py` (new) | P3 error codes |
| `connection_pool.py` (new) | P1 pooling logic |
| `tests/test_truncation.py` (new) | P0 tests |
| `tests/test_pooling.py` (new) | P1 tests |
| `tests/test_errors.py` (new) | P3 tests |
