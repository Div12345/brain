# Planning Handoff

**Claude Desktop** → creates plans → **Claude Code** executes them

## How It Works

1. User dumps idea in Claude Desktop
2. Claude Desktop asks clarifying questions
3. Saves plan to `~/brain/context/plans/plan-name.md`
4. Claude Code reads and executes

## Plan Format

```markdown
# Plan: [Name]

## Goal
What to achieve.

## Tasks
1. First thing
2. Second thing
3. Third thing

## Notes
Any constraints or preferences.
```

Keep it simple. All plans visible in one folder.

## Where Things Go

| What | Where |
|------|-------|
| Plans | `context/plans/*.md` |
| Tasks (ready to run) | `tasks/pending/*.md` |
| Results | `tasks/completed/*.md` |
| Logs | `logs/scheduler/*.md` |

## For Claude Desktop

Use Obsidian MCP `obsidian_update_note` to write plans.
Path: `context/plans/plan-name.md`
