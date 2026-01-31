---
created: 2026-01-31
tags:
  - research
  - automation
  - scheduling
  - claude-code
status: active
agent: overnight
aliases:
  - cron scheduling
  - task scheduler
---

# Task Automation & Scheduling

Options for running Claude agents on schedule.

## Recommended: claude-code-scheduler

**GitHub:** [jshchnz/claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler)

CC plugin for scheduled tasks. Cross-platform (Win/Mac/Linux).

**Install:**
```bash
/plugin marketplace add jshchnz/claude-code-scheduler
/plugin install scheduler@claude-code-scheduler
```

**Features:**
- Natural language: "every weekday at 9am"
- One-time & recurring
- Autonomous mode (edit files, commit)
- Git worktree isolation
- Windows Task Scheduler integration

**Example:**
```
You: Every night at 2am, check brain repo and run overnight analysis
Claude: Should this run in isolated worktree? → Yes
Claude: ✓ Task created
```

## Alternative: Windows Task Scheduler + CLI

For more control:

```powershell
# Create scheduled task
schtasks /create /tn "BrainOvernightRun" /tr "claude -p 'Run overnight brain analysis'" /sc daily /st 02:00
```

## Alternative: GitHub Actions

For repo-triggered automation:

```yaml
name: Overnight Analysis
on:
  schedule:
    - cron: '0 7 * * *'  # 2am EST = 7am UTC
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # API call to Claude for analysis
```

## For Brain System

### Recommended Setup
1. Install claude-code-scheduler plugin
2. Configure overnight task with worktree isolation
3. Task pushes results to brain repo
4. Morning: user reviews, answers questions

### Prompt Template for Scheduled Run
```
Read context/session-state.md and context/priorities.md from brain repo.
Check recent commits for other agent work.
Pick unclaimed work area.
Do research/analysis/building.
Commit changes with clear messages.
Update session-state.md.
Generate questions in prompts/pending.md.
```

## Related
- [[inspirations/claude-code-ecosystem#3. Hook System|CC Hooks]]
- [[agents/overnight]] - Agent definition
- [[prompts/pending#Q-2026-01-31-01]] - Schedule preference question
