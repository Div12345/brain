---
created: 2026-01-31
tags:
  - context
  - predictions
  - anticipation
updated: 2026-01-31T09:55
---

# Predictions

> What the system anticipates you'll need. Tested and refined over time.

## Philosophy

**"Be ready before you're asked."**

The system learns patterns and predicts:
- What information you'll need
- When you'll need it
- What tools would help
- What blockers might arise

## Prediction Types

| Type | Time Horizon | Example |
|------|--------------|---------|
| **Immediate** | Today | "You'll want the lit review notes open" |
| **Near-term** | This week | "Deadline for X approaching - need prep" |
| **Behavioral** | Recurring | "Mondays you usually do admin tasks" |
| **Contextual** | Situational | "After paper reading, you usually write notes" |

## Active Predictions

(Agents update based on pattern analysis)

### Format

```markdown
## P-[ID]: [Short description]

**Type:** immediate | near-term | behavioral | contextual
**Confidence:** high | medium | low
**Based on:** [Evidence]
**Action:** [What to prepare/surface]
**Validate by:** [How to check if prediction was right]
```

---

## Current Predictions

### P-2026-01-31-01: First Overnight Test Needed

**Type:** near-term
**Confidence:** high (90%)
**Based on:** System setup complete, overnight runner created, but never tested on actual hardware
**Action:** Prepare test checklist for overnight runner validation
**Validate by:** User runs overnight-brain.sh or overnight-brain.ps1 successfully

### P-2026-01-31-02: User Questions Will Block Progress

**Type:** immediate
**Confidence:** high (95%)
**Based on:** 5 questions in [[prompts/pending]] without answers
**Action:** Highlight questions Q-01, Q-02, Q-05 as blocking automation setup
**Validate by:** User answers questions in prompts/answered.md

### P-2026-01-31-03: Graph View Testing Needed

**Type:** near-term
**Confidence:** medium (70%)
**Based on:** Obsidian config created, all files have frontmatter, but graph untested
**Action:** User opens brain repo in Obsidian, checks graph view connectivity
**Validate by:** User confirms graph view shows connected nodes

---

## Prediction Validation

After each prediction:
1. Was it useful? (Y/N)
2. Was timing right? (Early/Right/Late)
3. What would have been better?

Record in `experiments/results/` to improve prediction accuracy.

## Patterns to Track

| Pattern | Indicators | Prediction |
|---------|------------|------------|
| Work rhythm | Daily note timestamps, activity | When focused work happens |
| Project attention | Link frequency, mentions | Which project needs focus |
| Task completion | Checkbox patterns | What actually gets done |
| Context switching | Topic jumps in notes | Energy/focus transitions |
| Blockers | Repeated mentions without resolution | What's stuck |

## Meta-Predictions

Predictions about the system itself:

| What | Prediction | Evidence |
|------|------------|----------|
| Tool needs | What capability is missing | Friction patterns |
| Information gaps | What context is missing | Questions asked repeatedly |
| Workflow improvements | What would reduce friction | Time spent on meta-work |

---

*Predictions are hypotheses. Track accuracy, iterate, improve.*
