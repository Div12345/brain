# Cohesive Daily System: Capture → Calendar → Behavior → Processing

**Date:** 2026-02-10
**Status:** brainstorm
**Author:** claude-code (while user at CMU dance)
**Depends on:** CE article principles, AW research, calendar plugin research, delegation tests

---

## The Problem

The user has many tools but no cohesive system. Capture happens in fragments (phone notes, daily notes, random thoughts). Planning is manual. Behavior data exists (2+ years of ActivityWatch) but is never used. Processing requires human attention for every triage decision. The overnight agent builds things but doesn't connect them.

**CE principle applied:** "Systems over artifacts." We need one system, not more tools.

## What Exists Today

### Working
| Component | Status | Interface |
|-----------|--------|-----------|
| Obsidian vault (OneVault) | Capture-ready (fixed today) | Phone + Desktop |
| Daily notes template | Capture-first design (fixed today) | Obsidian |
| Inbox as default folder | Configured (fixed today) | Obsidian |
| ActivityWatch | Running v0.12.2, 3 buckets | localhost:5600 |
| Claude Code + Obsidian MCP | Direct read/write | CC |
| Claude Desktop + Obsidian MCP | Delegation works | CD via MCP |
| Memory MCP (AIM) | Connected, vault-backed | CC |
| CC Scheduler | Designed but broken since Feb 3 | cron → CC |
| Brain repo task queue | 3 pending tasks | Git-based |

### Not Working / Not Built
| Component | Status | Blocker |
|-----------|--------|---------|
| Calendar view in Obsidian | No plugin installed | Needs Calendar + Day Planner |
| AW → Obsidian integration | Never built | No bridge exists |
| Automated inbox processing | Designed 3x, never built | Scope creep in overnight sessions |
| Behavior-adaptive scheduling | Config exists, no implementation | Scheduler broken |
| OpenCode delegation | MCP sandboxing blocks it | Architecture issue |
| Gemini CLI delegation | Timeout issues | Latency too high |
| Thread-of-thought tracking | Not started | No design exists |

### Hook Stack (Performance Concern)
Every single tool call fires **5 hooks**:

| Hook | Source | Timeout | What It Does |
|------|--------|---------|--------------|
| PreToolUse.js | Project (.claude/hooks/) | none | Reads session-handoff.md, injects context |
| pre-tool-enforcer.mjs | OMC plugin | 3s | Delegation enforcement |
| pretooluse.py | Hookify plugin | 10s | Runs enforce-delegation-retry regex |
| post-tool-verifier.mjs | OMC plugin | 3s | Post-tool verification |
| posttooluse.py | Hookify plugin | 10s | Post-tool hookify rules |

**On Stop:** 3 more hooks fire:
- OMC persistent-mode.mjs (5s)
- Hookify stop.py (10s)
- Ralph stop-hook.sh (no timeout — reads full transcript JSONL, runs jq + perl)

**On User Prompt:** 3 hooks:
- OMC keyword-detector.mjs (5s)
- OMC skill-injector.mjs (3s)
- Hookify userpromptsubmit.py (10s)

**Impact:** ~26s of hook timeout budget per tool call. On a session with 100 tool calls, that's potentially 2600s (43 min) of hook overhead if they all hit timeout. In practice most return fast, but the PreToolUse.js reads a file every call and hookify runs Python every call.

### MCP Stack (10 servers)
| Server | Purpose | Status |
|--------|---------|--------|
| OMC bridge | Agent orchestration | Connected |
| Context7 (x2) | Library docs lookup | Connected |
| paper-search | Academic paper search | Connected |
| obsidian | Vault read/write | Connected |
| memory (AIM) | Knowledge graph | Connected |
| zotero | Reference management | Connected |
| claude-desktop | Desktop delegation | Connected |
| notebooklm-mcp | NotebookLM access | Connected |
| github | GitHub API | Connected |

---

## The Design: Four Connected Layers

### Layer 1: Capture (DONE)

**Principle:** Zero-friction capture from any device. No decisions at capture time.

