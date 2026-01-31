# Off-Limits

> Files and directories agents should never modify without explicit user approval.

## System Files
- `/.git/` - Git internals
- `/CLAUDE.md` - Only via explicit task
- `/README.md` - Only via explicit task

## User Data
- Any file in user's Obsidian vault (read-only unless vault analysis task)
- Financial documents
- Work credentials

## Destructive Operations
- `git push` without user approval
- `git reset --hard`
- File deletion
- Overwriting without backup

## Notes

This file can be updated by user via prompts/answered.md or direct edit.

---
*Last reviewed: 2026-01-31*
