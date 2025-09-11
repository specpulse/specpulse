#!/bin/bash
# Generate task breakdown

FEATURE_DIR="${1}"

if [ -z "$FEATURE_DIR" ]; then
    # Find current feature from context
    FEATURE_DIR=$(grep -A1 "Active Feature" memory/context.md | tail -1 | cut -d: -f2 | xargs)
fi

TASK_FILE="tasks/${FEATURE_DIR}/tasks.md"

# Ensure template exists
if [ ! -f "$TASK_FILE" ]; then
    cp templates/task.md "$TASK_FILE"
fi

# Count tasks
TASK_COUNT=$(grep -c "^- \[" "$TASK_FILE" 2>/dev/null || echo "0")

echo "TASK_FILE=$TASK_FILE"
echo "TASK_COUNT=$TASK_COUNT"
echo "STATUS=generated"