# CC Scheduler - Implementation Plan

> Smart capacity-aware scheduler with learning capabilities

## Component Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CC SCHEDULER ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐       │
│  │   TRIGGER LAYER  │───▶│  DECISION LAYER  │───▶│ EXECUTION LAYER  │       │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘       │
│         │                        │                        │                  │
│         ▼                        ▼                        ▼                  │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐       │
│  │  Windows Task    │    │  Capacity Check  │    │  omc autopilot   │       │
│  │  Scheduler       │    │  Priority Queue  │    │  or ralph        │       │
│  │  + cron fallback │    │  Cost Estimator  │    │                  │       │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘       │
│                                  │                        │                  │
│                                  ▼                        ▼                  │
│                          ┌──────────────────┐    ┌──────────────────┐       │
│                          │  LEARNING LAYER  │◀───│  LOGGING LAYER   │       │
│                          │  Cost models     │    │  Structured logs │       │
│                          │  Success patterns│    │  brain/logs/     │       │
│                          └──────────────────┘    └──────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. TRIGGER LAYER

| Component | Source | Integration |
|-----------|--------|-------------|
| Windows Task Scheduler | Built-in Windows | PowerShell script triggers WSL |
| Cron (fallback) | Built-in Linux | Direct cron job in WSL |
| Manual trigger | New (ccq CLI) | `ccq run`, `ccq run --all` |
| Event trigger | Future | File watcher, git hook |

**Build:**
```
tools/cc-scheduler/
├── trigger/
│   ├── windows-task.ps1      # Windows → WSL bridge
│   ├── install-schedule.ps1  # Installs Windows Task
│   └── cron-setup.sh         # Alternative cron setup
```

**Code from:** None needed, simple scripts

---

### 2. CAPACITY LAYER

| Component | Source | Integration |
|-----------|--------|-------------|
| Rate limit API | omc `usage-api.ts` | Extract or call directly |
| Credentials reader | omc `usage-api.ts` | `~/.claude/.credentials.json` |
| Token refresh | omc `usage-api.ts` | Auto-refresh expired tokens |
| Cache (30s TTL) | omc `usage-api.ts` | Avoid hammering API |

**Build:**
```
tools/cc-scheduler/
├── lib/
│   └── capacity.py           # Python wrapper around omc pattern
```

**Code from:** omc (`~/.claude/plugins/marketplaces/omc/src/hud/usage-api.ts`)
- Extract ~150 lines: credential reading, API call, token refresh
- Rewrite in Python or call via Node subprocess

**API Endpoint:**
```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer {accessToken}

Response:
{
  "five_hour": {"utilization": 45, "resets_at": "2026-02-03T05:00:00Z"},
  "seven_day": {"utilization": 23, "resets_at": "2026-02-09T00:00:00Z"}
}
```

---

### 3. QUEUE LAYER

| Component | Source | Integration |
|-----------|--------|-------------|
| Task files | brain repo | `brain/tasks/pending/*.md` |
| Priority parsing | New | YAML frontmatter `priority: 1` |
| Cost estimation | New + learning | Estimate from task type + history |
| Dependency graph | New | `depends_on: [task-a, task-b]` |

**Build:**
```
tools/cc-scheduler/
├── lib/
│   ├── tasks.py              # Task parsing, priority sorting
│   └── queue.py              # Queue management, ordering
```

**Task File Format:**
```yaml
---
name: zotero-digest
priority: 1                    # Lower = higher priority
estimated_tokens: 50000        # Optional, learned over time
depends_on: []                 # Task dependencies
deadline: 2026-02-03T08:00:00  # Must complete by (optional)
mode: autonomous               # read-only | plan-first | autonomous
timeout: 30m
tags: [research, weekly]
---

## Task
Summarize papers added to Zotero this week...
```

**Code from:**
- overnight (`yail259/overnight`) - queue patterns
- claude-squad - task isolation concepts

---

### 4. DECISION LAYER

| Component | Source | Integration |
|-----------|--------|-------------|
| Capacity gating | New | Don't start if >90% used |
| Smart ordering | New | Priority + deadline + cost fit |
| Task splitting | Future | Break large tasks into phases |
| Retry logic | ClaudeNightsWatch | Adaptive backoff |

**Build:**
```
tools/cc-scheduler/
├── lib/
│   └── scheduler.py          # Core decision logic
```

