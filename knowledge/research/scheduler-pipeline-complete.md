# CC-Scheduler Pipeline: Complete Tooling Map

**Created:** 2026-02-03
**Purpose:** Map every stage to available tools, skills, MCPs, repos

---

## CRITICAL: Related Research Documents

| Document | Lines | Content |
|----------|-------|---------|
| `knowledge/analysis/scheduler-patterns-research.md` | 934 | Full patterns from 4 repos |
| `knowledge/analysis/scheduler-code-templates.md` | 908 | Ready-to-use TypeScript/Bash |
| `knowledge/research/scheduler-system-design-2026-02-02.md` | 134 | Original design doc |
| `knowledge/research/automatic-context-injection-mechanisms.md` | 349 | Hook/injection research |
| `knowledge/research/scheduler-observability-spec.md` | ~100 | 6-field metrics spec |
| `knowledge/research/scheduler-prime-principles.md` | ~80 | Core principles |

**READ THESE BEFORE IMPLEMENTING.**

---

## Available Stack

### MCP Servers
| MCP | Purpose | Key Tools |
|-----|---------|-----------|
| **memory** | Persist learnings | `aim_memory_store`, `aim_memory_search`, `aim_memory_link` |
| **obsidian** | Research vault | `obsidian_global_search`, `obsidian_read_note`, `obsidian_manage_tags` |
| **notebooklm-mcp** | Research synthesis | `notebook_query`, `research_start`, `studio_create` |
| **paper-search** | Academic research | `search_papers`, `search_arxiv`, `download_paper` |
| **zotero** | Citation management | `zotero_search_items`, `zotero_semantic_search` |
| **claude-desktop** | Desktop coordination | `claude_desktop_send`, `claude_desktop_read` |

### Plugin Tools (oh-my-claudecode)
| Tool | Purpose |
|------|---------|
| `lsp_diagnostics` | Code errors/warnings |
| `lsp_diagnostics_directory` | Project-wide type checking |
| `lsp_find_references` | Symbol usage tracking |
| `ast_grep_search` | Structural code patterns |
| `ast_grep_replace` | Structural transforms |
| `python_repl` | Data analysis, custom metrics |

### Skills (Relevant to Scheduler)
| Skill | When to Use |
|-------|-------------|
| `brain-system` | Working in brain repo |
| `autopilot` | Full autonomous task execution |
| `ralph` | Must-complete persistence |
| `plan` | Complex task planning |
| `analyze` | Deep investigation |
| `tdd` | Test-first development |
| `code-review` | Quality verification |

### Reference Repos
| Repo | Patterns to Adopt |
|------|-------------------|
| **claude-code-scheduler** | JSONL history, cron, execution tracking |
| **ClaudeNightsWatch** | hooks.json, activity logging |
| **claude-flow** | Pre/Post hooks, $TOOL_SUCCESS vars |
| **claude-squad** | State machine, tmux isolation |

---

## Pipeline Stages (Complete)

### Stage 1: Task Authoring

| Aspect | Detail |
|--------|--------|
| **What** | Human/agent writes task specification |
| **Inputs** | Objective, context, constraints |
| **Outputs** | `tasks/pending/*.md` with YAML frontmatter |
| **Concerns** | Clarity, self-containment, success criteria, appropriate scope |
| **Skills** | `plan` (for complex tasks), `brain-system` (for repo tasks) |
| **MCPs** | `obsidian` (research context), `memory` (past learnings) |
| **Tools** | Templates, beads (bd) for structure |
| **Repos** | claude-code-scheduler task format |
| **Status** | ❓ Need template |
| **Why Needed** | Garbage in → garbage out. Task quality determines success rate |

### Stage 2: Task Queueing

| Aspect | Detail |
|--------|--------|
| **What** | Scheduler selects next task by priority/dependencies |
| **Inputs** | All pending tasks, priorities, budget, dependencies |
| **Outputs** | Selected task for execution |
| **Concerns** | Priority scoring accuracy, dependency resolution, fairness |
| **Skills** | N/A (automated) |
| **MCPs** | N/A |
| **Tools** | `scheduler.py`, `task_queue.py` |
| **Repos** | claude-code-scheduler priority logic |
| **Status** | ✅ Exists |
| **Why Needed** | Without prioritization, wrong tasks run first |

