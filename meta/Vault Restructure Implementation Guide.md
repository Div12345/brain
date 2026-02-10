---
created: 2026-02-10
tags:
  - meta
  - implementation
  - vault-restructure
status: active
---

# Vault Restructure Implementation Guide

**Overview:** Complete roadmap for transitioning from old system to unified Vault Rules architecture.
**Timeline:** Phases 3-6 (Phases 1-2 complete)
**Execution Model:** Mix of user actions + agent delegation
**Success Criteria:** All projects have Command Centers, Inbox processed, Dashboard updated

---

## Phase Overview

| Phase | Scope | Executor | Est. Time | Status |
|-------|-------|----------|-----------|--------|
| 1 | Deep audit of structures | Architect | 4h | ✓ Complete |
| 2 | Design unified system | Architect | 4h | ✓ Complete |
| 3 | Implement consistent structure | Mixed | 6-8h | ⏳ NEXT |
| 4 | Build unified dashboard | Agent | 3-4h | Pending |
| 5 | Update vault rules + docs | Agent | 2-3h | Pending |
| 6 | Architect verification | Architect | 2h | Pending |

---

## Phase 3: Implement Consistent Project Structure

**Goal:** Every project has a Command Center + sessions/ folder with consistent structure

**Projects to create Command Centers for:**
1. `Projects/phd/` - Thesis work
2. `Projects/cardiac output estimation/` - ML project
3. `Projects/room redesign/` - Interior design
4. `Projects/brain system/` - Vault architecture
5. Optionally: `Projects/smartwatch for fall detection/` (if pursuing as separate project)

### 3.1: Create Projects/phd/Command Center.md

**Executor:** You or Claude Code
**Time:** 20-30 min
**Input sources:**
- PhD annual feedback notes (from Inbox)
- January 2025 target setting note
- Arterial analysis work (connects to phd)
- Advisor notes and timeline notes

**Command Center structure:**

```markdown
---
created: 2026-02-10
tags: [project, phd, research]
project: phd
status: active
---

# PhD: Arterial Stiffness and Cardiovascular Risk

## Overview
PhD research on using arterial stiffness (measured via
ultrasound waveforms) to predict cardiovascular outcomes
in specific populations.

## Current Status
- Year: [X of Y]
- Annual feedback received [date]
- Next milestone: [description]
- Overall progress: [%]

## Inventory
- Thesis chapters: [list]
- Data sources: arterial analysis pipeline output
- Literature: [Zotero collection links]
- Advisor: [name], frequency: [how often]

## Methodology
Research approach for arterial stiffness prediction:
1. Prepare waveform signals (signal QC, detrending)
2. Select robust features (Stability Selection)
3. Build interpretable models (Nested CV)
4. Validate on held-out cohort
5. Disseminate findings (publications, thesis chapters)

## Key Decisions
- 2026-02-08: Stability Selection stabilizes feature selection in HDLSS
- 2026-[date]: Using nested CV for unbiased performance
- 2026-[date]: Arterial analysis is foundation project
- [more decisions]

## Next Actions
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

## Learning Log
See Sessions/ folder for decision records
```

**After creation:**
- Move related Inbox notes to `Projects/phd/sessions/`
- Update Dashboard/Focus.md
- Commit with message: `[project] Create phd Command Center`

---

### 3.2: Create Projects/cardiac output estimation/Command Center.md

**Executor:** You or Claude Code
**Time:** 20-30 min
**Input sources:**
- Empty brainstorm templates
- "smartcuff subproject ideation"
- Cardiac output baseline results stub
- Arterial analysis methodology (reused)

**Command Center structure:**

```markdown
---
created: 2026-02-10
tags: [project, ml, cardiac-output]
project: cardiac output estimation
status: active
---

# Cardiac Output Estimation from Arterial Waveforms

## Overview
Estimate cardiac output (volume of blood per minute)
from arterial waveforms using ML. Separate project
from arterial analysis but shares code foundation.

## Current Status
- Phase: Planning / Conceptual
- Blocker: Missing "Dr. Hahn outcomes" data file
- Timeline: [TBD after data arrival]

## Inventory
- Code foundation: arterial_analysis pipeline
- Data: [to be obtained]
- Methods: Nested CV, feature selection
- Related: [[Projects/arterial analysis/]]

## Methodology
Similar to arterial analysis but targets different outcome:
1. Prepare waveforms (same signal QC)
2. Extract features (same feature selection methods)
3. Build CO estimators (regression + interpretability)
4. Validate on independent cohort
5. Compare vs existing CO measurement methods

## Key Decisions
- 2026-02-[date]: Separate from arterial analysis (different endpoint)
- [other decisions as they arise]

## Next Actions
- [ ] Locate "Dr. Hahn outcomes" file
- [ ] Understand outcome variable format
- [ ] Design validation split
- [ ] Begin code adaptation

## Blocking Issues
- DATA: "Dr. Hahn outcomes" file missing
  - Check: Email attachments? Downloads folder? Shared drive?
  - Action: Send to [[Projects/cardiac output estimation/data/]]

## Learning Log
Links to sessions as work progresses
```

