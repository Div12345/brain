#!/bin/bash
# Session logging hook for brain orchestration
# Usage: session-log.sh [start|stop|event] [message]

set -euo pipefail

LOG_DIR="${CLAUDE_PROJECT_DIR:-/home/user/brain}/logs"
LOG_FILE="$LOG_DIR/cc-sessions.log"
TIMESTAMP=$(date -Iseconds)

mkdir -p "$LOG_DIR"

EVENT="${1:-event}"
MESSAGE="${2:-}"

case "$EVENT" in
  start)
    echo "" >> "$LOG_FILE"
    echo "## Session $TIMESTAMP" >> "$LOG_FILE"
    echo "- Started" >> "$LOG_FILE"
    ;;
  stop)
    echo "- Ended: $TIMESTAMP" >> "$LOG_FILE"
    ;;
  *)
    if [ -n "$MESSAGE" ]; then
      echo "- [$TIMESTAMP] $MESSAGE" >> "$LOG_FILE"
    fi
    ;;
esac