### Stage 3: Capacity Check

| Aspect | Detail |
|--------|--------|
| **What** | Verify API rate limits allow execution |
| **Inputs** | OAuth API endpoint |
| **Outputs** | Go/no-go decision, wait time if blocked |
| **Concerns** | Accurate rate limit reading, budget allocation |
| **Skills** | N/A (automated) |
| **MCPs** | N/A |
| **Tools** | `capacity.py`, `budget.py` |
| **Repos** | ClaudeNightsWatch usage monitoring |
| **Status** | ✅ Exists |
| **Why Needed** | Prevents wasted runs that hit rate limits |

### Stage 4: Context Injection

| Aspect | Detail |
|--------|--------|
| **What** | Pass task metadata to Claude session |
| **Inputs** | Task ID, file path, run ID, budget info |
| **Outputs** | Env vars available in session, hook context |
| **Concerns** | Task awareness, where to log, what's the goal |
| **Skills** | `brain-system` (has context protocol) |
| **MCPs** | `memory` (inject past learnings) |
| **Tools** | Hooks (SessionStart, PreToolUse), env vars |
| **Repos** | claude-flow hooks, ClaudeNightsWatch hooks.json |
| **Status** | 📋 Researched, not implemented |
| **Why Needed** | Without context, Claude doesn't know it's a scheduled task |

**Env vars to pass:**
```
CCQ_TASK_ID, CCQ_RUN_ID, CCQ_LOG_FILE, CCQ_TASK_FILE, CCQ_BUDGET_REMAINING
```

### Stage 5: Execution

| Aspect | Detail |
|--------|--------|
| **What** | Claude runs the task via CLI |
| **Inputs** | Prompt, allowed tools, timeout |
| **Outputs** | Output stream, exit code |
| **Concerns** | Timeouts, error handling, tool permissions |
| **Skills** | `autopilot` (for complex), `ralph` (must-complete) |
| **MCPs** | All available to the task |
| **Tools** | `executor.py`, claude CLI |
| **Repos** | claude-squad subprocess handling |
| **Status** | ✅ Exists |
| **Why Needed** | Core execution engine |

### Stage 6: Debug Output (Live)

| Aspect | Detail |
|--------|--------|
| **What** | Stream output to terminal during execution |
| **Inputs** | Stdout from subprocess |
| **Outputs** | Terminal display |
| **Concerns** | Is it stuck? Progress visibility |
| **Skills** | N/A |
| **MCPs** | N/A |
| **Tools** | Non-blocking I/O, Popen streaming |
| **Repos** | claude-squad real-time output |
| **Status** | ✅ Exists |
| **Why Needed** | Human can see progress, abort if stuck |

### Stage 7: Output Capture

| Aspect | Detail |
|--------|--------|
| **What** | Save full session log to file |
| **Inputs** | All stdout/stderr |
| **Outputs** | `logs/scheduler/YYYY-MM-DD-HHMM-task.md` |
| **Concerns** | Truncation for huge outputs, file organization |
| **Skills** | N/A |
| **MCPs** | N/A |
| **Tools** | `log_utils.py` |
| **Repos** | claude-code-scheduler log rotation |
| **Status** | ✅ Exists |
| **Why Needed** | Full audit trail, debugging failures |

### Stage 8: Metrics Logging

| Aspect | Detail |
|--------|--------|
| **What** | Record execution metrics for feedback loop |
| **Inputs** | Result: success, duration, tokens, errors |
| **Outputs** | `logs/scheduler/history.jsonl` |
| **Concerns** | 6 fields minimum, append-only, queryable |
| **Skills** | N/A (automated) |
| **MCPs** | `memory` (store patterns found) |
| **Tools** | `log_utils.py`, JSON |
| **Repos** | **claude-code-scheduler JSONL pattern** |
| **Status** | 🔧 Implementing |
| **Why Needed** | **Enables stages 10-12. No data = no learning** |