**Decision Algorithm:**
```python
def select_next_task(queue, capacity):
    available_tokens = estimate_available_tokens(capacity)

    # Filter: only tasks that fit in remaining capacity
    runnable = [t for t in queue if t.estimated_tokens < available_tokens]

    # Sort: priority first, then deadline, then cost (small first)
    runnable.sort(key=lambda t: (
        t.priority,
        t.deadline or datetime.max,
        t.estimated_tokens
    ))

    # Check dependencies
    for task in runnable:
        if all_dependencies_met(task):
            return task

    return None  # Nothing runnable
```

**Code from:**
- ClaudeNightsWatch - retry/backoff patterns
- claude-code-orchestrator - DAG scheduling concepts

---

### 5. EXECUTION LAYER

| Component | Source | Integration |
|-----------|--------|-------------|
| Claude invocation | omc | `omc autopilot` or `omc ralph` |
| Context injection | brain repo | Inject priorities, rules, agent persona |
| Timeout handling | New | subprocess with timeout |
| Output capture | New | Capture stdout/stderr to log |

**Build:**
```
tools/cc-scheduler/
├── lib/
│   └── executor.py           # Wraps omc/claude execution
```

**Execution Modes:**

| Mode | omc Command | Use Case |
|------|-------------|----------|
| `autonomous` | `omc ralph "task prompt"` | Full autonomous with persistence |
| `parallel` | `omc ultrawork "task prompt"` | Parallel agent execution |
| `simple` | `claude -p "task prompt"` | Direct, no orchestration |

**Code from:**
- omc - Use existing `ralph`, `autopilot`, `ultrawork` modes
- No need to reimplement execution, just call omc

---

### 6. LOGGING LAYER

| Component | Source | Integration |
|-----------|--------|-------------|
| Structured logs | New | `brain/logs/scheduler/*.md` |
| Run index | New | `brain/logs/scheduler/index.jsonl` |
| Metrics tracking | New | Token usage, duration, success |
| Cost tracking | omc/ccusage | Actual token costs |

**Build:**
```
tools/cc-scheduler/
├── lib/
│   └── logging.py            # Structured logging
```

**Log Entry:**
```yaml
---
task: zotero-digest
run_id: run-2026-02-03-001
started: 2026-02-03T00:05:00
ended: 2026-02-03T00:18:00
status: completed
tokens_used: 48230
cost_usd: 0.24
capacity_before: 45%
capacity_after: 52%
---

# Execution Log
...
```

**Code from:**
- brain repo patterns - Obsidian-style markdown
- omc token tracking - `~/.omc/state/token-tracking.jsonl`

---

### 7. LEARNING LAYER

| Component | Source | Integration |
|-----------|--------|-------------|
| Cost model | New | Learn token costs per task type |
| Success patterns | New | What predicts success/failure |
| Adaptive estimates | New | Update estimates from actuals |

**Build:**
```
tools/cc-scheduler/
├── lib/
│   └── learning.py           # Pattern learning
├── data/
│   ├── cost-models.json      # Learned cost estimates
│   └── success-patterns.json # Success predictors
```

**Learning Loop:**
```python
def update_cost_model(task, actual_tokens):
    # Exponential moving average
    model = load_cost_model(task.type)
    model.estimated_tokens = 0.7 * model.estimated_tokens + 0.3 * actual_tokens
    save_cost_model(task.type, model)

def analyze_failure(task, log):
    # Extract failure patterns
    if "rate limit" in log:
        record_pattern("rate_limit", task)
    elif "timeout" in log:
        record_pattern("timeout", task)
    # etc.
```

**Code from:**
- Self-refine pattern concepts
- Voyager skill library pattern (store successful approaches)

---

## Integration Flow

