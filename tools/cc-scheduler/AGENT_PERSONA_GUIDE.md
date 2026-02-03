---
created: 2026-02-03
updated: 2026-02-03
tags:
  - documentation
  - agents
  - personas
  - cc-scheduler
---

# Agent Persona Patterns & Definition Guide

> How to define and coordinate autonomous agents in the brain system

## OVERVIEW

The brain system uses agent personas to define autonomous roles. Each agent has:
- **Identity:** Who they are, what makes them unique
- **Capabilities:** What they can/cannot do
- **Workflow:** How they typically operate
- **Output formats:** Standard templates they use
- **Integration points:** How they coordinate with others

---

## PART 1: AGENT DEFINITION STRUCTURE

### Standard Agent File Template

All agent files go in `agents/` and use this structure:

```yaml
---
created: 2026-02-03
tags:
  - agent
  - [primary-domain]
  - [secondary-domain]
status: active
aliases:
  - Alternative name 1
  - Alternative name 2
---

# [Agent Name]

> One-line pitch describing the agent's core purpose

## Identity

Who you are, what makes you unique, your role in the system.

## Core Principles

1. **Principle Name:** Description
2. **Principle Name:** Description
3. **Principle Name:** Description

(3-5 principles that guide your decisions)

## Typical Session Flow

How you work from start to finish.

### Phase 1: [Name] (time estimate)
1. Step 1
2. Step 2

### Phase 2: [Name] (time estimate)
1. Step 1
2. Step 2

## Capabilities

### Can Do

- Capability 1
- Capability 2
- Capability 3

### Cannot Do

- Limitation 1
- Limitation 2

## Output Formats

### [Format Type 1]
Template or pattern for this output type

### [Format Type 2]
Template or pattern for this output type

## Error Handling

When something goes wrong:
1. Step 1
2. Step 2

## Integration Points

### With [Other Agent Name]
- Reads from: [files]
- Writes to: [files]
- Coordinates via: [mechanism]

### With [Other Agent Name]
- Reads from: [files]
- Writes to: [files]
- Coordinates via: [mechanism]

### With User
- Morning review: [where user reviews work]
- Feedback: [where user provides input]
- Direction: [where user sets priorities]

## Related

- [[knowledge/research/related-topic]]
- [[context/relevant-context]]
- [[other-agent]]

---

# [Agent Name]

> Pitch
```

### Naming Convention

**Agent files:** `agents/{name}.md` (all lowercase, kebab-case)

**Agent IDs (in active-agents.md):** `{role}-{instance}` or `{interface}-{model}`

**Examples:**
- File: `agents/overnight.md` → ID: `overnight-A`
- File: `agents/architect.md` → ID: `architect-001`
- File: `agents/claude-code-executor.md` → ID: `claude-code-001`
- File: `agents/desktop-researcher.md` → ID: `desktop-opus`

---

## PART 2: OBSERVED AGENT TYPES

### Type 1: Autonomous Researcher (Overnight Pattern)

**Purpose:** Deep research, analysis, pattern identification while user unavailable

**Characteristics:**
```yaml
Triggers: Scheduled time (overnight, background)
Interface: Command-line / scheduled runner
Duration: Long sessions (1-4 hours)
Output: Knowledge files, questions, predictions
Safety: Read-only unless explicitly building new files
```

**Typical Workflow:**
```
1. Orientation (5 min)
   ├─ Read context/priorities
   ├─ Check tasks/pending for assignments
   ├─ Review prompts/answered for user input
   └─ Scan logs for recent activity

2. Analysis (varies)
   ├─ Web research on key topics
   ├─ Vault analysis (if Obsidian access)
   ├─ Pattern identification
   └─ Gap analysis

3. Building (varies)
   ├─ Create knowledge files
   ├─ Draft specifications
   ├─ Document findings
   └─ Generate predictions

4. Handoff (5 min)
   ├─ Update context/priorities
   ├─ Create session log
   ├─ Generate questions for user
   └─ Commit all changes
```

