---
created: 2026-02-03
updated: 2026-02-03
tags:
  - documentation
  - schema
  - tasks
  - cc-scheduler
---

# Task File Schema & System Format Reference

> Comprehensive documentation of task file formats, agent personas, and context management patterns observed in the brain system.

## PART 1: TASK FILE SCHEMA

### Standard Task Frontmatter Fields

All task files use YAML frontmatter. Fields are organized by requirement level.

#### REQUIRED Fields

| Field | Type | Format | Purpose | Example |
|-------|------|--------|---------|---------|
| `created` | ISO 8601 string | `YYYY-MM-DD[THH:MM:SSZ]` | When task was created | `2026-01-31` or `2026-01-31T08:30:00Z` |
| `tags` | Array | `[tag1, tag2, ...]` | Categorization & searchability | `[task, automation, hooks]` |

#### STRONGLY RECOMMENDED Fields

| Field | Type | Options | Purpose | Default | Example |
|-------|------|---------|---------|---------|---------|
| `priority` | String | `high` / `medium` / `low` | Task urgency for scheduling | `medium` | `high` |
| `requires` | Array | Capability names | What task needs to run | `[]` | `[web_search, github_access, file_creation]` |
| `preferred_interface` | String | `claude-code` / `claude-desktop` / `any` | Which agent interface best suited | `any` | `claude-code` |
| `timeout` | String | Duration format | Max execution time | `30m` | `60m`, `240m` |

#### OPTIONAL Fields

| Field | Type | Format | Purpose | Example |
|-------|------|--------|---------|---------|
| `id` | String | `task-YYYY-MM-DD-NNN` | Explicit task identifier | `task-2026-01-31-overnight` |
| `status` | String | `pending` / `active` / `completed` / `failed` | Current task state | `active` |
| `claimed_by` | String | Agent identifier | Which agent claimed task | `desktop-opus` |
| `updated` | ISO 8601 string | Timestamp | Last modification time | `2026-01-31T10:15` |
| `aliases` | Array | Names | Alternative task names | `[overnight agent, night agent]` |
| `blocked_by` | Array | File references | Dependencies | `[[prompts/pending#Q-2026-01-31-01]]` |
| `related` | Array | File references | Connected resources | `[[knowledge/research/task-automation-scheduling]]` |

### Complete Frontmatter Example

```yaml
---
id: task-2026-01-31-overnight
created: 2026-01-31T08:30:00Z
updated: 2026-02-03T15:00:00Z
priority: high
requires:
  - web_search
  - github_access
  - file_creation
preferred_interface: claude-desktop
timeout: 240m
status: active
claimed_by: desktop-opus
tags:
  - task
  - research
  - building
aliases:
  - overnight research
  - night analysis
blocked_by:
  - [[prompts/pending#Q-2026-01-31-01]]
related:
  - [[knowledge/research/multi-agent-coordination]]
  - [[agents/overnight]]
---
```

### Task Body Structure

All task files follow this content structure:

```markdown
---
[FRONTMATTER]
---

# Task: [Title]

## Mission / Objective
[High-level goal or why this task matters]

## Prerequisites / Context
[What needs to be true before starting]
[Links to relevant documentation]

## Scope
[Boundaries - what's in/out of scope]

## Steps / Work Streams (if applicable)
[Detailed breakdown of work to do]

### Step 1: [Name]
- [ ] Sub-task 1
- [ ] Sub-task 2

### Step 2: [Name]
- [ ] Sub-task 1

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Expected Output
[What success looks like]
[Where results go]

## Error Handling
[What to do if stuck]

## Related
[Links to related files/documentation]
```

### Naming Convention

**Pattern:** `task-{identifier}.{interface}.md` or `task-{date}-{name}.md`

**Examples:**
- `task-sched-001-overnight-schedule.md` - Descriptive naming
- `task-2026-01-31-overnight.md` - Date-based naming
- `task-cc-001-hooks-setup.claude-code.md` - With interface suffix when active/completed

