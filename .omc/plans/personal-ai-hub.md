# Personal AI Hub Plan

> Value-first personal AI assistant using existing tools

**Created:** 2026-02-02
**Status:** REVISED (Iteration 2)
**Plan ID:** personal-ai-hub

---

## Tonight Deliverable (MUST COMPLETE TODAY)

**One Working Thing:** A Claude command that reads your daily note and generates 3 actionable focus suggestions, stored to a file you can reference.

**Why This First:**
- Uses existing `mcp__obsidian__obsidian_read_note` - NO setup
- Delivers value in < 30 minutes
- Tests the full loop: read vault -> analyze -> output
- Validates the MCP integration works

**Acceptance Test:**
```
Run: "Read my daily note for today and suggest 3 things to focus on"
Result: File saved to context/daily-focus.md with 3 actionable items
Time: < 30 seconds
```

---

## Available Tools (Already Working)

**Obsidian MCP (8 tools):**
| Tool | Purpose | Tested? |
|------|---------|---------|
| `mcp__obsidian__obsidian_read_note` | Read any note | Test tonight |
| `mcp__obsidian__obsidian_global_search` | Search vault | Test tonight |
| `mcp__obsidian__obsidian_update_note` | Append/write notes | Test tonight |
| `mcp__obsidian__obsidian_list_notes` | List files | - |
| `mcp__obsidian__obsidian_manage_frontmatter` | YAML ops | - |
| `mcp__obsidian__obsidian_manage_tags` | Tag ops | - |
| `mcp__obsidian__obsidian_search_replace` | Find/replace | - |
| `mcp__obsidian__obsidian_delete_note` | Delete files | - |

**Memory MCP (10 tools):**
| Tool | Purpose | Tested? |
|------|---------|---------|
| `mcp__memory__aim_memory_store` | Store memories | Test tonight |
| `mcp__memory__aim_memory_search` | Search memories | Test tonight |
| `mcp__memory__aim_memory_get` | Get specific | - |
| `mcp__memory__aim_memory_add_facts` | Add to existing | - |
| `mcp__memory__aim_memory_link` | Link memories | - |
| `mcp__memory__aim_memory_list_stores` | List databases | - |
| `mcp__memory__aim_memory_read_all` | Dump all | - |
| `mcp__memory__aim_memory_forget` | Delete | - |
| `mcp__memory__aim_memory_remove_facts` | Remove facts | - |
| `mcp__memory__aim_memory_unlink` | Remove links | - |

**Key Insight:** No configuration needed. These tools exist. Use them.

---

## Task List (Value-First Order)

### Task 1: Daily Focus Generator (TONIGHT - 30 min)

**What:** Claude reads today's daily note, generates 3 focus items

**Steps:**
1. Find user's daily note path convention (ask once)
2. Use `mcp__obsidian__obsidian_read_note` to read today's note
3. Analyze content for: tasks, mentions, priorities
4. Generate 3 specific, actionable focus items
5. Save to `brain/context/daily-focus.md`

**Acceptance Criteria:**
- [ ] Reads daily note successfully
- [ ] Generates 3 relevant focus items (not generic)
- [ ] Saves output file
- [ ] Total time < 30 seconds

**Verification:** Run it. Read output. Is it useful? Yes/No.

**Files:** `context/daily-focus.md` (output only)

---

### Task 2: Pattern Scan on Existing Vault (TONIGHT - 45 min)

**What:** Run pattern detection on 1+ year of daily notes NOW

**Steps:**
1. Use `mcp__obsidian__obsidian_global_search` to find all daily notes
2. Sample last 30 days of notes
3. Extract: recurring topics, unresolved tasks, time patterns
4. Store findings to `knowledge/patterns/vault-scan-2026-02-02.md`
5. Store key patterns to memory MCP for future reference

**Acceptance Criteria:**
- [ ] Scans at least 30 daily notes
- [ ] Identifies 5+ recurring topics
- [ ] Finds 3+ unresolved blockers (mentioned 3+ times)
- [ ] Documents work time patterns
- [ ] Saves to both file and memory

**Verification:** Read output. Do patterns match user's perception?

**Files:** `knowledge/patterns/vault-scan-2026-02-02.md`

---

### Task 3: Quick Capture Flow (Day 2 - 30 min)

**What:** Single command to capture thought to daily note

**Steps:**
1. Create bash script that calls Claude with thought
2. Claude uses `mcp__obsidian__obsidian_update_note` to append
3. Auto-timestamps entry
4. Confirms capture

**Acceptance Criteria:**
- [ ] `capture "thought here"` works from terminal
- [ ] Appends to today's daily note
- [ ] Includes timestamp
- [ ] < 3 seconds total

**Verification:** Run 5 captures. Check daily note. All there?

**Files:** `tools/capture/quick.sh`

---

### Task 4: Morning Brief Generator (Day 3 - 45 min)

**What:** Generate morning briefing from vault + predictions

**Steps:**
1. Read yesterday's daily note
2. Read `context/predictions.md`
3. Search vault for recent high-priority items (`!` marker)
4. Generate briefing with: summary, predictions, focus areas
5. Save to `context/morning-brief.md`

**Acceptance Criteria:**
- [ ] Includes yesterday summary
- [ ] Lists active predictions
- [ ] Suggests 3 focus areas
- [ ] < 2 minute read time

**Verification:** Read it each morning for 3 days. Useful? Adjust.

**Files:** `context/morning-brief.md`

---

### Task 5: Doom-Scroll Replacement v1 (Day 4-5 - 1 hr)

**What:** Engaging review of your own knowledge

**Interface Decision:** Start with simplest - a markdown file that refreshes

