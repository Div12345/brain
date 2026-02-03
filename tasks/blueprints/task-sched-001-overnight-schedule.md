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

### 1. Install claude-code-scheduler
```bash
/plugin marketplace add jshchnz/claude-code-scheduler
/plugin install scheduler@claude-code-scheduler
```

### 2. Configure overnight task
```
You: Every night at [USER_TIME], run the overnight brain analysis prompt
Claude: Configure with worktree isolation? → Yes
```

### 3. Create overnight prompt
Save to `.claude/commands/overnight-run.md`:
```markdown
Read context/session-state.md and context/priorities.md.
Check recent commits for other agent activity.
Pick unclaimed work from context/active-agents.md.
Perform research/analysis on priorities.
Commit all changes with clear messages.
Update session-state.md.
Generate questions in prompts/pending.md.
Log session to logs/YYYY-MM-DD-overnight.md.
```

### 4. Test manually
```bash
claude /overnight-run
```

### 5. Verify scheduled task
```powershell
# Windows
schtasks /query /tn "ClaudeSchedule*"
```

## Acceptance Criteria
- [ ] Scheduler plugin installed
- [ ] Overnight task configured
- [ ] Test run completes successfully
- [ ] Commits appear in brain repo
- [ ] Session log created

## Blocked By
- [[prompts/pending#Q-2026-01-31-01]] - Need user's schedule preference

## Related
- [[knowledge/research/task-automation-scheduling]]
- [[agents/overnight]]
