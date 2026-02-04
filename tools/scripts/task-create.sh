#!/bin/bash
# task-create.sh - Create bead + scheduler task with minimal input
# Usage: task-create.sh "Title" "Goal description" [priority] [tags]
#
# Example:
#   task-create.sh "Fix auth bug" "Resolve the token expiry in login flow" 1 "bugfix,auth"

set -e

BRAIN_ROOT="${BRAIN_ROOT:-$HOME/brain}"
BEADS_FILE="$BRAIN_ROOT/.beads/issues.jsonl"
TASKS_DIR="$BRAIN_ROOT/tasks/pending"

# Input validation
if [[ $# -lt 2 ]]; then
    echo "Usage: task-create.sh \"Title\" \"Goal description\" [priority] [tags]"
    echo ""
    echo "Arguments:"
    echo "  Title       - Short task title"
    echo "  Goal        - One sentence goal description"
    echo "  priority    - 1=urgent, 2=normal (default), 3=low"
    echo "  tags        - Comma-separated tags (optional)"
    exit 1
fi

TITLE="$1"
GOAL="$2"
PRIORITY="${3:-2}"
TAGS="${4:-}"

# Generate bead ID (brain-xxx format)
BEAD_ID="brain-$(cat /dev/urandom | tr -dc 'a-z0-9' | head -c3)"

# Convert title to filename slug
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

# Find next task number
LAST_NUM=$(ls "$TASKS_DIR"/*.md 2>/dev/null | grep -oE '[0-9]{3}' | sort -n | tail -1)
if [[ -z "$LAST_NUM" ]]; then
    LAST_NUM="000"
fi
NEXT_NUM=$(printf "%03d" $((LAST_NUM + 5)))

TASK_FILE="$TASKS_DIR/${NEXT_NUM}-${SLUG}.md"
TIMESTAMP=$(date -Iseconds)

# Estimate tokens based on goal length
GOAL_LEN=${#GOAL}
if [[ $GOAL_LEN -lt 100 ]]; then
    EST_TOKENS=5000
    TIMEOUT="10m"
    MODEL="haiku"
elif [[ $GOAL_LEN -lt 300 ]]; then
    EST_TOKENS=10000
    TIMEOUT="20m"
    MODEL="sonnet"
else
    EST_TOKENS=20000
    TIMEOUT="30m"
    MODEL="sonnet"
fi

# Format tags for JSON
if [[ -n "$TAGS" ]]; then
    TAGS_JSON=$(echo "$TAGS" | tr ',' '\n' | sed 's/^/"/;s/$/"/' | paste -sd,)
    TAGS_JSON="[$TAGS_JSON]"
    TAGS_YAML=$(echo "$TAGS" | tr ',' '\n' | sed 's/^/  - /')
else
    TAGS_JSON="[]"
    TAGS_YAML=""
fi

# Create bead entry
BEAD_JSON=$(cat <<EOF
{"id":"$BEAD_ID","title":"$TITLE","description":"$GOAL","status":"open","priority":$PRIORITY,"issue_type":"task","owner":"overnight-agent@brain","created_at":"$TIMESTAMP","created_by":"task-create.sh","updated_at":"$TIMESTAMP","labels":$TAGS_JSON}
EOF
)

echo "$BEAD_JSON" >> "$BEADS_FILE"

# Create scheduler task file
cat > "$TASK_FILE" <<EOF
---
name: $SLUG
priority: $PRIORITY
estimated_tokens: $EST_TOKENS
mode: autonomous
timeout: $TIMEOUT
skill: analyze
model_hint: $MODEL
tags: [$(echo "$TAGS" | tr ',' ', ')]
depends_on: []
bead_id: $BEAD_ID
---

# $TITLE

## Goal
$GOAL

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain
- **MCP tools needed:** None

## What This Task Must Produce
[Specify deliverables]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Overnight Agent Instructions
1. [Step 1]
2. [Step 2]
3. Verify success criteria
EOF

echo "Created:"
echo "  Bead: $BEAD_ID"
echo "  Task: $TASK_FILE"
echo ""
echo "Edit $TASK_FILE to add specific deliverables and instructions."