**Rules:**
- Use kebab-case for multi-word names
- Include domain prefix (e.g., `cc-` for Claude Code, `sched-` for scheduling)
- When moving to active/completed, can add interface suffix
- All lowercase

### Lifecycle & Directory Placement

```
pending/
├─ task-sched-001-overnight-schedule.md         # Waiting to be claimed
└─ task-note-001-pattern-analysis.md

active/
├─ task-2026-01-31-overnight.desktop.md         # Actively being worked
└─ task-cc-001-hooks-setup.claude-code.md

completed/
├─ task-cc-001-hooks-setup.claude-code.md       # Successfully finished
└─ task-note-001-pattern-analysis.md

failed/
└─ task-xyz.claude-code.md                      # Errored out
```

**Transitions:**
1. **Claim:** Move from `pending/` → `active/`, update `status: active`, set `claimed_by`
2. **Succeed:** Move to `completed/`, set `status: completed`, append results
3. **Fail:** Move to `failed/`, set `status: failed`, log error details

---

## PART 2: AGENT PERSONA PATTERNS

### Agent Definition Structure

Agent files go in `agents/` and define autonomous roles.

```yaml
---
created: [date]
tags:
  - agent
  - [domain]
status: active
aliases:
  - Alternative names
---

# [Agent Name]

> One-line pitch

## Identity
[Who they are, what makes them unique]

## Core Principles
[3-5 guiding values]

## Typical Session Flow
[How they work step-by-step]

## Capabilities
### Can Do
[What they're allowed to do]

### Cannot Do
[Hard boundaries]

## Output Formats
[Standard templates they use]

## Error Handling
[What to do when stuck]

## Integration Points
[How they coordinate with other agents]

## Related
[Links to documentation]
```

### Observed Agent Types

#### 1. Overnight Agent (Autonomous Research/Analysis)

**Role:** Runs autonomous sessions while user is away, performing research, analysis, gap identification

**Key Characteristics:**
- Read-heavy (never modifies existing files)
- Creates files in knowledge/logs/inspirations
- Generates questions for user
- Commits frequently for visibility
- Logs all sessions

**Typical Output:**
- Research findings → `knowledge/research/`
- Session logs → `logs/YYYY-MM-DD-overnight.md`
- Questions → `prompts/pending/`
- Predictions → `knowledge/predictions/`

#### 2. Architect Agent (Tool Builder)

**Role:** Builds MCPs, plugins, hooks, commands when gaps identified

**Key Characteristics:**
- Research-first (always checks existing solutions)
- Multi-phase workflow (Gap → Research → Design → Build → Test → Document → Propose)
- Never auto-integrates (user must approve)
- Extensive documentation of decisions
- Design-before-code mentality

**Typical Output:**
- Gap analysis → `knowledge/tools/gaps/`
- Research findings → `knowledge/tools/research/`
- Specs → `tools/[type]/[name]/SPEC.md`
- Tests → `experiments/results/`
- Documentation → `tools/[type]/[name]/README.md`

#### 3. Claude Code Agent (Implementation)

**Role:** Handles code changes, file operations, command execution

**Characteristics:**
- Interface: VS Code editor + CLI
- Handles hooks configuration
- File operations and git
- Can be multi-session (maintains local state)

#### 4. Desktop Claude Agent (Research/Coordination)

**Role:** User-facing agent for research, questions, and multi-agent coordination

**Characteristics:**
- Interface: Claude Desktop chat
- Can coordinate between other agents
- Can read task files and assign work
- Generates questions for user

### Agent Registration & Coordination

Agents update `context/active-agents.md` to register:

```markdown
| Agent | Interface | Working On | Since | Status |
|-------|-----------|------------|-------|--------|
| overnight-A | Desktop Claude | Multi-agent coordination | 09:30 | Active |
| scientist-001 | Claude Code | Bootstrap research | 08:00 | Active |
```

---

## PART 3: CONTEXT & STATE MANAGEMENT PATTERNS

### Core Context Files

