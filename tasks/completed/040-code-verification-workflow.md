---
name: code-verification-workflow
bead_id: brain-9ie
priority: 2
estimated_tokens: 12000
mode: autonomous
timeout: 45m
skill: design
model_hint: sonnet
tags: [workflow, learning]
depends_on: []
---

# Code Verification Workflow Design

## Goal
Create systematic approach to verify Claude-generated code that fits user's experimental learning style.

## Environment Constraints
- **Execution env:** WSL2 Claude Code
- **Working dir:** ~/brain
- **Output:** Workflow docs + optional CC hook

## Problem Statement
User runs many unstructured cross-verifications on Claude's code, still lacks confidence. Wants guarantees without losing the experimental/learning aspect.

## Design Requirements

| Requirement | Description |
|-------------|-------------|
| Structured | Repeatable verification steps |
| Educational | User learns while verifying |
| Proportional | Effort matches risk/complexity |
| Documented | Verification results captured |

## Proposed Verification Levels

**Quick (1-2 min):** Syntax check, type check, linter
**Standard (5-10 min):** Unit tests, edge cases, manual review
**Deep (15-30 min):** Integration tests, security scan, code review

## Learning Hooks to Include
- Explain WHY the code works (not just THAT it works)
- Point out patterns worth learning
- Suggest follow-up reading/practice

## Deliverables
- `knowledge/workflows/code-verification.md` - The workflow guide
- `knowledge/patterns/verification-checklist.md` - Reusable checklist
- `.claude/hooks/verification-prompt.md` - Optional CC hook (stretch)

## Success Criteria
- [ ] Workflow documented with clear levels
- [ ] Includes learning/educational component
- [ ] Proportional to code complexity
- [ ] User can adopt incrementally
