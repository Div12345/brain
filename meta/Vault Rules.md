---
created: 2026-02-10
tags:
  - meta
  - vault
  - rules
status: active
updated: 2026-02-10T00:00
---

# Vault Rules: Unified System Architecture

**Version:** 2.0
**Effective:** 2026-02-10
**Replaces:** `obsidian-conventions.md` (deprecated), Flow-First Framework v2 (partially implemented)
**Status:** Active - implements overnight work + architect synthesis

> **Quick Start:** New to this vault? Read [[#Quick Reference]] first, then [[#The Three Systems]].

---

## Quick Reference

| Need | Go To | Why |
|------|-------|-----|
| What should I work on? | `Dashboard/Focus.md` | Shows active items across all projects |
| Quick note capture | `Inbox/Inbox.md` | Zero-friction, no decisions |
| Understanding a project | `Projects/{name}/Command Center.md` | Single source of truth for that project |
| Learning what changed | `Projects/{name}/sessions/` | Time-stamped decision records |
| Extracting learnings | `docs/solutions/` | Compound artifacts from completed work |
| System rules | This file (Vault Rules.md) | What goes where and why |
| How to structure something | `templates/` | Templates for sessions, projects, etc. |

---

## The Three Systems

The vault contains three distinct but interconnected systems:

### 1. **Projects System** (Goal-Oriented Work)
**Location:** `Projects/{project-name}/`
**Lifetime:** Has a beginning and end
**Definition:** Work toward a specific outcome (thesis research, feature, analysis)
**Examples:** `arterial analysis`, `cooking`, `phd`, `cardiac output estimation`, `room redesign`

**Each project contains:**
- `Command Center.md` - Single document consolidating all project knowledge
- `sessions/` - Time-stamped decision records and progress notes
- `data/` - Project-specific data files (optional)

**Project Command Center includes:**
1. **Current Status** - What's in progress, what's blocked
2. **Inventory** - What exists (data, code, findings, recipes, etc.)
3. **Methodology** - How we work on this (ML pipeline, cooking system, study design, etc.)
4. **Key Decisions** - Rationale for approach taken
5. **Next Actions** - What comes next
6. **Learning Log** - What we've discovered

### 2. **Knowledge System** (Concepts & Patterns)
**Location:** `knowledge/`
**Lifetime:** Evergreen (true across many contexts)
**Definition:** Concepts, frameworks, research findings with cross-project application
**Examples:** `ai-memory-systems.md`, `stability-selection.md`, `compound-engineering.md`

**Key Rules:**
- One clear idea per note (rule: "if you can't explain it in one sentence, split it")
- 2+ internal links (evidence of connection to larger graph)
- Proper tags (`#knowledge`, domain tag, status)
- Should be reusable across multiple projects

**Structure:**
- `knowledge/research/` - External findings (papers, articles, research)
- `knowledge/patterns/` - Observed behaviors and best practices
- `knowledge/frameworks/` - Architectural patterns and evaluation frameworks
- `knowledge/tools/` - Tool configurations and integration guides
- `knowledge/skills/` - AI agent skill definitions and workflows

### 3. **Meta System** (System Operations)
**Location:** `meta/`, `context/`, `Dashboard/`, `templates/`
**Lifetime:** Current cycle (can be versioned and retired)
**Definition:** How the vault itself works, current state, coordination

**Components:**
- `meta/Vault Rules.md` - This file. System architecture and rules.
- `meta/obsidian-conventions.md` - Formatting (YAML, tags, naming)
- `Dashboard/State.md` - Current focus and recent decisions
- `Dashboard/Focus.md` - What to work on now (auto-generated or manual)
- `context/` - Shared state, handoffs, predictions
- `Inbox/Inbox.md` - Capture point for fleeting thoughts
- `templates/` - Templates for consistent formatting

---

## The Unified Structure

```
brain/
├── Dashboard/
│   ├── State.md              # Current focus & recent decisions
│   └── Focus.md              # What to work on (active items)
│
├── Projects/                 # Goal-oriented work
│   ├── arterial analysis/
│   │   ├── Command Center.md
│   │   └── sessions/
│   ├── cooking/
│   │   ├── Command Center.md
│   │   └── sessions/
│   ├── phd/
│   │   ├── Command Center.md
│   │   └── sessions/
│   ├── cardiac output estimation/
│   │   ├── Command Center.md
│   │   └── sessions/
│   ├── room redesign/
│   │   ├── Command Center.md
│   │   └── sessions/
│   └── brain system/
│       ├── Command Center.md
│       └── sessions/
│
├── knowledge/                # Concepts & patterns (evergreen)
│   ├── research/             # External findings
│   ├── patterns/             # Observed behaviors
│   ├── frameworks/           # Architectural patterns
│   ├── tools/                # Tool guides
│   └── skills/               # AI skill definitions
│
├── Inbox/
│   └── Inbox.md              # Fleeting captures
│
├── Archive/                  # Deprecated/completed items
│   ├── Cooking Originals/    # Original 58 cooking notes
│   └── ... (other archived content)
│
├── Personal/                 # Sensitive personal content
│   ├── Fleeting/             # Philosophy, emotional captures
│   └── Growth/               # Therapy, identity exploration
│
├── docs/                     # Compound Engineering artifacts
│   ├── brainstorms/          # CE brainstorm outputs
│   ├── plans/                # CE plan outputs
│   └── solutions/            # CE compound outputs (learnings)
│
├── meta/                     # System documentation
│   ├── Vault Rules.md        # ← You are here
│   ├── obsidian-conventions.md
│   └── contribution-workflow.md
│
├── templates/                # Templates for consistent format
├── context/                  # Shared state & coordination
├── agents/                   # Agent definitions
├── tasks/                    # Formal task queue (for overnight)
├── tools/                    # Scripts and configs
├── messages/                 # Inter-agent messaging
└── logs/                     # Activity logs
```

---

## Rule 1: Projects Are Not Knowledge

**Core Principle:** Keep project work separate from conceptual knowledge.

**Projects:**
- Have a clear start and end
- Accumulate context and decisions
- Belong in `Projects/{name}/`
- Link TO knowledge, not vice versa

**Knowledge:**
- Applies across multiple projects
- Evergreen and reusable
- Belong in `knowledge/`
- Concepts that will outlast the project

**Example:**
- `Projects/arterial analysis/Command Center.md` = Project (specific goal: build ML pipeline)
- `knowledge/research/stability-selection.md` = Knowledge (reusable across multiple ML projects)
- The project links to the knowledge note

---

## Rule 2: Command Centers Are The Single Source of Truth

**Every project has exactly ONE command center:** `Projects/{name}/Command Center.md`

**Purpose:** Consolidate all project knowledge into one living document so you never have to search.

**Structure (must include these sections):**

1. **Overview** - One-sentence description of what this project is about
2. **Current Status** - Where are we now? (1-2 sentences)
3. **Inventory** - What exists?
   - For arterial analysis: codebase modules, data files, decision list
   - For cooking: ingredients by storage, meal stacks, shopping rules
   - For PhD: thesis chapters, timeline, advisor feedback
4. **Methodology** - How do we work on this?
   - For arterial analysis: ML pipeline diagram + frameworks
   - For cooking: 5-component stack system
   - For PhD: research methodology
5. **Key Decisions** - Why did we choose this approach?
   - Dated list of major decisions with rationale
6. **Next Actions** - What comes next? (checkbox list)
7. **Learning Log** - What have we discovered? (links to sessions/)

**Example from cooking:**
- **Inventory** lists 47 ingredients organized by storage (Fridge/Freezer/Pantry)
- **Methodology** explains the 5-component stack framework
- **Key Decisions** explain why frozen > fresh, why Trader Joe's
- **Next Actions** includes batch shopping, recipe testing
- **Learning Log** links to sessions with new discoveries

---

## Rule 3: Sessions Are Time-Stamped Decision Records

**Location:** `Projects/{name}/sessions/`
**Naming:** `YYYY-MM-DD-brief-topic.md` or `YYYY-MM-DD-session-type-topic.md`
**Frequency:** At least one per meaningful work block (can be daily or weekly)

**Required frontmatter:**
```yaml
---
date: YYYY-MM-DD
project: {project-name}
interface: cc|desktop|overnight
ce_stage: brainstorm|plan|work|assess|compound
tags:
  - session
status: draft|active|complete
---
```

**Must contain:**
1. **Context** - What was I trying to do?
2. **Key Points** - Main discoveries or work
3. **Decisions Made** - Every session must capture ≥1 decision (even "defer X")
4. **Questions Raised** - Open questions
5. **Next Actions** - What should happen next?

**After meaningful sessions:** Include "Compounds To" section linking to the appropriate `docs/solutions/` file created by the Compound step.

**Example:** `Projects/arterial analysis/sessions/2026-02-08-methodology-research-synthesis.md` captured the decision that Stability Selection + Nested CV are complementary, not competing.

---

## Rule 4: Knowledge Notes Are Developed, Not Stubs

**Red Flag Words (suggests it's not ready):**
- "TODO" at the top level
- "Maybe", "possibly", "could be"
- Single paragraph with no structure
- No tags
- Zero internal links

**Minimum viable knowledge note:**
- Clear one-sentence summary (first line after frontmatter)
- 2+ internal wikilinks to related concepts
- At least one section header for organization
- Proper tags: `#knowledge`, domain tag, status tag
- Evidence: Where did this idea come from? (cite source, project, or experience)

**Example: GOOD**
```markdown
---
created: 2026-02-08
tags: [knowledge, ml-feature-selection, research]
status: active
---

# Stability Selection in High-Dimensional Spaces

Stability Selection is a meta-method that stabilizes feature selection in finite samples
by running the base selector on many subsamples and keeping features selected in >60% of runs.

## When to Use
- HDLSS (High-Dimensional, Low-Sample-Size) regime
- Base selector is unstable (e.g., LASSO in finite samples)
- See also: [[Nested Cross-Validation]] for performance estimation

## Framework
(detailed content with references)
```

**Example: AVOID**
```markdown
# Stability Selection

TODO: fill this in

Maybe it's like bootstrapping?
```

---

## Rule 5: Archive Decisively

**What goes to Archive:**
- Completed projects (keep them, but clearly retired)
- Superseded system notes (old vault structure docs)
- Time-expired logistics (housing search 2025, past travel)
- Stale captures that won't be developed (philosophy fragments, tool lists)
- Original ingredient notes, recipe stacks (after consolidation into Command Center)

**Archive process:**
1. Create dated folder in `Archive/` explaining what's archived and why
2. Move the notes there
3. Update context/State.md with "archived X because Y"
4. Optional: Keep one summary note in the main system linking to the archive

**Why not just delete?**
- Preserve history and rationale
- Allow recovery if you change your mind
- Document what was tried and abandoned

---

## Rule 6: Inbox Is Zero-Friction Capture

**Location:** `Inbox/Inbox.md`
**Format:** No frontmatter, no tags, no structure required
**Purpose:** Dump fleeting thoughts, then process them later

**What goes here:**
- Quick ideas ("use Stability Selection for feature selection")
- Questions ("how do I validate cardiac output?")
- Observations ("frozen > fresh saves 20 min")
- Reminders ("find Dr. Hahn outcomes file")
- Incomplete thoughts (anything that might be useful)

**What does NOT go here:**
- Research outputs (these go straight to project sessions/)
- Finished decisions (these go to Command Centers)
- Knowledge concepts (these go to knowledge/)

**Processing:**
When you have time (daily or weekly), review Inbox and decide:
- **Move to project Command Center** (important for that project)
- **Move to project sessions/** (decision record)
- **Move to knowledge/** (if it's a reusable concept)
- **Move to Personal/** (if it's sensitive or philosophical)
- **Archive** (captured but not useful)
- **Delete** (captured but now stale)

---

## Rule 7: Personal/Fleeting Notes Have a Home

**Location:** `Personal/Fleeting/` or `Personal/Growth/`
**Why separate?** These aren't "knowledge" but deserve preservation
**Examples:** Gender exploration, therapy reflections, philosophical captures, emotional processing

**Rule:** These are ephemeral and OKAY to not compound. Archive monthly.

---

## Rule 8: Frontmatter Is Consistent

All notes (except Inbox) have:
```yaml
---
created: YYYY-MM-DD
tags:
  - primary-category
  - secondary-context
status: draft|active|complete|archived
---
```

**Tags taxonomy:**

**Content types:**
- `#knowledge` - Concept note
- `#project` - Active project
- `#session` - Decision record
- `#research` - External finding
- `#pattern` - Observed behavior
- `#framework` - System/architecture

**Domains:**
- `#ml-feature-selection`, `#ml-interpretability` - ML topics
- `#cooking`, `#phd`, `#arterial-analysis` - Project tags
- `#obsidian`, `#tools` - System topics

**Status:**
- `#status/draft` - Early stage
- `#status/active` - Being developed
- `#status/complete` - Ready to use
- `#status/archived` - Retired

---

## Rule 9: Links Connect Ideas

Use `[[wikilinks]]` liberally:
- **Knowledge notes link TO each other** (concepts relate)
- **Project notes link to knowledge** (projects use concepts)
- **Sessions link to Command Centers** (decisions feed the main doc)
- **Cross-project links are rare** (projects are mostly independent)

**Anti-pattern:** Orphan notes (notes with zero inbound/outbound links). If you write it, link it.

---

## Rule 10: The Compound Engineering Loop

After meaningful work sessions:

1. **Work** - Do the thing (research, build, write)
2. **Assess** - Review what you did
3. **Compound** - Extract learnings:
   - Update project Command Center with new decisions
   - Add to project session record with what you learned
   - Create `docs/solutions/` file if it's a generalized insight
   - Update relevant knowledge notes if frameworks evolved
4. **Repeat** - Next session builds on documented learning

**Example:** The overnight agent's cooking consolidation:
- **Work**: Analyzed 58 cooking notes
- **Assess**: Identified patterns (5-component system, energy levels, storage strategy)
- **Compound**: Created `Projects/cooking/Command Center.md` consolidating all knowledge
- **Result**: User has one living document instead of 58 scattered notes

---

## Rule 11: Projects Can Have Sub-Projects

**When to create a sub-project:**
- It has a different timeline or team
- It could be useful in other contexts
- It has enough complexity to deserve its own Command Center

**Example structure:**
```
Projects/
├── arterial analysis/
│   ├── Command Center.md
│   └── sessions/
├── cardiac output estimation/
│   ├── Command Center.md
│   └── sessions/
└── smartwatch for fall detection/
    ├── Command Center.md
    └── sessions/
```

These are separate projects, not sub-folders, because they have different scopes and timelines.

---

## Current Project Inventory

**Status as of 2026-02-10:**

| Project | Status | Command Center | Notes |
|---------|--------|-----------------|-------|
| **arterial analysis** | Active | `Projects/arterial analysis/Command Center.md` | ML pipeline for arterial stiffness prediction |
| **cardiac output estimation** | Active | Planned | Separate project, reuses arterial code |
| **phd** | Active | Planned | Thesis work, uses arterial analysis + cardiovascular theory |
| **cooking** | Active | ✓ Complete | 47 ingredients + 9 stacks consolidated by overnight |
| **room redesign** | Planning | Planned | Interior design for small space |
| **brain system** | Active | Planned | This vault's architecture and AI coordination |

---

## Inbox Status & Next Steps

**Current state (2026-02-10):**
- ~180 notes remain in Inbox after overnight work
- Overnight completed: cooking consolidation + analysis of non-cooking notes
- Pending: User review of overnight recommendations, decisions on sensitive notes

**Overnight recommendations:**
1. Create `Projects/phd/Command Center.md`
2. Create `Projects/cardiac output estimation/Command Center.md`
3. Create `Projects/room redesign/Command Center.md`
4. Batch-move research notes to appropriate project folders
5. Decide: `Personal/` folder for gender/therapy notes?
6. Archive philosophy fragments unless planning to develop

---

## Design Decisions Captured

**Why Projects, not folders?**
- Projects have beginnings and ends; folders don't
- Each project needs a Command Center consolidating knowledge
- Projects can be completed and archived; folders are structural

**Why Command Centers?**
- Prevents information scatter across multiple notes
- Single source of truth per project
- Easier to onboard someone else to the project
- Consolidates decisions + inventory + methodology

**Why separate Knowledge?**
- Reusable across projects
- Outlasts projects
- Deserves evergreen treatment
- Different evolution pattern (knowledge grows, projects end)

**Why Inbox?**
- Zero friction for fleeting thoughts
- Batching decision (process weekly, not immediately)
- Prevents premature structure that kills capture instinct

**Why sessions/ instead of logs/?**
- Emphasizes decision records, not just activity logs
- Timestamped for traceability
- Connected to projects, not global
- Sessions compound into Command Centers

---

## Migration Path from Old System

**Old structure had:**
- `02 - Knowledge/` (knowledge folder, legacy)
- Scattered project notes in Inbox
- `tasks/` for formal work
- `context/State.md` for overall state

**New system replaces with:**
- `Projects/{name}/Command Center.md` (replaces scattered notes)
- `knowledge/` (replaces `02 - Knowledge/`)
- `Dashboard/Focus.md` (replaces `tasks/` for human focus)
- `Dashboard/State.md` (replaces `context/State.md`)
- `Inbox/Inbox.md` (new capture system)

**Execution steps:**
1. ✓ Phase 1: Overnight agent audited all structures
2. ✓ Phase 2: Overnight created cooking Command Center
3. ⏳ Phase 3: Create Command Centers for remaining projects (phd, cardiac output, room redesign, brain system)
4. ⏳ Phase 4: Batch-move research notes to projects/
5. ⏳ Phase 5: Archive old system notes
6. ⏳ Phase 6: Update Dashboard/Focus.md with cross-project view

---

## For Agents Working in This Vault

**Key responsibilities:**
1. **Read Vault Rules** before starting work (this file)
2. **Update project Command Center** after sessions
3. **Create sessions/ notes** for decision records
4. **Link aggressively** - new notes should link to existing concepts
5. **Archive stale content** - don't let notes rot
6. **Compound systematically** - extract learnings after work

**Common agent tasks:**
- **Research synthesis** → Create/update knowledge note, link from project
- **Project work** → Update Command Center, create session record
- **Vault restructuring** → Batch-move with clear rationale, document in Dashboard/State.md
- **Inbox processing** → Categorize and move to appropriate system

---

## FAQ

**Q: Where do I put a literature note?**
A: If it's for a specific project, link it from the project Command Center. If it's a foundational concept (like Stability Selection), give it a Knowledge note.

**Q: Can I have sub-folders in Projects/?**
A: Yes, e.g., `Projects/arterial analysis/sessions/` and `Projects/arterial analysis/data/`. But each project has exactly one Command Center at the top level.

**Q: How often should I create sessions?**
A: At least after each meaningful work block. Could be daily if you work daily, weekly if you work in batches.

**Q: What if a note doesn't fit any category?**
A: If it's personal/fleeting, go to `Personal/`. If it's a capture you're not sure about, put it in `Inbox/` and decide later. If it's truly one-off, consider archiving rather than hoarding.

**Q: Should I delete old projects?**
A: No. Archive them in `Archive/{project-name}/` with a summary explaining why and when. Preserve history.

**Q: How do I handle collaborative projects?**
A: Each collaborator can have a session file. The Command Center is the merge point for shared understanding.

---

## See Also

- [[meta/obsidian-conventions.md]] - YAML and formatting rules
- [[Dashboard/State.md]] - Current focus and decisions
- [[templates/session-note.md]] - Template for new sessions
- [[meta/contribution-workflow.md]] - How to contribute to this vault

---

**Last updated:** 2026-02-10
**Next review:** 2026-03-10 (monthly check-in)
**Supersedes:** obsidian-conventions.md (partial), flow-first-framework-v2.md (partial implementation)
