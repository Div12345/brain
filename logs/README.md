# Logs Directory

Agents append activity logs here after each run.

## Format
`YYYY-MM-DD-HHMM-agentname.md`

## Required Sections
- **Task**: What was requested
- **Actions**: What was done
- **Findings**: Key discoveries
- **Next**: What successor agent should know
- **Duration**: Approximate runtime

## Example

```markdown
---
agent: overnight
started: 2026-01-31T02:00:00
ended: 2026-01-31T03:15:00
files_read: 34
files_written: 4
---

# Overnight Run 2026-01-31

## Task
Analyze vault daily notes, extract patterns

## Actions
- Read 30 daily notes (Jan 2026)
- Scanned 10 project files
- Identified 5 recurring themes

## Findings
- Theme: "PhD anxiety" appears 12/30 days
- Project "Cardiac Output" most active
- ...

## Next Agent Should Know
- Vault uses #status/incomplete tag inconsistently
- Some daily notes are very sparse (just links)
```
