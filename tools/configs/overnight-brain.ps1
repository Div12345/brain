# overnight-brain.ps1
# Brain System Overnight Task Runner
# Called by Windows Task Scheduler

param(
    [string]$BrainPath = "C:\brain",
    [int]$MaxRuntimeMinutes = 180
)

# Setup
$ErrorActionPreference = "Stop"
$startTime = Get-Date
$dateStr = Get-Date -Format "yyyy-MM-dd"
$logFile = Join-Path $BrainPath "logs\$dateStr-overnight.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | $Message" | Tee-Object -FilePath $logFile -Append
}

try {
    Set-Location $BrainPath
    Write-Log "=== Brain Overnight Run Started ==="
    
    # Check for pending tasks
    $pendingPath = Join-Path $BrainPath "tasks\pending"
    if (!(Test-Path $pendingPath)) {
        New-Item -ItemType Directory -Path $pendingPath -Force | Out-Null
        Write-Log "Created tasks/pending directory"
    }
    
    $pendingTasks = Get-ChildItem -Path "$pendingPath\*.md" -ErrorAction SilentlyContinue
    
    if ($pendingTasks.Count -eq 0) {
        Write-Log "No pending tasks found. Running default overnight prompt."
        $promptFile = Join-Path $BrainPath "agents\overnight.md"
        
        if (Test-Path $promptFile) {
            $prompt = Get-Content $promptFile -Raw
        } else {
            $prompt = @"
Read CLAUDE.md and context/priorities.md.
Check if any maintenance or analysis tasks would be valuable.
Write a brief status report to logs/.
Commit any changes made.
"@
        }
    } else {
        Write-Log "Found $($pendingTasks.Count) pending task(s)"
        
        # Sort by priority (if in frontmatter) or by date
        $taskFile = $pendingTasks | Sort-Object LastWriteTime | Select-Object -First 1
        Write-Log "Processing: $($taskFile.Name)"
        
        # Move to active
        $activePath = Join-Path $BrainPath "tasks\active"
        if (!(Test-Path $activePath)) {
            New-Item -ItemType Directory -Path $activePath -Force | Out-Null
        }
        
        $activeFile = Join-Path $activePath "$($taskFile.BaseName).claude-code.md"
        Move-Item -Path $taskFile.FullName -Destination $activeFile
        Write-Log "Claimed task: $activeFile"
        
        $prompt = @"
Read CLAUDE.md first.
Then execute the task in: $activeFile
When complete, move the file to tasks/completed/ with results appended.
If failed, move to tasks/failed/ with error details.
Commit all changes.
"@
    }
    
    # Update active-agent context
    $contextPath = Join-Path $BrainPath "context"
    if (!(Test-Path $contextPath)) {
        New-Item -ItemType Directory -Path $contextPath -Force | Out-Null
    }
    
    @"
---
agent: claude-code-overnight
started: $(Get-Date -Format "o")
log: logs/$dateStr-overnight.log
---
"@ | Set-Content (Join-Path $contextPath "active-agent.md")
    
    Write-Log "Launching Claude Code..."
    
    # Run Claude Code
    # Note: --dangerously-skip-permissions is for unattended runs
    # Remove if you want confirmation prompts
    $claudeOutput = claude --dangerously-skip-permissions -p $prompt 2>&1
    
    $claudeOutput | Out-File -FilePath $logFile -Append
    
    Write-Log "=== Claude Code Completed ==="
    
    # Clear active-agent
    Remove-Item (Join-Path $contextPath "active-agent.md") -ErrorAction SilentlyContinue
    
    # Git commit if changes
    git add -A
    $status = git status --porcelain
    if ($status) {
        git commit -m "Overnight run: $dateStr"
        Write-Log "Committed changes to git"
        
        # Optional: push to remote
        # git push origin main
    }
    
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    Write-Log $_.ScriptStackTrace
    exit 1
} finally {
    $duration = (Get-Date) - $startTime
    Write-Log "Total runtime: $($duration.TotalMinutes.ToString('F1')) minutes"
}
