#!/bin/bash
# Overnight task runner - triggered by Windows Task Scheduler
# Runs pending tasks via Gemini→Desktop pipeline (no CC API quota used)
#
# Usage: ./trigger-overnight.sh [--backend desktop|code|auto] [--dry]

set -euo pipefail

# Ensure nvm/node/gemini are in PATH (needed when launched from Windows Task Scheduler)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh" 2>/dev/null || true
# Fallback: add node directly if nvm had issues
export PATH="$HOME/.nvm/versions/node/v24.13.0/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRAIN_ROOT="$HOME/brain"
LOG_DIR="$BRAIN_ROOT/logs/scheduler"
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
LOG_FILE="$LOG_DIR/overnight-$TIMESTAMP.log"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

BACKEND="desktop"  # default
DRY=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --backend) BACKEND="$2"; shift 2 ;;
        --dry) DRY="--dry"; shift ;;
        *) shift ;;
    esac
done

log "=== Overnight Task Runner ==="
log "Backend: $BACKEND"
log "Started: $(date)"

# Pre-flight checks
if [[ "$BACKEND" == "desktop" || "$BACKEND" == "auto" ]]; then
    # Check Desktop debugger port
    if curl -s --connect-timeout 2 http://127.0.0.1:9229/json > /dev/null 2>&1; then
        log "Desktop debugger: available"
    else
        log "Desktop debugger: NOT available"
        if [[ "$BACKEND" == "desktop" ]]; then
            log "ERROR: Desktop backend requested but debugger not available."
            log "Enable 'Main Process Debugger' in Claude Desktop Help menu."
            exit 1
        fi
        log "Falling back to code backend"
        BACKEND="code"
    fi
fi

if [[ "$BACKEND" == "code" ]]; then
    # Check CC capacity
    log "Checking CC API capacity..."
fi

# Check for Gemini CLI
if [[ "$BACKEND" == "desktop" ]]; then
    if ! command -v gemini &> /dev/null; then
        log "ERROR: gemini CLI not found in PATH"
        exit 1
    fi
    log "Gemini CLI: $(gemini --version 2>/dev/null || echo 'unknown version')"
fi

# Run the scheduler
log "Running ccq..."
cd "$SCRIPT_DIR"

if [[ -n "$DRY" ]]; then
    python3 ccq run --backend "$BACKEND" --all --dry --force 2>&1 | tee -a "$LOG_FILE"
else
    python3 ccq run --backend "$BACKEND" --all --force 2>&1 | tee -a "$LOG_FILE"
fi

EXIT_CODE=$?

log "Exit code: $EXIT_CODE"
log "Finished: $(date)"
log "Log: $LOG_FILE"

exit $EXIT_CODE
