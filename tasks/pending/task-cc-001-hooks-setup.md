---
id: task-cc-001
created: 2026-01-31T08:30:00Z
priority: high
requires:
  - filesystem_access
  - git
preferred_interface: claude-code
timeout: 60m
---

# Task: Set Up CC Hooks for Brain System

## Objective
Configure Claude Code hooks to integrate with the brain orchestration system.

## Background
The brain system needs Claude Code to:
1. Check for tasks before starting work
2. Log sessions to the brain repo
3. Update context files on completion

## Requirements

### 1. Create CC Settings File
Create `.claude/settings.json` in the brain repo:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "cat context/priorities.md | head -30",
          "timeout": 3
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command", 
          "command": "echo \"Session ended at $(date)\" >> logs/cc-sessions.log",
          "async": true
        }]
      }
    ]
  }
}
```

### 2. Create CLAUDE.md
Create brain-specific `CLAUDE.md`:
- Brief project overview
- Key directories
- Coordination protocol
- Safety rules

### 3. Test Hook Execution
Verify hooks fire correctly by:
1. Starting CC in brain repo
2. Checking that priorities show on prompt
3. Confirming log entry on session end

## Acceptance Criteria
- [ ] `.claude/settings.json` exists with hooks
- [ ] `CLAUDE.md` provides context < 100 lines
- [ ] Hooks execute without errors
- [ ] Session logging works

## Notes
- Don't use async hooks that might interfere with git commits
- Keep hook timeout short (< 5s)
- Log format should be parseable

## Resources
- inspirations/claude-code-ecosystem.md
- tools/orchestration/DESIGN.md
