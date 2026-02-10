---
created: 2026-02-10
tags:
  - dashboard
  - focus
  - coordination
status: active
updated: 2026-02-10T00:00
---

# What To Work On Now

> Auto-generated or manually updated daily. Shows active items across all projects.
> See [[meta/Vault Rules.md]] for system architecture.

---

## Active Projects (In Progress)

### 1. Arterial Analysis (ML Pipeline)
**Status:** Code audit underway, methodology settled
**Current Phase:** Audit V2 - systematic module-by-module review with pytest output + determinism checks
**Owner:** Claude Desktop (Opus 4.6)
**Conversation:** b2de2d54-5ed2-4ed0-a345-4a7f32821903

**Next Actions:**
- [ ] Complete Audit V2 systematic review
- [ ] Trace feature selection leakage (file:line)
- [ ] Trace random state inventory (file:line)
- [ ] Save pytest output in docs/

**Blocked By:**
- None currently

**See Also:** [[Projects/arterial analysis/Command Center.md]]

---

### 2. Cooking System (Inventory + Recipes)
**Status:** ✓ COMPLETE - Command Center created
**Current Phase:** Live usage + refinement
**Owner:** You + overnight vault agent
**Output:** `Projects/cooking/Command Center.md` (47 ingredients + 9 stacks)

**What Was Done:**
- Consolidated 58 scattered cooking notes into one Command Center
- Organized ingredients by storage location (Fridge/Freezer/Pantry)
- Organized meals by energy level (Zero/Low/Medium/High Project)
- Captured 5-component stack framework (Base+Protein+Veggie+Sauce+Crunch)
- Extracted shopping rules and learned patterns

**Next Actions:**
- [ ] Use Command Center for daily meal planning
- [ ] Test energy-level categorization
- [ ] Add new batches as you shop
- [ ] Update learned patterns as you discover new combinations

**See Also:** [[Projects/cooking/Command Center.md]]

---

### 3. PhD / Thesis Work
**Status:** Needs Command Center
**Current Phase:** Annual feedback received, target setting in progress
**Owner:** You
**Evidence:** Annual feedback notes, target setting notes in Inbox

**Next Actions:**
- [ ] Create `Projects/phd/Command Center.md`
- [ ] Inventory: thesis chapters, timeline, advisor feedback
- [ ] Methodology: research approach for arterial stiffness work
- [ ] Key Decisions: why this research matters, why this approach
- [ ] Learning Log: link to arterial analysis work

**Blocked By:**
- Needs Command Center creation (assign to CC or overnight)

**See Also:** [[Projects/phd/Command Center.md]] (planned)

---

### 4. Cardiac Output Estimation
**Status:** Needs Command Center
**Current Phase:** Conceptual (reuses arterial analysis code)
**Owner:** You
**Evidence:** Empty brainstorm templates, methodology notes

**Next Actions:**
- [ ] Create `Projects/cardiac output estimation/Command Center.md`
- [ ] Inventory: what exists (data? code foundation?)
- [ ] Methodology: how it differs from arterial analysis
- [ ] Key Decisions: why separate project vs part of arterial?
- [ ] Next Actions: what comes first?

**Blocked By:**
- Missing data file ("Dr. Hahn outcomes")
- Needs Command Center creation

**See Also:** [[Projects/cardiac output estimation/Command Center.md]] (planned)

---

### 5. Room Redesign (Interior Design)
**Status:** Needs Command Center
**Current Phase:** Planning / inspiration gathering
**Owner:** You
**Evidence:** House organization notes, space strategy notes in Inbox

**Next Actions:**
- [ ] Create `Projects/room redesign/Command Center.md`
- [ ] Inventory: current situation (room dimensions, constraints)
- [ ] Methodology: design principles for small spaces
- [ ] Key Decisions: priorities (storage? aesthetics? function?)
- [ ] Next Actions: first steps (measure? sketch? shop?)

**Blocked By:**
- Needs Command Center creation

**See Also:** [[Projects/room redesign/Command Center.md]] (planned)

---

### 6. Brain System (Vault + AI Coordination)
**Status:** Architecture active, implementation ongoing
**Current Phase:** Vault restructure completion + dashboard setup
**Owner:** Claude Code + overnight
**Evidence:** This file, Vault Rules.md, overnight brainstorms

**Next Actions:**
- [ ] Create `Projects/brain system/Command Center.md`
- [ ] Inventory: what's complete (cooking consolidation, overnight pipeline, CC hooks)
- [ ] Methodology: compound engineering loop + multi-interface coordination
- [ ] Key Decisions: why this architecture (projects vs knowledge vs meta)
- [ ] Learning Log: patterns from vault restructuring

**See Also:** [[Projects/brain system/Command Center.md]] (planned)

---

## Inbox Processing Status

**Total Inbox notes:** ~180 (after cooking consolidation)
**Processed:** ~30 (cooking + non-cooking analysis by overnight)
**Pending:** ~150

### What the Overnight Agent Found