**Steps:**
1. Query vault for: most-linked notes, recent edits, "on this day" past years
2. Sample 10 interesting items
3. Format as scrollable list with excerpts
4. Save to `context/feed.md`
5. Set up hourly refresh (cron or manual)

**The Dopamine Question:** How does markdown replace doom-scroll?
- **Answer:** It doesn't compete on dopamine. It competes on *meaning*.
- Review shows YOUR insights, YOUR progress, YOUR patterns
- Each item is personally relevant, not algorithmically addictive
- Goal: 15 min/day of intentional review, not infinite scroll

**Acceptance Criteria:**
- [ ] 10 items per refresh
- [ ] Mix of: linked notes, recent, historical
- [ ] Each item has: title, excerpt, why-surfaced reason
- [ ] Refreshes hourly

**Verification:** Use for 3 days. Track time spent. Engaging?

**Files:** `context/feed.md`, `tools/surface/generate-feed.sh`

---

### Task 6: Workflow Template Library (Week 2)

**What:** 3 workflow templates based on actual vault patterns

**Steps:**
1. Use Task 2 patterns to identify common workflows
2. Document each as: trigger, steps, done-criteria
3. Store in `workflows/templates/`

**Templates (based on vault analysis from Task 2):**
- `research-paper.md` - Paper processing workflow
- `deep-work.md` - Focus session structure
- `admin-batch.md` - Batch admin tasks

**Acceptance Criteria:**
- [ ] 3 templates created
- [ ] Each based on actual observed patterns
- [ ] Each used at least once

**Files:** `workflows/templates/*.md`

---

## Success Metrics (With Tracking)

| Metric | Target | How to Measure | Baseline | Tracking |
|--------|--------|----------------|----------|----------|
| Daily focus usefulness | >60% useful | Rate each day: useful/not | 0 (new) | `context/metrics/focus-ratings.md` |
| Capture latency | <3 sec | Time 10 captures | N/A | `context/metrics/capture-times.md` |
| Review engagement | >15 min/day | Track time in feed | 0 | `context/metrics/review-time.md` |
| Pattern accuracy | >70% correct | User validates patterns | N/A | `context/metrics/pattern-validation.md` |
| Blockers resolved | >50% within week | Track blocker lifecycle | N/A | `context/blockers.md` with dates |

**Tracking Implementation:**
- Each metric file is a simple log: date, value, notes
- Weekly review: calculate averages, identify trends
- Adjust system based on data, not assumptions

---

## Constraints (Hard Rules)

| Constraint | Enforcement |
|------------|-------------|
| No new MCP configuration | Use existing tools only |
| Immediate value per task | Each task produces usable output |
| Test before building more | Don't start Task N+1 until Task N verified |
| Match existing patterns | Use `!` priority, `[[wikilinks]]`, current folders |
| No new habits required | System adapts to user |

---

## Anti-Goals (What We're NOT Building)

- Complex dashboards
- New apps to install
- Notification systems
- Habit trackers
- Anything requiring daily maintenance

---

## Decision Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Start with existing MCPs | Yes | Already configured, no setup time |
| Tonight deliverable | Daily focus generator | Fastest path to value |
| Feed interface | Markdown file | Simplest, can upgrade later |
| Pattern detection | Run on existing vault | 1+ year of data available NOW |
| Metrics tracking | Manual log files | Simple, no infrastructure |

---

## File Structure (Minimal)

```
brain/
├── context/
│   ├── daily-focus.md          # Task 1 output
│   ├── morning-brief.md        # Task 4 output
│   ├── feed.md                 # Task 5 output
│   ├── blockers.md             # Tracked blockers
│   └── metrics/
│       ├── focus-ratings.md    # Daily usefulness ratings
│       ├── capture-times.md    # Capture latency log
│       ├── review-time.md      # Feed engagement log
│       └── pattern-validation.md # Pattern accuracy log
├── knowledge/
│   └── patterns/
│       └── vault-scan-*.md     # Pattern scan results
├── tools/
│   ├── capture/
│   │   └── quick.sh            # Task 3
│   └── surface/
│       └── generate-feed.sh    # Task 5
└── workflows/
    └── templates/
        ├── research-paper.md   # Task 6
        ├── deep-work.md        # Task 6
        └── admin-batch.md      # Task 6
```

---

## Tonight's Execution Plan

**Time Budget:** 2 hours

| Time | Task | Output |
|------|------|--------|
| 0:00-0:10 | Get daily note path from user | Path confirmed |
| 0:10-0:30 | Task 1: Daily Focus Generator | `context/daily-focus.md` working |
| 0:30-1:15 | Task 2: Pattern Scan | `knowledge/patterns/vault-scan-*.md` |
| 1:15-1:30 | Verify both work | User confirms value |
| 1:30-2:00 | Document learnings | Update this plan with findings |

**Exit Criteria for Tonight:**
- [ ] Daily focus generator produces useful output
- [ ] Pattern scan reveals at least 3 insights user didn't expect
- [ ] Both outputs saved to files
- [ ] User says "this is useful"

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Daily note path unknown | Ask user first, don't assume |
| MCP tools fail | Test each tool before building on it |
| Patterns too generic | Require specific examples from vault |
| Over-engineering | Stop at "working", don't optimize yet |

---

## Next Steps After Tonight

If tonight succeeds:
1. Day 2: Quick capture (Task 3)
2. Day 3: Morning brief (Task 4)
3. Day 4-5: Feed v1 (Task 5)
4. Week 2: Workflows (Task 6)

If tonight fails:
1. Document what broke
2. Fix the blocker
3. Retry tonight's tasks

---

**PLAN_READY: .omc/plans/personal-ai-hub.md**
