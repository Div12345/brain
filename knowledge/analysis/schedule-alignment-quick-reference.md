# Schedule Alignment Quick Reference

**TL;DR:** 4-phase schedule (overnight/prep/work/handoff) + 80-8-7-5 token split + confidence routing

## Time Windows

| Phase | Time | What Happens | Token % |
|-------|------|--------------|---------|
| **Overnight** | 2-7 AM | Autonomous research, builds | 80% |
| **Morning Prep** | 7-9 AM | Generate briefing | 8% |
| **Work Hours** | 9 AM-6 PM | **RESERVED for user** | 0% scheduled |
| **Evening** | 6-10 PM | User assist + prep | 7% |
| **Buffer** | 10 PM-2 AM | Emergency reserve | 5% |

## Decision Rules

### When to Request Human Review vs Proceed

| Confidence | Action |
|------------|--------|
| >90% | Auto-proceed + notify |
| 70-90% | Generate plan, queue for morning review |
| 50-70% | Generate questions for user |
| <50% | Skip, mark needs-user-input |

### Risk-Based Approval

| Risk | Operations | Approval |
|------|------------|----------|
| **Safe** | Read, analyze, log | None |
| **Moderate** | Code edits, configs | Plan review |
| **Critical** | Delete, deploy, publish | Per-action |

## Capacity Preservation

**Critical Rule:** Never schedule autonomous work during 9 AM-6 PM

**Implementation:**
- All autonomous tasks: 2-7 AM window only
- Token tracking stops at 80% limit
- 100% capacity available for user during work hours

## Question Handling

### Overnight (2-7 AM)
- Batch ALL questions → `prompts/pending/*.md`
- Never interrupt user

### Morning (7-9 AM)
- Present batched questions in briefing
- Critical questions first

### Work Hours (9 AM-6 PM)
- Ask immediately ONLY if:
  - Confidence <50% AND
  - Priority = high
- Otherwise: queue for async answer

### Evening (6-10 PM)
- User may address queued questions
- Generate overnight task list

## Implementation Checklist

**Week 1:**
- [ ] Set up systemd timer for 2:00 AM
- [ ] Implement token tracking
- [ ] Create question batching to `prompts/pending/`

**Week 2:**
- [ ] Add morning briefing at 7:00 AM
- [ ] Implement confidence-based routing
- [ ] Monitor and adjust 80-8-7-5 allocation

## Templates

### Overnight Question Format
```markdown
---
priority: high|medium|low
confidence: 0.XX
blocking: true|false
---

# Question: [Brief title]

## Options
- [ ] A: [Option]
- [ ] B: [Option]
- [ ] C: Skip/defer

## Impact
If A: [Consequence]
If B: [Consequence]
If C: [What gets blocked]
```

### Morning Briefing Format
```markdown
# Morning Briefing - YYYY-MM-DD

## Overnight Summary
- Completed: N tasks
- Failed: M tasks
- Questions: K

## Key Results
1. [Finding]
2. [Finding]

## Questions for Review
### Critical
- Q-001: [Question] → [Options]

## Today's Suggestions
1. [Priority]
2. [Priority]
```

## Key Metrics to Track

1. **Overnight task completion rate** (target: >80%)
2. **Token budget adherence** (stay under 80% overnight)
3. **Question answer time** (morning vs evening)
4. **Work hours capacity used** (should be user-initiated only)
5. **False positive rate** (confidence >70% but wrong approach)

---
**Source:** Schedule alignment patterns research (2026-02-03)
