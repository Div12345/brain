# Self-Improvement Quick Reference

## TL;DR: What to Build

**Minimum Viable Feedback Loop (4 components)**:
1. Execution Tracking → `logs/executions/{timestamp}-{action}-{outcome}.json`
2. Outcome Measurement → Success/failure flags in logs
3. Storage → `knowledge/skills/{domain}/{skill}.md`
4. Retrieval → `grep -r "pattern" knowledge/skills/` before new tasks

**Start Here**: Implement Voyager skill library + Self-Refine loop (no fine-tuning needed)

---

## Critical Numbers

- **71.4%**: Systems that work WITHOUT fine-tuning
- **4**: Minimum components for viable feedback loop
- **5**: Implementation steps (all low complexity)
- **80%**: Target task success rate
- **30%**: Target skill reuse rate after 1 month
- **3**: Max iterations per refinement loop

---

## The Three Killers (Avoid These)

1. **Catastrophic Forgetting** → Solution: Persistent skill library
2. **Drift Without Grounding** → Solution: External validation checks
3. **No Failure Analysis** → Solution: Log failures explicitly

---

## Best Systems for File-Based Coordination

| System | Why It Fits | Complexity |
|--------|-------------|------------|
| Voyager Skill Library | File-based storage, compositional | Medium-High |
| Self-Refine Loop | Stateless iteration, simple | Low |
| Production Feedback | Standard logging pipeline | Low-Medium |

**Winner**: Hybrid of all three (leverages existing file structure)

---

## Week 1 Action Items

1. Create `knowledge/skills/` directory
2. Define skill metadata schema (name, domain, code, success_rate, last_used)
3. Create `logs/executions/` directory
4. Log first task execution with outcome
5. Manually save one successful pattern as a skill

---

## Metrics Dashboard (Copy to `context/metrics.md`)

```markdown
# Self-Improvement Metrics
Last Updated: {date}

## Primary (Weekly)
- Task Success Rate: {completed}/{total} = {percent}% (Target: >80%)
- Skill Reuse Rate: {reused}/{total} = {percent}% (Target: >30%)
- First-Try Success: {first_try}/{total} = {percent}% (Target: >60%)

## Warning (Continuous)
- Repeated Failures: {count} (Target: 0)
- Divergent Loops: {count} (Target: 0)
- Stale Skills: {count} unused >2mo
```

---

## Pattern: Skill File Format

```markdown
---
skill_id: {domain}-{name}
domain: {architecture|debugging|coordination|etc}
created: {timestamp}
last_used: {timestamp}
success_count: {int}
failure_count: {int}
avg_iterations: {float}
---

# {Skill Name}

## When to Use
{Description of applicability}

## Pattern
```{language}
{Executable code or pseudocode}
```

## Evidence
- Success rate: {percent}%
- Used in: {task-001, task-015, task-032}
- Failure modes: {known edge cases}
```

---

## Sources for Deep Dive

**Voyager**: https://github.com/MineDojo/Voyager  
**Gödel Agent**: https://github.com/Arvid-pku/Godel_Agent  
**Self-Refine**: https://selfrefine.info/  
**AlphaLLM**: Search "MCTS LLM reasoning"  
**Production Patterns**: Standard MLOps feedback loops
