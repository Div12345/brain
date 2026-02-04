# Skill: Overnight Scheduler Setup

> Parameterized skill for setting up the Brain overnight task scheduler.
> Converts the guide at `knowledge/guides/scheduler-setup.md` into executable steps.

## Parameters

```yaml
# Configure these for your environment
USER_HOME: /home/div           # WSL home directory
BRAIN_REPO: ~/brain            # Brain repo location  
WSL_DISTRO: Ubuntu-24.04       # WSL distribution name (wsl -l -v)
SCHEDULE_TIME: "02:00"         # Daily trigger time (24h format)
MORNING_CUTOFF: "08:00"        # Don't retry past this time
```

**Auto-detect WSL distro (optional):**
```bash
# Run in PowerShell to get your default WSL distro name
wsl.exe -l -v | Select-String '\*' | ForEach-Object { ($_ -split '\s+')[2] }
```

## Prerequisites

- [ ] Windows 10/11 with WSL2
- [ ] Claude CLI installed in WSL (`claude --version`)
- [ ] Python 3.x with required packages
- [ ] Git configured for push access

**Verify:**
```bash
wsl.exe bash -c "claude --version && python3 --version && git remote -v"
```

---

## Step 1: Create Directory Structure

```bash
# In WSL
mkdir -p ${BRAIN_REPO}/tools/configs
mkdir -p ${BRAIN_REPO}/tasks/{pending,staged,completed,state}
mkdir -p ${BRAIN_REPO}/logs
```

**Validate:**
```bash
ls -la ${BRAIN_REPO}/tools/configs ${BRAIN_REPO}/tasks ${BRAIN_REPO}/logs
```

---

## Step 2: Create Bash Script

Create `${BRAIN_REPO}/tools/configs/overnight-brain.sh`:

```bash
#!/bin/bash
# overnight-brain.sh - Brain System Overnight Task Runner

set -e

# === PARAMETERS (edit these) ===
BRAIN_DIR="${USER_HOME}/brain"  # Parameterized
# ===============================

LOG_DIR="$BRAIN_DIR/logs"
STATE_DIR="$BRAIN_DIR/tasks/state"
LOCK_FILE="$STATE_DIR/.scheduler-lock"
STATE_FILE="$STATE_DIR/scheduler-state.yaml"
DATE_STR=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/$DATE_STR-overnight.log"

source ~/.nvm/nvm.sh 2>/dev/null || true
mkdir -p "$LOG_DIR" "$STATE_DIR"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" | tee -a "$LOG_FILE"; }
remove_lock() { rm -f "$LOCK_FILE"; }
trap remove_lock EXIT

log "=== Brain Overnight Run Started ==="

# Lock check
if [ -f "$LOCK_FILE" ]; then
    lock_age=$(( ($(date +%s) - $(stat -c %Y "$LOCK_FILE")) / 60 ))
    [ "$lock_age" -lt 180 ] && log "Locked. Exiting." && exit 0
    rm -f "$LOCK_FILE"
fi
touch "$LOCK_FILE"
log "Lock acquired"

# Capacity check
log "Checking capacity..."
cd "$BRAIN_DIR/tools/cc-scheduler"
capacity_json=$(python3 -c "
import json
from lib.capacity import check_capacity
cap = check_capacity()
if cap:
    print(json.dumps({
        'limited': cap.is_limited,
        'five_hour': cap.five_hour_percent,
        'weekly': cap.weekly_percent,
        'resets_at': cap.five_hour_resets_at.isoformat() if cap.five_hour_resets_at else None
    }))
else:
    print(json.dumps({'error': 'no_credentials'}))
" 2>/dev/null) || capacity_json='{"error": "python_failed"}'

log "Capacity: $capacity_json"
limited=$(echo "$capacity_json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('limited', False))")

if [ "$limited" = "True" ]; then
    log "Rate limited. Exiting for retry."
    resets_at=$(echo "$capacity_json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('resets_at', ''))")
    echo "status: rate_limited_retry_scheduled" > "$STATE_FILE"
    echo "retry_at: $resets_at" >> "$STATE_FILE"
    exit 0
fi

# Run tasks
log "Running ccq..."
cd "$BRAIN_DIR"
python3 tools/cc-scheduler/ccq run --all 2>&1 | tee -a "$LOG_FILE" || true
log "ccq completed"

# Git commit
git add -A
[ -n "$(git status --porcelain)" ] && git commit -m "Overnight: $DATE_STR" && git push origin main || true

echo "status: completed" > "$STATE_FILE"
log "=== Run Completed ==="
```

**Validate:**
```bash
chmod +x ${BRAIN_REPO}/tools/configs/overnight-brain.sh
${BRAIN_REPO}/tools/configs/overnight-brain.sh  # Test run
cat ${BRAIN_REPO}/tasks/state/scheduler-state.yaml
```