```
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: TRIGGER                                                            │
│ Windows Task Scheduler fires at 00:05 → runs trigger/windows-task.ps1     │
│ PowerShell: wsl -d Ubuntu-24.04 -e /home/div/brain/tools/cc-scheduler/ccq │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: CAPACITY CHECK                                                     │
│ ccq calls lib/capacity.py → reads ~/.claude/.credentials.json             │
│ → calls api.anthropic.com/api/oauth/usage                                  │
│ Returns: {fiveHourPercent: 0, weeklyPercent: 23, resetsAt: ...}           │
│                                                                            │
│ If fiveHourPercent > 90: wait until resets_at, then retry                 │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: QUEUE LOADING                                                      │
│ lib/queue.py scans brain/tasks/pending/*.md                               │
│ Parses YAML frontmatter for priority, deadline, estimated_tokens          │
│ Sorts: priority → deadline → cost                                          │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: TASK SELECTION                                                     │
│ lib/scheduler.py picks best task that:                                     │
│ - Fits in available capacity                                               │
│ - Has all dependencies met                                                 │
│ - Highest priority among candidates                                        │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: EXECUTION                                                          │
│ lib/executor.py:                                                           │
│ 1. Moves task: pending/ → active/                                         │
│ 2. Updates context/active-agents.md                                        │
│ 3. Builds prompt: agent persona + rules + priorities + task               │
│ 4. Calls: omc ralph "prompt" --timeout 30m                                │
│ 5. Captures output                                                         │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: LOGGING                                                            │
│ lib/logging.py:                                                            │
│ 1. Moves task: active/ → completed/ or failed/                            │
│ 2. Writes log: brain/logs/scheduler/2026-02-03-00-05-zotero-digest.md     │
│ 3. Appends to index.jsonl                                                  │
│ 4. Records actual token usage, duration, success                           │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 7: LEARNING                                                           │
│ lib/learning.py:                                                           │
│ 1. Update cost estimate for this task type                                │
│ 2. Analyze failure patterns if failed                                      │
│ 3. Record success predictors if succeeded                                  │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ STEP 8: LOOP                                                               │
│ If more tasks in queue AND capacity available: goto STEP 4                │
│ Else: exit with summary                                                    │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Source Code Mapping

| Component | Lines | Source | Method |
|-----------|-------|--------|--------|
| Capacity API | ~150 | omc `usage-api.ts` | Extract & rewrite Python |
| Token refresh | ~50 | omc `usage-api.ts` | Include in capacity |
| Task parsing | ~80 | New (use python-frontmatter) | Write new |
| Queue ordering | ~60 | New | Write new |
| Decision logic | ~100 | New + ClaudeNightsWatch patterns | Write new |
| Executor wrapper | ~80 | New (calls omc) | Write new |
| Structured logging | ~100 | New (brain patterns) | Write new |
| Learning module | ~150 | New (Voyager concepts) | Write new |
| CLI (ccq) | ~100 | New (argparse/click) | Write new |
| Windows trigger | ~30 | New | Write new |

**Total new code: ~900 lines Python + ~30 lines PowerShell**

---

## Build Order

### Phase 1: Minimal Loop (Today) ✓ COMPLETE
```
[x] capacity.py     - Call omc rate limit API (40 lines)
[x] tasks.py        - Parse task files (110 lines)
[x] executor.py     - Call claude CLI with timeout (130 lines)
[x] logging.py      - Basic structured logs (120 lines)
[x] ccq             - CLI entry point (180 lines)
```
**Completed 2026-02-03** - Total: ~580 lines Python

### Phase 2: Smart Scheduling (This Week)
```
[ ] queue.py        - Priority ordering
[ ] scheduler.py    - Decision logic
[ ] windows-task.ps1 - Windows trigger
```

### Phase 3: Learning (Next Week)
```
[ ] learning.py     - Cost models, patterns
[ ] Metrics dashboard (optional)
```

---

## File Structure

```
brain/
├── tools/
│   └── cc-scheduler/
│       ├── ccq                    # Main executable
│       ├── DESIGN.md              # Architecture (existing)
│       ├── IMPLEMENTATION.md      # This file
│       ├── config.yaml            # Settings
│       ├── lib/
│       │   ├── __init__.py
│       │   ├── capacity.py        # Rate limit API
│       │   ├── tasks.py           # Task file parsing
│       │   ├── queue.py           # Queue management
│       │   ├── scheduler.py       # Decision logic
│       │   ├── executor.py        # omc/claude wrapper
│       │   ├── logging.py         # Structured logs
│       │   └── learning.py        # Pattern learning
│       ├── trigger/
│       │   ├── windows-task.ps1
│       │   ├── install-schedule.ps1
│       │   └── cron-setup.sh
│       └── data/
│           ├── cost-models.json
│           └── success-patterns.json
│
├── tasks/
│   ├── pending/                   # Queue (existing brain structure)
│   ├── active/
│   ├── completed/
│   └── failed/
│
├── logs/
│   └── scheduler/                 # Execution logs
│       ├── index.jsonl
│       └── *.md
│
└── agents/
    ├── overnight.md               # Agent persona (existing)
    └── rules.md                   # Safety rules
```

---

## Dependencies

```
# Python
pyyaml              # Config/frontmatter parsing
python-frontmatter  # Markdown frontmatter
requests            # API calls (for capacity check)
click               # CLI framework

# System
omc                 # Already installed - for ralph/autopilot
tmux                # Optional - for session isolation
```

---

## Next Steps

1. **You approve this plan?**
2. I build Phase 1 (minimal loop)
3. Test with one task
4. Iterate based on what we learn