**Key Integration:**
- Reads from: `context/`, `tasks/pending/`, `prompts/answered/`
- Writes to: `knowledge/`, `logs/`, `prompts/pending/`, `context/`
- Coordinates via: `context/session-state.md`, `context/active-agents.md`

**Example:** `agents/overnight.md`

### Type 2: Tool Builder (Architect Pattern)

**Purpose:** Design and build tools, MCPs, plugins when gaps identified

**Characteristics:**
```yaml
Triggers: Overnight agent identifies gap, user request, or pattern suggests value
Interface: Code editor (Claude Code preferred)
Duration: Medium-long sessions (1-2 hours per phase)
Output: Spec, code, tests, documentation, proposal
Safety: Never auto-integrate; always propose for user approval
```

**Typical Workflow (7 Phases):**
```
1. Gap Analysis (10 min)
   └─ Document problem clearly → knowledge/tools/gaps/

2. Research (20 min)
   ├─ GitHub: [problem] mcp, [problem] claude
   ├─ npm: existing packages
   ├─ Reddit/HN: discussions
   └─ Result: → knowledge/tools/research/

3. Design (15 min)
   └─ Minimal spec → tools/[type]/[name]/SPEC.md

4. Build (30-60 min)
   ├─ MCP: Node.js + SDK
   ├─ Plugin: Markdown command
   ├─ Hook: Config file
   └─ Code: Follows best practices

5. Test (20 min)
   ├─ Unit tests
   ├─ Integration tests
   └─ Failure tests → experiments/results/

6. Document (10 min)
   └─ User-facing README → tools/[type]/[name]/README.md

7. Propose Integration (5 min)
   └─ Create proposal → prompts/pending/
```

**Key Integration:**
- Reads from: `knowledge/`, `inspirations/`, `context/`
- Writes to: `tools/`, `knowledge/tools/`, `experiments/results/`, `prompts/pending/`
- Coordinates via: Task claiming, proposals

**Example:** `agents/architect.md`

### Type 3: Code Executor (Implementation Pattern)

**Purpose:** Execute code, make file changes, run commands, handle configuration

**Characteristics:**
```yaml
Triggers: Task assignment, user request in code context
Interface: Claude Code (VS Code editor)
Duration: Variable (5 min - 1 hour)
Output: Code changes, configurations, command results
Safety: Can modify any file; restricted by .claude/settings.json and policy
```

**Typical Workflow:**
```
1. Claim (1 min)
   └─ Move task from pending/ to active/

2. Understand (5 min)
   ├─ Read requirements
   ├─ Check existing code
   └─ Understand acceptance criteria

3. Execute (varies)
   ├─ Make changes (via editor or command)
   ├─ Test locally
   └─ Verify against criteria

4. Complete (2 min)
   ├─ Move task to completed/
   ├─ Update context/handoff.md
   └─ Commit with clear message
```

**Key Integration:**
- Reads from: `tasks/active/`, `context/`, any code files
- Writes to: Any code files, `tasks/completed/`, `context/handoff.md`
- Coordinates via: `context/active-agents.md`

**Capabilities:**
- Filesystem operations (read/write/delete)
- Git commands
- Command execution
- Code editing via VS Code
- Hook configuration

**Limitations:**
- Cannot push to remote (user must)
- Respects off-limits files
- Cannot delete core infrastructure files

### Type 4: Coordinator (Multi-Agent Orchestrator)

**Purpose:** Assign work, track progress, route tasks between specialized agents

**Characteristics:**
```yaml
Triggers: User-facing (chat interface)
Interface: Claude Desktop chat
Duration: Interactive (ongoing)
Output: Task assignments, coordination, summaries
Safety: Read-only; delegates all implementation
```

