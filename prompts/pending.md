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

### Q-2026-01-31-01: Overnight Schedule Preference

**Type:** context
**Priority:** high
**From:** Orchestration Architect Agent

**Question:**
What's your preferred overnight run schedule?

**Why I'm asking:**
Need to configure Windows Task Scheduler correctly. This affects when autonomous work happens.

**Options:**
- A) Daily at 2 AM → Maximum automation, runs every night
- B) Weeknights only (Mon-Fri) → Preserves weekend mornings
- C) On-demand only → You trigger when ready
- D) Other schedule → Specify

---

### Q-2026-01-31-02: Obsidian Vault Location

**Type:** context
**Priority:** high
**From:** Orchestration Architect Agent

**Question:**
What's the exact path to your main Obsidian vault?

**Why I'm asking:**
The CC Vault Analyst agent needs this to analyze folder structure. Desktop Commander MCP also needs it for file operations.

**Example:** `D:\Obsidian\MainVault` or `C:\Users\[name]\Documents\Obsidian\vault`

---

### Q-2026-01-31-03: Failed Task Notification

**Type:** validation
**Priority:** medium
**From:** Orchestration Architect Agent

**Question:**
If an overnight task fails, should the system notify you immediately or batch failures for morning review?

**Why I'm asking:**
Affects how error handling works in the overnight PowerShell script.

**Options:**
- A) Immediate notification (email/desktop alert) → Requires additional setup
- B) Batch for morning → Just log errors, you review logs
- C) Critical only immediate → Define what's "critical"

---

### Q-2026-01-31-04: Off-Limits Tasks

**Type:** context
**Priority:** medium
**From:** Orchestration Architect Agent

**Question:**
Are there any tasks that should NEVER run unattended (always require your presence)?

**Why I'm asking:**
Safety boundaries for autonomous operation. Some operations might need human oversight.

**Examples that might need oversight:**
- Anything touching work files?
- Financial documents?
- Deleting/moving files?
- Git pushes to remote?

---

### Q-2026-01-31-05: Brain Repo Location

**Type:** context
**Priority:** high
**From:** Orchestration Architect Agent

**Question:**
Where is (or will be) the brain repo cloned locally on your Windows machine?

**Why I'm asking:**
The Windows Task Scheduler configs assume `C:\brain`. If different, need to update paths.

**Example:** `C:\brain`, `C:\Users\[name]\Projects\brain`, `D:\AI\brain`

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
