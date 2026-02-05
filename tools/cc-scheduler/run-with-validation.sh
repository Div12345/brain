#!/bin/bash
# Run a Gemini task with output validation and retry
# Usage: ./run-with-validation.sh [expected_marker] [max_retries]

EXPECTED_MARKER="${1:-TASK COMPLETE}"
MAX_RETRIES="${2:-3}"
RETRY=0

while [ $RETRY -lt $MAX_RETRIES ]; do
    echo "[Attempt $((RETRY+1))/$MAX_RETRIES] Running task..."

    # Run the task and capture output
    OUTPUT=$(./ccq run --backend desktop --force 2>&1)
    EXIT_CODE=$?

    echo "$OUTPUT"

    # Check for expected marker
    if echo "$OUTPUT" | grep -q "$EXPECTED_MARKER"; then
        echo "[SUCCESS] Found expected marker: $EXPECTED_MARKER"
        exit 0
    fi

    # Check for quota exhaustion (don't retry)
    if echo "$OUTPUT" | grep -qi "quota\|rate.limit"; then
        echo "[QUOTA] Quota exhausted, not retrying"
        exit 1
    fi

    RETRY=$((RETRY+1))
    if [ $RETRY -lt $MAX_RETRIES ]; then
        echo "[RETRY] Marker not found, retrying in 10s..."
        sleep 10
    fi
done

echo "[FAILED] Expected marker '$EXPECTED_MARKER' not found after $MAX_RETRIES attempts"
exit 1