**Gems to keep and develop:**
1. `interpretable machine learning.md` - Comprehensive concept note (move to Projects/arterial analysis/)
2. `medical ML interpretability.md` - Stakeholder×explanation matrix (move to Projects/arterial analysis/)
3. `Feb 19 results with comments.md` - Dense research output (move to Projects/arterial analysis/data-results/)
4. `Compound Engineering How Every Codes With Agents.md` - Full Every.to article (move to Projects/brain system/)
5. `literature review completion on feature selection, evaluation.md` - Strategic planning (move to Projects/arterial analysis/sessions/)

**Stale captures to archive:**
- Philosophy fragments (intentionality, modes of thought, futility of learning)
- Tool lists without usage notes (old plugin explorations)
- Time-expired logistics (housing search 2025, past travel, Jan 2025 target setting)
- Superseded Obsidian meta-notes (vault setup thinking from 2025)

**Sensitive notes needing user decision:**
- Gender exploration notes (gender dysphoria, Why I'm a T-girl, etc.)
- Therapy reflections (Dec 5, guilt and shame, etc.)
- **Question:** Create `Personal/Growth/` folder?

### Recommended Processing Order

**Priority 1 - Move ML research to projects/ (10-15 min):**
- interpretable machine learning.md → Projects/arterial analysis/
- medical ML interpretability.md → Projects/arterial analysis/
- Feb 19 results.md → Projects/arterial analysis/data-results/
- literature review note → Projects/arterial analysis/sessions/

**Priority 2 - Create Command Centers (30-45 min):**
- [ ] Projects/phd/Command Center.md
- [ ] Projects/cardiac output estimation/Command Center.md
- [ ] Projects/room redesign/Command Center.md
- [ ] Projects/brain system/Command Center.md

**Priority 3 - Archive stale content (20 min):**
- Move philosophy captures to Archive/Fleeting/
- Move tool lists to Archive/Explorations/
- Move meta-notes to Archive/Vault Setup/

**Priority 4 - User decisions (varies):**
- Review sensitive notes
- Decide on Personal/ folder structure
- Batch-move remaining research notes

---

## Recent Decisions (From State.md)

| Decision | Rationale | Status |
|----------|-----------|--------|
| Consolidate cooking into Command Center | ~58 scattered notes → 1 living doc | ✓ Complete |
| Stability Selection + Nested CV are complementary | SS for feature ID, Nested CV for unbiased perf | ✓ Settled |
| Use frozen > fresh in cooking | Saves 20 min prep, quality equal/better | ✓ Active rule |
| Vault restructure: Projects/Knowledge/Meta split | Clearer conceptual boundaries, easier to navigate | ⏳ In progress |

---

## Waiting For

**Blocked items (waiting on external factors):**

| Item | Blocked On | Owner | Timeline |
|------|-----------|-------|----------|
| Task 4 (CV Deaths analysis) | Find "Dr. Hahn outcomes" data file | You | Check email/Downloads |
| cardiac output estimation project | Above data file | You | After data found |
| phd Command Center | Calendar/planning session | You | This week |
| room redesign | Inspiration gathering | You | Flexible |

---

## Suggested Next Session

Based on current state, next session should:

1. **Quick win (10 min):** Review Vault Rules.md and this Focus.md
2. **Decision point (5 min):** Do you want a `Personal/` folder for sensitive notes?
3. **Batch action (15 min):** Move the 5 gem notes to their project homes
4. **Creation (30 min):** Pick one Command Center to create (suggest starting with phd or brain system)
5. **Processing (20 min):** If time, start archiving stale captures

**Time estimate:** 60-90 min total to significantly advance the restructure.

---

## Long-term Rhythm

**Daily:**
- Check Dashboard/Focus.md
- Work on active project(s)
- Capture fleeting thoughts to Inbox/

**Weekly:**
- Process Inbox → move to appropriate homes
- Update project Command Centers with progress
- Check Dashboard/State.md for recent decisions

**Monthly:**
- Review vault structure
- Archive stale content
- Update this Focus.md with new priorities
- Compound learnings to docs/solutions/ if warranted

---

## System Health

**Green flags:**
- ✓ Projects have clear boundaries
- ✓ Research notes are well-developed
- ✓ Command Center pattern consolidates knowledge effectively
- ✓ Overnight agent successfully processed 58 cooking notes

**Yellow flags:**
- ⚠️ ~150 Inbox notes still pending sorting
- ⚠️ 5 major projects need Command Center creation
- ⚠️ Sensitive notes need proper home (Personal/ folder?)
- ⚠️ Cross-project graph links not fully mapped

**Action items to address flags:**
1. Create missing Command Centers (phases 3-4 of restructure)
2. Process remaining Inbox in batches
3. Establish Personal/ folder convention
4. Run graph analysis after major moves

---

## See Also

- [[meta/Vault Rules.md]] - Complete system architecture
- [[Dashboard/State.md]] - Current focus and recent decisions
- [[Projects/cooking/Command Center.md]] - Example of completed Command Center
- [[Inbox/Inbox.md]] - Fleeting captures to be processed

---

**Last updated:** 2026-02-10
**Next update:** 2026-02-11 (after user review)
**Frequency:** Daily check, weekly deep review, monthly strategic update
