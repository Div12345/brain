---
created: 2026-02-03
tags:
  - analysis
  - documentation
  - task-system
  - schema
type: system-documentation
---

# Task System Schema Analysis

**Date:** 2026-02-03
**Analyzed:** 5 task files across all states (pending, active, completed)
**Purpose:** Document existing task file format and patterns for scheduler implementation

---

## Executive Summary

The brain system uses a **file-based task queue** with:
- **YAML frontmatter** for metadata
- **Markdown body** for content and instructions
- **Lifecycle states**: pending → active → completed/failed
- **Coordination via file paths** (agent ID in filename indicates ownership)

---

## Task File Schema

### Location & Naming

```
tasks/{state}/{id}.{agent-suffix}.md

Examples:
- tasks/pending/task-sched-001-overnight-schedule.md
- tasks/active/task-2026-01-31-overnight.desktop.md
- tasks/completed/task-cc-001-hooks-setup.claude-code.md
```

**State directories:**
- `pending/` - Waiting to be claimed
- `active/` - Currently being worked
- `completed/` - Successfully finished
- `failed/` - Errored out

---

## Frontmatter Fields

### Required Fields

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `created` | ISO date | `2026-01-31` or `2026-01-31T08:30:00Z` | Creation timestamp |
| `tags` | array | `[task, analysis, obsidian]` | Categorization |
| `priority` | enum | `high`, `medium`, `low` | Urgency level |

### Recommended Fields

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `id` | string | `task-sched-001-overnight-schedule` | Unique identifier |
| `requires` | array | `[web_search, github_access, obsidian-mcp]` | Capabilities needed |
| `preferred_interface` | enum | `claude-code`, `claude-desktop`, `any` | Which agent should do this |
| `timeout` | duration | `30m`, `60m`, `240m` | Max execution time |

### Status Fields (active tasks only)

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `status` | enum | `active` | Current lifecycle state |
| `claimed_by` | string | `desktop-opus`, `claude-code` | Who is working on it |
| `updated` | ISO timestamp | `2026-01-31T10:05` | Last modification |

### Optional Fields

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `aliases` | array | `[overnight agent, night agent]` | Alternative names |
| `agent` | string | `overnight` | Associated agent name |

---

## Body Structure

### Minimal Format

```markdown
# Task: [Title]

## [Key Section 1]
[Content]

## [Key Section 2]
[Content]
```

### Standard Sections Found

**Requirement sections:**
- `## Mission` - High-level goal
- `## Objective` - What to accomplish
- `## Core Intentions` - Why this matters

**Instruction sections:**
- `## Steps` - Numbered procedure
- `## Prerequisites` - What must be true first
- `## Input` - What the task needs
- `## Expected Output` - Success definition

**Guidance sections:**
- `## Analysis Questions` - What to investigate
- `## Scope` - What's in/out of bounds
- `## Context` - Related files/references
- `## Blocked By` - Dependencies

**Delivery sections:**
- `## Deliverables` - What to produce
- `## Output Locations` - Where to save results
- `## Acceptance Criteria` - Pass/fail checklist
- `## Related` - Links to related docs

**Control sections:**
- `## Work Streams` - Parallel work areas
- `## Continue Until` - Stop conditions
- `## On Pause` - How to resume

---

## Example Task: Immediate State

**File:** `tasks/pending/task-sched-001-overnight-schedule.md`

```yaml
---
created: 2026-01-31
tags:
  - task
  - automation
  - scheduling
  - status/pending
priority: medium
requires:
  - claude-code
  - user_answers
preferred_interface: claude-code
timeout: 30m
---

# Task: Set Up Scheduled Overnight Runs
[Body content...]
```

**Key patterns:**
- Status indicated in tags: `status/pending`
- Priority and requires are clear
- Preferred interface specified
- Timeout is reasonable for type of work

---

## Example Task: Active State

**File:** `tasks/active/task-2026-01-31-overnight.desktop.md`

```yaml
---
id: task-2026-01-31-overnight
created: 2026-01-31T08:30:00Z
priority: high
requires:
  - web_search
  - github_access
  - file_creation
preferred_interface: claude-desktop
timeout: 240m
status: active
claimed_by: desktop-opus
---

# Task: Deep Orchestration Research & Build Night
[Body content...]
```

**Key patterns:**
- More precise ISO timestamp
- `status: active` field added
- `claimed_by` shows who's working on it
- Longer timeout (240m for complex work)
- Work streams section for parallel execution
- "Continue Until" section shows pause/resume protocol

---

## Example Task: Completed State

**File:** `tasks/completed/task-cc-001-hooks-setup.claude-code.md`

```yaml
---
created: 2026-01-31
tags:
  - task
  - claude-code
  - hooks
  - status/pending
priority: high
requires:
  - filesystem_access
  - git
preferred_interface: claude-code
timeout: 60m
---

# Task: Set Up CC Hooks for Brain System
[Body content...]
```

