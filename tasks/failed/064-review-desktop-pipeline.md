---
name: review-desktop-pipeline
priority: 6
estimated_tokens: 20000
mode: autonomous
timeout: 20m
skill: null
model_hint: sonnet
backend: desktop
tags: [review, claude-desktop, quality]
depends_on: [scheduler-desktop-backend]
---

# Review Desktop Pipeline Implementation

## Goal
Review all changes made by tasks 060-063 (test suite, MCP fixes, Gemini instructions, scheduler backend). Check for bugs, missing edge cases, security issues, and CE compliance. This is the "Assess" step of the compound loop.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain

## What This Task Must Produce

### Code Review Report at `docs/reviews/2026-02-05-desktop-pipeline-review.md`

Check each component:

**1. MCP Server (`tools/mcps/claude-desktop-mcp/server.py`)**
- HTML escaping is correct and complete
- Stop-button detection is robust (handles edge cases: button appearing/disappearing rapidly, button text changing)
- New tools (status/stop/read_interim) handle errors gracefully
- WebSocket connections are properly closed in all code paths
- No secrets or sensitive data in code

**2. Test Suite (`tools/mcps/claude-desktop-mcp/tests/`)**
- Tests are meaningful (not just smoke tests)
- Fixtures handle Desktop-unavailable correctly
- Integration tests clean up after themselves (don't leave Desktop in broken state)

**3. Gemini Instructions (`~/.gemini/GEMINI.md`)**
- Edge case handling is actionable (specific tools, timeouts, thresholds)
- No hallucinated tool names or parameters
- Task sizing guidance matches actual Desktop behavior

**4. Scheduler Integration (`tools/cc-scheduler/`)**
- Backend routing logic is correct
- Fallback from Desktop→Code works
- Task result capture is reliable
- Config changes are backward-compatible

**5. Cross-cutting concerns:**
- Are there any circular dependencies?
- Does the test suite actually test the NEW code (not just old code)?
- Are all file paths correct for WSL2 environment?
- Are timeouts reasonable?

### Also run:
- `cd ~/brain/tools/mcps/claude-desktop-mcp && .venv/bin/python -m pytest tests/ -v` — all tests pass?
- Check for any Python syntax errors in modified files
- Verify the MCP server starts without errors: `.venv/bin/python server.py` (should start and wait for stdio)

## Success Criteria
- [ ] Review report written to `docs/reviews/`
- [ ] All tests pass
- [ ] No critical issues found (or issues documented with fixes)
- [ ] MCP server starts without import errors

## Overnight Agent Instructions
1. Read the plan: `docs/plans/2026-02-05-feat-claude-desktop-compute-leverage-plan.md`
2. Read all modified files (server.py, tests/, GEMINI.md, scheduler changes)
3. Run tests
4. Check server startup
5. Write detailed review report
6. If critical issues found, fix them directly rather than just reporting
