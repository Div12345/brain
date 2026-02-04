---
name: scheduler-setup-skill
bead_id: brain-cka
priority: 3
estimated_tokens: 10000
mode: autonomous
timeout: 15m
skill: analyze
model_hint: sonnet
tags: [infrastructure, skill]
depends_on: []
---

# Skill: Scheduler Setup Guide

## Goal
Convert knowledge/guides/scheduler-setup.md into a proper parameterized skill.

## Environment Constraints
- **Execution env:** WSL2 Claude Code
- **Working dir:** ~/brain
- **Input:** knowledge/guides/scheduler-setup.md (current guide)

## What This Task Must Produce

### 1. Parameterized Skill Document
Create `knowledge/skills/scheduler-setup.md` with:
- Parameters for user home path (not hardcoded `/home/div`)
- Auto-detection of WSL distro name
- Variable for brain repo location
- Configurable schedule time

### 2. Validation Steps
Add verification commands after each setup step:
- Check script exists and is executable
- Verify WSL can run bash scripts
- Confirm task scheduler registered
- Test capacity check works

### 3. Rollback Instructions
Document how to:
- Remove scheduled tasks
- Clean up state files
- Restore previous configuration

## Success Criteria
- [ ] Skill document created at knowledge/skills/scheduler-setup.md
- [ ] All paths parameterized
- [ ] Validation steps included
- [ ] Rollback documented
- [ ] Original guide can be archived
