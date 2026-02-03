# CC Scheduler - Windows Task Scheduler Trigger
#
# This script triggers the autonomous scheduler run from Windows.
# Schedule this to run at 8 AM daily via Windows Task Scheduler.
#
# Setup:
#   1. Open Task Scheduler (taskschd.msc)
#   2. Create Basic Task > Name: "CC Scheduler Daily"
#   3. Trigger: Daily at 8:00 AM
#   4. Action: Start a program
#      - Program: powershell.exe
#      - Arguments: -ExecutionPolicy Bypass -File "C:\path\to\this\script.ps1"
#   5. Conditions: Start only if AC power (optional)
#
# Or run from PowerShell:
#   .\windows-task.ps1

param(
    [switch]$DryRun,
    [switch]$Force,
    [string]$Phase = "autonomous"
)

$ErrorActionPreference = "Stop"

# Configuration
$WSL_DISTRO = "Ubuntu-24.04"
$BRAIN_PATH = "~/brain"
$CCQ_PATH = "~/brain/tools/cc-scheduler/ccq"

# Build the command
$flags = @()
if ($DryRun) { $flags += "--dry" }
if ($Force) { $flags += "--force" }
$flags += "--phase"
$flags += $Phase

$flagStr = $flags -join " "

# Log file (Windows side)
$logDir = "$env:USERPROFILE\.cc-scheduler\logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$logFile = "$logDir\$(Get-Date -Format 'yyyy-MM-dd-HHmm').log"

Write-Host "CC Scheduler Trigger"
Write-Host "===================="
Write-Host "Time: $(Get-Date)"
Write-Host "Phase: $Phase"
Write-Host "Dry Run: $DryRun"
Write-Host "Log: $logFile"
Write-Host ""

# Check if WSL is available
try {
    $wslCheck = wsl -l -q 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "WSL not available"
    }
} catch {
    Write-Error "WSL is not available or not running"
    exit 1
}

# Run the scheduler
Write-Host "Starting ccq run..."
$startTime = Get-Date

$wslCommand = @"
cd $BRAIN_PATH && python3 $CCQ_PATH run --all $flagStr 2>&1
"@

# Execute and capture output
$output = wsl -d $WSL_DISTRO -e bash -c $wslCommand

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

# Log results
$logContent = @"
CC Scheduler Run
================
Start: $startTime
End: $endTime
Duration: $duration seconds
Phase: $Phase
Dry Run: $DryRun

Output:
-------
$output
"@

$logContent | Out-File -FilePath $logFile -Encoding utf8

# Display output
Write-Host ""
Write-Host "Output:"
Write-Host "-------"
Write-Host $output
Write-Host ""
Write-Host "Completed in $([math]::Round($duration, 1)) seconds"
Write-Host "Log saved to: $logFile"

# Return exit code based on output
if ($output -match "✗ Failed" -or $output -match "Error:") {
    exit 1
}
exit 0
