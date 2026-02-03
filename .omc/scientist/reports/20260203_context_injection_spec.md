# Context Injection Specification for Scheduled Claude Code Tasks
Generated: 2026-02-03 14:45:00

## Executive Summary

This specification defines MINIMAL context injection mechanisms for scheduled Claude Code tasks to enable task awareness, progress tracking, and metrics capture. Key recommendation: **PreToolUse hook + 9 environment variables** provides guaranteed context injection with 1-6% token overhead. This survives any session abandonment or interruption, requiring zero ongoing user action after one-time hook installation.

## Data Overview

- **Research Source**: `/home/div/brain/knowledge/research/automatic-context-injection-mechanisms.md` (349 lines)
- **Scheduler Source**: `tools/cc-scheduler/ccq` + `lib/executor.py`
- **Hook Mechanisms**: 3 available (SessionStart, PreToolUse, PostToolUse)
- **Current Environment Variables**: 1 (`CLAUDE_CODE_ENTRYPOINT`)
- **Proposed Environment Variables**: 9 (task metadata)

## Key Findings

### Finding 1: PreToolUse Hook Provides Guaranteed Context Injection

PreToolUse hook fires before EVERY tool call (Read, Edit, Write, Bash, Task, etc.), providing guaranteed context injection regardless of model attention or session state.

**Comparison of Hook Mechanisms:**
| Hook | Firing Frequency | Survives Abandonment? | Use Case |
|------|------------------|----------------------|----------|
| SessionStart | Once at session start | Partial (forgotten in long sessions) | Initial context only |
| PreToolUse | Every tool call | ✓ EXCELLENT | Continuous re-injection |
| PostToolUse | Every tool call | N/A | Capture, not injection |

**Metrics:**
| Metric | Value |
|--------|-------|
| Injection guarantee | 100% (fires before every tool) |
| User action required | 0 (automatic after one-time setup) |
| Latency overhead | 50-100ms per tool call |
| Token overhead | 150 tokens per injection (~1-6% of task) |

**Evidence:**
- PreToolUse fires on ALL contextTools: Read, Edit, Write, Bash, Task
- Not subject to model attention (forced injection at tool boundary)
- Re-injects even if task runs for hours or is interrupted mid-execution

### Finding 2: Current Scheduler Has Minimal Context Passing

Scheduler passes only task body as prompt and sets single environment variable.

**Current Mechanism:**
```python
# executor.py line 110, 127
cmd = ["claude", "-p", prompt, "--verbose", "--dangerously-skip-permissions"]
env={**os.environ, "CLAUDE_CODE_ENTRYPOINT": "ccq-scheduler"}
```

**What's Missing:**
- No task metadata (name, priority, deadline, tags)
- No progress tracking capability
- No metrics capture framework
- No checkpoint/resume mechanism

**Metrics:**
| Metric | Current | Proposed |
|--------|---------|----------|
| Environment variables | 1 | 9 |
| Task awareness | Prompt-only (model decides attention) | Guaranteed via hook |
| Progress tracking | None | Stage markers + state updates |
| Metrics capture | Log file only | Structured stage timings |

### Finding 3: MINIMAL Context = 9 Environment Variables + Brief Summary

Sufficient context for task awareness, progress tracking, and metrics requires only 9 environment variables and ~150 token summary.

**Proposed Environment Variables:**
| Variable | Purpose | Example |
|----------|---------|---------|
| `CCQ_TASK_NAME` | Task identification | `"analyze-user-behavior"` |
| `CCQ_TASK_MODE` | Execution mode | `"autonomous"` / `"read-only"` |
| `CCQ_TASK_PRIORITY` | Urgency level | `"high"` / `"medium"` / `"low"` |
| `CCQ_TASK_DEADLINE` | Time constraint | `"2026-02-05T23:59:59Z"` |
| `CCQ_TASK_TAGS` | Task categorization | `"analysis,metrics,weekly"` |
| `CCQ_TASK_TIMEOUT` | Max duration | `"30m"` / `"2h"` |
| `CCQ_TASK_ESTIMATED_TOKENS` | Capacity estimate | `"50000"` |
| `CCQ_SESSION_START` | Start timestamp | `"2026-02-03T14:30:00Z"` |
| `CLAUDE_CODE_ENTRYPOINT` | Scheduler identifier | `"ccq-scheduler"` (existing) |

