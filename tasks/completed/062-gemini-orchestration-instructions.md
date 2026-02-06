---
name: gemini-orchestration-instructions
priority: 7
estimated_tokens: 20000
mode: autonomous
timeout: 20m
skill: null
model_hint: sonnet
tags: [gemini, orchestration, claude-desktop]
depends_on: [desktop-mcp-core-fixes]
---

# Write Gemini Orchestration Instructions

## Goal
Rewrite `~/.gemini/GEMINI.md` with comprehensive orchestration instructions so Gemini CLI can autonomously steer Claude Desktop for tasks. Include the new MCP tools (status/stop/read_interim), edge case handling playbook, and CE-style quality enforcement.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain
- **Read-only task** — only writes to `~/.gemini/GEMINI.md`

## Context
Gemini CLI (v0.26.0, Pro tier) runs sync — all tool calls block. It sees claude-desktop MCP tools via `~/.gemini/settings.json`. The orchestration pattern:

```
gemini -p "task prompt" --yolo
  → claude_desktop_new (fresh conversation)
  → claude_desktop_send(message, wait_for_response=true)
  → claude_desktop_read (capture result)
  → handle edge cases via status/stop/read_interim
```

Desktop has 10 MCPs internally: desktop-commander (Windows shell), filesystem, github, sequential-thinking, obsidian, zotero, paper-search, memory, context7, notebooklm-mcp. So Desktop is a full agent — Gemini just needs to steer it, not proxy capabilities.

## What This Task Must Produce

### Updated `~/.gemini/GEMINI.md` with sections:

**1. Tool Inventory** — table of all claude-desktop MCP tools with descriptions, including new status/stop/read_interim

**2. Task Lifecycle** — step-by-step protocol:
- Start: `claude_desktop_new` → `claude_desktop_status` (verify idle)
- Send: `claude_desktop_send` with appropriate timeout
- Monitor: `claude_desktop_status` to check generating state
- Capture: `claude_desktop_read` for final response
- Verify: check response makes sense, isn't truncated

**3. Edge Case Playbook** — concrete instructions for each:
- Compaction: message count drops → new conversation, re-send with context
- Stuck: generating >5min with no progress → stop, retry simplified
- Crashed: connection error → relaunch, wait, retry
- Too long: >10K chars interim → stop, capture, "continue from..."
- Rate limited: back off 60s
- Quality degradation: fresh conversation

**4. Quality Enforcement (CE-style)**:
- After Desktop responds, evaluate: is the response complete? Does it address the task?
- If quality is low, send follow-up: "The response needs improvement because [specific issue]. Please revise."
- For code tasks: ask Desktop to run its own tests/verification
- Checkpoint important intermediate results

**5. Task Sizing Guidance**:
- Simple tasks (<5 min): single send→read cycle
- Medium tasks (5-15 min): send with high timeout, monitor via status
- Complex tasks (>15 min): break into sub-tasks, new conversation per subtask

**6. Desktop Capability Reminder**:
- Desktop has filesystem, shell, github, obsidian, zotero, paper-search, memory, context7, notebooklm MCPs
- Gemini should tell Desktop to USE these tools, not try to do the work itself
- Example: "Use your filesystem tools to read ~/brain/tasks/pending/ and list the files"

## Success Criteria
- [ ] `~/.gemini/GEMINI.md` contains all 6 sections above
- [ ] Instructions are concrete (specific selectors, timeouts, thresholds), not vague
- [ ] Edge case handling references the actual tool names (claude_desktop_status, etc.)
- [ ] Read current GEMINI.md first to preserve any non-Desktop content

## Overnight Agent Instructions
1. Read current `~/.gemini/GEMINI.md` to understand existing content
2. Read `docs/plans/2026-02-05-feat-claude-desktop-compute-leverage-plan.md` for edge case table and architecture
3. Read `server.py` to get exact tool names and parameters (especially new tools after task 061)
4. Write the updated GEMINI.md with all 6 sections
5. Keep it practical — Gemini needs clear, actionable instructions, not theory
6. Verify the file is valid markdown
