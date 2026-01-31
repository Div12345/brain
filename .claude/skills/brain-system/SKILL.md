---
name: brain-system
description: Working in the brain orchestration repo. Use when modifying brain/, context/, tasks/, knowledge/, or coordinating between interfaces.
allowed-tools: Read, Write, Edit, Bash(git:*), Grep, Glob
---

# Brain System Skill

## Overview
The brain repo is a self-evolving AI assistant system coordinating multiple Claude interfaces (Desktop, Claude Code, API).

## Key Directories

| Directory | Purpose | Write Permission |
|-----------|---------|------------------|
| `context/` | Shared state, priorities, handoffs | Yes |
| `tasks/` | Task queue (pending/active/completed/failed) | Yes |
| `knowledge/` | Learned patterns, insights | Yes |
| `logs/` | Session logs, metrics | Yes |
| `agents/` | Agent definitions | Careful |
| `tools/` | Tool specs, configs | Careful |
| `prompts/` | Q&A with user | Yes |
| `experiments/` | Hypothesis testing | Yes |

## Coordination Protocol

### Before Starting Work
1. Check `context/active-agent.md` - is another agent working?
2. Read `context/priorities.md` - what matters now?
3. Check `tasks/pending/` - is there assigned work?
4. Review `prompts/answered.md` - any new user input?

### Claiming a Task
1. Move task from `pending/` to `active/`
2. Rename with agent suffix: `task-001.claude-code.md`
3. Update `context/active-agent.md`

### Completing Work
1. Move task to `completed/` or `failed/`
2. Update `context/priorities.md` if needed
3. Clear `context/active-agent.md`
4. Log session to `logs/`
5. Commit changes

### Handoff Pattern
When passing work to another interface:
1. Write to `context/handoff.md`:
```markdown
## Handoff: [brief title]
**From:** claude-code
**To:** desktop
**Context:** What was done, what's needed
**Files:** Relevant paths
**Urgency:** [high/medium/low]
```

## Safety Rules

### Never
- Modify files in `context/off-limits.md`
- Delete without explicit instruction
- Push to remote without user approval
- Overwrite another agent's active work

### Always
- Log what you do
- Generate questions for ambiguity
- Test before committing
- Keep commits atomic and descriptive

## File Formats

### Task (YAML frontmatter + Markdown)
```markdown
---
id: task-XXX
created: ISO8601
priority: high/medium/low
requires: [tools needed]
preferred_interface: claude-code/desktop/any
timeout: Xm
---

# Task Title

## Objective
## Requirements
## Acceptance Criteria
```

### Knowledge Entry
```markdown
# Topic

## Summary
## Details  
## Source
## Relevance
## Tags

---
*Generated: YYYY-MM-DD by [agent]*
```

### Question
```markdown
## Q-YYYY-MM-DD-NN: Title

**Priority:** high/medium/low
**Context:** Background
**Question:** The question
**Options:** (if applicable)
**Blocks:** What's waiting
```

## Common Operations

### Check current state
```bash
cat context/priorities.md | head -20
cat context/active-agent.md
ls tasks/pending/
```

### Log session
```bash
echo "## Session $(date -Iseconds)" >> logs/cc-sessions.log
echo "- Did X, Y, Z" >> logs/cc-sessions.log
```

### Commit pattern
```bash
git add -A
git commit -m "[type]: Brief description"
# Types: research, task, knowledge, config, fix
```

## Integration Notes

- Desktop Claude: Uses GitHub MCP, reads via API
- Claude Code: Direct filesystem, git commands
- Overnight agent: Runs scheduled, autonomous mode
- User: Reviews prompts/pending.md in morning