All context files go in `context/` and use frontmatter:

```yaml
---
created: [date]
updated: [date]
tags:
  - context
  - [topic]
---
```

#### 3.1 Session State (`context/session-state.md`)

**Purpose:** Compaction-resilient state recovery after context window resets

**Key Fields:**
```yaml
---
created: 2026-01-31
tags:
  - context
  - session
  - compaction-resilient
updated: 2026-02-03
agent: [current-agent-name]
---
```

**Content Structure:**
- Active Agent (current worker)
- Session Summary (list of major outputs)
- Pending (blocked on what)
- Recovery Protocol (how to continue after reset)

**Recovery Protocol Pattern:**
```markdown
## Recovery Protocol
1. `gh api repos/Div12345/brain/commits --jq '.[0:5]'`
2. Read this file + [[context/predictions]]
3. Continue from pending list
```

#### 3.2 Active Agents (`context/active-agents.md`)

**Purpose:** Coordination - who's working on what, prevents duplicate work

**Structure:**
```markdown
| Agent | Interface | Working On | Since | Status |
|-------|-----------|------------|-------|--------|

## Claimed Work Areas
| Area | Agent | Notes |

## Recent Handoffs
| Time | From | To | Topic |

## Coordination Rules
1. Check before starting
2. Update when claiming
3. Clear when done
4. Commit frequently
```

#### 3.3 Priorities (`context/priorities.md`)

**Purpose:** Guidance for next agent - what matters most

**Structure:**
```markdown
| Priority | Task | Owner | Status |

## Immediate
[This run's priorities]

## Short-Term (This Week)
[Week-long priorities]

## Medium-Term (This Month)
[Month-long goals]

## Open Questions
[Blockers]

## Next Agent Should
[Checklist of recommended actions]
```

#### 3.4 Handoff Protocol (`context/handoff.md`)

**Purpose:** Explicit handoff information between agents

**Structure:**
```markdown
## Current Handoff
| Field | Value |
| From | Agent name |
| To | Next agent or user |
| Time | Timestamp |
| Status | What's complete |

## Context
[Brief summary]

## Key Files Created This Session
[List of files created/modified]

## Completed Actions
- [x] Action 1
- [x] Action 2

## Pending Actions
- [ ] Action 1 (needs user input)

## For Next Agent
1. Read [[context/session-state]]
2. Check [[context/priorities]]
3. Do this next

## Ready to Use
[What's immediately usable]

## Related
[Links to session docs]
```

### Time-Scoped Logs

Each agent logs their session:

**Pattern:** `logs/YYYY-MM-DD-{agent}.md` or `logs/YYYY-MM-DD-overnight.md`

**Content:**
```yaml
---
created: [start time]
completed: [end time]
agent: [agent name]
tags:
  - log
  - [agent]
---

# [Agent] Session - YYYY-MM-DD

## Duration
Start: HH:MM
End: HH:MM
Total: Xm

## Tasks Completed
- [ ] Task 1
- [ ] Task 2

## Findings Summary
[Key discoveries]

## Predictions Generated
[Links to prediction files created]

## Questions Generated
[Links to question files created]

## Files Created/Modified
[List of changes]

## Next Session Priorities
[Recommended next steps]
```

### Prediction Files

**Location:** `knowledge/predictions/` or inline in context files

**Pattern:** Links and confidence indicators

**Example from context/session-state.md:**
```markdown
## Pending (Blocked on User)
- Q-01: Overnight schedule preference
- Q-02: Obsidian vault path
- Q-03: Failed task notification
```

---

## PART 4: FRONTMATTER CONVENTIONS (OBSIDIAN FORMAT)

All files in brain system use YAML frontmatter + wikilinks:

### Standard Fields (All Files)

```yaml
---
created: 2026-02-03              # When created (ISO date or datetime)
updated: 2026-02-03              # Last modification
tags:                            # Obsidian tags for navigation
  - category
  - type
  - status/phase
---
```

### Optional Standard Fields

