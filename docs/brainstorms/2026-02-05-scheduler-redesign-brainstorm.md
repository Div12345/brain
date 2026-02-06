# Scheduler Redesign Brainstorm

**Date:** 2026-02-05
**Status:** Complete
**Next:** `/workflows:plan` when ready to implement

## What We're Building

Fix the cc-scheduler so overnight autonomous tasks actually execute, and embed CE-style workflow patterns (execute, review, compound) into task execution.

## Current State

### What works
- Full `ccq` CLI with smart scheduling, capacity checking, budget tracking
- Windows Task Scheduler (`BrainNightlyRun`) fires daily at 2:00 AM
- PowerShell → WSL → bash → `ccq run --all` pipeline is functional
- Capacity API check works (reports 5h and 7d usage correctly)
- Bounce-back retry mechanism exists (PowerShell schedules Windows retry on rate limit)
- Task file parser, multi-project queue, structured logging all work
- 4 tasks completed successfully on 2026-02-03 (manual trigger during autonomous phase)

### What's broken
- **Schedule window mismatch:** Config has `reserved` phase 8PM-8AM, trigger fires at 2AM → tasks silently skip every night
- **No CE workflow integration:** Each task is a single `claude -p` invocation with no built-in review or learning capture
- **Stale retry task:** `BrainRetryRun` from 2/3 still exists in Windows Task Scheduler (harmless but messy)

## Key Decisions

### 1. Fix trigger time to match schedule windows

User sleeps ~8AM-2PM. The existing config phase windows are actually correct:

| Phase | Window | Budget | Purpose |
|-------|--------|--------|---------|
| Autonomous | 08:00-14:00 | 80% | Heavy lifting while user sleeps |
| Briefing | 14:00-15:00 | 8% | Review results when user wakes |
| Buffer | 15:00-20:00 | 12% | Light tasks, user may be active |
| Reserved | 20:00-08:00 | 0% | User's active hours, no autonomous |

**The problem is the trigger, not the config.** Windows Task Scheduler fires at 2:00 AM, which is smack in the middle of the reserved phase (user is active at 2 AM). Tasks get silently skipped.

**Fix:** Move the Windows trigger from 2:00 AM → 8:00 AM (or 8:15 AM for margin) to align with autonomous phase start.

### 2. CE integration: Single smart task (recommended)

Rather than building a pipeline system, embed CE-style instructions into task prompts:

```
Task prompt structure:
1. Execute the work described below
2. Self-review: check your work against the acceptance criteria
3. Capture learnings: if you solved a non-trivial problem, write a solution doc to docs/solutions/
```

**Why this over chained stages:**
- No context loss between stages (same session)
- No pipeline infrastructure to build (YAGNI)
- Token usage is bounded by the single session
- Can split into separate stages later if sessions prove too token-heavy
- The `skill` field already supports prefixing prompts with OMC skills

**Fallback path:** If single-session token usage is too high, use `depends_on` chains:
```yaml
# Stage 1: Execute
name: feature-x-execute
depends_on: []

# Stage 2: Review
name: feature-x-review
depends_on: [feature-x-execute]
# Prompt: "Review the output in logs/scheduler/YYYY-MM-DD-*-feature-x-execute.md"

# Stage 3: Compound
name: feature-x-compound
depends_on: [feature-x-review]
# Prompt: "Capture learnings from logs/scheduler/..."
```

### 3. Clean up stale Windows tasks

Remove the orphaned `BrainRetryRun` task from 2/3.

## Open Questions

1. **Trigger time:** Move to 8:00 AM or 8:15 AM? (Small margin avoids edge cases at phase boundary)
2. **Task prompt template:** Should we create a standard "CE-aware" task template that includes the self-review and compound steps, or leave it per-task?
3. **Morning cutoff in PowerShell:** Currently set to 8 AM for retry scheduling — should move to 14:00 (2 PM) to match autonomous phase end

## Approach Summary

**Minimal changes, maximum impact:**
1. Move Windows Task Scheduler trigger from 2:00 AM → 8:00 AM (config windows are already correct)
2. Update PowerShell morning cutoff from 8 AM → 2 PM (match autonomous phase end)
3. Clean up stale `BrainRetryRun` task
4. Create a CE-aware task prompt template (optional, for future tasks)
5. Test with `ccq run --dry` to verify phase detection works at new trigger time