**Typical Workflow:**
```
1. Check State (2 min)
   ├─ Read context/session-state.md
   ├─ Review context/priorities.md
   ├─ Check context/active-agents.md
   └─ Scan tasks/pending/

2. Route Work (varies)
   ├─ Identify unclaimed tasks
   ├─ Match agent capabilities to requirements
   ├─ Create/assign new tasks
   └─ Update context/active-agents.md

3. Communicate (ongoing)
   ├─ Chat with user
   ├─ Ask clarifying questions
   ├─ Report progress
   └─ Handle exceptions

4. Summarize (5 min)
   └─ Update context files for next session
```

**Key Integration:**
- Reads from: All context files, task files, logs
- Writes to: `tasks/pending/`, `context/`, `prompts/pending/`
- Coordinates via: `context/active-agents.md`, file-based messaging

---

## PART 3: AGENT REGISTRATION

### How Agents Register

Agents add themselves to `context/active-agents.md`:

```markdown
| Agent | Interface | Working On | Since | Status |
|-------|-----------|------------|-------|--------|
| overnight-A | Desktop Claude | Multi-agent coordination | 09:30 | Active |
| scientist-001 | Claude Code | Bootstrap research | 08:00 | Active |
```

### Claiming Work Areas

When starting a task, update the "Claimed Work Areas" section:

```markdown
## Claimed Work Areas

| Area | Agent | Notes |
|------|-------|-------|
| `knowledge/research/multi-agent*` | overnight-A | Coordination patterns |
| `knowledge/tools/gaps/*` | architect-001 | Gap analysis |
| `tasks/pending/task-xyz*` | executor-low | Implementing feature |
```

**Rules:**
1. Use glob patterns (e.g., `knowledge/research/*`)
2. Add notes for context
3. Clear claim when done
4. Don't claim overlapping areas

### Recording Handoffs

When handing off to another agent, update `context/handoff.md`:

```markdown
## Recent Handoffs

| Time | From | To | Topic |
|------|------|----|-------|
| 10:15 | claude-code-web | any-agent | CC hooks + Obsidian conversion done |
| 14:30 | overnight-A | user | Deep research complete, questions pending |
```

---

## PART 4: CAPABILITY TAXONOMY

### System Capabilities

**Definition:** What systems/APIs the agent can use

| Capability | Meaning | Tools |
|------------|---------|-------|
| `filesystem_access` | Read/write local files | File API, bash |
| `git` | Git operations | git CLI |
| `bash` | Shell command execution | bash, shell |
| `web_search` | Search the internet | curl, web APIs |
| `github_access` | GitHub API | gh CLI, REST API |
| `obsidian_mcp` | Obsidian vault access | Obsidian MCP server |
| `claude_code` | Claude Code interface | CC editor |
| `claude_desktop` | Desktop Claude | Chat interface |
| `file_creation` | Create new files | File system |
| `api_calls` | Make HTTP requests | curl, node-fetch |

### Agent Capability Assignments

```yaml
---
# agents/overnight.md
capabilities:
  read:
    - filesystem_access
    - web_search
    - github_access
    - obsidian_mcp
  write:
    - filesystem_access (knowledge/, logs/, prompts/, context/)
    - git (commits only)
  interfaces:
    - command_line
    - scheduled
  cannot:
    - Direct user_input_required
    - Modify core system files
---
```

### Preferred Interface Matching

When creating tasks, set `preferred_interface` based on agent strengths:

| Agent Type | Preferred | Secondary | Avoid |
|------------|-----------|-----------|-------|
| Overnight Researcher | any (CLI) | claude-desktop | - |
| Tool Builder (Architect) | claude-code | any | - |
| Code Executor | claude-code | any | desktop (too slow for iteration) |
| Coordinator | claude-desktop | any | - |

---

## PART 5: SESSION LOGGING PATTERN

All agents log their work. Pattern: `logs/YYYY-MM-DD-{agent}.md`

### Standard Session Log Format

```yaml
---
created: 2026-02-03T14:00:00Z
completed: 2026-02-03T15:30:00Z
agent: overnight-a
tags:
  - log
  - overnight
---

# Overnight Agent Session - 2026-02-03

## Duration
- Start: 2026-02-03 02:00:00 UTC
- End: 2026-02-03 04:30:00 UTC
- Total: 2h 30m

## Objectives (from context/priorities)
1. [ ] Obsidian-ify brain repo
2. [ ] Research multi-agent coordination
3. [ ] Gap analysis for tooling

## What Got Done

### ✓ Completed (3 items)
1. Analyzed task file schemas
   - Created comprehensive schema documentation
   - Identified 8 field categories
   - Linked to examples

2. Mapped agent types
   - 4 primary types identified
   - Documented workflows
   - Created registration system

3. Documented context patterns
   - session-state.md structure
   - active-agents.md coordination
   - handoff protocol

### → In Progress (1 item)
1. Building cc-scheduler integration guide
   - Decision matrices 40% done
   - Examples being drafted

### ⏸ Blocked (1 item)
1. User preference for overnight schedule
   - [[prompts/pending#Q-2026-01-31-01]]
   - Waiting on answer

## Key Findings

### Discovery 1: Task Lifecycle is Robust
Brain system already has clear pending→active→completed workflow
with precise state tracking. No changes needed.

### Discovery 2: Agent Registration Prevents Conflicts
Using context/active-agents.md to claim work areas prevents
duplicate work between concurrent agents.

### Discovery 3: Frontmatter Conventions are Consistent
All files use same YAML structure + wikilinks. Can build
tooling around this pattern.

## Files Created
- `/home/div/brain/tools/cc-scheduler/TASK_FILE_SCHEMA.md`
- `/home/div/brain/tools/cc-scheduler/AGENT_PERSONA_GUIDE.md` (this file)

## Files Modified
- `context/session-state.md` (updated recovery protocol)
- `context/active-agents.md` (added new claims)

## Predictions Generated
- N/A (focus was documentation, not prediction)

## Questions Generated
- Q: How does cc-scheduler handle concurrent task claims?
- Q: What's the retry strategy if task fails?

## Next Session Should
1. Read this log + context/session-state.md
2. Review the two new documentation files
3. Continue cc-scheduler implementation
4. Test agent registration on example tasks

## Logs & Evidence
- Session output: [embedded above]
- Git history: See commits for TASK_FILE_SCHEMA.md, AGENT_PERSONA_GUIDE.md
- Related work: [[knowledge/research/multi-agent-coordination]]

## Artifacts Generated
- Session documentation (this file)
- 2 comprehensive guide files (6000+ lines total)

---

*End of session log*
```

### Key Session Log Sections

| Section | Purpose |
|---------|---------|
| Metadata | created, completed, agent, tags |
| Duration | Time tracking |
| Objectives | What was planned |
| What Got Done | ✓ done, → in progress, ⏸ blocked |
| Key Findings | Discoveries/insights |
| Files Created/Modified | What changed |
| Predictions Generated | Links to predictions made |
| Questions Generated | Links to questions for user |
| Next Session Should | Checklist for continuation |
| Artifacts | Deliverables produced |

---

## PART 6: MULTI-AGENT COORDINATION

### Coordination Mechanisms

**File-Based Coordination:**
```
context/
├─ active-agents.md          # Who's working where (poll this first!)
├─ session-state.md          # Compaction-resilient state
├─ handoff.md                # Explicit handoffs
├─ priorities.md             # What matters next
└─ predictions.md            # Expected future needs
```

**Task-Based Coordination:**
```
tasks/
├─ pending/                  # Available work
├─ active/                   # Being worked on
├─ completed/                # Done
└─ failed/                   # Errored
```

**Message-Based (If Needed):**
```
messages/
├─ inbox/                    # Incoming messages
└─ outbox/                   # Outgoing messages
```

### Coordination Protocol (Agent Perspective)

**Starting work:**
```
1. Read context/active-agents.md
   → Are you already listed?
   → Is your work area already claimed?

2. If you want to work:
   a. Check if work area claimed
   b. If not: Add yourself to "Currently Active"
   c. Add area to "Claimed Work Areas"
   d. Commit this change

3. Start work
   → Commit frequently (every 5-10 min)
   → Update context/active-agents.md as you claim new areas

4. When done:
   a. Clear your claim from "Claimed Work Areas"
   b. Remove yourself from "Currently Active"
   c. Create/update context/handoff.md with what you did
   d. Commit final changes
```

### Preventing Duplicate Work

**Anti-Pattern:** Two agents doing the same task

**Prevention:**
```
context/active-agents.md

| Area | Agent |
|------|-------|
| knowledge/research/multi-agent* | overnight-A |
| knowledge/research/obsidian* | overnight-B |
```

Agent C comes along, wants to research Obsidian. Sees it's claimed by overnight-B.
Result: Agent C picks different work or waits.

---

## PART 7: ERROR HANDLING PATTERNS

### When an Agent Gets Stuck

Standard protocol from `agents/overnight.md`:

```
If something goes wrong:
1. Log the error with full context
   → Where did it happen?
   → What were you trying to do?
   → What's the exact error?

2. Don't try to fix blindly
   → Document the issue
   → Move to next task

3. Generate a question for user
   → [[prompts/pending/Q-2026-02-03-XX.md]]

4. Continue with other tasks
   → Keep momentum going

5. Note in handoff what was skipped
   → Why this failed?
   → What needs user action?
```

### Failure Modes by Agent Type

**Overnight Researcher (Read-Only):**
```
Failure: Can't access external API
Action: Log error, skip that research, continue with other tasks

Failure: Obsidian vault corrupted
Action: Document issue, generate user question, skip vault analysis
```

**Tool Builder (Build Phase):**
```
Failure: Existing solution doesn't fit
Action: Document why, propose building new, ask user approval

Failure: Build fails tests
Action: Debug, fix, re-test, or document limitations
```

**Code Executor (Modify Phase):**
```
Failure: Tests fail after change
Action: Review change, fix, re-test, or rollback

Failure: Git conflict
Action: Resolve conflict, test again, commit
```

---

## PART 8: CREATING A NEW AGENT

### Step-by-Step

1. **Create agent file** `agents/{name}.md`

2. **Fill frontmatter:**
   ```yaml
   ---
   created: 2026-02-03
   tags:
     - agent
     - [domain1]
     - [domain2]
   status: active
   aliases:
     - Alternative name
   ---
   ```

3. **Define identity:**
   - One-line pitch
   - Who you are
   - What makes you unique

4. **Document workflow:**
   - Phases with time estimates
   - Step-by-step in each phase
   - Clear stopping conditions

5. **Specify capabilities:**
   - Can do (list)
   - Cannot do (list)
   - Access boundaries

6. **Define output:**
   - Output formats with templates
   - Where files go
   - Naming conventions

7. **Document integration:**
   - What files you read
   - What files you write
   - How you coordinate

8. **Test registration:**
   - Add yourself to `context/active-agents.md`
   - Test a simple task
   - Remove yourself when done

---

## SUMMARY

**Agent Persona System in Brain:**

1. **Definition:** Agents have explicit roles defined in `agents/` files
2. **Registration:** Agents register in `context/active-agents.md`
3. **Coordination:** File-based via context files
4. **Workflow:** Phase-based sessions with clear outputs
5. **Handoff:** Explicit via `context/handoff.md` + session logs
6. **Recovery:** Session state preserved for continuation

**Key Files:**
- `agents/{name}.md` - Agent definition
- `context/active-agents.md` - Who's working where
- `context/session-state.md` - Compaction-resilient state
- `context/handoff.md` - Handoff information
- `logs/YYYY-MM-DD-{agent}.md` - Session record

**Integration Pattern:**
```
Agent starts → Registers in active-agents.md
            → Does work in phases
            → Logs in logs/
            → Updates context/handoff.md
            → Unregisters from active-agents.md
Next agent starts with fresh context from session-state.md
```

---

*Last updated: 2026-02-03*
*Status: Complete and ready for cc-scheduler integration*