```yaml
aliases:                         # Alternative names for wikilinks
  - name1
  - name2
status: active|pending|done      # Current phase
priority: high|medium|low        # Importance
agent: agent-name                # Which agent owns this
```

### Wikilink Patterns

**Format:** `[[path/to/file]]` or `[[path/to/file#heading|display text]]`

**Examples from observed files:**
```markdown
- Read [[context/priorities]]
- Check [[tasks/pending/]] for assigned work
- Review [[prompts/answered]] for new user input
- Scan [[logs/]] for recent activity
- Continue [[agents/desktop|Desktop Claude]]
- Related: [[knowledge/research/ai-memory-systems|AI Memory Systems]]
```

**Resolution Rules:**
- Absolute paths from repo root
- No file extensions (.md implied)
- Can link to headings with `#`
- Display text optional after `|`

### Tag Conventions

Observed tag patterns:

**Categories:**
- `task` / `context` / `knowledge` / `agent` / `log`

**Domains:**
- `automation` / `scheduling` / `obsidian` / `hooks` / `mcp`

**Status:**
- `status/pending` / `status/active` / `status/done` / `status/blocked`

**Types:**
- `documentation` / `research` / `proposal` / `experiment`

**Example:** `tags: [task, automation, scheduling, status/pending]`

---

## PART 5: CAPABILITY REQUIREMENTS

### Capability Tags in Task `requires` Field

Common capabilities needed:

**System Access:**
- `filesystem_access` - Read/write files
- `git` - Git operations
- `bash` - Shell command execution

**External Services:**
- `web_search` - Search the internet
- `github_access` - GitHub API
- `obsidian_mcp` - Obsidian vault access
- `file_creation` - Can create new files

**Specialized:**
- `claude_code` - Claude Code interface
- `claude_desktop` - Desktop Claude
- `user_answers` - Need user to answer questions first

### Preferred Interface Options

| Value | Meaning |
|-------|---------|
| `claude-code` | Works best in VS Code editor (CC) |
| `claude-desktop` | Works best in chat interface (Desktop) |
| `any` | Either interface is fine |

---

## PART 6: TASK EXAMPLES FROM BRAIN SYSTEM

### Example 1: Scheduled Task

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

Configure automated overnight runs...

