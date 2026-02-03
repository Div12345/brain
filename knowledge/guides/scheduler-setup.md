# Overnight Scheduler Setup Guide

> Documentation for setting up the Brain overnight task scheduler system.
> This should eventually become a skill at `knowledge/skills/scheduler-setup.md`

## Overview

The system uses Windows Task Scheduler to trigger WSL bash scripts that run Claude Code tasks overnight with automatic retry on rate limits.

```
Windows Task Scheduler
    ↓
overnight-brain.ps1 (PowerShell wrapper)
    ↓
overnight-brain.sh (WSL bash - main logic)
    ↓
ccq run --all (Python task runner)
    ↓
claude CLI (actual execution)
```

## Components

### 1. Core Scripts (in `~/brain/tools/configs/`)

| File | Purpose |
|------|---------|
| `overnight-brain.sh` | Main bash script - checks capacity, runs tasks, handles locks |
| `overnight-brain.ps1` | Windows wrapper - calls bash, schedules retry tasks |
| `nightly-brain.xml` | Task Scheduler XML config for import |

### 2. State Files (in `~/brain/tasks/state/`)

| File | Purpose |
|------|---------|
| `.scheduler-lock` | Prevents duplicate runs |
| `scheduler-state.yaml` | Tracks last run, status, retry info |

### 3. Windows Scheduled Tasks

| Task Name | Schedule | Purpose |
|-----------|----------|---------|
| BrainNightlyRun | Daily 2:00 AM | Main overnight trigger |
| BrainRetryRun | One-time (dynamic) | Auto-scheduled on rate limit |

---

## Setup Steps

### Step 1: Ensure WSL Scripts Are Executable

```bash
chmod +x ~/brain/tools/configs/overnight-brain.sh
```

### Step 2: Test Bash Script Directly

```bash
# From WSL terminal
~/brain/tools/configs/overnight-brain.sh
```

Expected output:
- If rate limited: "Rate limited. Scheduling bounce-back retry."
- If available: "Capacity available. Running ccq..."

### Step 3: Test PowerShell Wrapper

```powershell
# From PowerShell (copies to temp because UNC paths don't work directly)
Copy-Item "\\wsl.localhost\Ubuntu-24.04\home\div\brain\tools\configs\overnight-brain.ps1" "$env:TEMP\overnight-brain.ps1"
& "$env:TEMP\overnight-brain.ps1"
```

### Step 4: Register Windows Scheduled Task

**Option A: Import XML**
```powershell
# Copy XML to temp location
Copy-Item "\\wsl.localhost\Ubuntu-24.04\home\div\brain\tools\configs\nightly-brain.xml" "$env:TEMP\nightly-brain.xml"

# Import task
schtasks /create /tn "BrainNightlyRun" /xml "$env:TEMP\nightly-brain.xml" /f
```

**Option B: Create via command**
```powershell
schtasks /create /tn "BrainNightlyRun" /tr "powershell.exe -ExecutionPolicy Bypass -Command \"Copy-Item '\\wsl.localhost\Ubuntu-24.04\home\div\brain\tools\configs\overnight-brain.ps1' '$env:TEMP\overnight-brain.ps1'; & '$env:TEMP\overnight-brain.ps1'\"" /sc daily /st 02:00 /f
```

**Option C: Use Task Scheduler GUI**
1. Open: `taskschd.msc`
2. Action → Create Task
3. General: Name = "BrainNightlyRun"
4. Triggers: Daily at 2:00 AM
5. Actions: Start program = `powershell.exe`
   Arguments: `-ExecutionPolicy Bypass -File "\\wsl.localhost\Ubuntu-24.04\home\div\brain\tools\configs\overnight-brain.ps1"`
6. Settings: 
   - Allow wake computer
   - Run whether user logged on or not (optional)

### Step 5: Verify Setup

```powershell
# List Brain tasks
Get-ScheduledTask -TaskName "Brain*" | Format-Table TaskName, State

# Check next run times
Get-ScheduledTask -TaskName "Brain*" | ForEach-Object {
    $info = Get-ScheduledTaskInfo $_
    [PSCustomObject]@{
        Name = $_.TaskName
        NextRun = $info.NextRunTime
        LastRun = $info.LastRunTime
    }
}
```

### Step 6: Manual Test Run

```powershell
# Trigger immediately
Start-ScheduledTask -TaskName "BrainNightlyRun"

# Watch logs
Get-Content "\\wsl.localhost\Ubuntu-24.04\home\div\brain\logs\$(Get-Date -Format 'yyyy-MM-dd')-overnight.log" -Wait
```

---

## How Bounce-Back Retry Works

```
┌─────────────────────────────────────────────────────────┐
│ Trigger (nightly or retry)                              │
├─────────────────────────────────────────────────────────┤
│ 1. Check lock file                                      │
│    - If exists & fresh (<3h): exit (prevent dupes)      │
│    - If stale: remove and continue                      │
│                                                         │
│ 2. Create lock file                                     │
│                                                         │
│ 3. Check capacity via ccq/API                           │
│    - Reads ~/.claude/.credentials.json                  │
│    - Calls api.anthropic.com/api/oauth/usage            │
│                                                         │
│ 4. If rate limited (5h >= 100%):                        │
│    - Get reset_time from API response                   │
│    - Update scheduler-state.yaml                        │
│    - PowerShell schedules one-time BrainRetryRun        │
│    - Exit                                               │
│                                                         │
│ 5. If capacity available:                               │
│    - Run: ccq run --all                                 │
│    - Tasks execute via claude CLI                       │
│    - Git commit & push results                          │
│    - Delete BrainRetryRun task if exists                │
│    - Update state to "completed"                        │
│                                                         │
│ 6. Remove lock file (always, via trap)                  │
└─────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Task doesn't run
```powershell
# Check task history
Get-WinEvent -LogName 'Microsoft-Windows-TaskScheduler/Operational' -MaxEvents 20 | 
    Where-Object {$_.Message -like "*Brain*"} | 
    Format-Table TimeCreated, Message -Wrap
```

### WSL not starting
```powershell
# Ensure WSL is running
wsl.exe --status
wsl.exe -l -v
```

### Permission issues
- Task Scheduler may need "Run with highest privileges"
- Or run as your user account with "Run only when user is logged on"

### Check logs
```bash
# From WSL
tail -50 ~/brain/logs/$(date +%Y-%m-%d)-overnight.log

# From PowerShell  
Get-Content "\\wsl.localhost\Ubuntu-24.04\home\div\brain\logs\*-overnight.log" -Tail 50
```

### Check state
```bash
cat ~/brain/tasks/state/scheduler-state.yaml
```

---

## Maintenance Commands

```powershell
# Delete a task
schtasks /delete /tn "BrainRetryRun" /f

# Disable nightly runs
Disable-ScheduledTask -TaskName "BrainNightlyRun"

# Re-enable
Enable-ScheduledTask -TaskName "BrainNightlyRun"

# Change schedule time
$trigger = New-ScheduledTaskTrigger -Daily -At 3:00AM
Set-ScheduledTask -TaskName "BrainNightlyRun" -Trigger $trigger
```

---

## Future: Convert to Skill

This document should become `knowledge/skills/scheduler-setup.md` with:
- [ ] Parameterized paths (not hardcoded to div's home)
- [ ] Auto-detection of WSL distro name
- [ ] Validation steps built into the skill
- [ ] Rollback instructions

Related beads: `brain-pmj` (Task Creator Skill)
