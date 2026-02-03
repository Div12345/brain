---
created: 2026-02-03
updated: 2026-02-03
tags:
  - documentation
  - context
  - coordination
  - cc-scheduler
---

# Context Management Patterns & File Formats

> How the brain system maintains state, coordinates agents, and ensures continuity across sessions

## OVERVIEW

The brain system uses file-based context to maintain state across agent sessions. This enables:

1. **Agent Coordination** - Multiple agents don't duplicate work
2. **Session Continuity** - Agents can resume after context window resets
3. **Priority Tracking** - Clear guidance on what matters next
4. **Handoff Clarity** - Explicit transfer of work between agents

All context files use YAML frontmatter + markdown content, stored in `context/`.

---

## PART 1: THE CONTEXT MANAGEMENT SYSTEM

### File Structure

```
context/
├─ session-state.md              # Compaction-resilient state (PRIMARY)
├─ active-agents.md              # Who's working on what (PRIMARY)
├─ priorities.md                 # What matters most (GUIDANCE)
├─ handoff.md                    # Current handoff info (REFERENCE)
├─ capabilities.md               # What agents can do
├─ ecosystem.md                  # What tools exist
├─ philosophy.md                 # Core values
├─ off-limits.md                 # What can't be touched
├─ predictions.md                # What might happen next
├─ self-improvement-metrics.md   # System health
├─ usage.md                      # System usage patterns
└─ metrics/
   └─ experiment-1-context.md    # Experiment tracking
```

### Reading Order (For Any Agent)

Always read in this order:

1. **First:** `session-state.md` - What's the current state?
2. **Second:** `active-agents.md` - Who's working where?
3. **Third:** `priorities.md` - What should I work on?
4. **Fourth:** `handoff.md` - What was just finished?
5. **Reference:** Others as needed

---

## PART 2: SESSION STATE (PRIMARY)

### Purpose

Preserves essential state across context window resets and agent transitions. Designed to survive conversation compaction.

### File Format

```yaml
---
created: 2026-01-31
tags:
  - context
  - session
  - compaction-resilient
updated: 2026-02-03T15:00:00Z
agent: [current-agent-name]
---

# Session State

> **COMPACTION RESILIENCE**: Read this first after context reset.

## Active Agent
- **[agent-id]** ([agent-interface]): [What they're working on] [Status]

## Session Summary (Extended)

### Major Outputs Created

**Research Docs (count):**
- [[knowledge/research/...]]
- [[knowledge/research/...]]

**Infrastructure Files Created:**
- [[context/...]]
- [[tools/...]]

**Files Updated:**
- CLAUDE.md
- ...

## Pending (Blocked on What)
- Q-01: Question text
- Q-02: Question text

## Recovery Protocol
1. `gh api repos/...` (git command to check recent commits)
2. Read this file + [[context/predictions]]
3. Continue from pending list
```

### Key Sections Explained

| Section | Purpose | When Updated |
|---------|---------|--------------|
| Active Agent | Who's currently working | Every session start |
| Session Summary | What was produced | Every session end |
| Pending | What's blocked waiting | Every session end |
| Recovery Protocol | How to continue | Every session end |

### Example Content

```yaml
---
created: 2026-01-31
tags:
  - context
  - session
  - compaction-resilient
updated: 2026-02-03T15:30:00Z
agent: scientist-001
---

# Session State

> **COMPACTION RESILIENCE**: Read this first after context reset.

## Active Agent
- **scientist-001** (Claude Code): Task analysis & documentation → Complete

## Session Summary (Extended)

**Research Docs Created (10):**
- [[knowledge/research/recursive-self-improvement]]
- [[knowledge/research/proactive-assistant-patterns]]
- [[knowledge/research/multi-agent-coordination]]
- [[knowledge/research/task-automation-scheduling]]
- [[knowledge/research/pkm-mcp-servers]]
- [[knowledge/research/obsidian-mcp-options]]
- [[knowledge/research/ai-memory-systems]]
- [[knowledge/research/claude-code-ecosystem]]
- [[knowledge/research/context-window-management]]
- [[knowledge/research/self-referential-bootstrap]]

**Patterns Created (2):**
- [[knowledge/patterns/multi-agent-coordination]]
- [[knowledge/patterns/compaction-recovery]]

**Infrastructure:**
- [[context/active-agents]]
- [[context/self-improvement-metrics]]
- [[context/predictions]]

**Files Updated:**
- HOME.md, ACTIVE.md, CLAUDE.md
- logs/2026-01-31-overnight.md

## Pending (Blocked on User)
- Q-01: Overnight schedule preference
- Q-02: Obsidian vault path
- Q-03: Failed task notification
- Q-04: Off-limits tasks
- Q-05: Brain repo local path

## Recovery Protocol
1. `gh api repos/Div12345/brain/commits --jq '.[0:5]'`
2. Read this file + [[context/predictions]]
3. Continue from pending list
```

