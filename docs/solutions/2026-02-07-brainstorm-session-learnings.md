---
date: 2026-02-07
category: workflow
tags: [research-methodology, delegation-patterns, session-management, brainstorming]
problem: Brainstorming sessions produce learnings scattered across conversation; patterns not captured for reuse
---

# Brainstorm Session Learnings: Problem Formulation, Delegation, and Task Capture

Four compoundable patterns emerged from a research brainstorming session. Each includes symptom, root cause, solution, and prevention mechanism.

## Learning 1: Problem Formulation Must Precede Literature Search

### Symptom
User felt their literature review was incomplete and kept searching for more papers, creating a frustration loop. Each new search surface more results, never reaching confidence that "enough" was reviewed.

### Root Cause
The gap wasn't missing papers — it was not having defined the problem structure well enough to know what to look for. Literature search without a structured problem definition becomes open-ended and exhausting.

### Solution
**Define the problem space FIRST, then do targeted research to fill specific gaps.**

Process:
1. Write down: model families, pipeline structure, key constraints, decision points
2. Identify specific gaps in understanding (e.g., "how do X models handle Y constraint?")
3. Search for papers that address those specific gaps
4. Avoid: open-ended "read everything about topic X" searches

### Prevention
Before any literature search, require: **"What specific question am I trying to answer?"**

Write this down explicitly. If you can't articulate it, the problem structure isn't ready yet.

---

## Learning 2: Delegation Requires Spec, Review, and User Final Judgment

### Symptom
User lost confidence in code that agents modified autonomously without intermediate review. Fire-and-forget delegation felt unsafe despite receiving correct output.

### Root Cause
Three missing steps:
1. Spec wasn't fully defined before delegation
2. Output was never reviewed by user before acceptance
3. No mechanism for user to guide or re-spec if agent took a different direction

### Solution
**Introduce review loop in every delegation:**

```
spec (inputs + expected outputs + done-when criteria)
  ↓
delegate to agent
  ↓
review output against spec
  ↓
user makes final judgment (accept / guide / re-spec)
```

Process:
1. Before delegating: write down inputs, expected output shape, acceptance criteria
2. After delegation: user reviews output (code review, test results, etc.)
3. If output doesn't match spec: guide agent or re-spec and retry
4. Only then: user accepts and moves forward

### Prevention
Every delegation needs: **inputs defined, expected output defined, "done when" criteria, review step before accepting.**

Create a delegation checklist:
- [ ] Input spec: what assumptions/files/context is the agent starting with?
- [ ] Output spec: what shape/format/behavior is expected?
- [ ] Done-when: what evidence proves completion?
- [ ] Review: who reviews and what are they checking for?

---

## Learning 3: Multi-Task Brainstorms Need "Tasks Identified" Section

### Symptom
User unsure how to capture a brainstorm that produced 4 independent task threads. Session template assumed one brainstorm → one linear chain.

### Root Cause
Brainstorm artifacts are designed to feed into a single next brainstorm or plan. But productive brainstorms often spawn multiple parallel tasks. The capture template didn't support this topology.

### Solution
**Add "Tasks Identified" section with per-task detail.**

Instead of flat "Feeds Forward" list, use:

```markdown
## Tasks Identified

### Task 1: [Name]
- **What:** [one-line description]
- **Delegation:** [who, model tier, estimated effort]
- **Done When:** [acceptance criteria]
- **Blocks:** [what depends on this task]
- **Next Session:** [reference to future brainstorm/plan if needed]

### Task 2: [Name]
...
```

This allows:
- Future sessions to link back via `[[reference]]`
- Parallel task tracking without forcing linear order
- Clear hand-off to delegation engine (ralph, ultrawork, etc.)
- Easier to see task dependencies

### Prevention
When a brainstorm produces multiple independent tasks, use "Tasks Identified" instead of "Feeds Forward". Treat each task as its own work stream.

---

## Learning 4: Meeting Feedback Requires Immediate Capture

### Symptom
User couldn't find what supervisor asked at last meeting. Feedback was mentioned in conversation but not logged anywhere retrievable.

### Root Cause
No habit of capturing meeting feedback immediately after the meeting. Feedback lives only in conversation history, which is not searchable by future sessions.

### Solution
**Create immediate meeting capture note after every research meeting.**

Template:

```markdown
# Meeting: [Date] [Topic]

## Feedback Received
- Point 1: [exact feedback or question]
- Point 2: [...]

## Action Items
- [ ] Item 1 (assigned to [person])
- [ ] Item 2 (assigned to [person])

## Questions to Address Before Next Meeting
- Question 1
- Question 2

## Links
- Brainstorm: [[reference-if-exists]]
- Plan: [[reference-if-exists]]
```

Store in: `context/meeting-feedback/YYYY-MM-DD-[topic].md`

### Prevention
Could be:
1. **Recurring reminder** in session start: "Did you have a meeting recently? Capture feedback."
2. **Part of daily note template:** Meeting section that auto-prompts
3. **Hook in meeting scheduler:** Auto-create capture stub when meeting added to calendar

---

## Implementation Checklist

To apply these learnings to future sessions:

- [ ] **Before lit search:** Write down the specific questions you're trying to answer (Learning 1)
- [ ] **Before delegation:** Create spec with inputs, outputs, done-when, review plan (Learning 2)
- [ ] **Brainstorm capture:** Use Tasks Identified section for multi-task brainstorms (Learning 3)
- [ ] **After meetings:** Create immediate feedback capture note (Learning 4)

---

## See Also
- `context/State.md` — Session state tracking (could include "meeting feedback pending" flag)
- `docs/brainstorms/` — Brainstorm session files
- `docs/plans/` — Planning session files (reference from Tasks Identified)
- `meta/contribution-workflow` — Delegation and review patterns
