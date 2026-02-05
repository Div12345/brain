---
name: learnings-query
description: Query past solutions before planning. Use at the start of any planning or problem-solving session to check if similar problems have been solved before. Prevents re-research.
allowed_tools:
  - Read
  - Grep
  - Glob
  - mcp__memory__aim_memory_search
  - mcp__memory__aim_memory_get
  - mcp__obsidian__obsidian_global_search
---

# Learnings Query

## Purpose
Before planning any task, check if the system has already solved a similar problem. This is the feedback link from Compound → Plan in the compound engineering loop. Without this, captured knowledge is never reused.

## When to Invoke
- At the start of any planning session (before OMC plan, ralplan, or brainstorming)
- When investigating a bug (before debugging from scratch)
- When implementing a feature in a domain where past work exists
- When an error message looks familiar

## Process

### Step 1: Identify Search Terms
From the current task/problem, extract:
- Error messages or symptoms (exact strings)
- Technology/framework names (e.g., "typescript", "mcp", "hookify")
- Problem category (e.g., "build-error", "configuration", "api-integration")
- File paths or module names involved

### Step 2: Search Past Solutions
Run these searches in parallel:

**A. Local solution docs:**
```
Glob: knowledge/solutions/*.md
Grep: <search terms> in knowledge/solutions/
```

**B. AIM Memory knowledge graph:**
```
aim_memory_search: <problem category>
aim_memory_search: <technology name>
```

**C. Obsidian vault (broader knowledge):**
```
obsidian_global_search: <key terms>
```

**D. Brain repo knowledge base:**
```
Grep: <search terms> in knowledge/
```

### Step 3: Assess Relevance
For each hit, check:
- Is this the same problem or just keyword overlap?
- Is the solution still valid (check date, check if referenced files still exist)?
- Does it fully solve the current problem or just partially?

### Step 4: Report Findings
Output one of:

**If relevant solutions found:**
```
## Prior Knowledge Found

### Directly Relevant
- [solution-doc-path]: <one-line summary of what it solved and how>
  - Applicability: <full/partial/reference-only>

### Partially Relevant
- [doc-path]: <why it's related but not a direct match>

### Recommended Approach
Based on prior solutions, suggest: <reuse solution X, adapt approach Y, or start fresh because Z>
```

**If no solutions found:**
```
## No Prior Solutions Found
Searched: knowledge/solutions/, AIM Memory, Obsidian vault
Terms: <what was searched>
Proceeding with fresh research.
```

### Step 5: Feed Into Planning
If relevant solutions were found, include them as context for the planning step. The planner should:
- Reuse proven approaches rather than inventing new ones
- Avoid dead ends documented in Investigation Notes
- Reference the solution doc in the new plan

## Principles
- **Search before research.** 30 seconds of local search saves 10 minutes of external research.
- **Trust but verify.** Past solutions may be outdated. Check that referenced files/APIs still exist.
- **Link forward.** If the current task extends a past solution, link the new plan to the old solution doc.
