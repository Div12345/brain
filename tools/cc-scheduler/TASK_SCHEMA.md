---
created: 2026-02-03
tags:
  - documentation
  - scheduler
  - task-system
type: reference
---

# Task System Schema Reference

Quick reference for cc-scheduler implementation.

## Task File Format

### Location
```
tasks/{state}/{id}.{agent-suffix}.md

States: pending, active, completed, failed
Agent suffixes: claude-code, desktop, overnight, etc.
```

### Minimal Frontmatter (REQUIRED)

```yaml
---
created: YYYY-MM-DD or ISO timestamp
tags: [array, of, tags]
priority: high | medium | low
---
```

### Full Frontmatter (RECOMMENDED)

```yaml
---
id: task-YYYY-MM-DD-NNN or task-NAME-001
created: 2026-01-31T08:30:00Z
tags: [task, category, status/pending]
priority: high | medium | low
requires: [capability1, capability2]
preferred_interface: claude-code | claude-desktop | any
timeout: 30m | 60m | 240m | Xm | Xh
---
```

### Active Task Fields (when status = active)

```yaml
status: active
claimed_by: agent-name
updated: ISO timestamp
```

## Body Structure

Standard sections (in recommended order):

```markdown
# Task: [Title]

## Mission / Objective
[High-level goal]

## Scope
[What's in/out of bounds]

## Steps / Prerequisites
[How to do it]

## Input / Prerequisites
[What's needed first]

## Expected Output / Deliverables
[What success looks like]

## Acceptance Criteria
[Measurable pass/fail conditions]

## Blocked By
[Dependencies or user answers needed]

## Related
[Links to related docs with [[wiki-syntax]]]
```

## Field Reference

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `created` | ISO date or timestamp | YES | `2026-01-31` or `2026-01-31T08:30:00Z` |
| `tags` | array | YES | `[task, automation, status/pending]` |
| `priority` | enum | YES | `high`, `medium`, `low` |
| `id` | string | NO | `task-sched-001-overnight` |
| `requires` | array | NO | `[web_search, github_access]` |
| `preferred_interface` | enum | NO | `claude-code`, `claude-desktop`, `any` |
| `timeout` | duration | NO | `30m`, `60m`, `240m` |
| `status` | enum | NO (active only) | `active` |
| `claimed_by` | string | NO (active only) | `claude-code`, `desktop-opus` |
| `updated` | ISO timestamp | NO (active only) | `2026-01-31T10:05` |

## Capability Names

Common `requires:` values:

```
web_search          # Web search capability
github_access       # GitHub API access
file_creation       # Create files in repo
filesystem_access   # Read/write filesystem
obsidian-mcp        # Obsidian vault access
user_answers        # Blocked on user input
claude-code         # Claude Code interface
git                 # Git operations
```

## Priority Levels

| Priority | Urgency | Typical Timeout | Example |
|----------|---------|-----------------|---------|
| high | Do ASAP | 30-60m | Research, critical fixes |
| medium | Do today | 30-120m | Automation, setup |
| low | Do eventually | 120-240m | Polish, long research |

## Task Lifecycle

### State Transitions

```
pending/ → active/ → completed/
                 ↘ failed/
```

### State Rules

| State | Filename Format | Contains | Action |
|-------|-----------------|----------|--------|
| pending | `task-XXX.md` | No `claimed_by` | Waiting to be claimed |
| active | `task-XXX.AGENT.md` | `status: active`, `claimed_by` | Being worked |
| completed | `task-XXX.AGENT.md` | Results appended | Success |
| failed | `task-XXX.AGENT.md` | Error details appended | Error |

### Scheduler Operations

1. **LIST PENDING**
   - Read `tasks/pending/`
   - Filter by `requires:` against available agents
   - Sort by `priority`
   - Return matching tasks

2. **CLAIM TASK**
   - Read task file
   - Add `status: active` and `claimed_by: AGENT`
   - Rename file to include agent suffix: `task-XXX.AGENT.md`
   - Move to `tasks/active/`
   - Update `context/active-agents.md`

3. **COMPLETE TASK**
   - Append results/summary to task file
   - Move to `tasks/completed/`
   - Remove from `context/active-agents.md`
   - Optionally clean up `active-agents.md`

4. **FAIL TASK**
   - Append error details to task file
   - Move to `tasks/failed/`
   - Remove from `context/active-agents.md`
   - Log to `logs/`

## Coordination Files

### active-agents.md

Tracks real-time work allocation:

```markdown
## Currently Active

| Agent | Interface | Working On | Since | Status |
|-------|-----------|------------|-------|--------|
| overnight-A | Desktop Claude | Multi-agent coordination | 09:30 | Active |

## Claimed Work Areas

| Area | Agent | Notes |
|------|-------|-------|
| `knowledge/research/multi-agent*` | overnight-A | Coordination patterns |

## Coordination Rules

1. **Check this file** before starting work
2. **Update claiming** when starting new area
3. **Clear claim** when done
4. **Don't duplicate** - if claimed, work elsewhere
5. **Commit frequently** - every 5-10 min for visibility
```

### priorities.md

Next-task guidance:

