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

### P-2026-01-31-01: arterial_analysis will remain primary focus

**Type:** near-term
**Confidence:** high (18/20 daily notes mention it)
**Based on:** Consistent daily mention pattern, no signs of completion, new data from Taiwan group
**Action:** Surface arterial_analysis context at session start
**Validate by:** Check next 5 daily notes for continued mentions

---

### P-2026-01-31-02: Template sections will remain unfilled

**Type:** behavioral
**Confidence:** high (0% usage over 20 notes)
**Based on:** Wellbeing metrics, habits, gratitude sections never filled
**Action:** Consider simplifying template OR accept this as intentional minimal use
**Validate by:** Check if any future notes fill these sections

---

### P-2026-01-31-03: Late-night work sessions will continue

**Type:** behavioral
**Confidence:** medium (multiple mentions of 7am bedtimes, all-nighters)
**Based on:** "slept at 7am", "worked all night", "3 hours of sleep"
**Action:** Could surface gentle reminder after midnight, but matches user philosophy of not imposing habits
**Validate by:** Check next 10 notes for time-of-day mentions

---

### P-2026-01-31-04: ML methodology questions will persist

**Type:** contextual
**Confidence:** medium
**Based on:** Repeated mentions of stability selection, nested CV, small dataset ML without resolution
**Action:** Surface a methodology decision tree or create a note synthesizing learnings
**Validate by:** Check if methodology mentions decrease after creating synthesis

---

### P-2026-01-31-05: Credit card payment may be forgotten again

**Type:** near-term
**Confidence:** medium (recurring pattern)
**Based on:** Mentioned 3+ times with `!!!` urgency without completion
**Action:** This is sensitive - do not surface unprompted, but if task management discussed, mention pattern
**Validate by:** Check if task appears in future notes still unchecked

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
