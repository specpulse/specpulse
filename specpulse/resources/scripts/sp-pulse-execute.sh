#!/bin/bash
# Execute tasks continuously from task list

set -euo pipefail  # Exit on error, unset vars, pipe failures

# Configuration
SCRIPT_NAME="$(basename "$0")"
# Script is in project-root/scripts/, so parent dir is project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $SCRIPT_NAME: $1" >&2
}

# Function to handle errors
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Validate arguments (optional - can be feature-dir or "next")
COMMAND="${1:-next}"
FEATURE_DIR="${2:-}"

# Find active feature if not provided
if [ -z "$FEATURE_DIR" ]; then
    CONTEXT_FILE="$PROJECT_ROOT/memory/context.md"
    if [ -f "$CONTEXT_FILE" ]; then
        # Extract active feature from context
        FEATURE_NAME=$(grep -A1 "Active Feature:" "$CONTEXT_FILE" | tail -1 | sed 's/.*: //' | xargs)
        FEATURE_ID=$(grep -A1 "Feature ID:" "$CONTEXT_FILE" | tail -1 | sed 's/.*: //' | xargs)
        if [ -n "$FEATURE_ID" ] && [ -n "$FEATURE_NAME" ]; then
            # Convert to branch name format
            BRANCH_SAFE_NAME=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
            FEATURE_DIR="${FEATURE_ID}-${BRANCH_SAFE_NAME}"
            log "Using active feature: $FEATURE_DIR"
        else
            error_exit "No active feature found in context file"
        fi
    else
        error_exit "No feature directory provided and no context file found"
    fi
fi

TASK_DIR="$PROJECT_ROOT/tasks/${FEATURE_DIR}"

# Ensure tasks directory exists
if [ ! -d "$TASK_DIR" ]; then
    error_exit "Tasks directory not found: $TASK_DIR"
fi

# Find latest task file
TASK_FILE=$(find "$TASK_DIR" -name "*.md" -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)

if [ -z "$TASK_FILE" ]; then
    error_exit "No task files found in $TASK_DIR"
fi

log "Analyzing task file: $TASK_FILE"

# Detect if decomposed (service-specific tasks)
IS_DECOMPOSED=false
if grep -qE "AUTH-T[0-9]|USER-T[0-9]|INT-T[0-9]" "$TASK_FILE" 2>/dev/null; then
    IS_DECOMPOSED=true
    log "Detected decomposed architecture with service-specific tasks"
fi

# Count task status
TOTAL_TASKS=$(grep -cE "^- \[.\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" 2>/dev/null || echo "0")
COMPLETED_TASKS=$(grep -cE "^- \[x\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" 2>/dev/null || echo "0")
PENDING_TASKS=$(grep -cE "^- \[ \] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" 2>/dev/null || echo "0")
IN_PROGRESS_TASKS=$(grep -cE "^- \[>\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" 2>/dev/null || echo "0")
BLOCKED_TASKS=$(grep -cE "^- \[!\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" 2>/dev/null || echo "0")

# Find next task to execute
case "$COMMAND" in
    "next"|"continue")
        # Find first in-progress task
        if [ "$IN_PROGRESS_TASKS" -gt 0 ]; then
            NEXT_TASK=$(grep -E "^- \[>\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" | head -1 | sed -E 's/.*\[(T[0-9]{3}|[A-Z]+-T[0-9]{3})\].*/\1/')
            log "Resuming in-progress task: $NEXT_TASK"
        # Otherwise find first pending task
        elif [ "$PENDING_TASKS" -gt 0 ]; then
            NEXT_TASK=$(grep -E "^- \[ \] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" | head -1 | sed -E 's/.*\[(T[0-9]{3}|[A-Z]+-T[0-9]{3})\].*/\1/')
            log "Starting next pending task: $NEXT_TASK"
        else
            if [ "$BLOCKED_TASKS" -gt 0 ]; then
                log "All tasks completed or blocked. $BLOCKED_TASKS tasks are blocked."
                NEXT_TASK="BLOCKED"
            else
                log "All tasks completed!"
                NEXT_TASK="COMPLETED"
            fi
        fi
        ;;
    "all"|"batch")
        log "Batch execution mode - will process all pending tasks"
        NEXT_TASK="BATCH"
        ;;
    T[0-9][0-9][0-9]|*-T[0-9][0-9][0-9])
        # Specific task requested
        NEXT_TASK="$COMMAND"
        log "Executing specific task: $NEXT_TASK"
        ;;
    *)
        error_exit "Unknown command: $COMMAND. Use 'next', 'continue', 'all', or specific task ID"
        ;;
esac

# Calculate progress
if [ "$TOTAL_TASKS" -gt 0 ]; then
    PROGRESS=$((COMPLETED_TASKS * 100 / TOTAL_TASKS))
else
    PROGRESS=0
fi

# Output execution plan
echo "TASK_FILE=$TASK_FILE"
echo "FEATURE_DIR=$FEATURE_DIR"
echo "IS_DECOMPOSED=$IS_DECOMPOSED"
echo "TOTAL_TASKS=$TOTAL_TASKS"
echo "COMPLETED_TASKS=$COMPLETED_TASKS"
echo "PENDING_TASKS=$PENDING_TASKS"
echo "IN_PROGRESS_TASKS=$IN_PROGRESS_TASKS"
echo "BLOCKED_TASKS=$BLOCKED_TASKS"
echo "PROGRESS=$PROGRESS%"
echo "NEXT_TASK=$NEXT_TASK"

# Provide execution guidance
if [ "$NEXT_TASK" = "COMPLETED" ]; then
    echo "STATUS=all_completed"
    echo "MESSAGE=All tasks have been completed! Consider running validation."
elif [ "$NEXT_TASK" = "BLOCKED" ]; then
    echo "STATUS=blocked"
    echo "MESSAGE=All remaining tasks are blocked. Review blockers and dependencies."
elif [ "$NEXT_TASK" = "BATCH" ]; then
    echo "STATUS=batch_ready"
    echo "MESSAGE=Ready to execute $PENDING_TASKS pending tasks in sequence."
else
    echo "STATUS=ready"
    echo "MESSAGE=Ready to execute task $NEXT_TASK"
fi

# List next 5 tasks for preview
if [ "$PENDING_TASKS" -gt 0 ]; then
    echo ""
    echo "NEXT_TASKS_PREVIEW:"
    grep -E "^- \[ \] (T[0-9]{3}|[A-Z]+-T[0-9]{3})" "$TASK_FILE" | head -5 | while read -r line; do
        echo "  $line"
    done
fi

exit 0