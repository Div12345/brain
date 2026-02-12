---
tags: [mcp, claude-desktop, truncation, async, cdp]
category: infrastructure
date: 2026-02-11
module: tools/mcps/claude-desktop-mcp
symptom: "CD MCP read truncates responses at 4000 chars, no async send/wait, can't detect new responses without full read"
root_cause: "Hard-coded text.substring(0, 4000) in get_messages() JS, blocking send+wait coupling, no response hash in status"
---

# Claude Desktop MCP Server: Truncation Fix + Async Patterns

## Problem

Three pain points from real-world CD delegation (Feb 10-11):

1. **Silent truncation**: `get_messages()` JS used `text.substring(0, 4000)` on every message. Long CD responses got silently cut off with no indication to callers.
2. **Blocking send-wait**: `claude_desktop_send(wait=true)` blocks until CD finishes. No way to send async and check later.
3. **Blind polling**: `claude_desktop_status` only returned `is_generating` and `message_count`. No way to detect "new response available" without reading the full message.

## Solution

### P0: Remove truncation, add caller-controlled limits
- Removed `text.substring(0, 4000)` from `get_messages()` and `text.substring(0, 10000)` from `read_interim()`
- Added `max_chars` param to `claude_desktop_read` (default 0 = unlimited)
- Each message now includes `is_truncated`, `total_chars` metadata
- Input validation with `max(0, ...)` on all numeric params

### P1: Decouple send from wait
- New `claude_desktop_wait` tool blocks until CD finishes, returns response
- Pattern: `send(wait=false)` → do other work → `wait(timeout=300)`
- When CD is idle, returns last assistant message immediately

### P2: Response hash in status (lightweight)
- `get_status()` JS now computes FNV-1a hash of last assistant message
- Samples first 500 + last 500 chars (detects changes at both ends)
- No Python-side `get_messages()` call — stays lightweight O(1)
- Returns `last_response_hash` and `last_response_length`

### P3: Chunked read
- `offset` and `limit` params on `claude_desktop_read` and `claude_desktop_read_interim`
- Response includes `has_more`, `total_chars`, `offset` for pagination

## Key Decisions

| Decision | Why |
|----------|-----|
| FNV-1a in JS, not md5 in Python | Avoids calling get_messages() on every status check (was O(n) → now O(1)) |
| Sample first 500 + last 500 chars | Detects changes at both ends of long responses |
| max_chars separate from offset/limit | Backwards-compatible truncation vs new chunked pagination |
| max(0, ...) input clamping | Prevents negative offset/limit edge cases |

## Gotchas

1. **max_chars applies BEFORE offset/limit**: If you set max_chars=4000 and offset=3000, you paginate the truncated text, not the original
2. **MCP server must be restarted** for changes to take effect (it's a subprocess)
3. **Desktop is single resource**: Don't call claude_desktop_wait from multiple agents simultaneously

## Files Changed

- `tools/mcps/claude-desktop-mcp/server.py` — all changes (+329 lines)
- `docs/plans/2026-02-11-feat-claude-desktop-mcp-async-truncation-fix-plan.md` — plan doc

## Testing

- `py_compile` passes
- Code review: 2 critical + 3 high issues found and fixed before commit
- Integration testing requires Desktop running with debugger enabled
