#!/usr/bin/env bash
# cc-session-audit.sh - Analyze Claude Code session transcript JSONL
# Usage: cc-session-audit.sh [--subagents] [path-to-jsonl]

set -euo pipefail

# Parse arguments
SUBAGENTS=false
JSONL=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --subagents)
            SUBAGENTS=true
            shift
            ;;
        *)
            JSONL="$1"
            shift
            ;;
    esac
done

# Find most recent JSONL if no file arg provided
if [[ -z "$JSONL" ]]; then
    JSONL=$(find ~/.claude/projects -name "*.jsonl" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
    if [[ -z "$JSONL" ]]; then
        echo "Error: No JSONL files found in ~/.claude/projects/" >&2
        exit 1
    fi
    echo "Auto-selected: $JSONL"
    echo ""
else
    if [[ ! -f "$JSONL" ]]; then
        echo "Error: File not found: $JSONL" >&2
        exit 1
    fi
fi

# Extract timestamps for duration (suppress SIGPIPE from grep | head)
FIRST_TS=$(set +o pipefail; grep -o '"timestamp":"[^"]*"' "$JSONL" | head -1 | sed 's/"timestamp":"//;s/"//')
LAST_TS=$(grep -o '"timestamp":"[^"]*"' "$JSONL" | tail -1 | sed 's/"timestamp":"//;s/"//')

# Convert ISO timestamps to epoch seconds for duration calc
FIRST_EPOCH=$(date -d "$FIRST_TS" +%s 2>/dev/null || echo 0)
LAST_EPOCH=$(date -d "$LAST_TS" +%s 2>/dev/null || echo 0)
DURATION_SEC=$((LAST_EPOCH - FIRST_EPOCH))
DURATION_HOURS=$((DURATION_SEC / 3600))
DURATION_MIN=$(( (DURATION_SEC % 3600) / 60 ))

# Total lines
TOTAL_LINES=$(wc -l < "$JSONL")

echo "=== SESSION SUMMARY ==="
echo "File: $JSONL"
echo "Total lines: $TOTAL_LINES"
echo "Start: $FIRST_TS"
echo "End:   $LAST_TS"
if [[ $DURATION_HOURS -gt 0 ]]; then
    echo "Duration: ${DURATION_HOURS}h ${DURATION_MIN}m"
else
    echo "Duration: ${DURATION_MIN}m"
fi
echo ""

echo "=== EVENT TYPE COUNTS ==="
grep -o '"type":"[^"]*"' "$JSONL" | sed 's/"type":"//;s/"//' | sort | uniq -c | sort -rn
echo ""

# Hook firings
echo "=== HOOK FIRINGS (by command) ==="
HOOK_COUNT=$(grep -c '"hook_progress"' "$JSONL" 2>/dev/null || true)
if [[ $HOOK_COUNT -gt 0 ]]; then
    grep '"hook_progress"' "$JSONL" | grep -o '"command":"[^"]*"' | sed 's/"command":"//;s/"//' | sort | uniq -c | sort -rn
    echo ""
    echo "Total hook firings: $HOOK_COUNT"
else
    echo "(none detected)"
fi
echo ""

# Tool call count
TOOL_CALLS=$(grep -c '"tool_use"' "$JSONL" 2>/dev/null || true)
echo "=== TOOL CALL COUNT ==="
echo "$TOOL_CALLS"
echo ""

# Hook/tool ratio
echo "=== HOOKS PER TOOL CALL ==="
if [[ $TOOL_CALLS -gt 0 ]]; then
    RATIO=$(awk "BEGIN {printf \"%.2f\", $HOOK_COUNT / $TOOL_CALLS}")
    echo "$RATIO"
else
    echo "N/A (no tool calls)"
fi
echo ""

# Token summary (transcript uses both camelCase and snake_case field names)
echo "=== TOKEN SUMMARY ==="
INPUT_TOKENS=$(grep -o '"input_tokens":[0-9]*' "$JSONL" 2>/dev/null | sed 's/"input_tokens"://' | awk '{s+=$1} END {print s+0}')
OUTPUT_TOKENS=$(grep -o '"output_tokens":[0-9]*' "$JSONL" 2>/dev/null | sed 's/"output_tokens"://' | awk '{s+=$1} END {print s+0}')
CACHE_CREATE=$(grep -o '"cache_creation_input_tokens":[0-9]*' "$JSONL" 2>/dev/null | sed 's/"cache_creation_input_tokens"://' | awk '{s+=$1} END {print s+0}')
CACHE_READ=$(grep -o '"cache_read_input_tokens":[0-9]*' "$JSONL" 2>/dev/null | sed 's/"cache_read_input_tokens"://' | awk '{s+=$1} END {print s+0}')

echo "Input tokens:          $INPUT_TOKENS"
echo "Output tokens:         $OUTPUT_TOKENS"
echo "Cache creation tokens: $CACHE_CREATE"
echo "Cache read tokens:     $CACHE_READ"
echo "Total (input+output):  $((INPUT_TOKENS + OUTPUT_TOKENS))"
echo ""

# System-reminder count
SYSTEM_REMINDER_COUNT=$(grep -c 'system-reminder' "$JSONL" 2>/dev/null || true)
echo "=== SYSTEM-REMINDER COUNT ==="
echo "$SYSTEM_REMINDER_COUNT (estimated hook-injected context blocks)"
echo ""

# Subagent analysis
if [[ "$SUBAGENTS" == true ]]; then
    JSONL_DIR="${JSONL%.jsonl}"
    SUBAGENT_DIR="$JSONL_DIR/subagents"

    if [[ -d "$SUBAGENT_DIR" ]]; then
        echo "=== SUBAGENT ANALYSIS ==="
        SUBAGENT_FILES=$(find "$SUBAGENT_DIR" -name "agent-*.jsonl" -type f | sort)

        if [[ -n "$SUBAGENT_FILES" ]]; then
            while IFS= read -r subagent_file; do
                AGENT_ID=$(basename "$subagent_file" .jsonl | sed 's/agent-//')
                LINE_COUNT=$(wc -l < "$subagent_file")

                # Extract model name
                MODEL=$(set +o pipefail; grep -o '"model":"[^"]*"' "$subagent_file" | head -1 | sed 's/"model":"//;s/"//' || echo "unknown")

                # Tool call analysis
                SUB_TOOL_CALLS=$(grep -c '"tool_use"' "$subagent_file" 2>/dev/null || true)

                # Top 5 tools
                TOP_TOOLS=""
                if [[ $SUB_TOOL_CALLS -gt 0 ]]; then
                    TOP_TOOLS=$(grep '"tool_use"' "$subagent_file" | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"//' | sort | uniq -c | sort -rn | head -5 | awk '{printf "%s(%d) ", $2, $1}')
                fi

                # Hook count
                SUB_HOOK_COUNT=$(grep -c '"hook_progress"' "$subagent_file" 2>/dev/null || true)

                # Token summary
                SUB_CACHE_CREATE=$(grep -o '"cache_creation_input_tokens":[0-9]*' "$subagent_file" 2>/dev/null | sed 's/"cache_creation_input_tokens"://' | awk '{s+=$1} END {print s+0}')
                SUB_CACHE_READ=$(grep -o '"cache_read_input_tokens":[0-9]*' "$subagent_file" 2>/dev/null | sed 's/"cache_read_input_tokens"://' | awk '{s+=$1} END {print s+0}')

                echo ""
                echo "Agent: $AGENT_ID (model: $MODEL)"
                echo "  Lines: $LINE_COUNT"
                echo "  Tool calls: $SUB_TOOL_CALLS"
                if [[ -n "$TOP_TOOLS" ]]; then
                    echo "  Top tools: $TOP_TOOLS"
                fi
                echo "  Hooks: $SUB_HOOK_COUNT"
                echo "  Cache create tokens: $SUB_CACHE_CREATE"
                echo "  Cache read tokens: $SUB_CACHE_READ"
            done <<< "$SUBAGENT_FILES"
        else
            echo "(no agent-*.jsonl files found)"
        fi
        echo ""
    else
        echo "=== SUBAGENT ANALYSIS ==="
        echo "(subagent directory not found: $SUBAGENT_DIR)"
        echo ""
    fi
fi

echo "=== AUDIT COMPLETE ==="
