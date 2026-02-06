---
title: Leverage Claude Desktop Enterprise as Compute Resource
type: feat
date: 2026-02-05
brainstorm: context/plans/claude-desktop-compute-leverage-idea.md
---

# Leverage Claude Desktop Enterprise as Compute Resource

## Overview

Use the enterprise Claude Desktop account (session-limited, no weekly cap) as a second compute backend alongside Claude Code API. The existing MCP server and bridge module provide most of the infrastructure. Gemini CLI serves as the external steering agent — it connects to Desktop via the same MCP tools.

## Problem Statement

- Claude Code API has a 7-day rolling quota (currently 67% used). Interactive sessions compete with overnight autonomous tasks.
- Enterprise Claude Desktop has session-only limits but sits idle most of the time.
- An MCP server exists (`tools/mcps/claude-desktop-mcp/`) with full Desktop control via CDP on port 9229.

## Existing Infrastructure

| Component | Status | Location |
|-----------|--------|----------|
| MCP server (official SDK) | Working | `tools/mcps/claude-desktop-mcp/server.py` |
| CDP control (send/read/navigate/relaunch) | Working | `server.py:245-280` |
| Bridge schemas (Task/Response, Pydantic) | Complete | `bridge/schema.py` |
| File watcher + concurrency control | Complete | `bridge/watcher.py` |
| Queue processor | Complete | `bridge/processor.py` |
| Notification module | Fixed | `bridge/notify.py:11` |
| Response waiting (hash-based stability) | Working but fragile with long responses | `server.py:282-302` |
| Config module | Complete | `bridge/config.py` |

## Completed — MVP (Phase 1 + 2)

### Phase 1: Restore Debugger Access

- [x] 1a. Verify debugger on port 9229 — `curl http://127.0.0.1:9229/json` returns targets
- [x] 1b. Confirm WSL → Windows localhost connectivity works
- [x] 1c. MCP server connects successfully from Claude Code

### Phase 2: Fix Bridge & Test MCP + Gemini Integration

- [x] 2a. Fix `bridge/notify.py:11` — `from server import get_main_process_ws as get_claude_ws`
- [x] 2b. Test `claude_desktop_info` — returns conversation ID, URL, title
- [x] 2c. Test send/read cycle — sent "2+2", got "4" back with thinking trace
- [x] 2d. Test create new conversation + send message workflow — works end-to-end
- [x] 2e. Add claude-desktop MCP to Gemini CLI (`~/.gemini/settings.json`)
- [x] 2f. Add Desktop control instructions to Gemini system prompt (`~/.gemini/GEMINI.md`)

## Remaining — Phase 3: Test Suite (TDD foundation)

Write tests BEFORE implementing changes. Probe scripts in `/tmp/probe-*.py` have the DOM knowledge.

- [x] 3a. Create `tests/` directory in `tools/mcps/claude-desktop-mcp/`
- [x] 3b. `tests/test_selectors.py` — assert `data-testid` attributes exist in DOM (catches Desktop updates)
- [x] 3c. `tests/test_status.py` — assert stop-button detection works for generating/idle states
- [x] 3d. `tests/test_send_read.py` — send→read round-trip integration test
- [x] 3e. `tests/conftest.py` — shared fixtures (ws connection, renderer eval helper)
- [x] 3f. `pytest.ini` or `pyproject.toml` test config

## Remaining — Phase 4: MCP Core Fixes

Fix the 3 existing tools + add 3 new tools. No model switching, file upload, or projects — YAGNI.

### Fix existing tools:
- [x] 4a. `send_message()` — escape HTML entities in message text (prevents injection)
- [x] 4b. `wait_for_response()` — replace hash-based stability with stop-button polling (`button[aria-label="Stop response"]` present = generating, absent = done)
- [x] 4c. Migrate all CSS selectors to `data-testid` where available (18 stable testids found via probing)
- [x] 4d. `claude_desktop_info` — add model name, message count, generating state to output

### Add new tools:
- [x] 4e. `claude_desktop_status` — lightweight: is it generating? idle? what model? message count? (no side effects)
- [x] 4f. `claude_desktop_stop` — click stop button to halt generation mid-response
- [x] 4g. `claude_desktop_read_interim` — read partial response while still generating

## Remaining — Phase 5: Gemini Orchestration

- [x] 5a. Update `~/.gemini/GEMINI.md` with new tool inventory (status/stop/read_interim)
- [x] 5b. Write edge case playbook in GEMINI.md: compaction detection, stuck recovery, session rotation
- [x] 5c. Write CE-style orchestration instructions: task lifecycle, quality checks, when to stop/retry
- [x] 5d. Test full Gemini→Desktop pipeline with new tools
- [x] 5e. Iteratively refine instructions based on CC review of Gemini run logs

## Remaining — Phase 6: Scheduler Integration

- [x] 6a. Add `backend: code | desktop | auto` to task frontmatter schema
- [x] 6b. Add Gemini-Desktop executor in scheduler — `gemini -p "task" --yolo` subprocess
- [x] 6c. Add `--backend` flag to `ccq`
- [x] 6d. Desktop capacity check — ping `127.0.0.1:9229` before routing
- [x] 6e. Wire Windows Task Scheduler trigger for Gemini-based overnight runs

