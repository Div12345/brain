---
module: ArterialAnalysis
date: 2026-02-12
problem_type: workflow_issue
component: tooling
symptoms:
  - "Refactoring plan for scientific MATLAB pipeline missed 8 critical implementation details"
  - "3-reviewer CE plan review caught implicit behaviors that would cause silent numerical failures"
  - "Over-engineering suggestions conflicted with explicit user requirements (inspect_subject)"
root_cause: missing_workflow_step
resolution_type: workflow_improvement
severity: high
tags: [scientific-pipeline, refactoring, oracle-testing, ship-of-theseus, plan-review, matlab, implicit-knowledge]
---

# Troubleshooting: Scientific Pipeline Refactoring Plans Miss Implicit Code Behaviors

## Problem
When planning a refactoring of a scientific MATLAB pipeline (567-line monolith → modular functions), the initial plan was structurally sound but missed 8 critical implementation details that lived in the source code as implicit behaviors. A 3-reviewer CE plan review process caught these before execution, preventing silent numerical failures.

## Environment
- Module: arterial_analysis / Stage 01 ensemble averaging
- Language: MATLAB R2025b (run from WSL)
- Affected Component: processData.m (567 lines), two driver scripts (357 + 319 lines)
- Date: 2026-02-12

## Symptoms
- Plan covered architecture, extraction order, and oracle testing but did not document ECG signal negation (`-data(:,2)`)
- Column-to-field mapping from `readxlc2` was assumed but never specified
- AB vs CF save function asymmetry (CF saves rejected subjects, AB doesn't) was invisible in the plan
- Reviewers suggested cutting `inspect_subject` from 8 modes to 1, contradicting user's explicit requirement for full inspectability
- One reviewer said `check_quality.m` violated the plan's own extraction principle ("inline if single-use AND trivial") — the plan author had missed this self-contradiction

## What Didn't Work

**Attempted Solution 1:** Writing a comprehensive plan with code-level issues table, extraction principles, and driver pseudocode
- **Why it failed:** The plan was excellent at documenting what TO DO but missed implicit behaviors in the current code that the executing agent would need to replicate. A plan author reads the code top-down for structure; implementation gaps hide in one-off lines (a minus sign, a column index, a save-condition asymmetry).

**Attempted Solution 2:** Running MATLAB `checkcode` on all files
- **Why it failed:** `checkcode` catches syntax issues (unused vars, deprecated patterns) but not semantic gaps like "this signal is negated before filtering" or "this save function has different behavior for rejected subjects."

## Solution

**Three-phase review process for scientific pipeline refactoring plans:**

1. **External domain review** — someone who understands floating-point tolerance, pipeline phasing, and rollback strategy. This caught: oracle tolerance too tight (1e-10 → 1e-12), Phase 3 doing too much in one step (violating plan's own Principle 4), missing rollback plan, memory footprint concerns.

2. **Multi-perspective CE plan review** — 3 parallel reviewers with different lenses:
   - **DHH-style (minimalism):** Caught over-engineering — `filter_signal.m` wrapping 2 lines, `check_quality.m` wrapping 1 line, inspect_subject over-scoped (but wrong about cutting it — user requirement)
   - **Kieran-style (code quality):** Caught implementation gaps — ECG negation, column mapping, CF save asymmetry, missing fail-flag equivalent, dead zero-to-NaN block, external dependencies. **This was the most valuable review.**
   - **Simplicity reviewer:** Confirmed the minimalism findings, added YAGNI analysis

3. **User arbitration** — User overrode the inspect_subject cut (their explicit requirement), accepted check_quality drop, kept filter_signal.

**8 implementation gaps found and added to plan:**

| Gap | What was missing | Risk if not caught |
|-----|-----------------|-------------------|
| ECG negation | `-data(:,2)` — minus sign in one line | R-peak detection fails catastrophically |
| Column mapping | readxlc2 columns 2-7 → named fields | Wrong signals assigned to wrong processing |
| CF save asymmetry | CF saves even rejected subjects | Oracle fails for ~90 CF subjects |
| Gin bounds handling | No fail-flag equivalent in process_signal | Runtime crash on subjects with no gin |
| Dead zero-to-NaN | Appears active but is dead code | Confusion in diff review |
| Calibration separation safety | Why extract→calibrate reordering is safe | Agent might not trust the separation |
| Master Excel oracle | Oracle only compared .mat files | Metadata drift breaks Phase 2 gating |
| External dependencies | pan_tompkin, natsortfiles, readxlc2 | Path errors crash batch run |

## Why This Works

Scientific pipeline code accumulates implicit behaviors — a minus sign on one line, an asymmetric save condition, a specific column mapping. These are invisible in architectural plans because they're single-line details, not structural decisions. But in scientific computing, a single wrong sign or column swap produces numerically plausible but wrong results.

The 3-reviewer approach works because each lens catches different things:
- **Minimalism** catches over-engineering that adds complexity without value
- **Code quality** catches implementation gaps by actually reading the source line-by-line
- **Simplicity** provides a tiebreaker and YAGNI analysis

The user must arbitrate because reviewers lack domain context about requirements (e.g., inspect_subject was a user requirement, not over-engineering).

## Prevention

1. **Before executing any scientific pipeline refactoring plan, run a code-quality reviewer that reads the source files line-by-line.** Architectural reviewers miss single-line implicit behaviors.

2. **Document all implicit behaviors in a "Implementation Gaps" section.** Specifically look for:
   - Signal negation/inversion
   - Channel/column mappings
   - Asymmetric behavior between similar code paths (AB save vs CF save)
   - External dependencies not in the repo
   - Dead code that looks alive

3. **Always include a rollback plan.** Each extraction = own commit. `git revert HEAD` if oracle fails.

4. **User must arbitrate reviewer conflicts.** Reviewers don't have requirements context. "YAGNI" is wrong when the user explicitly asked for the feature.

5. **Oracle tolerance for MATLAB refactoring: use 1e-12 (not 1e-10).** Floating-point reordering from vectorization introduces differences at 1e-14 to 1e-12. Report actual max deviation. Investigate anything at 1e-8 or above.

6. **Check the plan against its own principles.** The plan said "inline if single-use AND trivial" but proposed `check_quality.m` for a 1-line conditional. Self-contradiction. A reviewer caught it.

## Related Issues
- See also: [arterial-analysis-data-provenance-rebuild](2026-02-12-arterial-analysis-data-provenance-rebuild.md) — same project, earlier session establishing calibration separation and oracle testing pattern
- See also: [bottom-up-system-design-missing-interaction-layer](bottom-up-system-design-missing-interaction-layer-20260212.md) — interaction layer design for the same pipeline