**After creation:**
- Mark as blocked until data file found
- Update Dashboard/Focus.md with blocker
- Commit with message: `[project] Create cardiac output Command Center (blocked on data)`

---

### 3.3: Create Projects/room redesign/Command Center.md

**Executor:** You or Claude Code
**Time:** 20-30 min
**Input sources:**
- House organization notes
- Small space strategies notes
- Cooking in small space notes
- Inspiration Pinterest/photos (if any)

**Command Center structure:**

```markdown
---
created: 2026-02-10
tags: [project, design, personal]
project: room redesign
status: planning
---

# Room Redesign: Optimizing Small Living Space

## Overview
Interior design project to improve functionality and
aesthetics of [specific room/space]. Focus on storage,
organization, and quality of life.

## Current Status
- Phase: Inspiration + Planning
- Constraints: Small space, [other constraints]
- Timeline: [TBD]

## Inventory
- Current setup: [description]
- Key pain points: [list]
- Inspiration sources: [links/references]
- Budget: [if known]

## Methodology
Design approach:
1. Assess current space (measure, photograph, constraints)
2. Identify key needs (storage? aesthetics? function?)
3. Research solutions (organization systems, furniture options)
4. Create design (sketches, Pinterest board, etc.)
5. Implement iteratively

## Key Decisions
- 2026-02-[date]: Prioritize [storage|aesthetics|function]
- [other decisions as they arise]

## Next Actions
- [ ] Measure room (dimensions, ceiling height, outlets)
- [ ] Take reference photos (current state)
- [ ] Define priority (1 thing that matters most)
- [ ] Research [category] solutions
- [ ] Create Pinterest board / mood board

## Learning Log
Links to sessions as work progresses
```

**After creation:**
- Move related Inbox notes to `Projects/room redesign/sessions/`
- Update Dashboard/Focus.md
- Commit with message: `[project] Create room redesign Command Center`

---

### 3.4: Create Projects/brain system/Command Center.md

**Executor:** Claude Code or overnight
**Time:** 30-40 min
**Input sources:**
- Vault Rules.md (this system)
- Dashboard/Focus.md (just created)
- Compound Engineering article note
- Overnight brainstorms (cooking, inbox analysis)
- HOME.md, ACTIVE.md, context files

**Command Center structure:**

```markdown
---
created: 2026-02-10
tags: [project, system, ai-coordination]
project: brain system
status: active
---

# Brain System: Multi-Interface AI Coordination Vault

## Overview
Self-evolving vault system coordinating Claude Desktop,
Claude Code, and overnight agents to anticipate needs and
compound learnings systematically.

## Current Status
- Phase: Vault restructure (phases 3-6)
- Architecture: Projects / Knowledge / Meta split
- Interfaces: Desktop (Opus 4.6), Code (this), Overnight (scheduler)
- Key capability: Compound engineering loop automation

## Inventory
- Main vault: /home/div/brain/ (WSL) + /mnt/c/Users/din18/brain/ (Windows)
- Completed work: cooking consolidation, overnight audit
- Systems: compound loop, inter-agent messaging, scheduling
- Documentation: Vault Rules.md, meta/

## Methodology
Compound Engineering Loop applied to vault operations:
1. **Work** - Agent executes task (research, consolidation, analysis)
2. **Assess** - Review outcomes and decisions
3. **Compound** - Extract learnings, update Rules, feed into next task
4. **Repeat** - Each task makes next task easier

Key principle: **The system should improve with each work session.**

## Key Decisions
- 2026-02-10: Projects ≠ Knowledge (different lifecycles)
- 2026-02-10: Command Centers are single source of truth per project
- 2026-02-10: Vault split into Projects / Knowledge / Meta for clarity
- 2026-02-10: Cooking consolidation proves Command Center effectiveness
- 2026-02-08: Overnight agent can autonomously restructure vault
- 2026-02-08: Stability Selection + Nested CV for ML pipelines

## Next Actions
- [ ] Create remaining project Command Centers (phd, cardiac, room, smartwatch)
- [ ] Process remaining ~150 Inbox notes
- [ ] Build Dashboard/Focus.md cross-project view
- [ ] Establish Personal/ folder conventions
- [ ] Archive superseded system notes
- [ ] Document lessons learned in docs/solutions/

## Blocking Issues
- None - on critical path

## Learning Log
- [[docs/solutions/2026-02-05-obsidian-vault-analysis-without-mcp.md]] - Initial audit
- [[docs/solutions/workflow-issues/2026-02-08-cc-web-vault-org-session-salvage.md]] - Session salvage
- [[docs/brainstorms/.overnight-cooking-summary.md]] - Cooking consolidation
- [[docs/brainstorms/.overnight-inbox-analysis.md]] - Inbox deep analysis
- [[meta/Vault Rules.md]] - System architecture
```