**Key patterns:**
- Same frontmatter as pending
- Status in tags (can be `status/pending`, `status/completed`, etc.)
- File moved from active/ to completed/ directory
- Can append results to body when done

---

## Coordination Patterns

### Active Agents Coordination

**File:** `context/active-agents.md`

```markdown
## Currently Active

| Agent | Interface | Working On | Since | Status |
|-------|-----------|------------|-------|--------|
| overnight-A | Desktop Claude | Multi-agent coordination | 09:30 | Active |

## Claimed Work Areas

| Area | Agent | Notes |
|------|-------|-------|
| `knowledge/research/multi-agent*` | overnight-A | Coordination patterns |
```

**Key patterns:**
- Tracks who's doing what in real-time
- Prevents duplicate work
- Agents update on claiming/completing areas
- Handoff tracking for continuity

---

## Priority Management

**File:** `context/priorities.md`

```markdown
## Immediate
| Priority | Task | Owner | Status |
|----------|------|-------|--------|
| 1 | Obsidian-ify brain repo | overnight | 🔄 In progress |

## Short-Term (This Week)
| Priority | Task | Notes |
|----------|------|-------|

## Next Agent Should
- [ ] Continue Obsidian conversion...
- [ ] Test graph view connectivity
- [ ] Generate predictions
```

**Key patterns:**
- Time-horizon segmentation (Immediate → Short-term → Medium-term)
- Owner and status tracking
- Explicit handoff instructions for next agent
- Links to relevant documents

---

## Session State (Compaction Resilience)

**File:** `context/session-state.md`

```markdown
## Active Agent
- **scientist-001** (Claude Code): Bootstrap research ✓

## Session Summary (Extended)
**Research Docs Created (10):**
- [[knowledge/research/...]]

## Pending (Blocked on User)
- Q-01: Overnight schedule preference
- Q-02: Obsidian vault path

## Recovery Protocol
1. `gh api repos/...`
2. Read this file + [[context/predictions]]
3. Continue from pending list
```

**Key patterns:**
- Tracks what was accomplished in session
- Lists blocked items (waiting on user)
- Includes recovery protocol for context resets
- Used for compaction-resistant handoffs

---

## Agent Personas

### Overnight Agent

**File:** `agents/overnight.md`

**Key characteristics:**
- Autonomous, runs while user sleeps
- Read-only by default, builds new files only
- Phases: Orientation → Analysis → Building → Handoff
- Output to: `knowledge/`, `logs/`, `inspirations/`, `experiments/`
- Forbidden: Direct vault mods, external API calls, force-push
- Session logging: `logs/YYYY-MM-DD-overnight.md`

**Frontmatter pattern:**
```yaml
---
created: 2026-01-31
tags:
  - agent
  - orchestration
  - autonomous
status: active
aliases:
  - overnight agent
  - night agent
---
```

### Architect Agent

**File:** `agents/architect.md`

**Key characteristics:**
- Builds tools, MCPs, plugins when gaps identified
- Phases: Gap analysis → Research → Design → Build → Test → Document → Propose
- Pre-flight checklist (reads CLAUDE.md, safety.md, ecosystem.md)
- Quality standards: Minimal, Tested, Documented, Reversible, Observable, Configurable
- No auto-integration—always proposes first

**Decision workflow:**
- Gap → Research (existing solutions) → Design (if building new)
- All tools must have specs, tests, and documentation
- Rollback plan required

### Oracle Agent

**File:** `agents/oracle.md`

**Key characteristics:**
- Predicts what you'll need before asking
- Categories: Immediate (1-4h) → Daily → Weekly → Contextual → Behavioral
- Confidence calibration with factors (+/- adjustments)
- Phases: Data gathering → Pattern matching → Generate predictions → Prepare resources → Queue for delivery

**Output format:**
```markdown
## P-[YYYY-MM-DD]-[NN]: [Short description]

**Category:** immediate | daily | weekly | contextual | behavioral
**Confidence:** high (>80%) | medium (50-80%) | low (<50%)
**Evidence:** [Specific observations]
**Prediction:** [What will happen]
**Recommended Action:** [What to prepare]
**Surface When:** [Optimal moment]
**Validate By:** [How to check]
```

---

## Safety Boundaries

**File:** `context/off-limits.md`

Protected areas:
- **System Files:** OS config, shell profiles, credentials
- **User Data:** Obsidian vault without approval, deletions without confirmation
- **Destructive Ops:** rm -rf, force-push, overwrites
- **External Services:** Purchases, emails, public posts

Protocol: When unsure, log to `prompts/pending` and skip task.

---

## File Organization Patterns

### Knowledge Hierarchy