**Brief Context Injection (saves tokens):**
```
## Scheduled Task Context (Auto-Injected)

**Task:** analyze-user-behavior
**Mode:** autonomous
**Priority:** high
**Deadline:** 2026-02-05T23:59:59Z
**Tags:** analysis,metrics,weekly
**Timeout:** 30m
**Elapsed:** 12m

**What am I doing?** You are executing a scheduled task via cc-scheduler.
**Where am I?** Check tasks/active/analyze-user-behavior.md for full task spec.
**What should I log?** Log key decisions to .omc/logs/scheduler/analyze-user-behavior.log
```

**Token Estimate:** ~150 tokens (vs. full task spec at 500-1000 tokens)

## Specification

### Component 1: Environment Variables (Scheduler → Claude Process)

**Location:** `tools/cc-scheduler/lib/executor.py` line 127

**Implementation:**
```python
env={
    **os.environ,
    "CLAUDE_CODE_ENTRYPOINT": "ccq-scheduler",
    "CCQ_TASK_NAME": task.name,
    "CCQ_TASK_MODE": task.mode,
    "CCQ_TASK_PRIORITY": str(task.priority),
    "CCQ_TASK_DEADLINE": task.deadline.isoformat() if task.deadline else "",
    "CCQ_TASK_TAGS": ",".join(task.tags),
    "CCQ_TASK_TIMEOUT": task.timeout,
    "CCQ_TASK_ESTIMATED_TOKENS": str(task.estimated_tokens),
    "CCQ_SESSION_START": started_at.isoformat(),
}
```

**Effort:** 5 minutes (modify one dict in executor.py)

### Component 2: PreToolUse Hook (Guaranteed Injection)

**Location:** `~/.claude/hooks/PreToolUse.js` (global) or `.claude/hooks/PreToolUse.js` (project)

**Implementation:**
```javascript
export default async function PreToolUse(input) {
  const { tool } = input;

  // Only inject on substantive tools
  const contextTools = ['Read', 'Edit', 'Write', 'Bash', 'Task'];
  if (!contextTools.includes(tool)) {
    return {};
  }

  // Check if running from scheduler
  const entrypoint = process.env.CLAUDE_CODE_ENTRYPOINT;
  if (entrypoint !== 'ccq-scheduler') {
    return {}; // Not a scheduled task
  }

  // Build context from environment
  const taskName = process.env.CCQ_TASK_NAME;
  const taskMode = process.env.CCQ_TASK_MODE;
  const priority = process.env.CCQ_TASK_PRIORITY;
  const deadline = process.env.CCQ_TASK_DEADLINE;
  const tags = process.env.CCQ_TASK_TAGS;
  const timeout = process.env.CCQ_TASK_TIMEOUT;
  const sessionStart = process.env.CCQ_SESSION_START;

  if (!taskName) {
    return {}; // Missing required vars
  }

  // Calculate elapsed time
  const elapsed = Date.now() - new Date(sessionStart).getTime();
  const elapsedMin = Math.floor(elapsed / 60000);

  // Build brief context (save tokens)
  const context = `
## Scheduled Task Context (Auto-Injected)

**Task:** ${taskName}
**Mode:** ${taskMode}
**Priority:** ${priority}
**Deadline:** ${deadline || 'none'}
**Tags:** ${tags || 'none'}
**Timeout:** ${timeout}
**Elapsed:** ${elapsedMin}m

**What am I doing?** You are executing a scheduled task via cc-scheduler.
**Where am I?** Check tasks/active/${taskName}.md for full task spec.
**What should I log?** Log key decisions to .omc/logs/scheduler/${taskName}.log
  `.trim();

  return {
    hookSpecificOutput: {
      additionalContext: context
    }
  };
}
```

