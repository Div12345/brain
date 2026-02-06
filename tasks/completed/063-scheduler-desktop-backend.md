---
name: scheduler-desktop-backend
priority: 7
estimated_tokens: 30000
mode: autonomous
timeout: 30m
skill: null
model_hint: sonnet
tags: [scheduler, gemini, claude-desktop, integration]
depends_on: [gemini-orchestration-instructions]
---

# Add Desktop Backend to CC Scheduler

## Goal
Add `backend: desktop` option to cc-scheduler so tasks can be routed to Claude Desktop via Gemini CLI instead of Claude Code API. This saves CC API quota by offloading work to the enterprise Desktop account.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain
- **Scheduler at:** ~/brain/tools/cc-scheduler/
- **Gemini CLI:** `gemini` command available in PATH

## Architecture
```
ccq run --backend desktop
  → scheduler picks task from queue
  → spawns: gemini -p "<task prompt>" --yolo --model gemini-2.5-pro
  → gemini uses claude-desktop MCP tools to steer Desktop
  → captures stdout as task result
  → writes result to task completion file
```

## What This Task Must Produce

### 1. Task Schema Update
Add `backend` field to task frontmatter:
```yaml
backend: code | desktop | auto  # default: code
```
- `code`: current behavior via `claude -p`
- `desktop`: route to Desktop via Gemini CLI
- `auto`: prefer Desktop if available, fall back to Code

### 2. Desktop Executor
New module or function in scheduler that:
- Checks Desktop availability: `curl -s http://127.0.0.1:9229/json` returns 200
- Constructs Gemini prompt from task content (include task goal, constraints, success criteria)
- Runs `gemini -p "<prompt>" --yolo --model gemini-2.5-pro` as subprocess
- Captures stdout/stderr
- Writes result to task output location
- Handles Gemini exit codes (0=success, non-zero=failure)

### 3. CLI Flag
Update `ccq` to support:
- `ccq run --backend desktop` — force Desktop backend
- `ccq run --backend auto` — auto-select
- Default remains `code`

### 4. Capacity Check
Before routing to Desktop:
- Ping `127.0.0.1:9229` — if unreachable, fall back to Code or skip
- Check Gemini availability: `gemini --version` succeeds

### 5. Config Update
Add to `tools/cc-scheduler/config.yaml`:
```yaml
backends:
  desktop:
    gemini_command: gemini
    gemini_flags: ["--yolo", "--model", "gemini-2.5-pro"]
    desktop_check_url: "http://127.0.0.1:9229/json"
    timeout: 30m
```

## Success Criteria
- [ ] `ccq run --backend desktop` processes a task via Gemini→Desktop pipeline
- [ ] `ccq run --backend auto` checks Desktop availability before routing
- [ ] Task result is captured and written correctly
- [ ] Fallback to Code backend works when Desktop unavailable
- [ ] Config file updated with backend settings

## Overnight Agent Instructions
1. Read scheduler code: `tools/cc-scheduler/ccq`, `tools/cc-scheduler/config.yaml`
2. Read `tools/cc-scheduler/lib/` to understand existing executor pattern
3. Read the plan at `docs/plans/2026-02-05-feat-claude-desktop-compute-leverage-plan.md`
4. Add `backend` field handling to task parsing
5. Create Desktop executor (Gemini subprocess wrapper)
6. Add `--backend` flag to CLI
7. Add capacity check function
8. Update config.yaml with backend settings
9. Test with a simple task if Desktop is available
10. Ensure existing Code backend still works unchanged
