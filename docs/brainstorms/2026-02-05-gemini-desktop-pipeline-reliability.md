---
title: Gemini→Desktop Pipeline Reliability
date: 2026-02-05
type: brainstorm
status: open
---

# Gemini→Desktop Pipeline Reliability

## Context

We have a working Gemini→Claude Desktop pipeline via MCP, but it has reliability and trust gaps that need solving before it can run autonomously overnight.

## Current State

**What works:**
- Gemini can call claude_desktop_* MCP tools
- Desktop steering (send/read/status/stop) is functional
- Task execution completes when quota permits
- Logs capture execution output

**What's broken/unclear:**
- File access: Desktop is Windows, tasks reference WSL paths
- Gemini falls back to its own tools, bypassing Desktop entirely
- No structured output schema — freeform text hard to verify
- No checkpoints during long tasks
- Quality varies — some runs thorough, others superficial

## Key Questions

### 1. File Access Strategy

**Option A: Accept Gemini fallback**
- Let Gemini use its own tools when Desktop can't access files
- Pro: Works now, simple
- Con: Loses Desktop's specialized MCPs (Obsidian, Zotero, etc.)

**Option B: Windows path translation**
- Convert `/home/div/...` → `\\wsl$\Ubuntu\home\div\...`
- Pro: Desktop filesystem MCP can read
- Con: Only solves filesystem, not specialized MCPs

**Option C: Domain-specific routing**
- Obsidian tasks → use Obsidian MCP (REST API, no paths needed)
- Code tasks → use Gemini's tools (already works)
- Research tasks → use Desktop's paper/zotero MCPs
- Pro: Best tool for each job
- Con: Complex task routing logic needed

**Option D: Desktop Commander MCP**
- Install MCP that gives Desktop shell access
- Pro: Can run any command
- Con: Security concerns, overkill for most tasks

### 2. Task Completion Quality

**What defines "complete"?**
- Freeform: Any output counts (current)
- Checklist: Must address all bullet points in task spec
- Scored: Must achieve quality threshold (e.g., 4/5)

**How to enforce?**
- Task templates with explicit acceptance criteria
- Structured output schema (JSON with required fields)
- Self-assessment step before returning

### 3. Determinism & Logging

**Current logging:**
- YAML frontmatter: task name, duration, exit code
- Raw output dump
- Error classification

**Gaps:**
- No intermediate checkpoints during execution
- No structured extraction of key findings
- No diff between expected vs actual output

**Potential improvements:**
- Require tasks to emit `[CHECKPOINT: step_name]` markers
- Require `[RESULT: key=value]` for machine-parseable outcomes
- Post-execution validator that checks markers present

### 4. Trust & Review

**Question:** How many successful runs before trusting overnight autonomy?

**Options:**
- N=5 consecutive successes per task type
- Human review of first 3 runs of any new task
- Confidence score based on task complexity

**Question:** What review artifacts are needed?

- Execution log (have this)
- Diff of changes made (if code tasks)
- Quality score from reviewer agent

## Proposed Path Forward

### Phase 1: Stabilize Domain Routing (this week)
- [ ] Update task templates with explicit tool instructions per domain
- [ ] Obsidian tasks: must use Obsidian MCP
- [ ] Code review tasks: Gemini tools OK (already working)
- [ ] Research tasks: must use Desktop MCPs

### Phase 2: Structured Output (next week)
- [ ] Define output schema: `{status, findings[], quality_score, gaps[]}`
- [ ] Add schema requirement to GEMINI.md
- [ ] Update executor to validate output has required fields

### Phase 3: Review Layer (following week)
- [ ] CC session that reviews overnight logs
- [ ] Quality gate: tasks below 3/5 get flagged for human review
- [ ] Success tracking per task type

## Dependencies

- Gemini quota management (currently exhausts in ~1 long task)
- Desktop uptime (must be running overnight)
- MCP server stability

## Open Questions for User

1. Is domain-specific routing (Option C) acceptable complexity?
2. What's the minimum quality score to accept a task as done?
3. How many review cycles before trusting full autonomy?
