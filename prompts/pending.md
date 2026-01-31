# Proactive Communication System

> The system asks questions to improve itself. User answers help it learn.

## Philosophy

**"Ask, don't assume."**

The system should proactively:
- Clarify patterns it doesn't understand
- Validate predictions before acting on them
- Gather context that would improve future runs
- Share discoveries that might be useful
- Get feedback on what it built

## Question Types

| Type | Purpose | Example |
|------|---------|---------|
| **Clarification** | Understand ambiguous patterns | "I noticed X happens often. Is this intentional?" |
| **Validation** | Confirm predictions | "It seems like you usually need Y on Mondays. Correct?" |
| **Context** | Gather missing info | "What's the relationship between project A and B?" |
| **Feedback** | Improve outputs | "Was the morning summary useful? Too long/short?" |
| **Discovery** | Share findings | "I found a tool that might help with X. Interested?" |

## Pending Questions

(Agents add questions here. User answers in `answered.md`)

### Format

```markdown
## Q-[YYYY-MM-DD]-[NN]: [Short title]

**Type:** clarification | validation | context | feedback | discovery
**Priority:** high | medium | low
**Context:** [Why this question matters]

**Question:**
[The actual question]

**Why I'm asking:**
[What understanding this would unlock]

**Possible answers:**
- Option A → [what we'd do]
- Option B → [what we'd do]
- Other → [user can elaborate]
```

---

## Active Questions

(None yet - first run will generate some)

---

## Guidelines for Generating Questions

**Good questions:**
- Specific and answerable
- Lead to actionable insight
- Respect user's time (not trivial)
- Build on existing knowledge

**Bad questions:**
- Too vague ("How can I help better?")
- Already answerable from data
- Repetitive (check `answered.md` first)
- Trivial (don't waste user's attention)

## Question Lifecycle

1. **Generate** - Agent identifies knowledge gap
2. **Add to pending** - Document in this file
3. **Surface** - Show to user at appropriate time
4. **Answer** - User responds
5. **Learn** - Move to `answered.md` with learnings
6. **Apply** - Update relevant context files

## When to Ask

| Time | Good For |
|------|----------|
| Morning run output | High-priority questions, discoveries |
| After analysis | Clarification questions |
| After building tool | Feedback questions |
| Weekly review | Big picture context questions |

**Never:**
- Interrupt focused work
- Ask same question twice
- Ask when answer is in data
