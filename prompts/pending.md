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

### Q-2026-01-31-01: Daily template simplification

**Type:** validation
**Priority:** medium
**Context:** Your daily note template has 8+ sections but only 2 are regularly used.

**Question:**
The wellbeing metrics, habits, gratitude, and "Tomorrow's Intent" sections are unfilled in 100% of the 20 notes I analyzed. Should I:

**Why I'm asking:**
Understanding whether these are aspirational (keep them as reminders) or unused friction (remove them) affects how I interpret your workflow.

**Possible answers:**
- A: Keep them (aspirational, might use someday) → No changes
- B: Remove them (they add guilt/friction) → Propose simplified template
- C: Try a middle ground (collapse to one "reflection" section) → Propose minimal version
- Other → User elaborates

---

### Q-2026-01-31-02: arterial_analysis completion criteria

**Type:** context
**Priority:** high
**Context:** This project has been your daily focus for 30+ days with phrases like "wrap up", "finish", "get conclusions".

**Question:**
What specific outputs would mark arterial_analysis as "done enough" for the current phase?

**Why I'm asking:**
Without clear completion criteria, it's hard to predict when you'll need to context-switch to other projects. Understanding the finish line helps me anticipate what support you'll need.

**Possible answers:**
- A: A specific deliverable (paper draft, meeting slides, data summary)
- B: A methodology decision (finalizing CV approach, feature selection)
- C: External event (advisor feedback, deadline)
- Other → User elaborates

---

### Q-2026-01-31-03: Claude dependency comfort level

**Type:** clarification
**Priority:** low
**Context:** You wrote "I don't like my dependency on claude this much for coding" on 2026-01-14.

**Question:**
Is this something you want the system to help address (e.g., suggesting non-AI coding sessions), or is it a passing observation that doesn't require action?

**Why I'm asking:**
If it's a real concern, I could help by occasionally suggesting you tackle something without AI. If it's just venting, I won't add friction by bringing it up.

**Possible answers:**
- A: Yes, help me be less dependent → Occasionally suggest non-AI work
- B: No, just venting → Don't address
- C: It's complicated → User elaborates

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
