#!/bin/bash
# Generate task breakdown

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

# Validate arguments
if [ $# -eq 0 ]; then
    error_exit "Usage: $SCRIPT_NAME <feature-dir>"
fi

FEATURE_DIR="$1"

# Extract feature ID from directory name (e.g., "001-feature-name" -> "001")
FEATURE_ID=$(echo "$FEATURE_DIR" | grep -o '^[0-9]\{3\}' || echo "001")

# Sanitize feature directory
SANITIZED_DIR=$(echo "$FEATURE_DIR" | sed 's/[^a-zA-Z0-9_-]//g')

if [ -z "$SANITIZED_DIR" ]; then
    error_exit "Invalid feature directory: '$FEATURE_DIR'"
fi

TASK_DIR="$PROJECT_ROOT/tasks/${FEATURE_DIR}"
PLAN_DIR="$PROJECT_ROOT/plans/${FEATURE_DIR}"
SPEC_DIR="$PROJECT_ROOT/specs/${FEATURE_DIR}"
TEMPLATE_FILE="$PROJECT_ROOT/templates/task.md"

# Ensure tasks directory exists
mkdir -p "$TASK_DIR"

# Find latest spec file
if [ -d "$SPEC_DIR" ]; then
    SPEC_FILE=$(find "$SPEC_DIR" -name "spec-*.md" -printf "%T@ %p\n" | sort -n | tail -1 | cut -d' ' -f2-)
    if [ -z "$SPEC_FILE" ]; then
        error_exit "No specification files found in $SPEC_DIR. Please create specification first."
    fi
else
    error_exit "Specifications directory not found: $SPEC_DIR. Please create specification first."
fi

# Find latest plan file
if [ -d "$PLAN_DIR" ]; then
    PLAN_FILE=$(find "$PLAN_DIR" -name "plan-*.md" -printf "%T@ %p\n" | sort -n | tail -1 | cut -d' ' -f2-)
    if [ -z "$PLAN_FILE" ]; then
        error_exit "No plan files found in $PLAN_DIR. Please create plan first."
    fi
else
    error_exit "Plans directory not found: $PLAN_DIR. Please create plan first."
fi

# Find next available task number or create new one
if [ -d "$TASK_DIR" ]; then
    existing_tasks=$(find "$TASK_DIR" -name "task-*.md" | wc -l)
    task_number=$((existing_tasks + 1))
else
    task_number=1
fi
TASK_FILE="$TASK_DIR/task-$(printf "%03d" $task_number).md"

# Ensure task template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    error_exit "Template not found: $TEMPLATE_FILE"
fi

# Create task file
log "Creating task breakdown from template: $TASK_FILE"
cp "$TEMPLATE_FILE" "$TASK_FILE" || error_exit "Failed to copy task template"

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
COMPLETION_PERCENTAGE=0
if [ "${TOTAL_TASKS:-0}" -gt 0 ] && [ "${COMPLETED_TASKS:-0}" -ge 0 ]; then
    COMPLETION_PERCENTAGE=$(( (COMPLETED_TASKS * 100) / TOTAL_TASKS ))
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