### When to Update session-state.md

**At Start of Session:**
```
1. Read current content
2. Check recovery protocol
3. Note what you're working on in Active Agent
```

**At End of Session:**
```
1. Update Active Agent (yourself)
2. Add to Session Summary all files created/modified
3. List Pending (what's blocked)
4. Update timestamp
5. Commit with message: "Update session state: [brief summary]"
```

### Compaction Resilience Design

The file is structured to survive context window resets:

- **Kept brief:** Key facts only, not full details
- **Link-heavy:** Uses `[[wikilinks]]` to separate detailed info
- **List-based:** Easy to scan even in isolation
- **Recovery protocol:** Clear steps to get back up to speed

**Why this matters:** After conversation compaction, the agent might only have access to git history. This file enables recovery from that state:

```
Agent A finishes work → updates session-state.md
Context compaction happens (agent reset)
Agent B starts → reads session-state.md from git
Agent B runs: git log --oneline (from recovery protocol)
Agent B continues from Pending list
```

---

## PART 3: ACTIVE AGENTS (PRIMARY)

### Purpose

Real-time coordination file. Prevents duplicate work by tracking who's working where.

### File Format

```yaml
---
created: 2026-01-31
tags:
  - context
  - coordination
  - agents
updated: 2026-02-03T09:35
---

# Active Agents

> Coordination file for multi-agent work. Check before starting.

## Currently Active

| Agent | Interface | Working On | Since | Status |
|-------|-----------|------------|-------|--------|
| overnight-A | Desktop Claude | Multi-agent coordination | 09:30 | Active |
| overnight-B | Desktop Claude (remote) | Obsidian conversion, MCP research | 09:00 | Active |

## Claimed Work Areas

| Area | Agent | Notes |
|------|-------|-------|
| `knowledge/research/multi-agent*` | overnight-A | Coordination patterns |
| `knowledge/research/obsidian*` | overnight-B | MCP options |
| `prompts/` | overnight-B | Questions setup |

## Recent Handoffs

| Time | From | To | Topic |
|------|------|----|-------|
| 09:05 | overnight-B | any | Completed Obsidian MCP research |

## Coordination Rules

1. **Check this file** before starting work
2. **Update claiming** when starting new area
3. **Clear claim** when done with area
4. **Don't duplicate** - if claimed, work elsewhere
5. **Commit frequently** - every 5-10 min for visibility

## Agent Registration

New agents should:
1. Add themselves to "Currently Active"
2. Check claimed areas
3. Pick unclaimed work
4. Update this file
```

### Claiming Work Areas (Protocol)

**When starting a new area:**

1. Check "Claimed Work Areas" table
2. If your area is not listed:
   ```
   | `knowledge/research/neural-nets*` | myself-001 | Analysis of NN patterns |
   ```
3. Commit: `git add context/active-agents.md && git commit -m "Claim: neural-net research"`

**When done with area:**

1. Remove your row from "Claimed Work Areas"
2. Commit: `git add context/active-agents.md && git commit -m "Complete: neural-net research"`

**When blocked/paused:**

1. Add note in "Claimed Work Areas":
   ```
   | `knowledge/research/neural-nets*` | myself-001 | Blocked on Q-01 (user input) |
   ```
2. Continue with other areas if possible

### Work Area Glob Patterns

Use glob patterns to define scope clearly:

| Pattern | Matches | Use Case |
|---------|---------|----------|
| `knowledge/research/obsidian*` | `knowledge/research/obsidian-mcp-options.md` | Work on all Obsidian research |
| `tasks/active/task-cc*` | All active CC tasks | Working on multiple CC tasks |
| `tools/mcps/*` | All MCP tools | Building tools (broad claim) |
| `context/*` | Any context file | Coordinating system state |

**Guidelines:**
- More specific → narrower scope (less conflict)
- Broader pattern → "I'm working on this domain"
- Use `*` wildcard, not `[0-9]*` regexes

### Recent Handoffs Table

Records recent work transfers:

```markdown
| Time | From | To | Topic |
|------|------|----|-------|
| 09:05 | overnight-B | any | Completed Obsidian MCP research |
| 14:30 | architect-001 | user | Proposed 3 new tools, waiting approval |
```

**When to add entry:**
- Agent finishes and hands off to next
- Work transitions between agents
- Something important completes

