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

Configure Claude Code hooks to integrate with brain orchestration.

## Requirements

### 1. Create `.claude/settings.json`
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "cat context/priorities.md | head -30",
        "timeout": 3
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command", 
        "command": "echo \"Session ended at $(date)\" >> logs/cc-sessions.log",
        "async": true
      }]
    }]
  }
}
```

### 2. Test hook execution
- Start CC in brain repo
- Verify priorities show on prompt
- Confirm log entry on session end

## Acceptance Criteria
- [ ] `.claude/settings.json` exists with hooks
- [ ] [[CLAUDE]] provides context < 100 lines
- [ ] Hooks execute without errors
- [ ] Session logging works

## Related
- [[inspirations/claude-code-ecosystem#3. Hook System|Hook System docs]]
- [[.claude/skills/brain-system/SKILL|Brain Skill]]