**Effort:** 10 minutes (create hook file)

**Benefits:**
- Fires before EVERY tool call → survives any interruption
- Provides task awareness without relying on model attention
- Shows elapsed time → helps agent manage timeout
- Points to full task spec and log location

### Component 3: Stage Markers for Progress Tracking (Optional)

**Purpose:** Enable agents to report structured progress and timing data.

**Agent Usage Pattern:**
```python
print("[STAGE:begin:data_loading]")
# ... perform work ...
print("[STAGE:status:success]")
print("[STAGE:time:12.3]")
print("[STAGE:end:data_loading]")
```

**Marker Types:**
| Marker | Purpose | Example |
|--------|---------|---------|
| `[STAGE:begin:name]` | Start of stage | `[STAGE:begin:exploration]` |
| `[STAGE:end:name]` | End of stage | `[STAGE:end:exploration]` |
| `[STAGE:status:outcome]` | Success/failure | `[STAGE:status:success]` |
| `[STAGE:time:seconds]` | Duration | `[STAGE:time:45.2]` |

**Capture Mechanism:** PostToolUse hook reads stdout, extracts markers, appends to log file.

**Effort:** 15 minutes (add PostToolUse hook for marker extraction)

### Component 4: Task File State Updates (Optional)

**Purpose:** Enable resume from checkpoint on timeout or failure.

**Task Frontmatter Extension:**
```yaml
---
name: analyze-user-behavior
status: active  # pending → active → completed/failed
started_at: 2026-02-03T14:30:00Z
attempts: 1
last_checkpoint: "Completed data loading phase"
progress_percent: 35
stages_completed: ["data_loading", "preprocessing"]
---
```

**Update Mechanism:** PostToolUse hook extracts stage markers, updates task file frontmatter.

**Effort:** 20 minutes (add state update logic to PostToolUse hook)

## Implementation Priority

| Priority | Component | Effort | Impact | Enables |
|----------|-----------|--------|--------|---------|
| **P0** | Environment variables | 5 min | HIGH | All tracking capabilities |
| **P0** | PreToolUse hook (basic) | 10 min | HIGH | Task awareness |
| **P1** | Stage marker capture | 15 min | MEDIUM | Progress tracking |
| **P2** | Task file state updates | 20 min | MEDIUM | Resume from checkpoint |
| **P3** | PostToolUse metrics aggregation | 30 min | LOW | Performance analytics |

**Total for P0 (sufficient for MVP):** 15 minutes

## Token Budget Analysis

**Per Tool Call:**
- Context injection: ~150 tokens
- Hook overhead: ~50-100ms latency

**Per Task:**
- Typical tool calls: 50-200
- Total context tokens: 7,500-30,000 tokens
- Task capacity: 500,000 tokens (typical)
- **Overhead: 1-6%** (acceptable for guaranteed context)

**Comparison:**
| Approach | Token Overhead | Guarantee | Survives Abandonment |
|----------|----------------|-----------|---------------------|
| Prompt-only | 0% | No (model decides attention) | No |
| SessionStart hook | 0.03% (once) | Partial (forgotten) | Partial |
| PreToolUse hook | 1-6% | ✓ YES (every tool) | ✓ YES |
| Full task spec per tool | 10-40% | ✓ YES | ✓ YES (wasteful) |

## Visualizations

### Context Injection Flow
```
Scheduler (ccq)
    ↓ (sets environment variables)
Claude Process
    ↓ (executes task)
PreToolUse Hook
    ↓ (reads env vars, injects context)
Agent (scientist/architect/executor)
    ↓ (aware of task, logs progress)
PostToolUse Hook
    ↓ (captures stage markers)
Task Log + State File
```

### Token Overhead Distribution
```
Task Capacity (500k tokens)
█████████████████████████████████████████████████ Actual work (94-99%)
██ PreToolUse context injection (1-6%)
```

