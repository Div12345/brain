---
date: 2026-02-05
category: architecture
tags: [compound-engineering, oh-my-claudecode, plugins, hooks, routing, token-optimization]
problem: Multiple competing plugin systems causing routing conflicts, token waste, and no persistent artifacts
---

# CE + OMC Hybrid Architecture

## Problem
Three plugin systems (compound-engineering, oh-my-claudecode, superpowers) with overlapping capabilities. OMC hooks hijacked keywords before CLAUDE.md routing could apply. No persistent file artifacts from OMC execution. 100+ skills with duplicates consuming token budget.

## Root Cause
- OMC's `keyword-detector.mjs` hook runs on UserPromptSubmit and injects "MUST invoke" context that bypasses CLAUDE.md routing rules
- OMC skills (ralph, ultrawork, etc.) are designed for execution power but don't write persistent files
- CE workflows write persistent artifacts (docs/plans/, docs/solutions/) but lack OMC's parallelism
- No single system covered all four loop steps with file persistence

## Solution: CE Loop + OMC Execution Engine

### Architecture
- **CE** handles the workflow loop: brainstorm, plan, review, compound (all produce persistent files)
- **OMC** handles execution only: ralph, ultrawork, ecomode, autopilot (parallel power)
- **Routing rules** in `~/.claude/rules/routing.md` determine which system handles each task type

### Hook Modifications
Removed 4 keyword blocks from `keyword-detector.mjs` (both cache and marketplaces copies):
- `plan this`/`plan the` - now routed via CLAUDE.md to CE or OMC planner
- `research`/`analyze data`/`statistics` - routed to Context7, CE agents, etc.
- `deep analyze`/`investigate`/`debug` - routed by complexity
- Autopilot phrase patterns (`build me`, `create me`, `I want a`) - kept only explicit keyword `autopilot`

**Critical discovery:** OMC hooks execute from `~/.claude/plugins/cache/` not `~/.claude/plugins/marketplaces/`. The `${CLAUDE_PLUGIN_ROOT}` variable resolves to the cache directory. Must patch both copies.

### Token Optimization
- Removed `@` import prefix from omc-reference.md reference in CLAUDE.md - saves 6.4k tokens/session
- `@path` syntax in CLAUDE.md causes auto-loading regardless of surrounding text
- Disabled superpowers plugin (all 14 skills covered by CE+OMC)
- Disabled ralph-loop plugin (strict subset of OMC ralph)

### Plugin Decisions
| Plugin | Status | Reason |
|---|---|---|
| oh-my-claudecode | Enabled | Execution engine, LSP/AST tools, 32 agents |
| compound-engineering | Enabled | Workflow loop with persistent artifacts |
| superpowers | Disabled | All skills covered by CE+OMC |
| ralph-loop | Disabled | Subset of OMC ralph |
| hookify, commit-commands, feature-dev, code-simplifier, claude-md-management, claude-code-setup | Enabled | Unique capabilities, low overhead |

### Continuity Model
Each CE stage writes a file. When you come back, the file is there:
- Stop after brainstorming: `docs/brainstorms/YYYY-MM-DD-*.md`
- Stop after planning: `docs/plans/YYYY-MM-DD-*.md`
- Stop after execution: code committed, plan checkboxes updated
- Stop after compounding: `docs/solutions/YYYY-MM-DD-*.md`

If using OMC for execution: update CE plan file checkboxes before running compound.

## Prevention
- Never use `@path` syntax in CLAUDE.md for reference material - it auto-loads every session
- When editing OMC hooks, always patch the cache copy (`plugins/cache/omc/...`) not just marketplaces
- Run `/context` after configuration changes to verify token budget
- Check routing.md before invoking competing skills - first match wins

## Files Modified
- `~/.claude/CLAUDE.md` - Lean routing, explicit autopilot triggers only
- `~/.claude/rules/routing.md` - Priority tables for each task type
- `~/.claude/rules/compound-loop.md` - CE-first workflow per stage
- `~/.claude/omc-reference.md` - Removed @import self-reference
- `~/.claude/plugins/cache/omc/.../keyword-detector.mjs` - Removed 4 keyword blocks
- `~/.claude/plugins/marketplaces/omc/.../keyword-detector.mjs` - Same edits
- `brain/CLAUDE.md` - Updated to reference docs/ directories
- `brain/docs/{plans,brainstorms,solutions}/` - Created for CE artifacts
- `brain/.claude/skills/compound-capture/` - Deleted (redundant with CE)
- `brain/.claude/skills/learnings-query/` - Deleted (redundant with CE)
