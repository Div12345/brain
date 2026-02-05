---
name: compound-capture
description: Capture solved problems as compounding knowledge. Use after resolving bugs, completing features, or solving technical problems. Auto-invocable on phrases like "that worked", "it's fixed", "problem solved", "got it working".
allowed_tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash(git:*)
  - mcp__obsidian__obsidian_update_note
  - mcp__memory__aim_memory_store
  - mcp__memory__aim_memory_add_facts
  - mcp__memory__aim_memory_link
---

# Compound Capture

## Purpose
After solving a problem, capture the knowledge so future agents never re-solve it from scratch. This is the "Compound" step in the compound engineering loop.

## When to Invoke
- After a bug is fixed
- After a feature is completed
- After a technical problem is resolved
- After a non-obvious configuration is figured out
- When the user says "that worked", "fixed it", "got it working", "problem solved"
- Manually via `/compound-capture`

## Process

### Step 1: Extract (from conversation context)
Identify these elements from the current session:

| Element | Description |
|---------|-------------|
| **Problem** | What was broken or needed? Error messages, symptoms. |
| **Investigation** | What was tried? What didn't work and why? |
| **Root Cause** | The actual underlying issue. |
| **Solution** | What fixed it? Specific code, config, or approach. |
| **Prevention** | How to avoid this in the future. Rules, tests, hooks. |
| **Cross-references** | Related files, past solutions, external docs consulted. |

### Step 2: Write Solution Doc
Create file at: `knowledge/solutions/YYYY-MM-DD-<slug>.md`

Use this template:
```
# <Problem Title>

## Problem
<What was broken. Include error messages verbatim if applicable.>

## Root Cause
<The actual underlying issue, with file paths and line numbers.>

## Solution
<What fixed it. Include code snippets, commands, config changes.>

## Investigation Notes
<What was tried that didn't work and why. Saves future agents from dead ends.>

## Prevention
<How to avoid this in the future. Suggest: tests, hooks, CLAUDE.md rules, linter configs.>

## Cross-References
- Related files: <list>
- Related past solutions: <list any from knowledge/solutions/>
- External docs: <URLs consulted>

## Tags
<comma-separated: e.g., typescript, build-error, mcp, configuration>

---
*Captured: YYYY-MM-DD by claude-code via compound-capture*
```

### Step 3: Update Knowledge Graph
Store key facts in AIM Memory:
- Entity: the problem category (e.g., "typescript-build-errors")
- Relations: links to the solution file, related code files
- Facts: the root cause pattern, the fix pattern

### Step 4: Check for Systemic Actions
Ask whether this solution suggests any of:

| Action | When |
|--------|------|
| **Hookify rule** | If the mistake is a pattern that could be caught automatically |
| **CLAUDE.md update** | If agents need to know this for future tasks |
| **Test** | If the fix should be regression-tested |
| **Skill update** | If an existing skill should incorporate this knowledge |

Don't implement these automatically — suggest them to the user.

### Step 5: Confirm
Output a brief summary:
- Solution doc path
- Key facts stored
- Suggested systemic actions (if any)

## Principles
- **Be specific.** Include file paths, line numbers, error messages, code snippets.
- **Record dead ends.** What didn't work is as valuable as what did.
- **Link, don't duplicate.** Reference existing docs, don't copy them.
- **Stay thin.** Each solution doc should be scannable in 30 seconds.
