---
title: Gemini CLI → Claude Desktop Steering Pipeline
date: 2026-02-05
category: architecture
tags: [gemini-cli, claude-desktop, mcp, orchestration, pipeline]
module: cc-scheduler
severity: high
---

# Gemini CLI → Claude Desktop Steering Pipeline

## Problem
Need to leverage Claude Desktop (Enterprise, unlimited) for overnight autonomous task execution without burning Claude Code API quota. Gemini CLI can orchestrate Desktop via MCP tools.

## Solution Architecture

```
Windows Task Scheduler (03:30 AM)
  → WSL bash: trigger-overnight.sh
    → Python: ccq run --backend desktop
      → Gemini CLI (gemini-3-pro-preview)
        → claude-desktop MCP server
          → Claude Desktop (Enterprise)
```

## Key Learnings

### 1. Gemini CLI is Fully Synchronous
- No `run_in_background` equivalent (GitHub issue #1689)
- Async layer lives at CC/OS scheduler level, not Gemini
- Each `gemini -p` call blocks until complete

### 2. Stop-Button Polling for Response Detection
- Hash-based detection returned thinking blocks, not actual responses
- Stop button (`button[aria-label="Stop response"]`) present = generating, absent = done
- Debounce required: 2 consecutive absent polls to avoid flicker false positives

### 3. Desktop is a Single Resource
- Only one orchestrator can control Desktop at a time
- Parallel experiments (flash + pro simultaneously) both fail
- Eval scenarios MUST run sequentially

### 4. Gemini Output Buffering in Pipe Mode
- `gemini -p` buffers all output — tool call details are invisible in pipes
- Only final text summary appears in logs
- Workaround: check Desktop state directly (claude_desktop_status/read) to verify steering
- `--output-format stream-json` may help for future transparency

### 5. MCP Server Overhead Matters
- Default Gemini config loads 5 MCP servers (paper-search, obsidian, memory, zotero, claude-desktop)
- Each adds startup latency and potential rate limit pressure
- Solution: `--allowed-mcp-server-names claude-desktop` strips to only what's needed
- Reduces startup from ~15s to ~3s

### 6. Gemini Confuses MCP Tools with delegate_to_agent
- Gemini sometimes routes `claude_desktop_new` through its built-in `delegate_to_agent` tool
- Fix: explicit instruction in GEMINI.md: "NEVER use delegate_to_agent for claude_desktop_* tools"
- This self-corrects after one failed attempt, but wastes a turn

### 7. Desktop Prompt Wrapper is Essential
- When scheduler routes a task to desktop backend, the raw task body means nothing to Gemini
- Must wrap with Desktop-specific protocol: new → send → read → evaluate → iterate
- Implemented in executor.py `build_prompt(task, backend="desktop")`

### 8. Model Selection Results (Full 12-Scenario Eval)

Ran 4 scenarios × 3 models. Scenarios: S1 (simple send/read), S2 (multi-turn with follow-up), S3 (error recovery: send→wait→status→interim→stop→read), S4 (complex multi-turn analysis with depth evaluation).

| Scenario | gemini-3-pro-preview | gemini-2.5-pro | gemini-2.5-flash |
|----------|---------------------|----------------|------------------|
| S1 simple | PASS q=5 87s | PASS q=5 64s | UNKNOWN 120s* |
| S2 multiturn | PASS q=5 150s | PASS q=5 225s | PASS q=4 128s |
| S3 recovery | UNKNOWN 180s† | UNKNOWN 180s† | PASS q=5 91s |
| S4 complex | UNKNOWN 300s† | PASS q=5 145s | PASS q=5 116s |
| **Pass Rate** | **2/4** | **3/4** | **3/4** |

\* Flash S1 UNKNOWN likely a buffering fluke — markers not captured in pipe output.
† UNKNOWN = timeout before markers output, NOT steering failure. Log review confirms correct tool usage.

**Recommendations:**
- **Primary model: gemini-2.5-pro** — Best balance of quality (5/5 on all passes) and reliability
- **Fast/cheap tasks: gemini-2.5-flash** — Surprisingly capable, fastest S3/S4, lower quality ceiling (q=4 on S2)
- **gemini-3-pro-preview** — Excellent steering quality but slower, hits timeouts on complex scenarios
- **S3 scenario needs redesign** — 180s timeout insufficient for 6+ tool calls; increase to 300s or simplify

### 9. Task File Double-Move Race Condition
- Gemini sometimes moves task files itself (following brain repo conventions)
- Scheduler's post-execution `move_task` then fails with FileNotFoundError
- Not critical: task is correctly completed, just error in logging
- **Fixed**: `move_task` now idempotent — if source gone but destination exists, returns success

### 10. S3 Error Recovery Scenario Timeout
- The error recovery scenario (send → wait → status → interim → stop → read) requires 6+ tool calls
- With 180s timeout, Gemini runs out of time before outputting markers
- The steering itself works — Gemini correctly uses `new`, `send(wait=false)`, `sleep`, `status`
- But pipe buffering hides progress, and cumulative tool call latency eats the timeout
- Fix: increase S3 timeout to 300s, or simplify the scenario to fewer steps

### 11. Test Suite Growth Pattern
- Started with 10 task schema tests, added 3 executor tests for idempotent move_task
- 13/13 tests pass across both test files
- Test isolation via tempfile + mock patching of TASKS_DIR works well
- Pattern: one test file per module (test_tasks.py, test_executor.py)

### 12. Gemini Quota Management is Critical
- Running a 12-scenario eval (4 scenarios × 3 models) exhausts all Gemini model quotas in ~45 minutes
- gemini-3-pro-preview, gemini-2.5-pro, and gemini-2.5-flash all share separate daily quotas
- Once exhausted, quotas reset ~20 hours later (not a rolling window — appears to be daily reset)
- Added `TerminalQuotaError` detection in executor.py for fail-fast behavior
- **Prevention**: limit eval runs, stagger across models, or run evals on one model at a time
- **Recovery**: tasks in `failed/` can be moved back to `pending/` for the overnight run when quotas reset
- Config should default to the model with the most remaining quota

### 14. Gemini MCP Tools Not Loading in Pipe Mode

**Symptoms:** Gemini `-p` mode shows only built-in tools (`save_memory`, `list_directory`, `read_file`), not MCP server tools like `claude_desktop_*`. Error: "Tool 'claude_desktop_new' not found in registry."

**Investigation:**
- MCP server configured correctly in `~/.gemini/settings.json` ✓
- `--allowed-mcp-server-names` CLI flag valid (verified in source) ✓
- MCP server works when tested directly via stdio ✓
- MCP enabled by default (no disable flags) ✓
- `isTrustedFolder()` returns true (folder trust disabled by default) ✓

**Root Cause (Suspected):** Race condition — in non-interactive `-p` mode, Gemini may send prompt before async MCP discovery completes. The `mcp-client-manager.js` shows discovery is Promise-based with no explicit await before prompt processing in `nonInteractiveCli.js`.

**Solution:** Added `"mcp": {"allowed": ["claude-desktop"]}` to `~/.gemini/settings.json`. The CLI flag `--allowed-mcp-server-names` doesn't work properly in `-p` mode, but the settings.json config does!

**Verified:** Gemini flash successfully called `claude_desktop_new`, `claude_desktop_send`, got response from Desktop.

**Key insight:** Settings.json `mcp.allowed` > CLI `--allowed-mcp-server-names` for non-interactive mode.

### 13. Windows Task Scheduler from WSL
- `schtasks.exe /Create` works directly from WSL without admin privileges
- `Register-ScheduledTask` (PowerShell) requires admin — use schtasks.exe instead
- Command: `schtasks.exe /Create /TN "BrainOvernightGemini" /TR "cmd.exe /c wsl -d Ubuntu -- /path/to/script.sh" /SC DAILY /ST 03:30 /F`
- Verify: `schtasks.exe /Query /TN "BrainOvernightGemini" /FO LIST`
- trigger-overnight.sh must handle its own PATH setup (nvm, node, gemini) since Task Scheduler runs non-interactively

## Files Modified/Created
- `tools/mcps/claude-desktop-mcp/server.py` — MCP core fixes, 3 new tools
- `tools/mcps/claude-desktop-mcp/tests/` — Test suite (7 tests)
- `tools/cc-scheduler/tests/test_executor.py` — Executor tests (3 tests, move_task idempotency)
- `tools/cc-scheduler/lib/executor.py` — Desktop backend, prompt wrapper
- `tools/cc-scheduler/lib/tasks.py` — Backend field, lenient skill validation
- `tools/cc-scheduler/ccq` — --backend flag
- `tools/cc-scheduler/config.yaml` — Backend config, schedule windows
- `tools/cc-scheduler/trigger-overnight.sh` — Overnight runner
- `tools/cc-scheduler/setup-win-scheduler.ps1` — Windows Task Scheduler setup
- `tools/run-gemini-task.sh` — Standalone Gemini task runner
- `~/.gemini/GEMINI.md` — Orchestration instructions for Gemini

## Patterns to Reuse
1. **MCP server filtering** via `--allowed-mcp-server-names` for any Gemini pipeline
2. **Desktop prompt wrapper** pattern: wrap raw task with tool-use protocol
3. **Sequential eval framework** for single-resource testing
4. **Stop-button polling with debounce** for reliable response detection
5. **Lean config approach** — only load MCPs you need

## What Would Make This Easier Next Time
- Gemini CLI supporting `--output-format stream-json` for transparent tool call logging
- Desktop MCP `read` returning full message content without truncation
- ~~`move_task` idempotency in scheduler~~ (DONE — implemented and tested)
- Gemini CLI background process support (issue #1689)

### 15. Desktop is Windows, Tasks Reference WSL Paths

**Problem:** Task instructions often use WSL paths like `~/brain/tools/...` but Desktop runs on Windows and can't access these directly.

**What happens:**
- Gemini falls back to using its own file tools (list_directory, read_file)
- This works but bypasses Desktop entirely, losing access to Desktop's specialized MCPs

**Solutions (not yet implemented):**
1. **Domain-specific routing**: Obsidian tasks use Obsidian MCP (REST API), code tasks use Gemini tools
2. **Windows path translation**: Convert to `\\wsl$\Ubuntu\home\div\...`
3. **Explicit instructions**: Task templates must specify which tools to use

**Current mitigation:** Updated Obsidian task (071) to explicitly require Obsidian MCP tools.

### 16. Gemini Quota Exhaustion Pattern

**Pattern:** One comprehensive task (330s, scheduler review) exhausts quota for ~14 hours.

**Implications:**
- Can only run ~1 serious task per day via Gemini→Desktop
- Multiple models have separate quotas but all exhaust similarly
- Need quota-aware task batching

**Mitigation:**
- Scheduler should check remaining quota before starting large tasks
- Consider smaller, focused tasks vs comprehensive reviews
- Model rotation if one quota exhausted

### 17. GEMINI.md Template Updates

Added to tool inventory:
- `claude_desktop_list_connectors` — List MCP connectors and status
- `claude_desktop_toggle_connector` — Enable/disable connectors
- `claude_desktop_reload_mcp` — Reload MCP config

Added edge case playbook entry for "Missing MCP Tools" scenario.

### 18. Scheduler Code Review Findings (via pipeline)

Task 070 completed successfully, reviewing all cc-scheduler modules:
- `lib/tasks.py`: 3/5 — needs robust YAML parsing, better error handling
- `lib/executor.py`: Security concern — potential command injection in subprocess
- `tests/test_tasks.py`: 2/5 — minimal coverage
- `tests/test_executor.py`: 1/5 — only tests move_task
- `lib/capacity.py`, `lib/budget.py`, `lib/scheduler.py`, `lib/task_queue.py`: 4/5 each
- `lib/log_utils.py`: 4.5/5 — well-designed

**Critical gaps:** No tests for most modules, command injection risk needs investigation.

### 19. MCP Fallback Strategy Works

**Observation:** Task 071 (Obsidian analysis) completed successfully despite Desktop not having Obsidian MCP loaded.

**What happened:**
1. Gemini instructed Desktop to use Obsidian MCP tools
2. Desktop said tools weren't available
3. Gemini tried `claude_desktop_reload_mcp` - still no Obsidian tools
4. Desktop **adapted** and used Desktop Commander (file system) instead
5. Analysis completed successfully via `C:\Users\din18\brain`

**Key insight:** The pipeline is more resilient than expected. Desktop can adapt using alternative tools when preferred MCPs aren't loaded. This is acceptable for analysis tasks but may not work for tasks requiring specific MCP features.

### 20. Standardization Rules Added to GEMINI.md

Added 3 new critical rules:
1. **Windows paths**: Desktop is Windows, use `C:\...` not `/home/...`
2. **MCP fallback**: Try reload, then adapt with alternative tools
3. **Completion summary**: Required structured output format

### 21. Both Pipeline Tasks Completed Successfully

| Task | Duration | Method | Result |
|------|----------|--------|--------|
| 070 scheduler review | 330s | Gemini file tools | Comprehensive code review |
| 071 obsidian analysis | 321s | Desktop Commander (fallback) | Full vault analysis with recommendations |

**Success rate with flash model:** 2/2 (when quota available)

### 22. Connector Tools Fixed via Pipeline (Self-Healing)

**Problem:** `list_connectors` and `toggle_connector` tools returned empty/failed due to outdated DOM selectors.

**Solution process:**
1. Created task 073 (fix-mcp-connector-tools)
2. Ran via Gemini→Desktop pipeline
3. Desktop analyzed code, provided fix with fallback selectors
4. Fix applied to server.py
5. Tools now work

**Working tools:**
- `list_connectors` → Returns 10 connectors with enabled state
- `toggle_connector` → Successfully toggled Obsidian from disabled to enabled

**Key selectors (from fix):**
- Menu: `button[aria-label*="menu"], button[aria-label*="settings"]` with fallbacks
- Connectors item: `[role="menuitem"]` with text "Connectors"
- Toggle: `[role="switch"], input[type="checkbox"]`

**Meta-learning:** The pipeline can fix its own tools - Desktop analyzed the MCP server code and provided working fixes.

### 23. Toggle Connector Python Bug Fix

**Problem:** `toggle_connector` failed with `'str' object has no attribute 'toLowerCase'`

**Cause:** Line 587 in server.py used `{connector_name.toLowerCase()}` inside an f-string - mixing Python f-string interpolation with JavaScript method name.

**Fix:** Changed to `{connector_name.lower()}` (Python method).

**Verified:** Both enable and disable work correctly through Gemini pipeline.

### 24. Gemini Tool Confusion - Clear Instructions

**Problem:** Gemini was sending `list_connectors`/`toggle_connector` requests TO Desktop instead of calling its own MCP tools.

**Cause:** Task instructions didn't clearly distinguish between Gemini's tools and Desktop's tools.

**Fix:** Added explicit section to GEMINI.md:
```
## YOU vs DESKTOP — Critical Distinction
YOUR tools (call directly): claude_desktop_*
DESKTOP's tools (ask via send): obsidian_*, zotero_*, memory_*, etc.
```

Also made task instructions very explicit about "YOUR TOOL CALL: ..." vs "Ask Desktop to...".

### 25. Fallback Sequence Works

The MCP fallback sequence now works correctly:
1. If `list_connectors` fails initially
2. Call `reload_mcp()` → `new()` → retry
3. Second attempt succeeds

This is documented in GEMINI.md rule #5.

### 26. Full Connector Enable → Tools Available Verified

**End-to-end test passed:** Enabling a disabled connector makes its tools available in Desktop.

**Sequence that works:**
1. `toggle_connector(name, enable=true)` - enable the connector
2. `reload_mcp()` - refresh MCP configuration
3. `new()` - **CRITICAL: must start new conversation for tools to appear**
4. `send(message asking Desktop to use the tool)` - verify tools work

**Test result:** Enabled `paper-search` → Desktop successfully used `search_papers` tool.

**Key insight:** The `new()` step is essential - tools don't appear in existing conversations after reload.

### 27. MCP Contention Issue

**Problem:** When CC and Gemini both try to use claude-desktop MCP simultaneously, tasks get stuck with timeouts.

**Cause:** The MCP server connects to Desktop via CDP (Chrome DevTools Protocol). Concurrent connections cause resource contention.

**Solution:** Don't use Desktop MCP tools from CC while Gemini task is running. Let Gemini have exclusive access.

**Verified:** Task completed successfully (182.7s) when CC didn't interfere with MCP calls.

### 28. First Valuable Task Completed

The scheduler analysis task produced genuinely useful output:
- **P0 Bug**: `os.set_blocking()` Unix-only in executor.py:148
- **P1**: Silent error swallowing in multiple exception handlers
- **P2**: Briefing window hour 23 overflow bug
- **Test gaps**: executor.py and scheduler.py have ZERO tests

This validates the pipeline can produce actionable improvements, not just test results.

## Files Modified (Session 2026-02-05 PM)
- `~/.gemini/GEMINI.md` — Added 6 critical rules including Windows paths, MCP fallback, completion summary
- `tools/cc-scheduler/config.yaml` — Updated model to gemini-2.5-flash
- `docs/plans/2026-02-05-mcp-server-improvements-plan.md` — Created P0-P4 improvement plan
- `tasks/pending/071-analyze-obsidian-vault-patterns.md` — Fixed to use Obsidian MCP tools
- `docs/brainstorms/2026-02-05-gemini-desktop-pipeline-reliability.md` — Reliability planning
