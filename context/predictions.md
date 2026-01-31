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

(First run will generate these from vault analysis)

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