## Prerequisites
- [ ] User answers [[prompts/pending#Q-2026-01-31-01|schedule preference]]
- [ ] CC installed with permissions

## Steps
### 1. Install claude-code-scheduler
### 2. Configure overnight task
...
```

**Key Patterns:**
- ✓ Blocked by user answers (in Prerequisites)
- ✓ Specific interface preference (claude-code)
- ✓ Clear timeout (30m)
- ✓ Checkboxes for progress tracking

### Example 2: Research Task

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
tags:
  - task
  - research
  - building
---

# Task: Deep Orchestration Research & Build Night

## Mission
Continue building the brain system overnight...

## Work Streams

### Stream 1: Deep Tool Research
- [ ] Get claude-flow installation details
- [ ] Research hookify
...

### Stream 2: Build Out Infrastructure
...

## Continue Until
- Rate limited, OR
- Major blocker requiring user input, OR
- All streams exhausted
```

**Key Patterns:**
- ✓ Actively claimed (`status: active`, `claimed_by`)
- ✓ Long timeout (240m) for deep work
- ✓ Multiple work streams with independent checkboxes
- ✓ Clear stopping conditions

### Example 3: Analysis Task

**File:** `tasks/completed/task-note-001-pattern-analysis.md`

```yaml
---
created: 2026-02-01
tags:
  - task
  - analysis
  - obsidian
  - status/pending
priority: high
requires:
  - obsidian-mcp
preferred_interface: claude-code
timeout: 60m
---

# Task: Analyze Daily Note & Log Patterns

## Objective
1. Understand what sections are used
2. Find the daily note → next day disconnect
3. Analyze logs for patterns

## Analysis Questions
- [ ] Which template sections have >50% fill rate?
- [ ] What do users actually write?
...

## Deliverables
1. `knowledge/analysis/daily-note-patterns.md`
2. `knowledge/proposals/optimized-daily-template.md`
```

**Key Patterns:**
- ✓ Clear objective with numbered questions
- ✓ Specific deliverable paths
- ✓ MCP-specific requirement

---

## PART 7: DECISION MATRIX FOR CC-SCHEDULER

### When Creating a New Task File

**Question → Field Decision:**

| Question | Field(s) | Example |
|----------|----------|---------|
| Is this urgent? | `priority: high` | Yes → high, No → medium/low |
| Does it need specific interface? | `preferred_interface` | Code work → claude-code, Chat → claude-desktop |
| How long will it take? | `timeout` | 30 min fix → 30m, Deep research → 240m |
| What does it need? | `requires: [...]` | List capabilities needed |
| Is it blocked? | Add Prerequisites section | Link to `[[prompts/pending#Q-ID]]` |
| Is it related to other work? | `related:` + Related section | `[[knowledge/...]]`, `[[agents/...]]` |
| Is this final? | `status: completed` | Append results at end |

### When Claiming a Task (Agent Perspective)

1. Check `context/active-agents.md` - is anyone else working here?
2. If clear, move file from `pending/` to `active/`
3. Add to file: `status: active`, `claimed_by: [your-id]`
4. Update `context/active-agents.md` with your work area
5. Start work (checkboxes track progress)
6. Commit frequently (every 5-10 min)

### When Completing a Task

1. Mark all checkboxes complete
2. Append results/summary to task file
3. Move to `completed/` folder
4. Update `status: completed`
5. Update `context/active-agents.md` (remove your claim)
6. Add note to `context/handoff.md`
7. Commit with clear message

---

## PART 8: ANTI-PATTERNS TO AVOID

| Anti-Pattern | Why It's Bad | Right Way |
|--------------|-------------|-----------|
| Task with no timeout | Ambiguous expectations | Always set explicit timeout |
| No `requires` field | Agent doesn't know prerequisites | Always list capabilities needed |
| Unclear acceptance criteria | Can't tell when done | Write checkboxes or explicit criteria |
| Task created without priority | Can't rank work | Always set high/medium/low |
| Duplicate work in active | Two agents doing same thing | Check `context/active-agents.md` first |
| No links to related files | Context lost | Use wikilinks to relevant docs |
| Task blocked but no `blocked_by` | No visibility on why stuck | Explicitly link to what's blocking |
| Abandoned task without status | Confusing state | Always move to completed/failed or update status |

---

## SUMMARY TABLE

Quick reference for task file creation:

| Element | Required? | Type | Example |
|---------|-----------|------|---------|
| Frontmatter | YES | YAML | `---...---` |
| `created` | YES | ISO date | `2026-02-03` |
| `tags` | YES | Array | `[task, research, status/pending]` |
| `priority` | Recommended | String | `high`, `medium`, `low` |
| `requires` | Recommended | Array | `[web_search, git]` |
| `preferred_interface` | Recommended | String | `claude-code`, `claude-desktop`, `any` |
| `timeout` | Recommended | Duration | `30m`, `60m`, `240m` |
| `status` | Optional | String | `pending`, `active`, `completed` |
| `claimed_by` | If active | String | `desktop-opus`, `claude-code-a` |
| Title | YES | Markdown | `# Task: [Name]` |
| Objectives/Steps | YES | Content | Clear sections with [ ] checkboxes |

---

## RELATED DOCUMENTATION

- `tasks/README.md` - Original task lifecycle docs
- `agents/overnight.md` - Overnight agent persona
- `agents/architect.md` - Architect agent workflow
- `context/session-state.md` - State recovery patterns
- `context/active-agents.md` - Coordination file
- `meta/obsidian-conventions.md` - Wikilink/frontmatter rules (if exists)

---

*Last updated: 2026-02-03*
*Author: Research Agent*
*Status: Complete and ready for cc-scheduler integration*
