# Overnight Learning Agent

> This agent doesn't just analyze - it **learns** and **proposes improvements** to itself.

## Core Philosophy (From Your Vault)

**Extracted from `99 - Meta/Task Management System - Overview.md`:**

| Principle | Implication for Agent |
|-----------|----------------------|
| Minimal viable structure | Don't over-engineer. Add complexity only when pain points emerge |
| Match your brain | Learn your existing patterns, don't impose new ones |
| Low friction | If using AI outputs feels like work, the system has failed |
| Iterate based on use | This is version 1.0. Evolve based on what actually helps |
| Energy states matter | Reflective mood ≠ productive action-taking |
| Time windows | Frame work in "shouldn't take more than a few hours" chunks |
| Context switching cost | Research vs admin vs personal need different headspaces |

## Phase 1: Context Loading (5 min)

1. Read `CLAUDE.md` from this repo
2. Read `context/priorities.md` for current focus
3. Read last 3 files in `logs/` for continuity
4. Read `meta/improvements.md` for pending system improvements

## Phase 2: Vault Pattern Discovery (30 min)

### 2A. Daily Note Analysis

Read last 30 daily notes from `01 - Personal/Daily/`. Extract:

| Pattern Type | What to Look For |
|--------------|------------------|
| **Recurring tasks** | What shows up multiple times but never completes? |
| **Energy indicators** | Words like "tired", "productive", "stuck", "flowing" |
| **Time patterns** | When does real work happen vs planning/reflection? |
| **Friction points** | Tasks that keep moving day-to-day |
| **Completion patterns** | What actually gets checked off? What doesn't? |
| **Tool mentions** | Zotero, Claude, cc, obsidian - what's actually used? |
| **Project links** | Which [[wikilinks]] appear most? |

### 2B. Structure Preferences

Learn from existing vault structure:

| Source | What to Extract |
|--------|-----------------|
| `99 - Meta/` | How they document systems |
| `00 - Dashboard/` | What views matter |
| Template files | Their preferred formats |
| Tag usage | How they categorize |
| Frontmatter patterns | What metadata they use |

### 2C. Project State Discovery

Scan `03 - Projects/`:

| For Each Project | Capture |
|------------------|---------|
| Last modified date | Active vs stale? |
| Progress log | Momentum or stuck? |
| Open questions | What's blocking? |
| Links to daily notes | Frequency of attention |

## Phase 3: Knowledge Synthesis (20 min)

Create `knowledge/vault-analysis-YYYY-MM-DD.md` with:

```markdown
---
created: YYYY-MM-DD
agent: overnight-learning
confidence: medium
---

# Vault Analysis - [Date]

## Summary
(3 sentences: what's working, what's stuck, what's invisible)

## Patterns Discovered

### What Actually Gets Done
(Evidence-based: tasks that complete vs ones that don't)

### Energy & Time Patterns
(When productive work happens based on note content timing/mood words)

### Friction Points
(Recurring blockers, tasks that keep moving forward)

### Hidden Curriculum
(Things worked on but not explicitly tracked)

## Structural Observations

### What's Working in Current Vault
(Don't change these)

### Mismatches
(Structure that exists but isn't used, or behavior without structure)

## Recommendations

### For Tomorrow Morning
(1-3 things that would actually help, not "productivity porn")

### Optimal Daily Output
(Based on patterns: what info at what time would reduce friction?)

### System Improvements
(Specific, low-friction changes to brain repo or workflow)
```

## Phase 4: Self-Improvement Proposals (15 min)

The agent should propose improvements to **itself** and the **brain repo**:

### Check Against Superpowers Patterns

Review `/skills/` from superpowers plugin and ask:
- Is there a skill that would help this workflow?
- Should overnight agent use subagent-driven-development for complex analysis?
- Would brainstorming skill help refine recommendations?

### Check Against Hookify Potential

Could any discovered friction points become hooks?
- Repeated task that never completes → hook reminder?
- Pattern of late-night work → warning about sleep?
- Ignored inbox item → escalation?

### Propose CLAUDE.md Updates

Based on discoveries, should `brain/CLAUDE.md` be updated?
- New directories needed?
- Different workflow for specific task types?
- Better context files structure?

### Write to `meta/improvements.md`

```markdown
## Proposed Improvements - [Date]

### For Brain Repo Structure
| Change | Rationale | Effort | Impact |
|--------|-----------|--------|--------|
| ... | ... | Low/Med/High | Low/Med/High |

### For Overnight Agent
| Change | Rationale |
|--------|-----------|
| ... | ... |

### For Daily Workflow
| Suggestion | When to Use | Why |
|------------|-------------|-----|
| ... | ... | ... |

### Hooks to Consider
| Trigger | Action | File |
|---------|--------|------|
| ... | ... | `.claude/hookify.*.local.md` |
```

## Phase 5: Optimal Daily Output Design (10 min)

Based on discovered patterns, propose:

### Morning Output (Wake Up)
What should appear in daily note or dashboard?
- Priority tasks ranked by actual completion likelihood
- Projects that need attention based on stall patterns
- Reminders timed to energy patterns

### Evening Output (Before Sleep)
What synthesis would help next day?
- What got done vs planned
- What moved forward vs stuck
- Tomorrow's realistic scope

### Create `knowledge/daily-output-spec.md`
Document what the system should produce and when.

## Phase 6: Context Update (5 min)

Update files for next agent:

| File | Update With |
|------|-------------|
| `context/priorities.md` | New focus areas from analysis |
| `context/projects.md` | Discovered project states |
| `context/patterns.md` | Behavioral observations |

## Phase 7: Logging (5 min)

Create `logs/YYYY-MM-DD-HHMM-overnight.md`:

```markdown
---
agent: overnight-learning
started: ISO timestamp
ended: ISO timestamp
vault_files_read: N
brain_files_written: N
proposals_made: N
---

# Overnight Run - [Date]

## What I Did
(Phases completed, files read/written)

## Key Discoveries
(3-5 bullet points)

## Proposals Made
(Summary of improvements suggested)

## What Next Agent Should Know
(Context for continuity)

## Self-Assessment
(What worked well, what was hard, what should change about this process)
```

## Constraints

| Rule | Reason |
|------|--------|
| **READ ONLY** on Obsidian vault | No edits to original data |
| **WRITE** only to GitHub brain repo | All outputs here |
| **NO** external APIs, emails, deletions | Safety |
| **SELF-CONTINUE** on context fill | Summarize and keep going |
| **Match existing patterns** | Don't impose new structure |
| **Low-friction proposals only** | If it feels like work, don't suggest it |

## Success Criteria

After this run, there should be:

1. **Knowledge file** with genuine insights (not generic observations)
2. **At least 3 specific, actionable proposals** in `meta/improvements.md`
3. **Updated context files** for next run
4. **Daily output spec** proposing what info at what time
5. **Self-assessment** in log about what to improve about the agent itself

## Anti-Patterns to Avoid

| Don't Do This | Why |
|---------------|-----|
| Generic "organize your tasks" advice | Doesn't match their philosophy |
| Suggest complex new systems | "Avoid draining spirals of setup" |
| Ignore what's already working | "Match your brain" |
| Over-structure the analysis | "Minimal viable structure" |
| Create overwhelming output | "Low friction" |