**What's in place:**
- Daily note opens automatically with "Dump here" section
- New files default to `Inbox/`
- Edit mode is default (not preview)
- Template is minimal — no guilt-inducing empty sections

**Phone workflow:** Open Obsidian → type/voice → done. It goes to daily note or Inbox.

**What compounds:** Every capture becomes a node that can be linked, processed, and scheduled later.

### Layer 2: Calendar + Timeline View (NEEDS PLUGIN INSTALL)

**Recommended plugins:**
1. **Calendar** (Liam Cain) — sidebar calendar, click date → open daily note
2. **Day Planner** (ivan-lednev) — timeline view of day, drag tasks into time slots
3. **Periodic Notes** (optional) — weekly/monthly review templates

**Integration with capture:** Day Planner reads time-stamped items from daily notes. If user writes `- 14:00 meeting with advisor`, it appears on the timeline.

**What this enables:**
- Visual day view (not just a list of tasks)
- Time-blocking by dragging items
- Weekly view for patterns
- Natural connection to AW data (see Layer 3)

**Install action:** User installs Calendar + Day Planner from Obsidian community plugins on phone.

### Layer 3: Behavior-Adaptive Planning (AW Integration — NEEDS BUILDING)

**What ActivityWatch provides:**
- `aw-watcher-window`: Every app/window switch with timestamp + duration
- `aw-watcher-afk`: Active vs idle periods
- `aw-watcher-web-firefox`: Every browser tab with URL + title

