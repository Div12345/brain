# CC-Scheduler Completion Plan

**Created:** 2026-02-03
**Goal:** Make scheduler trustworthy for async task execution
**Status:** AWAITING APPROVAL

---

## Overview

Four phases to make the scheduler production-ready:

| Phase | What | Effort | Unlocks |
|-------|------|--------|---------|
| **1** | Task Schema + Template | 20 min | Capability-aware tasks |
| **2** | Smart Executor Routing | 25 min | Auto skill/model selection |
| **3** | Validation Script | 15 min | Trust before running |
| **4** | Smoke Test | 10 min | Prove it works end-to-end |

**Total:** ~70 min to fully trustworthy system

---

## Phase 1: Task Schema + Template

### What
- Update `tasks.py` to parse new frontmatter fields
- Create capability-aware task template
- Document all available skills, MCPs, modes

### New Task Schema
```yaml
---
name: task-name
priority: 1-5
timeout: 30m
estimated_tokens: 10000

# Execution routing (NEW)
skill: autopilot | ralph | ultrawork | ecomode | plan | null
model_hint: haiku | sonnet | opus
mode: autonomous | read-only | plan-first

# Capabilities needed (NEW)
mcps_required: [memory, obsidian]
inject_capabilities: true  # Add skills list to prompt

# Metadata
tags: [category]
depends_on: []  # other task names
---
```

### Template Location
`tasks/templates/capability-aware-task.md`

### Validation Criteria
- [ ] `tasks.py` parses all new fields without error
- [ ] Template renders with all capability documentation
- [ ] Sample task loads correctly: `./ccq list`

---

## Phase 2: Smart Executor Routing

### What
- Executor reads `skill` field and prefixes prompt appropriately
- Executor passes `--model` flag based on `model_hint`
- Executor logs which routing was used

### Changes to `executor.py`

```python
def build_command(task: Task) -> list[str]:
    cmd = ["claude", "-p"]

    # Skill routing
    prompt = task.body
    if task.skill and task.skill != "null":
        prompt = f"/oh-my-claudecode:{task.skill} {prompt}"

    cmd.append(prompt)
    cmd.append("--verbose")
    cmd.append("--dangerously-skip-permissions")

    # Model routing
    if task.model_hint == "haiku":
        cmd.extend(["--model", "claude-haiku-3"])
    elif task.model_hint == "opus":
        cmd.extend(["--model", "claude-opus-4"])
    # sonnet is default, no flag needed

    # Tool restrictions
    if task.mode == "read-only":
        cmd.extend(["--allowedTools", "Read,Glob,Grep,WebSearch,WebFetch"])

    return cmd
```

### Validation Criteria
- [ ] `./ccq run --dry` shows correct command with skill prefix
- [ ] Model flag appears for haiku/opus tasks
- [ ] Read-only mode restricts tools correctly

---

## Phase 3: Validation Script

### What
Create `./ccq validate` command that checks:
1. All pending tasks have valid schema
2. Required MCPs are available
3. Skills referenced exist
4. No circular dependencies
5. Estimated tokens fit in budget

### Output Example
```
Validating 3 pending tasks...

✓ task-001-research.md
  - Schema: valid
  - Skill: autopilot (exists)
  - MCPs: memory, obsidian (available)
  - Tokens: 15,000 (fits in 89% weekly budget)

✗ task-002-broken.md
  - Schema: INVALID - missing 'timeout' field
  - Skill: foobar (NOT FOUND)

Summary: 1 valid, 1 invalid
```

### Validation Criteria
- [ ] `./ccq validate` runs without error
- [ ] Catches intentionally broken task file
- [ ] Reports MCP availability correctly

---

## Phase 4: Smoke Test

### What
Run a minimal task end-to-end to prove the system works:

```yaml
---
name: smoke-test-scheduler
priority: 1
timeout: 5m
estimated_tokens: 1000
skill: null
model_hint: haiku
mode: read-only
inject_capabilities: false
---

# Smoke Test

1. Report the current time
2. List files in tasks/pending/
3. Output: "Scheduler smoke test passed at {timestamp}"
```

### Validation Criteria
- [ ] Task completes successfully
- [ ] Output appears in `logs/scheduler/`
- [ ] Entry appears in `history.jsonl`
- [ ] Task moves to `tasks/completed/`

---

## Capability Documentation (for template)

### OMC Skills
| Skill | When to Use | Token Cost |
|-------|-------------|------------|
| `autopilot` | Full autonomous build from idea | High |
| `ralph` | Must complete, persistence | High |
| `ultrawork` | Max parallelism, speed | High |
| `ecomode` | Token-efficient parallel | Medium |
| `plan` | Complex planning needed | Medium |
| `analyze` | Deep investigation | Medium |
| `deepsearch` | Find code patterns | Low |
| `null` | Simple task, no orchestration | Lowest |

### Model Hints
| Hint | Use For | Cost |
|------|---------|------|
| `haiku` | Simple lookups, quick checks | $0.25/M |
| `sonnet` | Standard implementation | $3/M |
| `opus` | Complex reasoning, debugging | $15/M |

### Available MCPs
| MCP | Purpose |
|-----|---------|
| `memory` | Persist learnings across sessions |
| `obsidian` | Access research vault |
| `github` | Repo operations |
| `paper-search` | Academic research |
| `zotero` | Citations |
| `notebooklm-mcp` | Research synthesis |

### Modes
| Mode | Tools Allowed |
|------|---------------|
| `autonomous` | All tools |
| `read-only` | Read, Glob, Grep, WebSearch, WebFetch |
| `plan-first` | All tools, but plan before executing |

---

## Execution Order

```
Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4
(schema)    (routing)   (validate)  (smoke)
   │            │            │          │
   └── can test with ./ccq list        │
                │            │          │
                └── can test with --dry │
                             │          │
                             └── proves trust
```

---

## Approval Checkpoints

### Checkpoint 1: After Phase 1
> "Schema and template ready. Run `./ccq list` to verify parsing works. Approve to continue to routing?"

### Checkpoint 2: After Phase 2
> "Executor routing ready. Run `./ccq run --dry` to see command generation. Approve to continue to validation?"

### Checkpoint 3: After Phase 3
> "Validation script ready. Run `./ccq validate` to check tasks. Approve to run smoke test?"

### Checkpoint 4: After Phase 4
> "Smoke test passed. System is ready. You can now write tasks and trust them to run."

---

## After Completion

You will be able to:
1. Write tasks using the capability-aware template
2. Trust `./ccq validate` to catch errors before running
3. Run `./ccq run` knowing it routes to correct skill/model
4. Check `./ccq logs` to see results
5. Focus on your actual work while scheduler handles execution

---

**READY FOR APPROVAL**

Reply with which phases to proceed with, or approve all.
