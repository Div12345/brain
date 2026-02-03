# overnight-brain.ps1
# Brain System Overnight Task Runner - WSL Version
# Called by Windows Task Scheduler, executes in WSL

param(
    [int]$MaxRuntimeMinutes = 180
)

$ErrorActionPreference = "Stop"
$startTime = Get-Date
$dateStr = Get-Date -Format "yyyy-MM-dd"
$logFile = "\\wsl.localhost\Ubuntu-24.04\home\div\brain\logs\$dateStr-overnight.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | $Message" | Tee-Object -FilePath $logFile -Append
}

try {
    Write-Log "=== Brain Overnight Run Started (WSL) ==="
    
    # The main script to run in WSL
    $wslScript = @'
#!/bin/bash
source ~/.nvm/nvm.sh 2>/dev/null
cd ~/brain

DATE=$(date +%Y-%m-%d)
LOGFILE="logs/${DATE}-overnight.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') | WSL script started" >> "$LOGFILE"

# Check pending tasks
PENDING=$(ls -1 tasks/pending/*.md 2>/dev/null | grep -v .gitkeep | head -1)

if [ -z "$PENDING" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') | No pending tasks, running default prompt" >> "$LOGFILE"
    PROMPT="Read CLAUDE.md and context/priorities.md. Check for maintenance tasks. Write status to logs/."
else
    TASKNAME=$(basename "$PENDING")
    echo "$(date '+%Y-%m-%d %H:%M:%S') | Processing: $TASKNAME" >> "$LOGFILE"
    
    # Move to active
    mkdir -p tasks/active
    mv "$PENDING" "tasks/active/${TASKNAME%.md}.claude-code.md"
    ACTIVEFILE="tasks/active/${TASKNAME%.md}.claude-code.md"
    
    PROMPT="Read CLAUDE.md first. Then execute the task in: $ACTIVEFILE. When complete, move to tasks/completed/ with results. If failed, move to tasks/failed/ with error. Commit all changes."
fi

# Write active-agent context
cat > context/active-agent.md << EOF
---
agent: claude-code-overnight
started: $(date -Iseconds)
log: logs/${DATE}-overnight.log
---
EOF

echo "$(date '+%Y-%m-%d %H:%M:%S') | Launching Claude Code..." >> "$LOGFILE"

# Run Claude Code
claude --dangerously-skip-permissions -p "$PROMPT" >> "$LOGFILE" 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S') | Claude Code completed" >> "$LOGFILE"

# Clear active-agent
rm -f context/active-agent.md

# Git commit if changes
git add -A
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "Overnight run: $DATE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') | Committed changes" >> "$LOGFILE"
    git push origin main 2>> "$LOGFILE" || echo "Push failed (may need auth)" >> "$LOGFILE"
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') | WSL script completed" >> "$LOGFILE"
'@

    # Write temp script and execute in WSL
    $tempScript = "\\wsl.localhost\Ubuntu-24.04\tmp\overnight-run.sh"
    $wslScript | Set-Content -Path $tempScript -NoNewline
    
    Write-Log "Executing in WSL..."
    
    # Run the script in WSL with proper shell
    $output = wsl.exe bash -c "chmod +x /tmp/overnight-run.sh && /tmp/overnight-run.sh" 2>&1
    $output | Out-File -FilePath $logFile -Append
    
    Write-Log "=== WSL Execution Completed ==="
    
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    Write-Log $_.ScriptStackTrace
    exit 1
} finally {
    $duration = (Get-Date) - $startTime
    Write-Log "Total runtime: $($duration.TotalMinutes.ToString('F1')) minutes"
    
    # Cleanup
    Remove-Item "\\wsl.localhost\Ubuntu-24.04\tmp\overnight-run.sh" -ErrorAction SilentlyContinue
}