**Known patterns from data:**
- Night owl: active ~3:45AM-9AM, sleeps until ~10PM (today's data)
- 14-21 hours daily screen time
- Dominant projects identifiable from window titles

**Integration design:**

```
AW API (localhost:5600)
    │
    ▼
[AW Bridge Script] ─── runs daily at wake time
    │
    ├── Yesterday's summary → Daily/{yesterday}.md appendix
    │   (top apps, focus time, context switches, deep work blocks)
    │
    ├── Current pattern → context/behavior-state.md
    │   (sleep schedule, peak focus times, current project focus)
    │
    └── Anomaly detection → Inbox/ note if unusual
        (significantly different pattern, new app heavy use)
```

**The AW bridge is a Python script** that:
1. Queries AW API for yesterday's events
2. Aggregates: top windows, total active time, longest focus blocks, AFK patterns
3. Appends a `## Activity Summary` section to yesterday's daily note
4. Updates a `context/behavior-state.md` with rolling patterns
5. Scheduler reads behavior-state to adjust autonomous windows

**What compounds:** Over time, the system learns when you actually work, not when you think you work. Planning adapts to reality.

### Layer 4: Processing Pipeline (CD Delegation — NEEDS BUILDING)

**The inbox processing problem:** Notes pile up in Inbox. User has 152 unprocessed. No automated triage.

**Reliable delegation path:** Claude Code → Claude Desktop (via MCP)

**Processing pipeline design:**

```
Trigger: Daily at briefing_time (11:00 per scheduler config)
    │
    ▼
[CC Scheduler] ── triggers CC session with task
    │
    ▼
[Claude Code] ── reads Inbox/ via Obsidian MCP
    │
    ├── For each note:
    │   ├── Classify: project link? action item? reference? fleeting?
    │   ├── If project: move to Projects/{name}/, add [[link]]
    │   ├── If action: extract task, add to daily note or task queue
    │   ├── If reference: move to Knowledge/, tag appropriately
    │   └── If fleeting: leave in Inbox for manual review
    │
    └── Generate triage summary → Daily/{today}.md
```

**Why CC not CD for this:** CC has direct Obsidian MCP access (fastest, most reliable). CD delegation adds latency with no benefit for batch processing. CD is useful when you need desktop context (screenshots, browser state).

**What compounds:** Inbox stays manageable. Projects accumulate relevant notes automatically. The triage rules improve over session learnings.

---

## Thread-of-Thought Tracking (New Concept)

The user mentioned wanting to track "threads of thought" across all tools. This is the meta-layer.

**What a thread is:** A line of thinking that spans multiple sessions, tools, and captures. Example: "arterial analysis methodology" is a thread that appears in daily notes, CC sessions, Zotero references, and code commits.

**How to track threads:**

1. **Memory MCP (AIM)** already exists and is connected to the vault
   - Store active threads as entities: `{name, status, last_touched, related_notes}`
   - Link threads to notes as they're processed
   - Query threads to see what's active

2. **AW can identify threads** by window title patterns
   - If user is in "arterial_analysis" code + Zotero + paper PDFs → that thread is active
   - AW bridge can detect thread switches and log them

3. **Daily note "Threads" section** — auto-populated by processing pipeline
   - What threads were active today (from AW data)
   - What new captures relate to which threads (from inbox processing)
   - What threads are stale (not touched in N days)

**Implementation:** This is a later phase. First get Layers 2-4 working.

---

## Implementation Sequence

Following CE's "80/20 planning" — plan enough to start confidently:

### Phase 1: Calendar View (30 min, user does on phone)
- [ ] Install Calendar plugin from community plugins
- [ ] Install Day Planner plugin from community plugins
- [ ] Try adding a time-stamped item to daily note, verify timeline shows it

### Phase 2: AW Bridge Script (2-3 CC sessions)
- [ ] Write Python script: query AW API → aggregate yesterday
- [ ] Test with real data (yesterday's AW events)
- [ ] Add to daily note as `## Activity Summary` appendix
- [ ] Create `context/behavior-state.md` with rolling patterns
- [ ] Set up cron or scheduler trigger

### Phase 3: Inbox Processing Pipeline (2-3 CC sessions)
- [ ] Write classification prompt/rules for inbox notes
- [ ] Test on 10 notes manually (verify classification accuracy)
- [ ] Automate: CC reads inbox, classifies, moves, links
- [ ] Add triage summary to daily note
- [ ] Set up scheduler trigger at briefing_time

### Phase 4: Hook Optimization (1 session)
- [ ] Benchmark current hook overhead (time 10 tool calls)
- [ ] Remove or combine redundant hooks (PreToolUse.js duplicates OMC context injection?)
- [ ] Consider: does hookify pretooluse.py need to run on every tool call? Can it be scoped?
- [ ] Fix ralph stop hook — add timeout, optimize transcript parsing for large files

### Phase 5: Thread Tracking (later)
- [ ] Define thread schema in Memory MCP
- [ ] Add thread detection to AW bridge
- [ ] Add thread section to daily note template
- [ ] Connect inbox processing to thread linking

### Phase 6: Fix Scheduler (later)
- [ ] Diagnose why scheduler broke on Feb 3
- [ ] Get overnight autonomous runs working again
- [ ] Connect scheduler to behavior-state (adaptive windows)

---

## What This Replaces

| Before | After |
|--------|-------|
| Capture goes to random places | Everything → daily note or Inbox |
| Day is a text list | Day is a visual timeline (Day Planner) |
| AW data sits unused | AW summarizes your day, adapts your schedule |
| 152 inbox notes pile up | Pipeline processes inbox daily |
| No thread awareness | Threads tracked across tools and sessions |
| 5 hooks per tool call | Optimized hook stack |
| Scheduler broken | Overnight agent runs reliably |

---

## CE Principles Applied

1. **Minimalism with necessity** — 4 layers, each does one thing. No premature abstractions.
2. **Systems over artifacts** — One connected system, not more brainstorm docs.
3. **80/20 planning** — Phase 1 is literally "install 2 plugins." Start there.
4. **Each unit compounds** — AW data makes planning better. Processing makes capture worthwhile. Calendar makes processing visible.
5. **Taste in infrastructure** — The system should feel good to use on your phone at a dance.

---

## Open Questions

1. **Day Planner format:** Does it need specific time format in daily notes? (Check docs before installing)
2. **AW bridge frequency:** Daily? Or real-time? Daily is simpler and sufficient.
3. **Inbox classification rules:** What are the actual project names to route to? Need user input.
4. **Thread naming:** How does the user think about their threads? Need to observe, not prescribe.
5. **Scheduler fix:** Is it a config issue or code issue? Need to diagnose.