**After creation:**
- Update Dashboard/Focus.md to show this project
- Commit with message: `[project] Create brain system Command Center`

---

### 3.5: Move Gem Notes to Projects

**Executor:** You or Claude Code
**Time:** 10-15 min per note
**Input:** The 5 gems identified by overnight agent

**Gem 1: interpretable machine learning.md**
- Current location: Inbox
- New location: `Projects/arterial analysis/interpretable-machine-learning.md`
- Rationale: Core methodology for pipeline explainability
- Action: Move file, update wikilinks, link from Command Center

**Gem 2: medical ML interpretability.md**
- Current location: Inbox
- New location: `Projects/arterial analysis/medical-ml-interpretability.md`
- Rationale: Stakeholder requirements for clinical deployment
- Action: Move file, consider merging with Gem 1, update links

**Gem 3: Feb 19 results with comments.md**
- Current location: Inbox
- New location: `Projects/arterial analysis/data-results/feb-19-results.md`
- Rationale: Research output, dense performance metrics
- Action: Create data-results/ folder, move file, link from Command Center

**Gem 4: Compound Engineering article**
- Current location: Inbox (full Every.to article)
- New location: `Projects/brain system/compound-engineering-article.md`
- Rationale: Philosophical foundation for brain system approach
- Action: Move, add to brain system Knowledge Log

**Gem 5: literature review completion on feature selection, evaluation.md**
- Current location: Inbox
- New location: `Projects/arterial analysis/sessions/2026-02-10-lit-review-planning.md`
- Rationale: Active planning for pipeline finalization
- Action: Move, convert open questions to checklist in arterial Command Center

**After all moves:**
- Update arterial Command Center with links to new locations
- Update brain system Command Center with article reference
- Update Dashboard/Focus.md with completed moves
- Commit with message: `[move] Relocate gem notes to project homes`

---

### 3.6: Standardize All Project Structures

**Executor:** Agent (script or batch)
**Time:** 20-30 min
**Scope:** Ensure all projects have consistent folder structure

**Target structure for each project:**

```
Projects/{name}/
├── Command Center.md          # REQUIRED - Single source of truth
├── sessions/                  # REQUIRED - Time-stamped decision records
│   ├── 2026-02-08-[topic].md
│   └── 2026-02-10-[topic].md
├── data/                      # OPTIONAL - Project-specific data
└── [other-folders-as-needed]
```

**Checklist for each project:**
- [ ] Command Center.md exists
- [ ] Sessions/ folder exists and has ≥1 session file
- [ ] All project notes link back to Command Center
- [ ] All sessions have proper frontmatter
- [ ] Project is linked from Dashboard/Focus.md

---

## Phase 4: Build Unified Dashboard

**Goal:** Create Dashboard/Focus.md that shows all projects at a glance
**Executor:** Claude Code or agent
**Time:** 3-4 hours
**Status:** Currently in progress (Focus.md drafted)

### Tasks:

1. **Dashboard/State.md enhancement**
   - Update with latest decisions from all projects
   - Add "recent wins" section
   - Link to latest sessions

2. **Dashboard/Focus.md completion** (drafted above)
   - Show all active projects
   - Inbox status
   - Suggested next actions
   - Waiting items

3. **Create Dashboard/Graph Analysis**
   - Identify high-hub notes (most links)
   - Identify orphans (zero links)
   - Suggest connection opportunities
   - Tag distribution analysis

4. **Create Dashboard/Weekly Review Template**
   - Quick format for reviewing progress
   - Questions to ask each project
   - Inbox processing status
   - Recommendations for next week

---

## Phase 5: Update Vault Rules and Docs

**Goal:** Ensure documentation matches implemented system
**Executor:** Agent with user review
**Time:** 2-3 hours

### Tasks:

1. **Vault Rules.md review and finalization** (done above)
   - Incorporate feedback from implementation
   - Add any patterns discovered
   - Add FAQ from user questions

