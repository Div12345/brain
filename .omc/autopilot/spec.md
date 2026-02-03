# Workflow Improvements Specification

## Overview

Three immediate-impact deliverables for PhD researcher workflow optimization.

---

## Deliverable 1: Simplified Daily Note Template

### Problem
Current template has 9 sections, only "Today's Focus" is used. Creates guilt and friction.

### Solution
Minimal 2-section template with optional reflection.

### Template Design

```markdown
---
date: {{date}}
tags: [type/daily]
---

# {{date}}

## What I worked on
- [[project-link]] - brief note
-

## Tomorrow
-

---
<!-- Optional: Expand if needed
## Reflections
-->
```

### Implementation
- File: `99 - Meta/Templates/Daily Note - Minimal.md`
- Update Obsidian daily note settings to use new template
- Old notes remain unchanged (no migration needed)

---

## Deliverable 2: arterial_analysis Completion Checklist

### Problem
4 open questions exist but aren't actionable. User needs clear completion criteria.

### Solution
Convert questions to verifiable checklist items in Command Center.

### Checklist Content

```markdown
## Completion Checklist

### Methodology Validation
- [ ] **In-fold filtering impact**: Run experiment comparing pre-CV vs in-fold filter scores
  - Output: `experiment_results/infold_vs_precv_comparison.csv`
  - Success: Document whether rankings change meaningfully (>10% difference)

- [ ] **Stability analysis**: Compute feature selection stability across CV folds
  - Output: `experiment_results/feature_stability_report.md`
  - Success: Jaccard similarity >0.7 across folds OR documented rationale for instability

- [ ] **Literature gap check**: Verify feature selection approach against Meinshausen 2009, Vabalas 2019
  - Output: Section in `Literature Review - Feature Selection in Low-N High-P.md`
  - Success: Can justify method choice with citations

- [ ] **cfPWV test evaluation**: Run final model on held-out test set (n=76)
  - Output: `experiment_results/cfpwv_test_results.csv`
  - Success: Test R² within 0.1 of CV estimate

### Final Deliverable
- [ ] **Paper/thesis section**: Draft methodology + results section
  - Output: `writing/arterial_methods_draft.md`
  - Success: Advisor-reviewable draft
```

### Implementation
- Add to existing `03 - Projects/arterial analysis/Command Center.md`
- Location: After "Open Questions" section

---

## Deliverable 3: Session Context Surfacing

### Problem
Claude sessions don't automatically know arterial_analysis status.

### Solution
Brain repo context file that surfaces on session start.

### Context File

```markdown
# Current Focus: arterial_analysis

**Status**: 1/5 checklist items complete
**Next action**: Run in-fold filtering experiment
**Blockers**: None

## Quick Links
- [[03 - Projects/arterial analysis/Command Center|Command Center]]
- [[03 - Projects/arterial analysis/Literature Review - Feature Selection in Low-N High-P|Literature Review]]

## Recent Activity
- 2026-02-01: Literature search, Chen 1996 paper added
```

### Implementation
- File: `context/current-focus.md` in brain repo
- Update session-state.md to reference it
- Claude Code CLAUDE.md already points to context/

---

## Implementation Sequence

1. **Daily template** (5 min) - Create template file in Obsidian
2. **Completion checklist** (5 min) - Add section to Command Center
3. **Context surfacing** (5 min) - Create current-focus.md

Total: ~15 minutes to immediate impact.

---

## Success Criteria

| Deliverable | Success Metric |
|-------------|----------------|
| Daily template | User fills 100% of sections (2 sections vs 2/9) |
| Completion checklist | User can identify next action in <10 seconds |
| Context surfacing | Claude session shows status within 30 seconds |
