#!/bin/bash
# auto-continue.sh
# Auto-continuation script for Claude Code sessions
# Monitors for incomplete work and restarts agents

set -euo pipefail

BRAIN_PATH="${BRAIN_PATH:-/home/user/brain}"
MAX_RETRIES="${MAX_RETRIES:-3}"
RETRY_DELAY="${RETRY_DELAY:-30}"
LOG_FILE="$BRAIN_PATH/logs/auto-continue.log"

log() {
    echo "$(date -Iseconds) | $1" | tee -a "$LOG_FILE"
}

check_incomplete_work() {
    # Check if there's incomplete work that needs continuation

    # 1. Check session-state for in-progress items
    if grep -q "\- \[ \]" "$BRAIN_PATH/context/session-state.md" 2>/dev/null; then
        return 0  # Has incomplete work
    fi

    # 2. Check for active tasks
    if [ -n "$(find "$BRAIN_PATH/tasks/active" -name "*.md" 2>/dev/null)" ]; then
        return 0  # Has active tasks
    fi

    # 3. Check for urgent messages
    if [ -n "$(find "$BRAIN_PATH/messages/inbox" -name "MSG-*-high-*.md" 2>/dev/null)" ]; then
        return 0  # Has urgent messages
    fi

    return 1  # No incomplete work
}

get_continuation_prompt() {
    # Generate context-aware continuation prompt
    cat << 'PROMPT'
Read context/session-state.md first.
Check context/priorities.md for current focus.
Check tasks/active/ for claimed work.
Check messages/inbox/ for new messages.

Continue from where the previous session left off.
If blocked, log to prompts/pending.md and continue with other work.
Commit progress frequently.
PROMPT
}

run_agent() {
    local agent_type="$1"
    local retries=0

    while [ $retries -lt $MAX_RETRIES ]; do
        log "Starting $agent_type agent (attempt $((retries + 1))/$MAX_RETRIES)"

        # Update active-agent
        cat > "$BRAIN_PATH/context/active-agent.md" << EOF
---
agent: $agent_type-auto
started: $(date -Iseconds)
status: running
---

# Active Agent

Auto-continuation session.
EOF

        # Get the continuation prompt
        PROMPT=$(get_continuation_prompt)

        # Run Claude Code
        if claude --dangerously-skip-permissions -p "$PROMPT" 2>&1 | tee -a "$LOG_FILE"; then
            log "$agent_type completed successfully"
            break
        else
            retries=$((retries + 1))
            log "$agent_type failed, retrying in ${RETRY_DELAY}s..."
            sleep "$RETRY_DELAY"
        fi
    done

    if [ $retries -eq $MAX_RETRIES ]; then
        log "ERROR: $agent_type failed after $MAX_RETRIES attempts"
        return 1
    fi

    return 0
}

main() {
    log "=== Auto-Continue Check ==="

    # Pull latest changes
    cd "$BRAIN_PATH"
    git fetch origin 2>/dev/null || true
    git pull origin "$(git branch --show-current)" 2>/dev/null || true

    # Check if continuation needed
    if check_incomplete_work; then
        log "Incomplete work detected, starting continuation"
        run_agent "claude-code"
    else
        log "No incomplete work found"
    fi

    # Clear active-agent if we're done
    if [ -f "$BRAIN_PATH/context/active-agent.md" ]; then
        cat > "$BRAIN_PATH/context/active-agent.md" << 'EOF'
---
agent: None
status: idle
---

# Active Agent

No active agent.
EOF
    fi

    # Commit any changes
    git add -A
    if ! git diff --cached --quiet; then
        git commit -m "Auto-continue: $(date +%Y-%m-%d)"
        git push origin "$(git branch --show-current)" || true
    fi

    log "=== Auto-Continue Complete ==="
}

# Run main if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