2. **Update HOME.md**
   - Point to new Dashboard
   - Link to Vault Rules.md
   - Update navigation
   - Remove outdated sections

3. **Update ACTIVE.md**
   - Expand to show project ownership
   - Link to Command Centers
   - Link to Dashboard/Focus.md

4. **Update CLAUDE.md**
   - Point to Vault Rules.md for system architecture
   - Link to Dashboard/Focus.md for priorities
   - Update instructions for working in this vault

5. **Create meta/System Operations Handbook**
   - How to add a new project
   - How to archive a completed project
   - How to handle sensitive notes
   - How to update Command Centers
   - How to run Compound Engineering loop

6. **Archive deprecated docs**
   - `obsidian-conventions.md` → keep as reference, mark deprecated
   - Flow-First Framework v2 → archive with note about what was adopted
   - Old CLAUDE.md sections → archive

---

## Phase 6: Architect Verification

**Goal:** Verify system completeness and consistency
**Executor:** Architect (you or designated reviewer)
**Time:** 2 hours
**Checklist:**

**Structure completeness:**
- [ ] All 6 projects have Command Centers
- [ ] All projects have sessions/ folders
- [ ] All Command Centers have required sections
- [ ] All sessions have proper frontmatter

**Inbox processing:**
- [ ] ~150 remaining notes categorized
- [ ] Gems moved to projects
- [ ] Stale content archived
- [ ] User decisions captured (sensitive notes)
- [ ] All remaining notes linked to appropriate systems

**Documentation:**
- [ ] Vault Rules.md complete and accurate
- [ ] Dashboard/Focus.md reflects current state
- [ ] HOME.md updated
- [ ] CLAUDE.md updated
- [ ] All deprecations documented

**Knowledge graph health:**
- [ ] Run orphan analysis (zero-link notes)
- [ ] Run hub analysis (high-link notes)
- [ ] Check for broken wikilinks
- [ ] Verify cross-project links appropriate

**Verification output:**
- Create `docs/solutions/2026-02-10-vault-restructure-complete.md`
- Document any issues found and how they were resolved
- List recommendations for ongoing vault health

---

## Execution Timeline Suggested

**Day 1 (2026-02-10):**
- [ ] Review Vault Rules.md and Focus.md (15 min)
- [ ] Create Projects/phd/Command Center.md (30 min)
- [ ] Create Projects/brain system/Command Center.md (40 min)
- **Total: 85 min**

**Day 2 (2026-02-11):**
- [ ] Create Projects/cardiac output estimation/Command Center.md (30 min)
- [ ] Create Projects/room redesign/Command Center.md (30 min)
- [ ] Move 5 gem notes to projects (45 min)
- [ ] Commit all changes (5 min)
- **Total: 110 min**

**Day 3+ (2026-02-12+):**
- [ ] Process remaining ~150 Inbox notes (batches, 20-30 min per batch)
- [ ] Overnight agent: Build Dashboard enhancements
- [ ] Overnight agent: Update documentation
- [ ] Architect: Verify and document

---

## Risk Mitigation

**Risk: Losing context during moves**
- Mitigation: Keep detailed session records of what moved where
- Commit frequently after each major move
- Use batch commits with clear messages

**Risk: Broken wikilinks**
- Mitigation: Use Obsidian's "Broken links" view to catch misses
- Test graph view before finalizing
- Create redirect note if name changes

**Risk: Notes don't fit categories**
- Mitigation: This is okay - use Personal/, Clippings/, or create new categories
- Document the exception in that note's frontmatter
- Revisit during monthly reviews

**Risk: User hasn't decided on sensitive notes**
- Mitigation: Create Personal/ folder structure anyway
- Move notes there with clear explanations
- User can review and organize later

---

## Success Metrics

**After Phase 6 complete:**

1. **Structure:** ✓ All 6 projects have Command Centers + sessions
2. **Inbox:** ✓ <50 unprocessed notes (rest categorized/archived)
3. **Documentation:** ✓ Vault Rules describe actual system
4. **Graph health:** ✓ <20 orphan notes, 0 broken links
5. **User experience:** ✓ Can quickly navigate to any active project
6. **Compound ready:** ✓ System positioned to systematically improve

---

## See Also

- [[meta/Vault Rules.md]] - System architecture
- [[Dashboard/Focus.md]] - Current priorities
- [[Dashboard/State.md]] - Recent decisions
- [[Projects/cooking/Command Center.md]] - Example of complete Command Center

---

**Document created:** 2026-02-10
**Last updated:** 2026-02-10
**Next review:** 2026-02-12 (after Phase 3 completion)
