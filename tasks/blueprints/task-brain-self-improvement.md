---
name: brain-self-improvement
priority: high
project: brain
estimated_tokens: 100000
mode: autonomous
timeout: 60m
schedule: daily
tags: [brain, improvement, daily]
---

## Task
Analyze brain system, identify improvements, implement safe enhancements.

## Context
- Logs: logs/scheduler/, logs/metrics/
- Context files: context/*.md
- Code: tools/cc-scheduler/

## Acceptance Criteria
- [ ] Analyzed recent execution patterns
- [ ] Identified 1-3 improvement opportunities
- [ ] Implemented at least 1 safe enhancement
- [ ] Logged all changes with reasoning

## Workflow
1. Read recent scheduler logs (logs/scheduler/index.jsonl)
2. Analyze: success rates, token usage, failures
3. Identify bottlenecks or inefficiencies
4. For each improvement:
   - Assess risk (safe = read/log only, moderate = config, risky = code)
   - If safe: implement directly
   - If moderate: implement with detailed logging
   - If risky: write proposal to knowledge/proposals/
5. Update IMPLEMENTATION.md with learnings
6. Log session to logs/brain-improvement/

## Risk Assessment
| Risk Level | Actions Allowed |
|------------|-----------------|
| Safe | Read files, write logs, update docs |
| Moderate | Modify config.yaml, add tasks |
| Risky | Modify Python code - proposal only |

## Error Handling
- If blocked: Write to prompts/pending/
- If timeout: Save progress, mark continuation