---

## PART 4: PRIORITIES (GUIDANCE)

### Purpose

Guide next agent on what matters most. Updated at end of each session.

### File Format

```yaml
---
created: 2026-01-31
tags:
  - context
  - priorities
  - status/active
updated: 2026-01-31T09:30
---

# Current Priorities

> Updated by agents after each run. Read this first.

## Immediate

| Priority | Task | Owner | Status |
|----------|------|-------|--------|
| 1 | [Task description] | [[agents/overnight]] | 🔄 In progress |
| 2 | [Task description] | claude-code | ✅ Done |
| 3 | [Task description] | user | Blocked |

## Short-Term (This Week)

| Priority | Task | Notes |

## Medium-Term (This Month)

| Priority | Task |

## Open Questions

See [[prompts/pending]] for full list:
- Question 1
- Question 2
- Question 3

## Next Agent Should

- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3

---

*Last updated: 2026-01-31T09:30 by claude-code-web*
```

### Sections Explained

| Section | Purpose |
|---------|---------|
| Immediate | This session/day's priorities |
| Short-Term | This week's work |
| Medium-Term | This month's goals |
| Open Questions | Blockers needing user input |
| Next Agent Should | Checklist for continuation |

### How to Update priorities.md

**At start of session:**
1. Read Immediate section
2. Pick tasks from there

**At end of session:**
1. Move completed items to history (or mark ✅)
2. Add new discoveries to appropriate timeframe
3. Update Open Questions section
4. Update "Next Agent Should" with checklist

**Example transition:**

```yaml
# Before (from yesterday)
## Immediate
| 1 | Obsidian-ify brain repo | [[agents/overnight]] | 🔄 In progress |
| 2 | Set up CC hooks | claude-code | ✅ Done |

# After (today's update)
## Immediate
| 1 | Test overnight runner | user | ⏸ Waiting |
| 2 | Answer pending questions | user | Blocked |
| 3 | Review predictions | any | 🔄 In progress |

## Short-Term (This Week)
| 1 | Validate overnight run | Check [[knowledge/]] and [[logs/]] |
| 2 | Review [[inspirations/claude-code-ecosystem]] | Apply patterns |
```

---

## PART 5: HANDOFF (REFERENCE)

### Purpose

Explicit transfer of current work from one agent to next. Clear snapshot of what just happened.

### File Format

```yaml
---
created: 2026-01-31
tags:
  - context
  - coordination
  - handoff
status: active
aliases:
  - agent handoff
  - coordination
---

# Agent Handoff Protocol

## Current Handoff

| Field | Value |
|-------|-------|
| From | [Agent name] |
| To | [Next agent or "Any agent" or "User"] |
| Time | [ISO timestamp] |
| Status | [Brief summary] |

## Context

[Detailed explanation of what was done and why]

## Key Files Created This Session

- `path/to/file1.md` - [What it is]
- `path/to/file2.md` - [What it is]

## Completed Actions

- [x] Action 1
- [x] Action 2

## Pending Actions (Need User Input)

- [ ] Action that needs user decision/input
- [ ] Another action

## For Next Agent

1. Read [[context/session-state]] first
2. Check [[context/priorities]]
3. Review [[prompts/pending]] - several questions need answers
4. [Specific recommended next step]

## Ready to Use

[What's immediately usable without further setup]

## Related

- [[context/session-state]] - Compaction-resilient state
- [[knowledge/...]] - Session documentation
- [[tasks/completed/...]] - Completed tasks
```

### Example Handoff