```
knowledge/
├── research/           # Deep-dive research papers
│   ├── multi-agent-coordination.md
│   ├── task-automation-scheduling.md
│   ├── obsidian-mcp-options.md
│   └── ...
├── analysis/           # Pattern analysis from observations
│   ├── daily-note-patterns.md
│   ├── task-system-schema.md
│   └── ...
├── patterns/           # Reusable patterns discovered
│   ├── multi-agent-coordination.md
│   └── compaction-recovery.md
├── proposals/          # Proposed improvements
│   ├── optimized-daily-template.md
│   └── arterial-log-template.md
├── tools/              # Tool designs and gaps
│   ├── gaps/
│   ├── research/
│   └── specs/
└── predictions/        # Oracle predictions
    └── [date].md
```

### Context Hierarchy

```
context/
├── active-agents.md         # Real-time coordination
├── priorities.md            # What to work on next
├── session-state.md         # Compaction-resilient state
├── predictions.md           # Oracle-generated predictions
├── capabilities.md          # What agents can do
├── off-limits.md           # Safety boundaries
├── ecosystem.md            # Tools and integrations
├── usage.md                # Metrics and stats
└── handoff.md              # Agent transition protocol
```

### Tasks Hierarchy

```
tasks/
├── README.md               # Lifecycle documentation
├── pending/                # Waiting to claim
│   ├── task-sched-001-*.md
│   ├── task-note-*.md
│   └── ...
├── active/                 # Currently claimed
│   ├── task-2026-01-31-overnight.desktop.md
│   └── ...
├── completed/              # Successfully finished
│   ├── task-cc-001-hooks-setup.claude-code.md
│   └── ...
└── failed/                 # Errors occurred
    └── [tasks that failed]
```

---

## Key Insights for Scheduler

### 1. Task Lifecycle Management

Tasks move through states via **file system operations**:
1. Create in `pending/`
2. Agent reads and moves to `active/`, renames to include agent suffix
3. Agent appends results to file
4. Agent moves to `completed/` or `failed/`

**For scheduler:** Schedule the claim/execute/complete cycle as file operations.

### 2. Capability Matching

Tasks declare `requires:` array. Scheduler can:
- Match task requirements to agent capabilities
- Block task if no agent can handle it
- Route to preferred_interface if specified
- Respect timeout constraints

### 3. Coordination via Files

No central database. Coordination happens through:
- `context/active-agents.md` - Who's working on what
- `context/priorities.md` - What to do next
- Task filenames - ownership indicated by suffix

**For scheduler:** Use file-based signaling; agents read/write coordination files.

### 4. Session Continuity

Recovery from context resets via:
- `context/session-state.md` - Extended summary of what happened
- Recovery protocol: Check git history → Read session state → Continue
- Blocked items: What's waiting on user input

**For scheduler:** Preserve session state across interruptions.

### 5. Agent Handoff Protocol

Handoff happens through:
- Update `context/priorities.md` with "Next Agent Should" section
- Log session to `logs/YYYY-MM-DD-[agent].md`
- Generate questions in `prompts/pending` for user review
- Update `context/active-agents.md` claim status

**For scheduler:** Implement explicit handoff steps between agents.

---

## Metadata Patterns by Task Type

### Research Tasks

```yaml
priority: high | medium
requires:
  - web_search
  - github_access
timeout: 60m
preferred_interface: claude-code
```

Sections: Objective → Scope → Analysis Questions → Deliverables → Acceptance Criteria

### Automation Tasks

```yaml
priority: medium
requires:
  - user_answers (blocked)
  - filesystem_access
timeout: 30m
preferred_interface: claude-code
```

Sections: Prerequisites → Steps → Acceptance Criteria → Blocked By

### Long-running Tasks

```yaml
priority: high
requires:
  - web_search
  - github_access
  - file_creation
timeout: 240m
preferred_interface: claude-desktop
```

Sections: Mission → Core Intentions → Work Streams → Continue Until → On Pause

### Analysis Tasks

```yaml
priority: high
requires:
  - obsidian-mcp
timeout: 60m
preferred_interface: claude-code
```

Sections: Objective → Scope → Analysis Questions → Deliverables → Acceptance Criteria → Related

---

## Validation Checklist

For scheduler implementation, verify:

- [ ] Task files use consistent YAML frontmatter
- [ ] `created` field is always present
- [ ] `priority` is one of: high, medium, low
- [ ] `requires` is array of capability strings
- [ ] `preferred_interface` respected when possible
- [ ] `timeout` is sensible duration for task type
- [ ] Body has clear sections with actionable content
- [ ] Acceptance criteria are measurable
- [ ] Blocked items are linked to prompts/answered
- [ ] Deliverables have clear locations
- [ ] Related links use wiki syntax `[[path/to/file]]`

---

## Related Documentation

- `tasks/README.md` - Task lifecycle documentation
- `agents/overnight.md` - Overnight agent definition
- `agents/architect.md` - Tool-building agent
- `agents/oracle.md` - Prediction agent
- `context/active-agents.md` - Real-time coordination
- `context/off-limits.md` - Safety boundaries
- `CLAUDE.md` - Global instructions and patterns

---

*Analysis complete. Ready for scheduler implementation.*
