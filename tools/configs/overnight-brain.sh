#!/bin/bash
# overnight-brain.sh
# Brain System Overnight Task Runner - Pure Bash Version with Bounce-Back Retry

set -e

# Config
BRAIN_DIR="$HOME/brain"
LOG_DIR="$BRAIN_DIR/logs"
STATE_DIR="$BRAIN_DIR/tasks/state"
LOCK_FILE="$STATE_DIR/.scheduler-lock"
STATE_FILE="$STATE_DIR/scheduler-state.yaml"
DATE_STR=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/$DATE_STR-overnight.log"

# Source nvm for node/npm access
source ~/.nvm/nvm.sh 2>/dev/null || true

mkdir -p "$LOG_DIR" "$STATE_DIR"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" | tee -a "$LOG_FILE"
}

remove_lock() {
    rm -f "$LOCK_FILE"
}

update_state() {
    local status="$1"
    local retry_at="${2:-}"
    local last_task="${3:-}"
    local error="${4:-}"
    
    cat > "$STATE_FILE" << EOF
# Scheduler State - Auto-generated
last_run: $(date -Iseconds)
status: $status
retry_at: $retry_at
last_task: $last_task
error: $error
EOF
}

schedule_retry() {
    local retry_time="$1"
    log "Would schedule retry at $retry_time (manual trigger needed on Windows)"
    # For Windows Task Scheduler, we'd need PowerShell
    # For now, just log it
}

cleanup() {
    remove_lock
    log "Lock released"
}
trap cleanup EXIT

# Main
log "=== Brain Overnight Run Started ==="

# 1. Check lock
if [ -f "$LOCK_FILE" ]; then
    lock_age=$(( ($(date +%s) - $(stat -c %Y "$LOCK_FILE")) / 60 ))
    if [ "$lock_age" -lt 180 ]; then
        log "Lock file exists (age: ${lock_age}m). Another instance running. Exiting."
        update_state "skipped_locked"
        exit 0
    else
        log "Stale lock file detected. Removing."
        rm -f "$LOCK_FILE"
    fi
fi

# 2. Create lock
touch "$LOCK_FILE"
log "Lock acquired"

# 3. Check capacity
log "Checking capacity..."
cd "$BRAIN_DIR/tools/cc-scheduler"

capacity_json=$(python3 -c "
import json
from lib.capacity import check_capacity
cap = check_capacity()
if cap:
    print(json.dumps({
        'limited': cap.is_limited,
        'five_hour': cap.five_hour_percent,
        'weekly': cap.weekly_percent,
        'resets_at': cap.five_hour_resets_at.isoformat() if cap.five_hour_resets_at else None
    }))
else:
    print(json.dumps({'error': 'no_credentials'}))
" 2>/dev/null) || capacity_json='{"error": "python_failed"}'

log "Capacity response: $capacity_json"

limited=$(echo "$capacity_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('limited', False))" 2>/dev/null || echo "False")
five_hour=$(echo "$capacity_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('five_hour', 0))" 2>/dev/null || echo "0")
weekly=$(echo "$capacity_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('weekly', 0))" 2>/dev/null || echo "0")
resets_at=$(echo "$capacity_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('resets_at', ''))" 2>/dev/null || echo "")

log "Capacity: 5h=${five_hour}% 7d=${weekly}% limited=${limited}"

# 4. If limited, schedule retry and exit
if [ "$limited" = "True" ]; then
    log "Rate limited. Scheduling bounce-back retry."
    
    if [ -n "$resets_at" ]; then
        update_state "rate_limited_retry_scheduled" "$resets_at"
        schedule_retry "$resets_at"
    else
        update_state "rate_limited_no_reset_time"
    fi
    
    exit 0
fi

# 5. Run ccq
log "Capacity available. Running ccq..."
cd "$BRAIN_DIR"

python3 tools/cc-scheduler/ccq run --all 2>&1 | tee -a "$LOG_FILE" || true

log "ccq run completed"

# 6. Git commit and push
log "Committing changes..."
cd "$BRAIN_DIR"
git add -A
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "Overnight run: $DATE_STR"
    git push origin main 2>&1 | tee -a "$LOG_FILE" || log "Push failed"
fi

update_state "completed"
log "=== Run Completed ==="
