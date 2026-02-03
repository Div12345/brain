# overnight-brain.ps1
# Brain System Overnight Task Runner - Windows Wrapper
# Calls bash script in WSL and handles Windows Task Scheduler retry

param(
    [switch]$IsRetry = $false
)

$ErrorActionPreference = "Stop"
$stateFile = "\\wsl.localhost\Ubuntu-24.04\home\div\brain\tasks\state\scheduler-state.yaml"
$retryTaskName = "BrainRetryRun"

function Schedule-Retry {
    param([string]$ResetTimeISO)
    
    try {
        # Parse ISO time and convert to local
        $resetTime = [datetime]::Parse($ResetTimeISO).ToLocalTime().AddMinutes(2)
        
        # Don't schedule past 8am
        $morningCutoff = (Get-Date).Date.AddHours(8)
        if ($resetTime -gt $morningCutoff -and (Get-Date) -lt $morningCutoff) {
            Write-Host "Reset time past morning cutoff. Skipping retry."
            return
        }
        
        # Remove existing retry task
        & "$env:SystemRoot\System32\schtasks.exe" /delete /tn $retryTaskName /f 2>$null
        
        $retryTimeStr = $resetTime.ToString("HH:mm")
        $retryDateStr = $resetTime.ToString("MM/dd/yyyy")
        
        # Schedule one-time retry using wsl bash
        & "$env:SystemRoot\System32\schtasks.exe" /create /tn $retryTaskName /tr "wsl.exe bash -c '~/brain/tools/configs/overnight-brain.sh'" /sc once /st $retryTimeStr /sd $retryDateStr /f
        
        Write-Host "Scheduled retry: $retryTaskName at $retryTimeStr on $retryDateStr"
    } catch {
        Write-Host "Failed to schedule retry: $_"
    }
}

# Run the bash script
Write-Host "Running overnight-brain.sh in WSL..."
wsl.exe bash -c "~/brain/tools/configs/overnight-brain.sh"

# Check state file for retry needed
if (Test-Path $stateFile) {
    $state = Get-Content $stateFile -Raw
    
    if ($state -match "status:\s*rate_limited") {
        if ($state -match "retry_at:\s*(\S+)") {
            $retryTime = $Matches[1]
            Write-Host "Rate limited. Scheduling Windows retry..."
            Schedule-Retry -ResetTimeISO $retryTime
        }
    } elseif ($state -match "status:\s*completed") {
        # Clean up retry task if exists
        & "$env:SystemRoot\System32\schtasks.exe" /delete /tn $retryTaskName /f 2>$null
        Write-Host "Completed successfully."
    }
}
