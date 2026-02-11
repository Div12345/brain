# Task 083: Comprehensive Windows OneNote Inventory

**Status:** Pending  
**Created:** 2026-02-11  
**Priority:** High  
**Assigned To:** Claude Desktop / Windows Agent  
**Target:** Windows Machine (C:\Users\din18\)

## Objective
Perform comprehensive OneNote inventory scan across all locations on Windows machine. Find ALL notebooks, backups, and related files. Create structured markdown report in Obsidian vault.

## Scope: Locations to Scan

### 1. Known Backup Location (Pitt University)
```
C:\Users\din18\OneDrive - University of Pittsburgh\Onenote
```
- Status: Known backup from Sept 2023 (onepkg format)
- Priority: HIGH (verify if accessible)

### 2. OneDrive Locations
```
C:\Users\din18\OneDrive\
C:\Users\din18\OneDrive*\  (search for all OneDrive* directories)
```

### 3. Local Storage
```
C:\Users\din18\Documents\OneNote Notebooks\
C:\Users\din18\AppData\Local\Microsoft\OneNote\
```

### 4. System-Wide File Search
Search entire `C:\Users\din18\` for:
- `*.onepkg` (OneNote backup packages)
- `*.one` (OneNote files)
- `*.onetoc2` (OneNote table of contents)

## Data to Capture Per Notebook

For each file/notebook found, report:

| Field | Description |
|-------|-------------|
| **Full Path** | Complete Windows path |
| **File Name** | Just the filename |
| **File Type** | onepkg backup / live notebook / .one file / cache / other |
| **Size** | In MB or GB |
| **Last Modified** | Date and time |
| **Account** | Pitt edu / personal / BITS / unknown / other |
| **Status** | Active / Backup / Orphaned / Sync active / Sync paused |

## Account Information to Verify

- [ ] Which Microsoft accounts are signed in to OneNote app?
- [ ] Which OneDrive accounts are configured?
- [ ] Sync status: Active / Paused / Disconnected for each
- [ ] Account email addresses
- [ ] Tenant info (Pitt org, personal Microsoft, BITS)

## Output Requirements

### Format
Create structured markdown with sections per account:

```markdown
## Account: [Account Email/Name]
### Status: [Active/Backup/Unknown]
### Location: [General Location]

| Notebook/File | Full Path | Type | Size | Modified | Status |
|---|---|---|---|---|---|
```

### Destination
Save to Obsidian vault:
- **Path:** `Projects/Mining Results/onenote-inventory.md`
- **Method:** Obsidian MCP `obsidian_update_note`
  - targetType: "filePath"
  - targetIdentifier: "Projects/Mining Results/onenote-inventory.md"
  - modificationType: "wholeFile"
  - wholeFileMode: "overwrite"
  - overwriteIfExists: true

## Success Criteria

- [ ] All 4 location categories scanned
- [ ] File search completed for all file types
- [ ] At least 3 different accounts checked
- [ ] Size information captured for all files
- [ ] Last modified dates documented
- [ ] Account associations identified
- [ ] Sync status verified
- [ ] Markdown table created with >5 rows of data
- [ ] Obsidian note created successfully
- [ ] Report includes summary paragraph explaining what was found

## Notes

- **Pitt Backup Expectation:** Sept 2023 backup likely in onepkg format at known location
- **Account Diversity:** User likely has Pitt edu + personal Microsoft account
- **Old BITS Reference:** May find historical notebooks from BITS university period
- **AppData Cache:** May contain sync metadata, include if relevant

## Completion Checklist

- [ ] Task started in Claude Desktop
- [ ] All locations scanned
- [ ] Account info verified
- [ ] Obsidian note created
- [ ] Report reviewed for completeness
- [ ] Task moved to completed/