```markdown
## Immediate
| Priority | Task | Owner | Status |
|----------|------|-------|--------|
| 1 | Obsidian-ify brain repo | overnight | 🔄 In progress |

## Next Agent Should
- [ ] Continue Obsidian conversion
- [ ] Test graph view connectivity
- [ ] Generate predictions
- [ ] Log session to [[logs/]]
```

### session-state.md

Compaction-resilient session summary:

```markdown
## Active Agent
- **scientist-001** (Claude Code): Bootstrap research ✓

## Session Summary (Extended)
**Research Docs Created (10):**
- [[knowledge/research/recursive-self-improvement]]
- ...

## Pending (Blocked on User)
- Q-01: Overnight schedule preference
- Q-02: Obsidian vault path

## Recovery Protocol
1. `gh api repos/Div12345/brain/commits --jq '.[0:5]'`
2. Read this file + [[context/predictions]]
3. Continue from pending list
```

## Agent Suffixes

Common values for `{agent-suffix}` in filenames:

```
claude-code          # Claude Code agent
desktop              # Desktop Claude
overnight            # Overnight agent
desktop-opus         # Desktop Claude (Opus model)
scientist-001        # Data scientist agent
architect            # Architecture agent
```

## Example Task Files

### Pending Task (Minimal)

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

Configure automated overnight runs for brain system.

## Prerequisites
- [ ] User answers [[prompts/pending#Q-2026-01-31-01|schedule preference]]
- [ ] CC installed with permissions

## Steps
1. Install scheduler plugin
2. Configure overnight task
3. Create overnight prompt
4. Test manually
5. Verify scheduled task

## Acceptance Criteria
- [ ] Scheduler plugin installed
- [ ] Overnight task configured
- [ ] Test run completes successfully
- [ ] Commits appear in brain repo
- [ ] Session log created

## Blocked By
- [[prompts/pending#Q-2026-01-31-01]] - Need user's schedule preference
```

### Active Task (Full)

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

Continue building the brain system overnight.

## Mission
Research, prototype, document. Make tangible progress that CC can build on tomorrow.

## Core Intentions (from user)
- Self-evolving system that learns patterns
- Builds its own tools when gaps exist
- Scientific experimentation with logging
- Proactive - anticipate, don't wait
- No harm to existing systems

## Work Streams

### Stream 1: Deep Tool Research
- [ ] Get claude-flow installation details & gotchas
- [ ] Research hookify / CC hooks system
- [ ] Find CC plugin architecture docs
- [ ] Research AIM memory MCP capabilities

### Stream 2: Build Out Infrastructure
- [ ] Create overnight agent definition
- [ ] Draft CC startup hook
- [ ] Prototype usage tracking schema

### Stream 3: Knowledge Synthesis
- [ ] Document learnings in knowledge/insights/
- [ ] Update inspirations/ with new discoveries

## Output Locations
- Research → `inspirations/`
- Designs → `tools/`
- Insights → `knowledge/insights/`
- Questions → `prompts/pending.md`
- Logs → `logs/`

## Continue Until
- Rate limited, OR
- Major blocker requiring user input, OR
- All streams exhausted

## On Pause
Write status to `context/overnight-status.md` so work can resume.
```

## Key Patterns

### 1. Status in Tags

Some tasks use `status/pending`, `status/active` in tags:

```yaml
tags:
  - task
  - automation
  - status/pending
```

Scheduler can use this for filtering/display.

### 2. Links to Blocked Items

Tasks reference user questions:

```markdown
## Blocked By
- [[prompts/pending#Q-2026-01-31-01]] - Need user input
```

Scheduler can check if linked items exist.

### 3. Acceptance Criteria as Checklist

```markdown
## Acceptance Criteria
- [ ] Scheduler plugin installed
- [ ] Overnight task configured
- [ ] Test run completes successfully
```

Agents mark these off when completing.

### 4. Related Links

```markdown
## Related
- [[prompts/pending#Q-2026-01-31-01]]
- [[knowledge/research/task-automation-scheduling]]
- [[agents/overnight]]
```

Scheduler can use for context discovery.

### 5. Work Streams for Parallelization

```markdown
## Work Streams

### Stream 1: Deep Tool Research
- [ ] Task 1
- [ ] Task 2

### Stream 2: Build Out Infrastructure
- [ ] Task 3
- [ ] Task 4
```

Scheduler can decompose into sub-tasks.

## Scheduler Implementation Checklist

- [ ] Parse YAML frontmatter correctly
- [ ] Handle both ISO timestamps and simple dates in `created`
- [ ] Match task `requires:` against agent capabilities
- [ ] Respect `preferred_interface` when available
- [ ] Enforce `timeout` constraints
- [ ] Implement state transitions (pending → active → completed/failed)
- [ ] Update `context/active-agents.md` on claim/completion
- [ ] Add `status: active` and `claimed_by` fields when claiming
- [ ] Preserve task body when moving between states
- [ ] Rename files to include agent suffix in active/ directory
- [ ] Handle blocked tasks (don't schedule if blocked)
- [ ] Generate session logs with task summaries
- [ ] Implement recovery from incomplete tasks
- [ ] Support "Continue Until" conditions for long-running tasks
- [ ] Implement "On Pause" handoff protocol

---

*Last updated: 2026-02-03 by scientist-low*
