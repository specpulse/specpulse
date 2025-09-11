#!/bin/bash
# Generate task breakdown

set -euo pipefail  # Exit on error, unset vars, pipe failures

# Configuration
SCRIPT_NAME="$(basename "$0")"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $SCRIPT_NAME: $1" >&2
}

# Function to handle errors
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Validate arguments
if [ $# -eq 0 ]; then
    error_exit "Usage: $SCRIPT_NAME <feature-dir>"
fi

FEATURE_DIR="$1"

# Sanitize feature directory
SANITIZED_DIR=$(echo "$FEATURE_DIR" | sed 's/[^a-zA-Z0-9_-]//g')

if [ -z "$SANITIZED_DIR" ]; then
    error_exit "Invalid feature directory: '$FEATURE_DIR'"
fi

# Find feature directory if not provided
if [ -z "$FEATURE_DIR" ]; then
    CONTEXT_FILE="$PROJECT_ROOT/memory/context.md"
    if [ -f "$CONTEXT_FILE" ]; then
        FEATURE_DIR=$(grep -A1 "Active Feature" "$CONTEXT_FILE" | tail -1 | cut -d: -f2 | xargs)
        if [ -z "$FEATURE_DIR" ]; then
            error_exit "No active feature found in context file"
        fi
        log "Using active feature from context: $FEATURE_DIR"
    else
        error_exit "No feature directory provided and no context file found"
    fi
fi

TASK_FILE="$PROJECT_ROOT/tasks/${FEATURE_DIR}/tasks.md"
TEMPLATE_FILE="$PROJECT_ROOT/templates/task.md"
PLAN_FILE="$PROJECT_ROOT/plans/${FEATURE_DIR}/plan.md"
SPEC_FILE="$PROJECT_ROOT/specs/${FEATURE_DIR}/spec.md"

# Ensure tasks directory exists
mkdir -p "$(dirname "$TASK_FILE")"

# Check if specification and plan exist first
if [ ! -f "$SPEC_FILE" ]; then
    error_exit "Specification file not found: $SPEC_FILE. Please create specification first."
fi

if [ ! -f "$PLAN_FILE" ]; then
    error_exit "Implementation plan not found: $PLAN_FILE. Please create plan first."
fi

# Ensure task template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    error_exit "Template not found: $TEMPLATE_FILE"
fi

# Create task file if it doesn't exist
if [ ! -f "$TASK_FILE" ]; then
    log "Creating task breakdown from template: $TASK_FILE"
    cp "$TEMPLATE_FILE" "$TASK_FILE" || error_exit "Failed to copy task template"
else
    log "Task breakdown already exists: $TASK_FILE"
fi

# Validate task structure
log "Validating task breakdown..."

# Check for required sections
REQUIRED_SECTIONS=("## Task List:" "## Task Organization" "## Critical Path" "## Execution Schedule")
MISSING_SECTIONS=()

for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$TASK_FILE"; then
        MISSING_SECTIONS+=("$section")
    fi
done

if [ ${#MISSING_SECTIONS[@]} -gt 0 ]; then
    log "WARNING: Missing required sections: ${MISSING_SECTIONS[*]}"
fi

# Count tasks and analyze structure
TOTAL_TASKS=$(grep -c "^- \[.\]" "$TASK_FILE" 2>/dev/null || echo "0")
COMPLETED_TASKS=$(grep -c "^- \[x\]" "$TASK_FILE" 2>/dev/null || echo "0")
PENDING_TASKS=$(grep -c "^- \[ \]" "$TASK_FILE" 2>/dev/null || echo "0")
BLOCKED_TASKS=$(grep -c "^- \[!\]" "$TASK_FILE" 2>/dev/null || echo "0")

# Check for parallel tasks
PARALLEL_TASKS=$(grep -c "\[P\]" "$TASK_FILE" 2>/dev/null || echo "0")

# Check constitutional gates compliance
CONSTITUTIONAL_SECTION=$(grep -A 20 "Constitutional Gates Compliance" "$TASK_FILE" 2>/dev/null || echo "")
GATES_COUNT=$(echo "$CONSTITUTIONAL_SECTION" | grep -c "\[ \]" 2>/dev/null || echo "0")

# Check if plan has constitutional gates completed
PLAN_GATE_STATUS=$(grep -A5 "Gate Status:" "$PLAN_FILE" | tail -1 | sed 's/.*\[\(.*\)\].*/\1/' || echo "PENDING")

if [ "$PLAN_GATE_STATUS" != "COMPLETED" ]; then
    log "WARNING: Implementation plan constitutional gates not completed. Task generation may be premature."
fi

# Calculate completion percentage
if [ "$TOTAL_TASKS" -gt 0 ]; then
    COMPLETION_PERCENTAGE=$((COMPLETED_TASKS * 100 / TOTAL_TASKS))
else
    COMPLETION_PERCENTAGE=0
fi

log "Task analysis completed - Total: $TOTAL_TASKS, Completed: $COMPLETED_TASKS ($COMPLETION_PERCENTAGE%), Parallel: $PARALLEL_TASKS"

# Output comprehensive status
echo "TASK_FILE=$TASK_FILE"
echo "SPEC_FILE=$SPEC_FILE"
echo "PLAN_FILE=$PLAN_FILE"
echo "TOTAL_TASKS=$TOTAL_TASKS"
echo "COMPLETED_TASKS=$COMPLETED_TASKS"
echo "PENDING_TASKS=$PENDING_TASKS"
echo "BLOCKED_TASKS=$BLOCKED_TASKS"
echo "PARALLEL_TASKS=$PARALLEL_TASKS"
echo "CONSTITUTIONAL_GATES_PENDING=$GATES_COUNT"
echo "COMPLETION_PERCENTAGE=$COMPLETION_PERCENTAGE"
echo "MISSING_SECTIONS=${#MISSING_SECTIONS[@]}"
echo "STATUS=generated"