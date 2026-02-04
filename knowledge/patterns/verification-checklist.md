# Code Verification Checklist

Quick reference for verifying Claude-generated code.

## Before Accepting Any Code

- [ ] Read the diff (`git diff` or inline review)
- [ ] Understand what each line does (ask if unclear)
- [ ] Check: Does this match what I asked for?

## Quick Level (1-2 min)

- [ ] File saves without syntax errors
- [ ] Type checker passes (`tsc --noEmit` / `mypy` / `pyright`)
- [ ] Linter passes (`eslint` / `ruff` / `clippy`)
- [ ] No obvious copy-paste errors

## Standard Level (5-10 min)

All of Quick, plus:

- [ ] Existing tests still pass
- [ ] New test added for new behavior
- [ ] Edge cases considered:
  - [ ] Empty/null input
  - [ ] Very large input
  - [ ] Invalid input
  - [ ] Concurrent access (if applicable)
- [ ] Manual execution works as expected
- [ ] Error messages are helpful

## Deep Level (15-30 min)

All of Standard, plus:

- [ ] Integration/E2E tests pass
- [ ] Security review:
  - [ ] No hardcoded secrets
  - [ ] Input validation present
  - [ ] Output encoding correct
  - [ ] Auth checks in place
  - [ ] No SQL/command injection
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] Rollback plan exists

## Red Flags (Always Deep Verify)

- [ ] Modifies auth/permissions
- [ ] Handles user data/PII
- [ ] Uses eval/exec/dynamic code
- [ ] Disables security features
- [ ] Writes to production
- [ ] Complex branching logic
- [ ] Unfamiliar patterns

## Learning Capture

After verification:

```markdown
**What I learned:**
**Pattern to remember:**
**Question to explore:**
```

## Quick Commands Reference

```bash
# TypeScript
tsc --noEmit
npm test

# Python
mypy .
pytest

# Rust
cargo check
cargo test

# General
git diff --stat
git diff [file]
```
