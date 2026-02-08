# Setup Windows Task Scheduler for overnight Gemini→Desktop runs
# Run this script in PowerShell as Administrator
#
# Usage: powershell -ExecutionPolicy Bypass -File setup-win-scheduler.ps1

$TaskName = "BrainOvernightGemini"
$Description = "Run brain tasks via Gemini→Claude Desktop pipeline while sleeping"

# Schedule: 3:30 AM daily (user sleeps ~3AM-11AM)
$TriggerTime = "03:30"

# WSL command to run
# trigger-overnight.sh handles its own PATH setup (nvm/node/gemini)
$WslCommand = "wsl -d Ubuntu -- /home/div/brain/tools/cc-scheduler/trigger-overnight.sh --backend desktop"

# Remove existing task if present
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Removing existing task: $TaskName"
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create trigger
$trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime

# Create action
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c $WslCommand"

# Settings: run whether user is logged on or not, wake to run
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -WakeToRun `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 6) `
    -RestartCount 1 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# Register
Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $Description `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -RunLevel Highest

Write-Host ""
Write-Host "Task '$TaskName' created successfully!"
Write-Host "  Schedule: Daily at $TriggerTime"
Write-Host "  Backend: Gemini -> Claude Desktop"
Write-Host ""
Write-Host "To test: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "To check: Get-ScheduledTask -TaskName '$TaskName' | Select-Object State"
Write-Host "To disable: Disable-ScheduledTask -TaskName '$TaskName'"
Write-Host "To remove: Unregister-ScheduledTask -TaskName '$TaskName'"