**Schema:**
```jsonl
{"task_id":"X","success":true,"error_type":null,"tokens":12000,"duration_s":45,"log_file":"...","timestamp":"..."}
```

### Stage 9: Task Transition

| Aspect | Detail |
|--------|--------|
| **What** | Move task file to final state directory |
| **Inputs** | Exit code, task file |
| **Outputs** | Task in `completed/` or `failed/` |
| **Concerns** | Atomic move, state consistency |
| **Skills** | N/A |
| **MCPs** | N/A |
| **Tools** | `executor.py` shutil.move |
| **Repos** | Standard pattern |
| **Status** | ✅ Exists |
| **Why Needed** | Clean state management, prevents re-running |

### Stage 10: Review Gate

| Aspect | Detail |
|--------|--------|
| **What** | Human reviews outputs, approves/rejects |
| **Inputs** | Logs, metrics, diffs |
| **Outputs** | Approval/rejection, feedback |
| **Concerns** | When to trigger, notification method, what to check |
| **Skills** | `code-review`, `analyze` |
| **MCPs** | `claude-desktop` (notify), `obsidian` (log review) |
| **Tools** | Scheduled review sessions, PR-style approval |
| **Repos** | N/A - custom design needed |
| **Status** | ❓ Not designed |
| **Why Needed** | Human-in-the-loop prevents drift, catches errors |

**Design options:**
- Daily review of all completed tasks
- Threshold-based (review if >N tokens or failure)
- PR-style for code changes

### Stage 11: Feedback Analysis

| Aspect | Detail |
|--------|--------|
| **What** | Analyze metrics to find patterns |
| **Inputs** | `history.jsonl` |
| **Outputs** | Insights: failure patterns, token trends, success rates |
| **Concerns** | What queries to run, statistical significance |
| **Skills** | `research`, `analyze` |
| **MCPs** | `python_repl` (computation), `memory` (store insights) |
| **Tools** | jq queries, Python analysis |
| **Repos** | claude-code-scheduler `getExecutionStats()` |
| **Status** | ❓ Not designed |
| **Why Needed** | Turns data into actionable insights |

**Queries to support:**
- Success rate by task type
- Token efficiency over time
- Common error categories
- Duration trends

### Stage 12: Self-Adjustment

| Aspect | Detail |
|--------|--------|
| **What** | System improves based on analysis |
| **Inputs** | Patterns, learnings |
| **Outputs** | Updated prompts, routing rules, timeouts |
| **Concerns** | What to adjust automatically, safety limits |
| **Skills** | `learner` (extract skills from sessions) |
| **MCPs** | `memory` (persist adjustments) |
| **Tools** | Configuration updates, prompt mutation |
| **Repos** | Gödel Agent pattern (from your research) |
| **Status** | ❓ Future |
| **Why Needed** | Closes the loop - system gets better over time |

**Safe adjustments:**
- Increase timeout for slow tasks
- Route simple tasks to haiku
- Add common error checks to prompts

**Unsafe (require human approval):**
- Change success criteria
- Modify core prompts
- Add new tool permissions

---

## Implementation Priority

| Priority | Stage | Effort | Unlocks |
|----------|-------|--------|---------|
| **P0** | #8 Metrics Logging | 15 min | Stages 10, 11, 12 |
| **P1** | #4 Context Injection | 10 min | Task awareness |
| **P2** | #1 Task Template | 30 min | Better task quality |
| **P3** | #11 Feedback Analysis | 30 min | Actionable insights |
| **P4** | #10 Review Gate | 1 hr | Human oversight |
| **P5** | #12 Self-Adjustment | 2 hr | Closed loop |

---

## Stack Necessity Summary

| Component | Necessary For | Skip If... |
|-----------|---------------|------------|
| **JSONL history** | Feedback loop | You don't want learning |
| **Env vars** | Context injection | Tasks don't need awareness |
| **Hooks** | Live status, injection | Basic logging sufficient |
| **Memory MCP** | Persist learnings | File-based enough |
| **python_repl** | Custom analysis | jq queries sufficient |
| **Review gates** | Human oversight | Full autonomy acceptable |

---

*This document maps the complete scheduler pipeline with all available tooling.*
