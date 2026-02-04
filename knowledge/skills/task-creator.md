# Task Creator Skill

Create properly-specified tasks in both bd (bead) AND scheduler format with automatic linking.

## When to Use

- Creating new scheduled tasks for overnight/autonomous execution
- Converting ideas into actionable task specifications
- Ensuring bd↔scheduler sync from the start

## Input Template

Provide these fields (copy and fill in):

```markdown
## Quick Spec

**Goal:** [One sentence - what does "done" look like?]

**Environment:**
- Execution: [WSL2 | Windows | Docker]
- Working dir: [path, default ~/brain]
- Tools needed: [MCP tools, CLI tools, etc.]

**Blockers:** [Known issues, or "None"]

**Dependencies:** [bead IDs like brain-xyz, or "None"]

**Priority:** [1=urgent, 2=normal, 3=low]

**Complexity:** [simple|medium|complex]
```

## Output Generation

The skill produces TWO linked artifacts:

### 1. Bead Entry (bd)

**If bd CLI available (Claude Desktop/Windows):**
```bash
bd create "Task Title" \
  -d "Full description with goal, environment, success criteria" \
  --priority 2 \
  --labels "tag1,tag2" \
  --owner "overnight-agent@brain"
```

**If bd CLI unavailable (WSL):**
Append to `.beads/issues.jsonl`:
```json
{
  "id": "brain-xxx",
  "title": "Task Title",
  "description": "Full description...",
  "status": "open",
  "priority": 2,
  "issue_type": "task",
  "owner": "overnight-agent@brain",
  "created_at": "ISO-8601",
  "created_by": "Task Creator Skill",
  "updated_at": "ISO-8601",
  "labels": ["tag1", "tag2"]
}
```

### 2. Scheduler Task File

Create `tasks/pending/NNN-task-name.md`:

```yaml
---
name: task-name
priority: 1-3
estimated_tokens: <from complexity>
mode: autonomous | plan-first
timeout: <from complexity>
skill: analyze | plan | ecomode
model_hint: haiku | sonnet | opus
tags: [tag1, tag2]
depends_on: [other-task-names]
bead_id: brain-xxx
---

# Task Title

## Goal
[One sentence goal]

## Environment Constraints
- **Execution env:** [WSL2 | Windows | etc.]
- **Working dir:** [path]
- **MCP tools needed:** [list]
- **Depends on:** [bead IDs or task names]

## What This Task Must Produce
[Specific deliverables with file paths]

## Success Criteria
- [ ] [Verifiable criterion 1]
- [ ] [Verifiable criterion 2]

## Overnight Agent Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

## Complexity → Defaults Mapping

| Complexity | Tokens | Timeout | Mode | Model |
|------------|--------|---------|------|-------|
| simple | 5000 | 10m | autonomous | haiku |
| medium | 10000 | 20m | autonomous | sonnet |
| complex | 20000 | 30m | plan-first | sonnet/opus |

## Task Numbering

- Check existing files in `tasks/pending/`, `tasks/active/`, `tasks/completed/`
- Use next available number in sequence (e.g., 055, 060, 065)
- Increment by 5 to leave room for insertions

## BD ↔ Scheduler Sync Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    SOURCE OF TRUTH                          │
│                                                             │
│   .beads/issues.jsonl  ←─── bd is authoritative            │
│         │                                                   │
│         │ bead_id reference                                │
│         ▼                                                   │
│   tasks/pending/NNN-name.md  ←─── scheduler reads          │
│         │                                                   │
│         │ on execution                                      │
│         ▼                                                   │
│   tasks/active/NNN-name.md                                 │
│         │                                                   │
│         │ on completion                                     │
│         ▼                                                   │
│   tasks/completed/NNN-name.md                              │
│         │                                                   │
│         │ sync back                                         │
│         ▼                                                   │
│   bd update brain-xxx --status closed                      │
│   (or append close event to issues.jsonl)                  │
└─────────────────────────────────────────────────────────────┘
```

### Sync Rules

1. **Creation:** Always create bead FIRST, then scheduler task with bead_id
2. **Status Updates:**
   - Scheduler moves file: pending → active → completed/failed
   - Bead status: open → in_progress → closed
3. **Closing:** When task completes:
   - Move file to `tasks/completed/`
   - Update bead: `bd update <id> --status closed` or edit jsonl
   - Add `closed_at` and `close_reason` to bead

### Finding Bead ID

After `bd create`, the ID is returned. If using jsonl directly:
- IDs are format `brain-xxx` (3 random alphanumeric chars)
- Generate with: `brain-$(cat /dev/urandom | tr -dc 'a-z0-9' | head -c3)`

## Example: Full Task Creation

**Input:**
```markdown
## Quick Spec

**Goal:** Create a script that backs up Obsidian vault to GitHub daily

**Environment:**
- Execution: WSL2
- Working dir: ~/brain
- Tools needed: git, cron

**Blockers:** None

**Dependencies:** None

**Priority:** 3

**Complexity:** simple
```

**Output 1 - Bead (append to .beads/issues.jsonl):**
```json
{"id":"brain-v8k","title":"Obsidian Vault Daily Backup Script","description":"Create a script that backs up Obsidian vault to GitHub daily.\n\n## Environment\n- Execution: WSL2\n- Working dir: ~/brain\n- Tools: git, cron\n\n## Success Criteria\n- Script created at tools/scripts/vault-backup.sh\n- Cron job documented\n- Test run successful","status":"open","priority":3,"issue_type":"task","owner":"overnight-agent@brain","created_at":"2026-02-03T20:00:00Z","created_by":"Task Creator Skill","updated_at":"2026-02-03T20:00:00Z","labels":["automation","obsidian"]}
```

**Output 2 - Scheduler Task (tasks/pending/055-vault-backup-script.md):**
```yaml
---
name: vault-backup-script
priority: 3
estimated_tokens: 5000
mode: autonomous
timeout: 10m
skill: analyze
model_hint: haiku
tags: [automation, obsidian]
depends_on: []
bead_id: brain-v8k
---

# Obsidian Vault Daily Backup Script

## Goal
Create a script that backs up Obsidian vault to GitHub daily.

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain
- **Tools needed:** git, cron

## What This Task Must Produce
- `tools/scripts/vault-backup.sh` - backup script
- Documentation of cron setup in script comments

## Success Criteria
- [ ] Script created and executable
- [ ] Cron job syntax documented
- [ ] Manual test run successful

## Overnight Agent Instructions
1. Create backup script with git add/commit/push
2. Add error handling for network failures
3. Document cron syntax for daily execution
4. Test with dry-run
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| Creating scheduler task without bead | Always create bead first |
| Vague goal: "Fix the thing" | Specific: "Fix auth timeout by increasing TTL to 1hr" |
| No bead_id in scheduler task | Always link via bead_id |
| Closing task without closing bead | Sync both on completion |
| Guessing bead ID format | Use brain-xxx with 3 random chars |

## Integration with cc-scheduler

The scheduler reads tasks from `tasks/pending/` and:
1. Validates YAML frontmatter
2. Checks dependencies (depends_on resolved)
3. Estimates cost from estimated_tokens
4. Executes based on priority and budget

See `tools/cc-scheduler/config.yaml` for scheduler configuration.