## Remaining — Phase 7: Review Layer + Real Workload

- [x] 7a. Scheduled CC session that reviews Gemini run logs for quality/completeness
- [x] 7b. Route first real non-research tasks through pipeline
- [x] 7c. Capture learnings → `docs/solutions/`

## Architecture Decision: Sync Gemini Worker

Gemini CLI has no `run_in_background` for tool calls (open issue [#1689](https://github.com/google-gemini/gemini-cli/issues/13594)). All tool calls block synchronously. The async layer lives one level up:

```
CC scheduler (run_in_background=True)
  └→ Bash("gemini -p 'task' --yolo")   ← blocks
       └→ claude_desktop_send(wait=true) ← blocks
            └→ Desktop works
       └→ gemini captures, follows up
  └→ CC gets notified on exit ✓

OR standalone overnight:
Windows Task Scheduler → PowerShell → WSL
  └→ gemini -p "task" --yolo
  └→ exit code + output file = result
```

## Edge Case Handling

| Edge Case | Detection | Response |
|-----------|-----------|----------|
| Compaction | Message count drops, response ignores context | `claude_desktop_new` → re-send with checkpoint |
| Stuck generation (>5min) | Stop button present, no new text 60s+ | `claude_desktop_stop` → retry simplified |
| Desktop crashed | Status returns connection error | `claude_desktop_relaunch` → wait 10s → retry |
| Too-long response | Interim >10K chars, still generating | `claude_desktop_stop` → capture → "continue from..." |
| Thinking too long | Only thinking block for >3min | Wait up to 5min, then stop + retry with "be concise" |
| Rate limited | Response contains "rate limit" text | Back off 60s → retry |
| Session degradation | Quality declining (orchestrator judgment) | `claude_desktop_new` → fresh context |
| Network disconnect | WebSocket fails on 9229 | Retry 3x with 5s backoff → alert if persistent |

## Key DOM Findings (from probing)

- **Generation state**: Stop button `button[aria-label="Stop response"]` is definitive. Present = generating, absent = done.
- **18 stable `data-testid` selectors** found (more resilient than CSS classes)
- **Model visible** via `[data-testid="model-selector-dropdown"]` text content
- **File input** at `#chat-input-file-upload-bottom` with DataTransfer API available
- **Message container**: uses `[data-testid="user-message"]` for role detection

## How to Use Now (MVP)

### From Claude Code (this session)
The MCP tools are available as `mcp__claude-desktop__*`. Use directly:
```
claude_desktop_new → claude_desktop_send(message, wait_for_response=true) → claude_desktop_read
```

### From Gemini CLI
```bash
gemini
# Then in chat: "Use Claude Desktop to research [topic]"
# Gemini will use the claude-desktop MCP tools automatically
```

### Failure Recovery
- **Timeout**: increase `timeout` param or set `wait_for_response=false` and poll with `read`
- **Compaction**: `claude_desktop_new` to start fresh
- **Unresponsive**: `claude_desktop_relaunch` then retry

## Acceptance Criteria

- [x] Claude Desktop debugger accessible from WSL via port 9229
- [x] MCP tools (send/read/info/new) work from Claude Code session
- [x] Bridge notify.py bug fixed
- [x] Gemini CLI configured with claude-desktop MCP
- [x] Gemini CLI has system instructions for Desktop control
- [x] At least one research task successfully routed to Desktop via Gemini CLI
- [x] At least one task successfully routed to Desktop via scheduler

## Files Changed

| File | Change | Status |
|------|--------|--------|
| `tools/mcps/claude-desktop-mcp/bridge/notify.py:11` | Fix import bug | Done |
| `~/.gemini/settings.json` | Add claude-desktop MCP server entry | Done |
| `~/.gemini/GEMINI.md` | Add Desktop control instructions | Done |
| `tools/cc-scheduler/lib/tasks.py` | Add `backend` field to Task dataclass | Done |
| `tools/cc-scheduler/lib/executor.py` | Add Desktop execution path | Done |
| `tools/cc-scheduler/ccq` | Add `--backend` flag | Done |

## Dependencies & Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Debugger disappears after Desktop update | Blocks everything | Re-enable from Help menu or `--inspect=9229` flag |
| Desktop "amnesia" on long tasks | Lost work | Keep tasks short, checkpoint, session rotation |
| WSL → Windows localhost connectivity | Can't reach port 9229 | Already verified working |
| Desktop compaction mid-task | Partial results | Detect via message count, restart in new conversation |
| Gemini CLI MCP stability | Tools may not connect | Fallback to Claude Code MCP tools directly |

## References

- MCP server: `tools/mcps/claude-desktop-mcp/server.py`
- Bridge module: `tools/mcps/claude-desktop-mcp/bridge/`
- Scheduler: `tools/cc-scheduler/`
- Brainstorm: `context/plans/claude-desktop-compute-leverage-idea.md`
- MCP plugin idea: `context/plans/mcp-plugin-restructure-idea.md`
- Gemini CLI config: `~/.gemini/settings.json`
- Gemini system prompt: `~/.gemini/GEMINI.md`
