#!/bin/bash
# CC Scheduler - Autonomous Run Trigger
#
# Usage:
#   ./run.sh              # Normal run
#   ./run.sh --dry        # Dry run
#   ./run.sh --force      # Force run (ignore schedule)
#
# For cron (8 AM daily):
#   0 8 * * * /home/div/brain/tools/cc-scheduler/trigger/run.sh >> ~/.cc-scheduler/cron.log 2>&1

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CCQ="$SCRIPT_DIR/../ccq"
LOG_DIR="$HOME/.cc-scheduler/logs"
BRAIN_DIR="$HOME/brain"

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d-%H%M)
LOG_FILE="$LOG_DIR/$TIMESTAMP.log"

echo "CC Scheduler Run - $TIMESTAMP" | tee "$LOG_FILE"
echo "==============================" | tee -a "$LOG_FILE"

cd "$BRAIN_DIR"

# Pass all arguments to ccq
python3 "$CCQ" run --all "$@" 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

echo "" | tee -a "$LOG_FILE"
echo "Exit code: $EXIT_CODE" | tee -a "$LOG_FILE"
echo "Log: $LOG_FILE"

exit $EXIT_CODE