### Hook Firing Frequency
```
Session Timeline:
|---[SessionStart]---|--[Tool]--|--[Tool]--|--[Tool]--|--[Tool]--|
     ↑ Once             ↑ Pre/Post ↑ Pre/Post ↑ Pre/Post ↑ Pre/Post
     Context injected   Re-injected Re-injected Re-injected Re-injected
```

## Limitations

1. **PreToolUse latency overhead**: Each tool call adds ~50-100ms for file read and context formatting
   - **Mitigation**: Acceptable for scheduled tasks (not interactive)
   - **Impact**: 5-20 seconds total overhead for 100-200 tool calls

2. **Token cost**: 1-6% overhead for context injection
   - **Mitigation**: Use brief summary (150 tokens) instead of full task spec (500-1000 tokens)
   - **Impact**: 7,500-30,000 tokens per task (small vs. 500k capacity)

3. **One-time setup required**: Hook installation needed before first use
   - **Mitigation**: Global hook at `~/.claude/hooks/PreToolUse.js` works for all projects
   - **Impact**: 10 minutes one-time setup

4. **Environment variable visibility**: Sensitive task data in process environment
   - **Mitigation**: Scheduled tasks are local, not multi-tenant
   - **Impact**: Low risk for personal use

5. **Stage marker adoption**: Requires agents to use structured markers
   - **Mitigation**: Document in agent system prompts (scientist already uses markers)
   - **Impact**: Gradual adoption, works with existing agents

## Recommendations

### For Immediate Implementation (P0 - 15 minutes)

1. **Add environment variables to executor.py** (5 minutes)
   - Modify `env` dict at line 127
   - Pass all 9 task metadata variables

2. **Create PreToolUse hook** (10 minutes)
   - Location: `~/.claude/hooks/PreToolUse.js`
   - Inject brief context on contextTools
   - Gate on `CLAUDE_CODE_ENTRYPOINT=ccq-scheduler`

### For Enhanced Tracking (P1 - 15 additional minutes)

3. **Create PostToolUse hook for stage markers** (15 minutes)
   - Extract `[STAGE:*]` markers from stdout
   - Append to `.omc/logs/scheduler/{task-name}.log`
   - Enable progress tracking and timing analysis

### For Resume Capability (P2 - 20 additional minutes)

4. **Add task file state updates** (20 minutes)
   - Update frontmatter with progress data
   - Enable resume from last checkpoint on timeout

### Testing Plan

1. **Verify environment variables are passed:**
   ```bash
   # Add to test task body:
   echo "Task: $CCQ_TASK_NAME, Priority: $CCQ_TASK_PRIORITY"
   ```

2. **Verify hook injection:**
   - Create simple read-only task
   - Check that context appears in Claude output
   - Verify context includes task name, mode, elapsed time

3. **Measure overhead:**
   - Run task with and without hook
   - Compare execution times (expect +5-20 seconds for 100-200 tools)
   - Compare token usage (expect +1-6%)

4. **Test abandonment recovery:**
   - Start task, kill process mid-execution
   - Restart task
   - Verify context re-injected on first tool call

## Next Actions

1. **Implement P0 components** (15 minutes total)
   - Modify `tools/cc-scheduler/lib/executor.py` to add environment variables
   - Create `~/.claude/hooks/PreToolUse.js` with basic context injection

2. **Test with simple task** (5 minutes)
   - Create test task: "List all Python files in knowledge/ and report count"
   - Run via `ccq run`
   - Verify context injection appears in output

3. **Measure performance impact** (10 minutes)
   - Compare execution time and token usage with/without hook
   - Verify overhead is within acceptable range (1-6%)

4. **Document for agent system prompts** (10 minutes)
   - Add to scientist/architect/executor agent instructions
   - Recommend using stage markers for progress reporting

---

*Generated by Scientist Agent (oh-my-claudecode)*
*Analysis based on 349 lines of context injection research and scheduler implementation review*
