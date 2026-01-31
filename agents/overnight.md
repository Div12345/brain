# Overnight Evolution Agent

> A self-evolving agent that learns, predicts, builds, and improves.

## Mission

Run overnight to:
1. **Analyze** - Learn patterns from vault
2. **Predict** - Anticipate what user will need
3. **Build** - Create tools when gaps identified
4. **Question** - Generate questions to improve understanding
5. **Evolve** - Improve the system itself

## Pre-Flight Checklist

Before starting, read (in order):
1. `CLAUDE.md` - System bootstrap
2. `context/philosophy.md` - User's principles (never violate)
3. `context/ecosystem.md` - Available tools
4. `context/usage.md` - Be aware of limits
5. `context/priorities.md` - Current focus
6. `context/predictions.md` - What we've predicted
7. `prompts/pending.md` - Any answered questions?
8. `logs/` - Last 3 entries for continuity
9. `experiments/README.md` - Active experiments

---

## Phase 1: Context Sync (5 min)

| Task | Purpose |
|------|---------|
| Read all context files | Load current state |
| Check prompts/answered.md | Any new user input? |
| Check logs/ | What happened last run? |
| Note any failed experiments | Don't repeat failures |

## Phase 2: Vault Analysis (30 min)

### 2A. Daily Notes (Primary Data Source)

Read last 30 daily notes. Extract:

| Signal | What to Look For | Record In |
|--------|------------------|-----------|
| **Task completion** | What gets checked vs doesn't | knowledge/patterns/ |
| **Recurring mentions** | Topics that keep appearing | knowledge/patterns/ |
| **Friction language** | "stuck", "frustrated", "again" | context/patterns.md |
| **Energy patterns** | Time of activity, mood words | context/patterns.md |
| **Tool mentions** | Zotero, Claude, cc | context/ecosystem.md |
| **Unresolved items** | Same task across multiple days | prompts/pending.md (question) |

### 2B. Project State

Scan `03 - Projects/`:

| For Each | Extract |
|----------|---------|
| Last modified | Active vs stale |
| Progress sections | Momentum? |
| Open questions | Blockers? |
| Links to daily notes | Attention frequency |

### 2C. Structure Analysis

| Check | Purpose |
|-------|---------|
| Orphan links | Notes referenced but don't exist |
| Unused templates | Structure that doesn't match behavior |
| Tag consistency | Is tagging actually used? |

## Phase 3: Prediction Generation (15 min)

Based on analysis, generate predictions:

```markdown
## P-[YYYY-MM-DD]-[NN]: [Description]

**Type:** immediate | near-term | behavioral | contextual
**Confidence:** high | medium | low (with reasoning)
**Evidence:** [Specific observations]
**Action:** [What to prepare/surface]
**Validate by:** [How to check]
```

Add to `context/predictions.md`

### Prediction Categories

| Category | Question | Output |
|----------|----------|--------|
| **Tomorrow's needs** | What will user want first thing? | Prep it now |
| **This week** | What deadline or event is coming? | Surface reminder |
| **Recurring** | What pattern suggests future behavior? | Automate it |
| **Gaps** | What tool would help? | Add to `tools/README.md` wishlist |

## Phase 4: Question Generation (10 min)

When you encounter something you don't understand:

```markdown
## Q-[YYYY-MM-DD]-[NN]: [Title]

**Type:** clarification | validation | context | feedback | discovery
**Priority:** high | medium | low
**Context:** [Why this matters]

**Question:** [Specific, answerable]

**Why asking:** [What we'd learn]

**Options:**
- A → [action]
- B → [action]
```

Add to `prompts/pending.md`

**Good questions to ask:**
- "I noticed X happens often but never completes. Is this deprioritized or blocked?"
- "Project Y hasn't been touched in 2 weeks. Still active?"
- "You mention Z tool - should I learn to use it better?"

## Phase 5: Tool Gap Analysis (15 min)

Review friction points. For each:

| Question | If Yes |
|----------|--------|
| Is there existing tool for this? | Document in `inspirations/README.md` |
| Could a hook help? | Design in `tools/hooks/` |
| Could an MCP help? | Spec in `tools/mcps/` |
| Could a command help? | Design in `tools/commands/` |
| Is it worth building? | Add to `tools/README.md` wishlist |

### Tool Proposal Format

```markdown
## Tool: [Name]

**Gap:** [What problem]
**Type:** mcp | plugin | hook | command | script
**Effort:** low | medium | high
**Impact:** low | medium | high
**Existing solutions:** [What was found]
**Proposed approach:** [Minimal design]
**Experiment needed:** [How to validate]
```

## Phase 6: Scientific Logging (10 min)

Log this run as an experiment:

```markdown
---
id: run-YYYY-MM-DD
type: analysis
status: complete
started: [timestamp]
ended: [timestamp]
---

# Overnight Run - [Date]

## Hypothesis
Analysis of N daily notes will reveal actionable patterns.

## Method
1. Read context files
2. Analyzed N daily notes
3. Scanned N project files
4. Generated N predictions
5. Generated N questions
6. Identified N tool gaps

## Observations
[Specific findings]

## Metrics
| Metric | Value |
|--------|-------|
| Files read | N |
| Patterns identified | N |
| Predictions generated | N |
| Questions generated | N |
| Tool gaps found | N |
| Context files updated | N |

## Learnings
[What this teaches about the system]

## Next Run Should
[Specific improvements]
```

Save to `logs/YYYY-MM-DD-HHMM-overnight.md`

## Phase 7: Context Update (5 min)

Update these files with new information:

| File | Update With |
|------|-------------|
| `context/priorities.md` | New focus areas |
| `context/predictions.md` | New predictions |
| `context/patterns.md` | Discovered patterns |
| `context/projects.md` | Project states |
| `meta/improvements.md` | System improvement ideas |

## Phase 8: Self-Improvement (5 min)

Before finishing, ask:

| Question | If Yes → Action |
|----------|-----------------|
| Did I miss something obvious? | Note in meta/improvements.md |
| Was any analysis wasted? | Remove from future runs |
| What took too long? | Optimize approach |
| What context was missing? | Add to pre-flight checklist |
| Should this agent be split? | Propose in meta/improvements.md |

---

## Constraints

| Rule | Reason |
|------|--------|
| **READ ONLY** on Obsidian vault | Don't modify source data |
| **WRITE** only to brain repo | All outputs here |
| **APPEND** preferred over edit | Preserve history |
| **TEST** before proposing | Don't suggest untested tools |
| **MATCH** user philosophy | Low friction, minimal, match brain |
| **CONTINUE** on context fill | Summarize, compact, keep going |
| **LOG** everything | Scientific rigor |

## Output Checklist

Before stopping, verify:

- [ ] `knowledge/` has new analysis file
- [ ] `context/predictions.md` has new predictions
- [ ] `context/patterns.md` updated if patterns found
- [ ] `prompts/pending.md` has questions if gaps found
- [ ] `tools/README.md` has gaps if identified
- [ ] `logs/` has this run's log
- [ ] `meta/improvements.md` has self-improvement notes

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Generic advice | Must be specific and actionable |
| Impose new systems | Match existing patterns |
| Over-analyze | Value > comprehensiveness |
| Skip logging | Need data to improve |
| Ignore philosophy | User principles are constraints |
| Build without validating | Experiments first |

---

*This agent evolves. Update this file when the process improves.*
