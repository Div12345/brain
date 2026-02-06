---
title: Fix scheduler trigger timing and add CE-aware task templates
type: fix
date: 2026-02-05
brainstorm: docs/brainstorms/2026-02-05-scheduler-redesign-brainstorm.md
---

# Fix Scheduler Trigger Timing & CE-Aware Task Templates

## Overview

The cc-scheduler infrastructure is fully functional but hasn't executed any overnight tasks since 2026-02-03 because the Windows Task Scheduler trigger fires at 2:00 AM — inside the "reserved" phase (8PM-8AM) when autonomous execution is blocked. The config phase windows are correct for the user's sleep pattern (~8AM-2PM). The fix is moving the trigger to align with the autonomous window, plus adding CE-aware task prompt templates for richer overnight execution.

## Problem Statement

1. `BrainNightlyRun` fires at 2:00 AM → `ccq` detects "reserved" phase → skips all tasks silently
2. Tasks execute as bare `claude -p` with no self-review or learning capture
3. Stale `BrainRetryRun` one-time task lingering from Feb 3

## Proposed Solution

Five targeted changes, no architectural rework needed.

## Acceptance Criteria

- [x] 1. Move Windows trigger to 8:05 AM
- [x] 2. Update PowerShell morning cutoff to 2:00 PM
- [x] 3. Delete stale BrainRetryRun task
- [x] 4. Create CE-aware task prompt template
- [x] 5. Verify with dry run during autonomous phase
- [ ] 6. Verify with real run (next morning)

## Implementation Steps

### Step 1: Move Windows Task Scheduler trigger (2:00 AM → 8:05 AM)

**What:** Update `BrainNightlyRun` scheduled task start time.

**Command (run from PowerShell on Windows side):**
```powershell
schtasks.exe /change /tn "BrainNightlyRun" /st 08:05
```

**Why 8:05 not 8:00:** 5-minute margin avoids edge cases at the exact phase boundary where `get_current_phase()` transitions from reserved → autonomous.

**Verification:**
```powershell
schtasks.exe /query /tn "BrainNightlyRun" /v /fo LIST | Select-String "Start Time"
# Expected: Start Time: 8:05:00 AM
```

### Step 2: Update PowerShell morning cutoff (8 AM → 2 PM)

**File:** `tools/configs/overnight-brain.ps1` line 22

**Current:**
```powershell
$morningCutoff = (Get-Date).Date.AddHours(8)
```

**Change to:**
```powershell
$morningCutoff = (Get-Date).Date.AddHours(14)
```

**Why:** The morning cutoff prevents scheduling retries past the useful window. Since the autonomous phase ends at 2 PM, retries past 2 PM are pointless. The current 8 AM cutoff was from the old 2 AM trigger assumption.

### Step 3: Delete stale BrainRetryRun task

**Command (PowerShell):**
```powershell
schtasks.exe /delete /tn "BrainRetryRun" /f
```

**Verification:**
```powershell
schtasks.exe /query /tn "BrainRetryRun" 2>&1
# Expected: ERROR - task does not exist
```

### Step 4: Create CE-aware task prompt template

**File:** `tools/cc-scheduler/templates/ce-aware-task.md` (new)

Template that task authors can copy when creating tasks in `tasks/pending/`. Adds a structured suffix to the task body instructing the Claude session to self-review and capture learnings.

**Template content (appended to task body by executor when `ce_aware: true` in frontmatter):**

```markdown
## Post-Execution Protocol

After completing the primary task above:

1. **Self-Review** — Re-read your changes. Check against the acceptance criteria. If anything is wrong, fix it now.
2. **Capture Learnings** — If you solved a non-trivial problem or discovered a gotcha:
   - Write a solution doc to `docs/solutions/YYYY-MM-DD-<topic>.md`
   - Include: category, symptoms, root cause, solution, prevention
3. **Summary** — Write a brief session summary to the log (stdout) covering: what was done, what was learned, what's left.
```

**Executor change:** In `lib/executor.py` `build_prompt()`, if the task has `ce_aware: true` in frontmatter, append the template content after the task body.

**Task parser change:** In `lib/tasks.py`, add `ce_aware: bool = False` to the `Task` dataclass. Parse it from frontmatter.

### Step 5: Verify with dry run

**Command (from WSL):**
```bash
cd ~/brain && python3 tools/cc-scheduler/ccq run --dry
```

**Expected output:** Should show "autonomous" phase (if run between 8AM-2PM) and list runnable tasks with their scores. Currently `tasks/pending/research-ai-coding-assistants-2026.md` is the only pending task.

**If run outside autonomous window:** Use `--force` to override:
```bash
python3 tools/cc-scheduler/ccq run --dry --force
```

### Step 6: Verify real execution (next morning)

After the trigger fires at 8:05 AM on the next day:

1. Check log: `cat logs/$(date +%Y-%m-%d)-overnight.log`
2. Confirm phase shows "autonomous" not "reserved"
3. Confirm task(s) executed (check `tasks/completed/` and `logs/scheduler/`)

## Files Changed

| File | Change |
|------|--------|
| Windows Task Scheduler `BrainNightlyRun` | Start time 2:00 AM → 8:05 AM |
| `tools/configs/overnight-brain.ps1:22` | Morning cutoff 8 → 14 |
| Windows Task Scheduler `BrainRetryRun` | Delete |
| `tools/cc-scheduler/templates/ce-aware-task.md` | New template file |
| `tools/cc-scheduler/lib/tasks.py` | Add `ce_aware` field to Task dataclass |
| `tools/cc-scheduler/lib/executor.py` | Append CE template when `ce_aware: true` |

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| User still awake at 8:05 AM occasionally | Low | Tasks run in background, non-disruptive. `ccq` checks capacity first. |
| CE-aware suffix makes prompts too long | Low | Template is ~150 words. Monitor token usage in first few runs. |
| WSL not running at 8:05 AM | Low | Windows Task Scheduler starts WSL automatically via `wsl.exe` |

## References

- Brainstorm: `docs/brainstorms/2026-02-05-scheduler-redesign-brainstorm.md`
- Scheduler config: `tools/cc-scheduler/config.yaml`
- Phase logic: `tools/cc-scheduler/lib/scheduler.py:23-30`
- Executor: `tools/cc-scheduler/lib/executor.py`
- Task parser: `tools/cc-scheduler/lib/tasks.py`
- PowerShell trigger: `tools/configs/overnight-brain.ps1`
- Bash trigger: `tools/configs/overnight-brain.sh`
