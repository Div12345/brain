---
name: experiment-execution
priority: medium
project: brain
estimated_tokens: 120000
mode: autonomous
timeout: 90m
schedule: daily
tags: [experiments, research, daily]
---

## Task
Run hypothesis-driven experiments on brain system capabilities.

## Context
- Ideas: knowledge/experiments/ideas.md
- Results: knowledge/experiments/results/
- Tools: All available MCPs, CLI tools

## Acceptance Criteria
- [ ] Selected experiment from backlog
- [ ] Defined clear hypothesis
- [ ] Executed with measurements
- [ ] Documented results (confirm/reject)

## Workflow
1. Read experiment backlog (knowledge/experiments/ideas.md)
2. Select highest priority experiment not yet run
3. Define:
   - Hypothesis: "If X, then Y"
   - Method: Steps to test
   - Metrics: How to measure success
4. Execute experiment with careful logging
5. Record results to knowledge/experiments/results/YYYY-MM-DD-{name}.md
6. Update ideas.md (mark done, add follow-ups)

## Result Template
```markdown
# Experiment: {name}
Date: YYYY-MM-DD
Hypothesis: {hypothesis}
Method: {steps taken}
Results: {measurements}
Conclusion: CONFIRMED / REJECTED / INCONCLUSIVE
Follow-ups: {next experiments}
```

## Error Handling
- If experiment fails: Document failure mode, still counts as result
- If no experiments in backlog: Create 2-3 new experiment ideas based on recent work
