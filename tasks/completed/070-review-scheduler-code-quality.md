---
name: review-scheduler-code-quality
priority: 3
estimated_tokens: 30000
mode: autonomous
timeout: 25m
backend: desktop
model_hint: sonnet
tags: [review, scheduler, quality]
depends_on: []
ce_aware: true
---

# Review cc-scheduler Code Quality

## Goal
Perform a thorough code review of the cc-scheduler codebase at ~/brain/tools/cc-scheduler/. Focus on correctness, edge cases, and maintainability.

## Files to Review
- `lib/tasks.py` — Task schema parsing and validation
- `lib/executor.py` — Task execution engine with Desktop backend
- `ccq` — CLI entry point
- `config.yaml` — Configuration
- `tests/test_tasks.py` and `tests/test_executor.py` — Test coverage

## What to Check
1. **Error handling** — Are all failure modes handled? Can the scheduler crash unexpectedly?
2. **Edge cases** — What happens with malformed YAML? Empty files? Missing directories?
3. **Test coverage** — Are there gaps? What scenarios are untested?
4. **Configuration** — Is config.yaml being loaded correctly everywhere?
5. **Security** — Any command injection risks in subprocess calls?

## Output
Write a review summary with:
- Critical issues (must fix)
- Suggested improvements (nice to have)
- Test gap analysis
- Overall quality assessment (1-5)
