---
created: 2026-02-01
tags:
  - task
  - workflow
  - verification
  - status/pending
priority: medium
requires:
  - claude-code
preferred_interface: claude-code
timeout: 45m
---

# Task: Design Structured Code Verification Workflow

Create a systematic approach to verify Claude-generated code that fits user's experimental learning style.

## Problem

User runs many unstructured cross-verifications on Claude's code, still lacks confidence. Wants guarantees without losing the experimental/learning aspect.

## Design Goals

1. **Structured** - Repeatable verification steps
2. **Educational** - User learns while verifying
3. **Proportional** - Effort matches risk/complexity
4. **Documented** - Verification results are captured

## Proposed Components

### 1. Verification Levels
- **Quick** (1-2 min): Syntax check, type check, linter
- **Standard** (5-10 min): Unit tests, edge cases, manual review
- **Deep** (15-30 min): Integration tests, security scan, code review

### 2. Learning Hooks
- Explain WHY the code works (not just THAT it works)
- Point out patterns worth learning
- Suggest follow-up reading/practice

### 3. Confidence Markers
- Test coverage %
- Static analysis results
- Manual review checklist completion

## Deliverables

1. `knowledge/workflows/code-verification.md` - The workflow guide
2. `.claude/hooks/verification-prompt.md` - Optional CC hook for auto-verification
3. `knowledge/patterns/verification-checklist.md` - Reusable checklist

## Acceptance Criteria

- [ ] Workflow documented with clear levels
- [ ] Includes learning/educational component
- [ ] Proportional to code complexity
- [ ] User can adopt incrementally

## Related

- [[prompts/answered#A-2026-02-01-03]]
