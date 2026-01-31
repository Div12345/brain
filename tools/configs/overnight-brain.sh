#!/bin/bash
# overnight-brain.sh
# Brain System Overnight Task Runner for Linux/macOS/WSL
# Alternative to overnight-brain.ps1 for non-Windows systems

set -euo pipefail

# Configuration
BRAIN_PATH="${BRAIN_PATH:-$HOME/brain}"
MAX_RUNTIME_MINUTES="${MAX_RUNTIME_MINUTES:-180}"
DATE_STR=$(date +%Y-%m-%d)
LOG_FILE="$BRAIN_PATH/logs/$DATE_STR-overnight.log"
CONTEXT_PATH="$BRAIN_PATH/context"
PENDING_PATH="$BRAIN_PATH/tasks/pending"
ACTIVE_PATH="$BRAIN_PATH/tasks/active"

# Logging
log() {
    local timestamp=$(date -Iseconds)
    echo "$timestamp | $1" | tee -a "$LOG_FILE"
}

# Ensure directories exist
mkdir -p "$BRAIN_PATH/logs" "$PENDING_PATH" "$ACTIVE_PATH" "$CONTEXT_PATH"

# Start
log "=== Brain Overnight Run Started ==="
START_TIME=$(date +%s)

# Check for pending tasks
PENDING_TASKS=$(find "$PENDING_PATH" -name "*.md" -type f 2>/dev/null | head -1)

if [ -z "$PENDING_TASKS" ]; then
    log "No pending tasks found. Running default overnight prompt."

    PROMPT_FILE="$BRAIN_PATH/agents/overnight.md"
    if [ -f "$PROMPT_FILE" ]; then
        PROMPT=$(cat "$PROMPT_FILE")
    else
        PROMPT="Read CLAUDE.md and context/priorities.md.
Check if any maintenance or analysis tasks would be valuable.
Write a brief status report to logs/.
Commit any changes made."
    fi
else
    TASK_COUNT=$(find "$PENDING_PATH" -name "*.md" -type f | wc -l)
    log "Found $TASK_COUNT pending task(s)"

    # Get first task (sorted by name)
    TASK_FILE=$(find "$PENDING_PATH" -name "*.md" -type f | sort | head -1)
    TASK_NAME=$(basename "$TASK_FILE" .md)
    log "Processing: $TASK_NAME"

    # Move to active
    ACTIVE_FILE="$ACTIVE_PATH/${TASK_NAME}.claude-code.md"
    mv "$TASK_FILE" "$ACTIVE_FILE"
    log "Claimed task: $ACTIVE_FILE"

    PROMPT="Read CLAUDE.md first.
Then execute the task in: $ACTIVE_FILE
When complete, move the file to tasks/completed/ with results appended.
If failed, move to tasks/failed/ with error details.
Commit all changes."
fi

# Update active-agent context
cat > "$CONTEXT_PATH/active-agent.md" << EOF
---
created: $(date -Iseconds)
tags:
  - context
  - coordination
  - status/active
updated: $(date -Iseconds)
---

# Active Agent

| Field | Value |
|-------|-------|
| Agent | claude-code-overnight |
| Since | $(date -Iseconds) |
| Log | logs/$DATE_STR-overnight.log |
| Status | Running |

## Session

Overnight automated run via cron/systemd.
EOF

log "Launching Claude Code..."

# Run Claude Code
# Note: --dangerously-skip-permissions is for unattended runs
# Requires claude CLI to be in PATH
if command -v claude &> /dev/null; then
    claude --dangerously-skip-permissions -p "$PROMPT" 2>&1 | tee -a "$LOG_FILE" || true
else
    log "ERROR: claude command not found in PATH"
    exit 1
fi

log "=== Claude Code Completed ==="

# Clear active-agent
rm -f "$CONTEXT_PATH/active-agent.md" 2>/dev/null || true

# Git commit if changes
cd "$BRAIN_PATH"
git add -A

if ! git diff --cached --quiet; then
    git commit -m "Overnight run: $DATE_STR

Automated overnight agent run.

https://claude.ai/code/session_overnight_$DATE_STR"
    log "Committed changes to git"

    # Optional: push to remote (uncomment if desired)
    # git push origin main
    # log "Pushed to remote"
else
    log "No changes to commit"
fi

# Calculate runtime
END_TIME=$(date +%s)
RUNTIME=$((END_TIME - START_TIME))
RUNTIME_MINUTES=$((RUNTIME / 60))
log "Total runtime: ${RUNTIME_MINUTES} minutes"

exit 0
