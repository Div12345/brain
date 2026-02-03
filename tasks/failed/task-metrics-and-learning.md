---
name: metrics-and-learning
priority: medium
project: brain
estimated_tokens: 40000
mode: autonomous
timeout: 30m
schedule: daily
tags: [metrics, learning, daily]
---

## Task
Aggregate metrics, update cost models, generate insights.

## Context
- Logs: logs/scheduler/index.jsonl
- Budget: .omc/state/weekly-budget.json
- Models: .omc/state/cost-models.json

## Acceptance Criteria
- [ ] Daily metrics computed
- [ ] Cost models updated with actuals
- [ ] Anomalies flagged
- [ ] Weekly summary (if Sunday)

## Workflow
1. Parse scheduler logs for today
2. Compute:
   - Tasks: attempted/completed/failed
   - Tokens: estimated vs actual
   - Success rate by task type
3. Update cost-models.json (EMA: 0.7*old + 0.3*actual)
4. Flag anomalies (>20% variance from estimates)
5. Write to logs/metrics/YYYY-MM-DD.md
6. If Sunday: generate weekly summary

## Metrics Template
```markdown
# Daily Metrics: YYYY-MM-DD

## Execution
- Tasks attempted: N
- Tasks completed: N
- Tasks failed: N
- Success rate: X%

## Tokens
- Estimated: N
- Actual: N
- Variance: X%

## Anomalies
- {list any tasks with >20% variance}

## Learnings
- {patterns observed}
```

## Error Handling
- If no logs for today: Report "no activity" and exit
- If cost-models.json missing: Initialize with defaults
