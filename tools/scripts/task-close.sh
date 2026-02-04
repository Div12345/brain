#!/bin/bash
# task-close.sh - Close a task (update bead + move task file)
# Usage: task-close.sh <bead_id> "Close reason"
#
# Example:
#   task-close.sh brain-xyz "Completed - see output in knowledge/results.md"

set -e

BRAIN_ROOT="${BRAIN_ROOT:-$HOME/brain}"
BEADS_FILE="$BRAIN_ROOT/.beads/issues.jsonl"
PENDING_DIR="$BRAIN_ROOT/tasks/pending"
ACTIVE_DIR="$BRAIN_ROOT/tasks/active"
COMPLETED_DIR="$BRAIN_ROOT/tasks/completed"

if [[ $# -lt 2 ]]; then
    echo "Usage: task-close.sh <bead_id> \"Close reason\""
    exit 1
fi

BEAD_ID="$1"
CLOSE_REASON="$2"
TIMESTAMP=$(date -Iseconds)

# Find task file with this bead_id
TASK_FILE=$(grep -l "bead_id: $BEAD_ID" "$PENDING_DIR"/*.md "$ACTIVE_DIR"/*.md 2>/dev/null | head -1 || true)

if [[ -z "$TASK_FILE" ]]; then
    echo "Warning: No task file found with bead_id: $BEAD_ID"
else
    FILENAME=$(basename "$TASK_FILE")
    mv "$TASK_FILE" "$COMPLETED_DIR/$FILENAME"
    echo "Moved: $TASK_FILE -> $COMPLETED_DIR/$FILENAME"
fi

# Add close entry to beads
CLOSE_JSON=$(cat <<EOF
{"id":"$BEAD_ID","status":"closed","closed_at":"$TIMESTAMP","close_reason":"$CLOSE_REASON","updated_at":"$TIMESTAMP"}
EOF
)

echo "$CLOSE_JSON" >> "$BEADS_FILE"
echo "Closed bead: $BEAD_ID"
echo "Reason: $CLOSE_REASON"
