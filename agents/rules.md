---
name: scheduler-rules
applies_to: all-scheduled-tasks
created: 2026-02-03
---

# Safety Rules for Scheduled Execution

> These rules are prepended to every scheduled task. Keep them concise.

## File Safety
- NEVER delete files without creating a backup first
- NEVER modify files outside the task's working_dir unless explicitly instructed
- NEVER touch: `.env*`, `*.key`, `.ssh/*`, `~/.config/*`, system files
- Prefer creating new files over modifying existing ones

## Git Safety
- NEVER force push
- NEVER commit directly to main/master
- NEVER rewrite git history
- Use descriptive commit messages: `[type]: description`

## Brain Repo Conventions
- Research output → `knowledge/`
- Execution logs → `logs/`
- Questions for user → `prompts/pending/`
- Context updates → `context/` (append, don't overwrite)
- Use Obsidian links: `[[like-this]]`

## Execution Discipline
- Respect the task timeout
- If stuck on something > 5 minutes, log it and move on
- If uncertain about a destructive action, skip it and note in output
- Complete what you can; document what you couldn't

## Output Requirements
- Always produce some output file or update
- If nothing to report, create a brief summary anyway
- Note any errors or issues encountered
- Suggest follow-up tasks if relevant
