#!/bin/bash
# Run a brain task via Gemini CLI instead of CC.
# Usage: ./run-gemini-task.sh <task-file> [model]
# Output logged to logs/gemini/<taskname>-<timestamp>.log

set -euo pipefail

TASK_FILE="$1"
MODEL="${2:-gemini-2.5-pro}"
TASK_NAME=$(basename "$TASK_FILE" .md)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_DIR="$HOME/brain/logs/gemini"
LOG_FILE="$LOG_DIR/${TASK_NAME}-${TIMESTAMP}.log"

mkdir -p "$LOG_DIR"

# Set working directory to brain root so Gemini can access all paths
cd "$HOME/brain"

# Extract task content
TASK_CONTENT=$(cat "$TASK_FILE")

# Build prompt
PROMPT="You are an autonomous coding agent. Execute the following task completely.

WORKING DIRECTORY: $HOME/brain
TASK FILE: $TASK_FILE

--- TASK ---
$TASK_CONTENT
--- END TASK ---

Instructions:
- Read all referenced files before making changes
- Write code directly using your shell tool
- Run tests after writing code
- If Desktop is unavailable on port 9229, write tests that skip gracefully
- Do NOT ask questions, just execute the task fully
- When done, print TASK_COMPLETE or TASK_FAILED with a brief summary"

echo "=== Gemini Task Runner ===" | tee "$LOG_FILE"
echo "Task: $TASK_NAME" | tee -a "$LOG_FILE"
echo "Model: $MODEL" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "Log: $LOG_FILE" | tee -a "$LOG_FILE"
echo "=========================" | tee -a "$LOG_FILE"

# Run Gemini non-interactively
gemini -p "$PROMPT" --yolo --model "$MODEL" --allowed-mcp-server-names claude-desktop 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=$?
echo "" | tee -a "$LOG_FILE"
echo "=========================" | tee -a "$LOG_FILE"
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "Exit code: $EXIT_CODE" | tee -a "$LOG_FILE"

# Move task to completed or failed based on exit
if [ $EXIT_CODE -eq 0 ] && grep -q "TASK_COMPLETE" "$LOG_FILE"; then
    echo "Status: COMPLETED" | tee -a "$LOG_FILE"
    mv "$TASK_FILE" "$HOME/brain/tasks/completed/" 2>/dev/null || true
else
    echo "Status: FAILED" | tee -a "$LOG_FILE"
    mv "$TASK_FILE" "$HOME/brain/tasks/failed/" 2>/dev/null || true
fi
