# Task 083: OneNote Inventory — Preparation Complete

**Date:** 2026-02-11  
**Status:** ✅ READY FOR EXECUTION  
**Prepared By:** Claude Code (WSL/Linux)  
**Target Agent:** Claude Desktop / Overnight Agent (Windows)

## Summary

Successfully prepared a comprehensive OneNote inventory task for execution on Windows machine. Created complete task specification, agent alert, and coordination registry entries. All files committed and pushed to GitHub.

## Deliverables

### 1. Task Definition File
- **Path:** `tasks/pending/083-windows-onenote-inventory.md`
- **Commit:** aad4dab
- **Size:** 113 lines
- **Contents:** Complete task specification with objective, scope, requirements, output format, and success criteria

### 2. Agent Alert Message
- **Path:** `messages/outbox/MSG-20260211-claude-code-to-desktop-onenote-inventory.md`
- **Commit:** 25f507f
- **Size:** 41 lines
- **Contents:** High-priority alert to Claude Desktop with task summary, key locations, and action steps

### 3. Coordination Registry Update
- **Path:** `context/active-agents.md`
- **Commit:** ab7eb99
- **Status:** Updated with agent registration, claimed work area, handoff timestamp, and task tracking

## Task Scope

**Objective:** Find ALL OneNote notebooks across all Windows locations

**Target Machine:** Windows (C:\Users\din18\)

**Locations to Scan:**
1. `C:\Users\din18\OneDrive - University of Pittsburgh\Onenote` — HIGH PRIORITY (Sept 2023 backup)
2. `C:\Users\din18\OneDrive\` — MEDIUM PRIORITY (personal)
3. `C:\Users\din18\Documents\OneNote Notebooks\` — MEDIUM PRIORITY (local storage)
4. `C:\Users\din18\AppData\Local\Microsoft\OneNote\` — LOW PRIORITY (app cache)
5. System-wide search for `*.onepkg`, `*.one`, `*.onetoc2` — HIGH PRIORITY

**Data to Capture (per notebook):**
- Full Windows path
- File name
- File type (onepkg backup / live notebook / .one / cache)
- Size (MB/GB)
- Last modified date
- Account association (Pitt edu / personal / BITS / unknown)
- Status (active / backup / orphaned / sync state)

**Account Information:**
- Signed-in Microsoft accounts
- Configured OneDrive accounts
- Sync status per account
- Account email addresses
- Tenant information

## Output Specification

**Location:** Obsidian vault  
**Path:** `Projects/Mining Results/onenote-inventory.md`

**Format:** Markdown table with sections per account
```markdown
## Account: [Account Email/Name]
### Status: [Active/Backup/Unknown]
### Location: [General Location]

| Notebook/File | Full Path | Type | Size | Modified | Status |
|---|---|---|---|---|---|
```

**MCP Method:** `obsidian_update_note`
- targetType: "filePath"
- targetIdentifier: "Projects/Mining Results/onenote-inventory.md"
- modificationType: "wholeFile"
- wholeFileMode: "overwrite"
- overwriteIfExists: true

## Success Criteria

10-point checklist:
- All 4 location categories scanned
- File search completed for all file types
- At least 3 different accounts checked
- Size information captured for all files
- Last modified dates documented
- Account associations identified
- Sync status verified
- Markdown table created with >5 rows of data
- Obsidian note created successfully
- Report includes summary paragraph

## Git Status

All work committed and pushed to GitHub:
- Commit 1: aad4dab — Task definition file
- Commit 2: 25f507f — Agent alert message
- Commit 3: ab7eb99 — Coordination registry update
- Remote: origin/main

## Handoff Details

**From:** Claude Code (WSL/Linux environment)  
**To:** Claude Desktop / Overnight Agent (Windows environment)  
**Date:** 2026-02-11 17:30 UTC  
**Status:** Ready for pickup

The Windows agent can now:
1. Pick up task from `tasks/pending/083-windows-onenote-inventory.md`
2. Execute location scans using PowerShell or File Explorer
3. Verify account information in OneNote app settings
4. Generate markdown report with structured table
5. Save to Obsidian vault using MCP tools
6. Move task to `tasks/completed/` when finished

## Why This Approach

Running in Linux/WSL environment, cannot:
- Access Windows paths directly (C:\Users\...\)
- Use Claude Desktop MCP tools
- Execute PowerShell commands on Windows

Instead created complete, self-contained task specification:
- Fully detailed requirements
- Clear success criteria
- Output format documented
- Registered in coordination system
- Agent alert message sent
- Ready for any Windows-based agent to execute

## Duration Estimate

20-30 minutes total:
- PowerShell searches: 5-10 minutes
- Data collection: 5-10 minutes
- Account verification: 3-5 minutes
- Report generation: 3-5 minutes
- Obsidian save: 2-3 minutes

## Next Steps

When Claude Desktop picks up this task:
1. Read: `tasks/pending/083-windows-onenote-inventory.md`
2. Execute: Location scans on Windows machine
3. Gather: All notebook data and account information
4. Generate: Markdown report with structured table
5. Save: To Obsidian vault using MCP tools
6. Complete: Move task to `tasks/completed/`

## Files Created

1. `/home/div/brain/tasks/pending/083-windows-onenote-inventory.md` (113 lines)
2. `/home/div/brain/messages/outbox/MSG-20260211-claude-code-to-desktop-onenote-inventory.md` (41 lines)
3. Updated: `/home/div/brain/context/active-agents.md`

## Status

✅ COMPLETE AND READY FOR EXECUTION

Task is fully defined, scoped, and ready for Windows agent pickup. All supporting files and coordination entries in place.
