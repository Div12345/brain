# overnight-brain.ps1
# Brain System Overnight Task Runner - WSL Version with Bounce-Back Retry
# Called by Windows Task Scheduler

param(
    [int]$MaxRuntimeMinutes = 180,
    [switch]$IsRetry = $false
)

$ErrorActionPreference = "Stop"
$startTime = Get-Date
$dateStr = Get-Date -Format "yyyy-MM-dd"
$timeStr = Get-Date -Format "HHmm"
$logFile = "\\wsl.localhost\Ubuntu-24.04\home\div\brain\logs\$dateStr-overnight.log"
$lockFile = "\\wsl.localhost\Ubuntu-24.04\home\div\brain\tasks\state\.scheduler-lock"
$stateFile = "\\wsl.localhost\Ubuntu-24.04\home\div\brain\tasks\state\scheduler-state.yaml"
$retryTaskName = "BrainRetryRun"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "$timestamp | $Message"
    Write-Host $line
    $line | Out-File -FilePath $logFile -Append -Encoding utf8
}

function Remove-Lock {
    Remove-Item $lockFile -ErrorAction SilentlyContinue
}

function Schedule-Retry {
    param([datetime]$RetryTime)
    
    # Remove existing retry task if any
    & "$env:SystemRoot\System32\schtasks.exe" /delete /tn $retryTaskName /f 2>$null
    
    $retryTimeStr = $RetryTime.ToString("HH:mm")
    $retryDateStr = $RetryTime.ToString("MM/dd/yyyy")
    $scriptPath = "\\wsl.localhost\Ubuntu-24.04\home\div\brain\tools\configs\overnight-brain.ps1"
    
    # Schedule one-time retry
    & "$env:SystemRoot\System32\schtasks.exe" /create /tn $retryTaskName /tr "powershell.exe -ExecutionPolicy Bypass -File `"$scriptPath`" -IsRetry" /sc once /st $retryTimeStr /sd $retryDateStr /f
    
    Write-Log "Scheduled retry at $retryTimeStr on $retryDateStr"
}

function Update-State {
    param(
        [string]$Status,
        [string]$RetryAt = "",
        [string]$LastTask = "",
        [string]$Error = ""
    )
    
    $stateDir = Split-Path $stateFile -Parent
    if (!(Test-Path $stateDir)) {
        New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
    }
    
    $state = @"
# Scheduler State - Auto-generated
last_run: $(Get-Date -Format "o")
status: $Status
is_retry: $IsRetry
retry_at: $RetryAt
last_task: $LastTask
error: $Error
"@
    $state | Set-Content $stateFile -Encoding utf8
}

try {
    Write-Log "=== Brain Overnight Run Started $(if ($IsRetry) {'(RETRY)'} else {'(SCHEDULED)'}) ==="
    
    # 1. Check lock - prevent duplicate runs
    if (Test-Path $lockFile) {
        $lockAge = (Get-Date) - (Get-Item $lockFile).LastWriteTime
        if ($lockAge.TotalMinutes -lt 180) {
            Write-Log "Lock file exists (age: $($lockAge.TotalMinutes.ToString('F0'))m). Another instance running. Exiting."
            Update-State -Status "skipped_locked"
            exit 0
        } else {
            Write-Log "Stale lock file detected. Removing."
            Remove-Lock
        }
    }
    
    # 2. Create lock
    New-Item -ItemType File -Path $lockFile -Force | Out-Null
    Write-Log "Lock acquired"
    
    # 3. Check capacity via ccq
    Write-Log "Checking capacity..."
    
    $capacityScript = @'
source ~/.nvm/nvm.sh 2>/dev/null
cd ~/brain/tools/cc-scheduler
python3 -c "
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
"
'@
    
    $capacityJson = wsl.exe bash -c $capacityScript 2>$null | Select-Object -Last 1
    
    if ([string]::IsNullOrWhiteSpace($capacityJson)) {
        Write-Log "Failed to check capacity. Proceeding anyway..."
        $capacity = @{ limited = $false }
    } else {
        try {
            $capacity = $capacityJson | ConvertFrom-Json
        } catch {
            Write-Log "Failed to parse capacity: $capacityJson"
            $capacity = @{ limited = $false }
        }
    }
    
    Write-Log "Capacity: 5h=$($capacity.five_hour)% 7d=$($capacity.weekly)% limited=$($capacity.limited)"
    
    # 4. If limited, schedule retry and exit
    if ($capacity.limited -eq $true) {
        Write-Log "Rate limited. Scheduling bounce-back retry."
        
        if ($capacity.resets_at) {
            $resetTime = [datetime]::Parse($capacity.resets_at).ToLocalTime().AddMinutes(2)
        } else {
            # Default: retry in 1 hour
            $resetTime = (Get-Date).AddHours(1)
        }
        
        # Don't retry past 8am (user's active hours)
        $morningCutoff = (Get-Date).Date.AddHours(8)
        if ($resetTime -gt $morningCutoff -and (Get-Date) -lt $morningCutoff) {
            Write-Log "Reset time ($resetTime) is past morning cutoff. Not scheduling retry."
            Update-State -Status "rate_limited_no_retry" -RetryAt $resetTime.ToString("o")
        } else {
            Schedule-Retry -RetryTime $resetTime
            Update-State -Status "rate_limited_retry_scheduled" -RetryAt $resetTime.ToString("o")
        }
        
        Remove-Lock
        exit 0
    }
    
    # 5. Run ccq
    Write-Log "Capacity available. Running ccq..."
    
    $runScript = @'
source ~/.nvm/nvm.sh 2>/dev/null
cd ~/brain
python3 tools/cc-scheduler/ccq run --all 2>&1
'@
    
    $output = wsl.exe bash -c $runScript 2>&1
    $output | Out-File -FilePath $logFile -Append -Encoding utf8
    
    Write-Log "ccq run completed"
    
    # 6. Check if we got rate limited mid-run (parse output)
    if ($output -match "Rate limited|is_limited") {
        Write-Log "Hit rate limit during run. Checking for retry..."
        
        # Re-check capacity for new reset time
        $capacityJson = wsl.exe bash -c $capacityScript 2>$null | Select-Object -Last 1
        if ($capacityJson) {
            $capacity = $capacityJson | ConvertFrom-Json
            if ($capacity.resets_at) {
                $resetTime = [datetime]::Parse($capacity.resets_at).ToLocalTime().AddMinutes(2)
                $morningCutoff = (Get-Date).Date.AddHours(8)
                if ($resetTime -lt $morningCutoff -or (Get-Date) -gt $morningCutoff) {
                    Schedule-Retry -RetryTime $resetTime
                    Update-State -Status "mid_run_limited_retry_scheduled" -RetryAt $resetTime.ToString("o")
                }
            }
        }
    } else {
        Update-State -Status "completed"
        
        # Clean up retry task if exists
        & "$env:SystemRoot\System32\schtasks.exe" /delete /tn $retryTaskName /f 2>$null
    }
    
    # 7. Git commit and push
    Write-Log "Committing changes..."
    
    $gitScript = @'
source ~/.nvm/nvm.sh 2>/dev/null
cd ~/brain
git add -A
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "Overnight run: $(date +%Y-%m-%d)"
    git push origin main 2>&1 || echo "Push failed"
fi
'@
    
    wsl.exe bash -c $gitScript 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
    
    Write-Log "=== Run Completed ==="
    
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    Update-State -Status "error" -Error $_.Exception.Message
} finally {
    Remove-Lock
    $duration = (Get-Date) - $startTime
    Write-Log "Total runtime: $($duration.TotalMinutes.ToString('F1')) minutes"
}
