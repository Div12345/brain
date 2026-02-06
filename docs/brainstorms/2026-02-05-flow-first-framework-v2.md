# Flow-First Framework v2

> Based on research from [Knowledge Vault](https://gist.github.com/naushadzaman/164e85ec3557dc70392249e548b423e9), [axtonliu workflows](https://www.axtonliu.ai/newsletters/ai-2/posts/obsidian-claude-code-workflows), and [obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm)

---

## Core Insight

**The system should tell you what to do, not the other way around.**

Instead of maintaining files, you:
1. **Capture** thoughts in one place (inbox)
2. **Process** them with a command (`/process`)
3. **Work** with context auto-loaded
4. **The system tracks** what's active, done, waiting

---

## Proposed Structure (Minimal)

```
brain/
├── CLAUDE.md                    # Entry point - auto-loads context
├── inbox.md                     # SINGLE capture file - drop anything here
├── active.md                    # Current focus items (auto-populated)
├── waiting.md                   # Delegated/blocked items
├── done.md                      # Completed items (auto-archived)
│
├── projects/                    # Per-project context
│   ├── cardiac-output/
│   │   ├── CLAUDE.md            # Project-specific context
│   │   ├── knowledge.md         # Accumulated decisions/learnings
│   │   └── gameplan.md          # Current execution plan
│   └── arterial-analysis/
│       ├── CLAUDE.md
│       ├── knowledge.md
│       └── gameplan.md
│
├── docs/                        # CE artifacts (existing)
│   ├── brainstorms/
│   ├── plans/
│   └── solutions/
│
└── .claude/
    └── skills/                  # Flow commands
        ├── capture/             # /capture - quick add to inbox
        ├── process/             # /process - move inbox → active/project
        ├── focus/               # /focus - show what needs attention
        ├── done/                # /done - archive completed item
        └── review/              # /review - weekly review flow
```

---

## The Five Flows

### Flow 1: Capture (Zero Friction)

**Trigger:** Thought appears anywhere
**Action:** Add to `inbox.md` (one line, no formatting needed)
**Result:** Item queued for processing

```markdown
<!-- inbox.md -->
# Inbox

- look at arterial analysis code structure
- idea: nested CV for cardiac output validation
- question: which feature selection method?
- read that paper on transfer functions
```

No tags, no frontmatter, no structure. Just dump.

---

### Flow 2: Process (On Demand)

**Trigger:** `/process` command or daily review
**Action:** Claude reads inbox, asks "what is this?" for each item
**Result:** Items move to:
- `active.md` (if actionable now)
- `waiting.md` (if blocked/delegated)
- `projects/{name}/knowledge.md` (if it's a decision/learning)
- `projects/{name}/gameplan.md` (if it's a next step)
- Deleted (if captured but not needed)

---

### Flow 3: Focus (Session Start)

**Trigger:** `/focus` command or session start
**Action:** Claude reads active.md + waiting.md + current project
**Result:** Shows you:

```
┌─────────────────────────────────────────────────────┐
│ FOCUS                                               │
│                                                     │
│ Active (3):                                         │
│ • [cardiac] Continue gameplan - validation section  │
│ • [arterial] Review code structure                  │
│ • [brain] Finalize workflow framework               │
│                                                     │
│ Waiting (2):                                        │
│ • [overnight] Multi-model quota fallback            │
│ • [blocked] Arterial repo location                  │
│                                                     │
│ Inbox (4 items unprocessed)                         │
│                                                     │
│ Suggested next: Continue cardiac gameplan           │
└─────────────────────────────────────────────────────┘
```

---

### Flow 4: Work (CE Loop)

**Trigger:** Pick an active item
**Action:**
1. Load project CLAUDE.md (context)
2. Load knowledge.md (past decisions)
3. Load gameplan.md (current plan)
4. Do the work (brainstorm/plan/code/review)
5. Update knowledge.md with new decisions
6. Update gameplan.md with progress

**Key insight from axtonliu:** `knowledge.md` accumulates (append-only), `gameplan.md` evolves (current state).

---

### Flow 5: Done (Archive)

**Trigger:** `/done item-description` or mark in active.md
**Action:**
1. Move item from active.md → done.md with date
2. Prompt: "Any learnings to capture?"
3. If yes → add to knowledge.md or docs/solutions/
4. Update gameplan.md if relevant

---

## Per-Project Context (The Magic)

Each project folder has:

### `CLAUDE.md` (Project-specific)
```markdown
# Cardiac Output Estimation

## Context
Predicting cardiac output from arterial waveforms using ML.
Uses code from arterial-analysis as foundation.

## Current Phase
Literature review → feature selection → model development

## Constraints
- Must use nested CV for validation
- Interpretability matters (clinicians need to understand)
- Python 3.12, scikit-learn preferred

## Key Files
- knowledge.md - all decisions so far
- gameplan.md - current execution plan
```

### `knowledge.md` (Append-Only Accumulation)
```markdown
# Knowledge: Cardiac Output

## Decisions
- 2026-02-05: Use nested CV over simple train/test (rationale: small dataset)
- 2026-02-05: Start with arterial_analysis code review before new code
- 2026-02-04: Feature selection deferred until baseline model works

## Questions Answered
- Q: Which estimator for stability? A: Defer - try multiple, compare

## Key References
- [[arterial_analysis]] codebase
- [Paper on ARX transfer functions]
```

### `gameplan.md` (Current Execution State)
```markdown
# Gameplan: Cardiac Output

## Current CE Stage
plan

## Active Plan
[[docs/plans/2026-02-05-cardiac-output-cv-analysis-plan.md]]

## Next Actions
- [ ] Review arterial_analysis code structure
- [ ] Identify reusable components
- [ ] Draft validation methodology section

## Blocked
- [ ] Find arterial_analysis repo location on disk
```

---

## Skills to Create

| Skill | Trigger | What It Does |
|-------|---------|--------------|
| `/capture` | Quick add | Append to inbox.md |
| `/process` | Daily or on demand | Walk through inbox, sort items |
| `/focus` | Session start | Show active + waiting + suggestion |
| `/done` | Item completed | Archive + prompt for learnings |
| `/review` | Weekly | Review all projects, update gameplans |
| `/compound` | After work session | Extract learnings → knowledge.md or docs/solutions/ |

---

## How This Maps to Your Existing System

| Existing | New Role |
|----------|----------|
| `tasks/pending/` | For **overnight delegation only** (formal task files) |
| `tasks/active/` | Replaced by `active.md` for human focus |
| `context/State.md` | Replaced by `/focus` command + per-project gameplan.md |
| `docs/brainstorms/` | Still used for CE brainstorm artifacts |
| `docs/plans/` | Still used for CE plan artifacts |
| `docs/solutions/` | Still used for CE compound artifacts |
| `sessions/` | **Not needed** - knowledge.md captures decisions |

---

## Overnight Pipeline (Unchanged)

The existing Gemini→Desktop pipeline stays the same:
- Formal task files in `tasks/pending/`
- Scheduler picks up and executes
- Results logged
- Task moved to `completed/`

The only change: add `/focus` awareness of waiting.md items.

---

## Lit Review Pipeline (Specialized Flow)

```
/lit-search "cardiac output estimation methods"
    → paper-search MCP finds papers
    → Add to Zotero
    → Create inbox items for each

/lit-process
    → For each paper in inbox tagged #paper:
    → Read PDF, extract key points
    → Add to NotebookLM notebook
    → Update project knowledge.md with findings

/lit-query "what validation methods are used?"
    → grounded-query skill
    → Query NotebookLM with sources
    → Source-backed answer
```

---

## What Makes This Different

1. **Single capture point** (inbox.md) - no decision about where to put things
2. **Commands, not files to maintain** - `/focus` tells you what to do
3. **Per-project context auto-loads** - CLAUDE.md + knowledge.md + gameplan.md
4. **Accumulation is automatic** - knowledge.md grows, gameplan.md stays current
5. **No State.md to maintain** - the state IS the active.md + gameplan.md files
6. **Compound step is prompted** - `/done` asks "any learnings?"

---

## Open Questions

1. **Inbox location:** Should inbox.md be in brain repo root, or in Obsidian OneVault for iPad capture?
2. **Sync:** If inbox.md is in brain repo, how do you capture from iPad?
3. **Review cadence:** Daily `/process`? Weekly `/review`? What fits your rhythm?
4. **Skill creation:** Want me to create these skills now, or refine the design first?

---

*This is v2 of the framework. Let's discuss before implementing.*