---

## Step 3: Create PowerShell Wrapper

Create `${BRAIN_REPO}/tools/configs/overnight-brain.ps1`:

```powershell
# overnight-brain.ps1 - Windows wrapper with retry scheduling

param([switch]$IsRetry = $false)

# === PARAMETERS ===
$wslDistro = "${WSL_DISTRO}"
$brainPath = "${BRAIN_REPO}"
$morningCutoff = ${MORNING_CUTOFF}
# ==================

$userHome = "${USER_HOME}" -replace '/', '\'  # Convert to Windows path format
$stateFile = "\\wsl.localhost\$wslDistro$($brainPath -replace '~',$userHome)\tasks\state\scheduler-state.yaml"
$retryTaskName = "BrainRetryRun"

function Schedule-Retry($ResetTimeISO) {
    $resetTime = [datetime]::Parse($ResetTimeISO).ToLocalTime().AddMinutes(2)
    $cutoff = (Get-Date).Date.AddHours([int]$morningCutoff.Split(':')[0])
    if ($resetTime -gt $cutoff) { return }
    
    & schtasks /delete /tn $retryTaskName /f 2>$null
    & schtasks /create /tn $retryTaskName /tr "wsl.exe bash -c '$brainPath/tools/configs/overnight-brain.sh'" /sc once /st $resetTime.ToString("HH:mm") /sd $resetTime.ToString("MM/dd/yyyy") /f
}

wsl.exe bash -c "$brainPath/tools/configs/overnight-brain.sh"

if (Test-Path $stateFile) {
    $state = Get-Content $stateFile -Raw
    if ($state -match "retry_at:\s*(\S+)") { Schedule-Retry $Matches[1] }
    elseif ($state -match "status:\s*completed") {
        & schtasks /delete /tn $retryTaskName /f 2>$null
    }
}
```

**Validate:**
```powershell
Copy-Item "\\wsl.localhost\${WSL_DISTRO}\${BRAIN_REPO}\tools\configs\overnight-brain.ps1" "$env:TEMP\overnight-brain.ps1"
& "$env:TEMP\overnight-brain.ps1"
```

---

## Step 4: Register Windows Task

```powershell
# Variables
$wslDistro = "${WSL_DISTRO}"
$brainPath = "${BRAIN_REPO}" -replace '~', '/home/div'
$scheduleTime = "${SCHEDULE_TIME}"

# Create task
schtasks /create /tn "BrainNightlyRun" `
    /tr "powershell.exe -ExecutionPolicy Bypass -Command `"Copy-Item '\\wsl.localhost\$wslDistro$brainPath\tools\configs\overnight-brain.ps1' '$env:TEMP\overnight-brain.ps1'; & '$env:TEMP\overnight-brain.ps1'`"" `
    /sc daily /st $scheduleTime /f
```

**Validate:**
```powershell
Get-ScheduledTask -TaskName "Brain*" | Format-Table TaskName, State
Get-ScheduledTaskInfo -TaskName "BrainNightlyRun" | Select-Object NextRunTime
```

---

## Step 5: Test Full Flow

```powershell
# Trigger manually
Start-ScheduledTask -TaskName "BrainNightlyRun"

# Watch logs (PowerShell)
Get-Content "\\wsl.localhost\${WSL_DISTRO}\${BRAIN_REPO}\logs\$(Get-Date -Format 'yyyy-MM-dd')-overnight.log" -Wait
```

```bash
# Check results (WSL)
cat ${BRAIN_REPO}/tasks/state/scheduler-state.yaml
ls ${BRAIN_REPO}/tasks/completed/
git log --oneline -3
```

---

## Rollback

```powershell
# Remove scheduled tasks
schtasks /delete /tn "BrainNightlyRun" /f
schtasks /delete /tn "BrainRetryRun" /f

# Verify removed
Get-ScheduledTask -TaskName "Brain*"
```

```bash
# Clean state files (WSL)
rm -f ${BRAIN_REPO}/tasks/state/.scheduler-lock
rm -f ${BRAIN_REPO}/tasks/state/scheduler-state.yaml
```

---

## Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| Task doesn't run | `Get-ScheduledTaskInfo` | Check trigger time, user permissions |
| WSL errors | `wsl --status` | Restart WSL: `wsl --shutdown` |
| Lock stuck | `stat` lock file | Delete if >3h old |
| Capacity check fails | `cat ~/.claude/.credentials.json` | Re-auth Claude |

**Logs:**
```bash
tail -50 ${BRAIN_REPO}/logs/$(date +%Y-%m-%d)-overnight.log
```

---

## Success Criteria

- [ ] `overnight-brain.sh` exists and is executable
- [ ] `overnight-brain.ps1` exists
- [ ] `BrainNightlyRun` task registered
- [ ] Manual trigger completes without error
- [ ] State file shows `status: completed`
