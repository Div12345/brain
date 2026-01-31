---
created: 2026-01-31
tags:
  - research
  - self-improvement
  - meta-learning
  - autonomous
status: active
agent: overnight
aliases:
  - recursive improvement
  - Gödel Agent
  - meta-prompting
---

# Recursive Self-Improvement Patterns

Research on AI systems that improve themselves.

## Key Frameworks

### 1. Gödel Agent (Most Relevant)
[Paper](https://arxiv.org/abs/2410.04444)

Self-referential framework that modifies own logic via LLM prompting.

**Core idea:** Agent uses LLM to:
1. Evaluate current performance
2. Propose modifications to own code/prompts
3. Test modifications
4. Adopt if improved

**For brain system:**
- Agent reviews own prompt effectiveness
- Suggests improvements to [[.claude/skills/]]
- Tests on sample tasks
- Commits improvements if validated

### 2. Darwin Gödel Machine
[Sakana AI](https://sakana.ai/dgm/)

Evolutionary approach - generates variations, selects best performers.

**Key insight:** "Less-performant ancestors can lead to breakthroughs" - don't prune too aggressively.

### 3. Meta-Prompting
AI improves its own prompts iteratively.

```python
class MetaPromptEngine:
    def improve(self, prompt, performance_data):
        critique = llm("Analyze why this prompt underperformed: " + prompt)
        improved = llm("Improve this prompt based on: " + critique)
        return improved
```

### 4. STOP (Self-Taught Optimizer)
Scaffolding program recursively improves itself using fixed LLM.

### 5. Voyager Pattern
From Minecraft agent - skills library that expands.

**Pattern:**
1. Attempt task
2. If fails, refine code via LLM
3. If succeeds, store in skills library
4. Future tasks can use learned skills

## Brain Self-Improvement Protocol

### V1: Simple Retrospective
After each session:
1. Review what worked/didn't
2. Update [[knowledge/patterns/]] with learnings
3. Refine [[.claude/skills/]] based on failures
4. Log in [[logs/]] for future reference

### V2: Automated Feedback Loop
```
context/self-improvement/
  metrics.md        # Track task success rates
  retrospectives/   # Session analyses
  experiments/      # Prompt variations being tested
```

### V3: Full Gödel Pattern (Future)
- Agent proposes modifications to own prompts
- Tests on held-out tasks
- Commits improvements automatically
- Tracks lineage of changes

## Implementation for Brain

### Immediate (V1)
Create `context/retrospective.md`:
```markdown
## Session: YYYY-MM-DD

### What Worked
- ...

### What Didn't
- ...

### Pattern Updates
- Added to knowledge/patterns/: ...
- Refined skill: ...

### Questions Generated
- ...
```

### Phase 2 (V2)
Add metrics tracking:
```markdown
## Metrics

| Task Type | Attempts | Success | Rate |
|-----------|----------|---------|------|
| Research | 10 | 8 | 80% |
| Code gen | 5 | 3 | 60% |
```

## Anti-Patterns to Avoid

1. **Over-optimization** - Don't converge too fast
2. **No validation** - Always test changes
3. **Lost lineage** - Track why changes were made
4. **Circular improvement** - Need external signal

## Related
- [[agents/overnight]] - Main agent
- [[knowledge/research/ai-memory-systems]] - Memory patterns
- [[context/session-state]] - Current state