```yaml
---
created: 2026-02-03
tags:
  - context
  - coordination
  - handoff
---

# Agent Handoff Protocol

## Current Handoff

| Field | Value |
|-------|-------|
| From | scientist-001 (Claude Code) |
| To | Any agent |
| Time | 2026-02-03T15:30:00Z |
| Status | Analysis complete - task file schema & agent patterns documented |

## Context

Completed comprehensive analysis of brain system's task file formats, agent personas, and context management patterns. Created two major documentation files (6000+ lines total) for cc-scheduler integration.

## Key Files Created This Session

- `tools/cc-scheduler/TASK_FILE_SCHEMA.md` - Complete task file field reference
- `tools/cc-scheduler/AGENT_PERSONA_GUIDE.md` - Agent definition patterns
- `tools/cc-scheduler/CONTEXT_MANAGEMENT_PATTERNS.md` - Context file formats (this file)

## Completed Actions

- [x] Analyzed all existing task files (5 files reviewed)
- [x] Documented field taxonomy (16 fields + usage patterns)
- [x] Identified 4 agent types + workflows
- [x] Mapped context file purposes
- [x] Created schema reference
- [x] Created agent guide
- [x] Created context guide

## Pending Actions (Need Continuation)

- [ ] Build cc-scheduler task validation engine
- [ ] Build cc-scheduler task assignment logic
- [ ] Implement agent registration system
- [ ] Test with existing tasks
- [ ] Document decision-making matrices for task creation

## For Next Agent

1. Read [[context/session-state]] first (new content just added)
2. Check [[context/priorities]] - verify Immediate items
3. Review [[prompts/pending]] - Q-01 through Q-05 need user answers
4. **Next step:** Start building cc-scheduler validation engine
   - Use schema from TASK_FILE_SCHEMA.md
   - Validate: required fields, timeout format, priority enum
   - Warn on: missing optional fields, malformed wikilinks

## Ready to Use

- 3 comprehensive documentation files (ready for cc-scheduler code)
- Updated session-state.md with recovery protocol
- Updated priorities with next week's work
- Updated active-agents.md with completed claims

## Related

- [[context/session-state]] - Complete session state
- [[context/active-agents]] - Agent registration
- [[context/priorities]] - What matters next
- [[tasks/completed/task-note-001-pattern-analysis]] - Prior analysis work
```

### When to Update handoff.md

**At end of each significant work session:**

1. Write "Current Handoff" section with status
2. List all files created this session
3. Check off completed actions
4. Note any pending actions
5. Give clear "Next steps" for following agent
6. Update timestamp
7. Commit with message: "Handoff: [brief summary]"

---

## PART 6: OTHER CONTEXT FILES

### capabilities.md

Lists what the system can do.

```yaml
---
created: 2026-01-31
tags:
  - context
  - capabilities
---

# System Capabilities

> What the brain system can and cannot do

## Can Do

- [ ] Web search via curl/APIs
- [ ] GitHub access via gh CLI
- [ ] Read Obsidian vault via MCP
- [ ] Create/modify files
- [ ] Execute bash commands
- [ ] Run git operations

## Cannot Do

- [ ] Push to remote (requires auth)
- [ ] Modify user's local Obsidian directly
- [ ] Call external APIs (no auth)
- [ ] Execute code outside sandbox

## By Agent Type

### Overnight Agent (Autonomous Researcher)
**Can:** Read system files, web search, create knowledge files, generate predictions
**Cannot:** Modify code, delete files, push to remote

### Code Executor
**Can:** Edit any file, run commands, git operations
**Cannot:** Push to remote, modify off-limits files
```

### ecosystem.md

What tools/MCPs/plugins exist in the system.

```yaml
---
created: 2026-01-31
tags:
  - context
  - ecosystem
---

# Tool Ecosystem

## Installed MCPs

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| obsidian-mcp | 1.0.0 | Vault access | Active |
| context7 | 2.1.0 | Documentation lookup | Active |

## Claude Code Plugins

| Plugin | Purpose |
|--------|---------|
| scheduler | Scheduled task execution |

## Hooks

| Hook | Trigger | Action |
|------|---------|--------|
| session-log | Stop event | Log to logs/ |
```

### off-limits.md

What can't be touched.

```yaml
---
created: 2026-01-31
tags:
  - context
  - safety
---

# Off-Limits Files

> Don't modify these without explicit approval

## System Files
- `.claude/settings.json` (unless updating hooks)
- `CLAUDE.md` (global instructions)
- `meta/safety.md` (this list)

## User Files
- User's actual Obsidian vault (read-only)
- `.env` files
- Personal configuration

## Danger Zone
- Deleting any git history
- Modifying completed tasks
- Changing priorities without user input
```

---

## PART 7: CONTEXT WORKFLOW (HOW TO USE)

### For Any Agent Starting a Session

```
1. ORIENTATION (5 min)
   ├─ Read: context/session-state.md
   ├─ Read: context/active-agents.md
   ├─ Read: context/priorities.md
   └─ Skim: context/handoff.md

2. DECIDE WHAT TO WORK ON
   ├─ Check "Next Agent Should" in priorities.md
   ├─ Check "Claimed Work Areas" in active-agents.md
   └─ Pick unclaimed area OR continue prior work

3. CLAIM WORK (if new area)
   ├─ Add row to "Claimed Work Areas" in active-agents.md
   ├─ Add yourself to "Currently Active" table
   └─ Commit: "Claim: [area name]"

4. DO WORK
   └─ Commit frequently (every 5-10 min)

5. HANDOFF (when done)
   ├─ Update session-state.md (outputs created)
   ├─ Update active-agents.md (clear your claim)
   ├─ Update priorities.md (what's next)
   ├─ Update handoff.md (what you did)
   ├─ Create logs/YYYY-MM-DD-[agent].md
   └─ Commit: "Complete: [summary]"
```

