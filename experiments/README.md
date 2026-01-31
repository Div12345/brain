# Experiments Framework

> Scientific rigor for system evolution. Every change is a hypothesis to test.

## Philosophy

**"Strong opinions, weakly held"** - Make predictions, test them, update beliefs.

## Experiment Lifecycle

```
1. OBSERVE   → Notice a pattern or gap
2. QUESTION  → What would improve this?
3. HYPOTHESIZE → "If X, then Y"
4. DESIGN    → Minimal test that could falsify hypothesis
5. IMPLEMENT → Build the test (sandboxed)
6. MEASURE   → Collect data
7. ANALYZE   → Did it work? Why/why not?
8. LEARN     → Update system knowledge
9. ITERATE   → Next experiment or ship it
```

## Experiment Types

| Type | Purpose | Example |
|------|---------|---------|
| **Tool** | Test if new tool solves problem | "MCP for X reduces friction by Y%" |
| **Workflow** | Test if process change helps | "Morning summary increases task completion" |
| **Prediction** | Test if we can anticipate needs | "User will need X within 3 days" |
| **Integration** | Test if systems work together | "Hookify + Obsidian sync without conflict" |

## Active Experiments

(Agents add experiments here)

| ID | Hypothesis | Status | Started |
|----|------------|--------|---------|
| - | - | - | - |

## Experiment Template

Create files in `experiments/active/` using:

```markdown
---
id: exp-YYYY-MM-DD-NN
type: tool|workflow|prediction|integration
status: designing|running|analyzing|complete
started: YYYY-MM-DD
hypothesis: "If X, then Y"
success_criteria: "Measurable outcome"
---

# Experiment: [Name]

## Background
Why we're running this experiment.

## Hypothesis
If [intervention], then [expected outcome].

## Method
1. Step 1
2. Step 2
3. ...

## Success Criteria
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)

## Data Collection
What we're measuring and how.

## Results
(Fill after experiment)

## Analysis
(Fill after experiment)

## Decision
Ship / Iterate / Abandon

## Learnings
What this teaches us for future experiments.
```

## Metrics to Track

| Metric | Why |
|--------|-----|
| Task completion rate | Are outputs actually used? |
| Time to insight | How fast does value emerge? |
| Friction events | What causes slowdowns? |
| Prediction accuracy | Are we anticipating correctly? |
| Tool adoption | Are built tools actually used? |
| Token efficiency | Are we optimizing API usage? |

## Experiment Results Archive

Completed experiments go in `experiments/results/` with format:
`exp-YYYY-MM-DD-NN-[outcome].md`

Outcomes: `success`, `partial`, `failed`, `abandoned`

---

*Every system change should be traceable to an experiment or explicit decision.*