### For Context Window Resets

```
Agent gets reset mid-session:

1. Agent B starts cold with no context
2. Reads: session-state.md (has recovery protocol)
3. Runs: git log --oneline (see recent commits)
4. Reads: active-agents.md (who was working on what)
5. Continues from: context/priorities#Pending
6. Updates: session-state.md with new findings
```

### For Multi-Agent Coordination

```
Agent A completes work:
1. Updates context/handoff.md ("From: Agent A, To: Agent B")
2. Updates context/active-agents.md (clears claim)
3. Commits all changes
4. Agent B reads context files
5. Agent B registers in active-agents.md
6. Agent B continues from handoff

Key: No blocking/waiting - file-based coordination
```

---

## PART 8: DECISION MATRIX

When managing context, use this matrix:

| Situation | Action | File | When |
|-----------|--------|------|------|
| Starting session | Read recovery protocol | session-state.md | Always first |
| Claiming work | Add to "Claimed Work Areas" | active-agents.md | Before starting |
| Work completed | Clear claim + update summary | session-state.md + active-agents.md | End of session |
| Priority changed | Update table | priorities.md | User input or discovery |
| Unexpected issue | Generate question | prompts/pending/ + handoff.md | When blocked |
| Handing off to next agent | Update all context | handoff.md + session-state.md | End of session |
| Agent gets stuck | Note blocker + continue elsewhere | active-agents.md + handoff.md | When blocked |

---

## PART 9: CONTEXT FILE MAINTENANCE

### Update Frequency

| File | Update | Frequency |
|------|--------|-----------|
| session-state.md | Add findings | Per session end |
| active-agents.md | Claim/clear work | Per work area |
| priorities.md | Update guidance | Per session end |
| handoff.md | New handoff info | Per agent transition |
| capabilities.md | New tools | When ecosystem changes |
| ecosystem.md | Tool updates | When tools change |

### Commit Discipline

Always commit context file changes:

```bash
# Starting work
git add context/active-agents.md
git commit -m "Claim: knowledge/research/topic"

# Making progress
git add context/
git commit -m "Progress: [brief summary of work]"

# Completing session
git add context/
git commit -m "Complete: [summary] → session-state, priorities, handoff updated"
```

### Compaction-Safe Design

These files are designed to survive context resets:

- **Minimal detail:** Key facts only, detailed info in linked files
- **Link-heavy:** Uses `[[wikilinks]]` to separate knowledge
- **List-based:** Easy to parse in isolation
- **Timestamped:** Can see how stale info is
- **Recovery protocol:** Clear procedure to resume

**Test:** If you only had git history + session-state.md, could you continue? YES.

---

## SUMMARY TABLE

Quick reference for context management:

| File | Purpose | Read When | Update When |
|------|---------|-----------|------------|
| session-state.md | Compaction-resilient recovery | Starting session | Session end |
| active-agents.md | Coordination (prevent duplicates) | Deciding what to work on | Claiming/clearing work |
| priorities.md | Guidance on what matters | Planning work | Session end |
| handoff.md | Current status + next steps | Continuing prior work | Agent transition |
| capabilities.md | What system can do | Planning feasibility | Ecosystem changes |
| ecosystem.md | What tools exist | Research phase | Tool installation |
| off-limits.md | Safety boundaries | Before making changes | Policy changes |

---

## EXAMPLE WORKFLOW

**Scenario:** Agent A finishes, Agent B starts

```
AGENT A (End of Session)
├─ Updates session-state.md with findings
├─ Clears claim from active-agents.md
├─ Updates priorities.md with next steps
├─ Updates handoff.md with "To: Any agent"
└─ Commits: "Complete: obsidian research → ready for implementation"

[Context window reset]

AGENT B (Start of Session)
├─ Reads session-state.md
│  ├─ Sees: "Obsidian research complete"
│  ├─ Sees: Recovery protocol
│  └─ Continues from: Pending list
├─ Reads active-agents.md
│  ├─ Sees: No active agents (everyone cleared)
│  └─ Claims new work area
├─ Reads priorities.md
│  ├─ Sees: "Next Agent Should" checklist
│  └─ Picks from there
├─ Reads handoff.md
│  ├─ Sees: What Agent A completed
│  └─ Knows what's ready to use
└─ Starts work, commits frequently
```

---

*Last updated: 2026-02-03*
*Status: Complete reference for cc-scheduler integration*
