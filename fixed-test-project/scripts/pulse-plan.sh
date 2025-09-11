#!/bin/bash
# Generate implementation plan

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

PLAN_FILE="$PROJECT_ROOT/plans/${FEATURE_DIR}/plan.md"
TEMPLATE_FILE="$PROJECT_ROOT/templates/plan.md"
SPEC_FILE="$PROJECT_ROOT/specs/${FEATURE_DIR}/spec.md"

# Ensure plans directory exists
mkdir -p "$(dirname "$PLAN_FILE")"

# Check if specification exists first
if [ ! -f "$SPEC_FILE" ]; then
    error_exit "Specification file not found: $SPEC_FILE. Please create specification first."
fi

# Ensure plan template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    error_exit "Template not found: $TEMPLATE_FILE"
fi

# Create plan if it doesn't exist
if [ ! -f "$PLAN_FILE" ]; then
    log "Creating implementation plan from template: $PLAN_FILE"
    cp "$TEMPLATE_FILE" "$PLAN_FILE" || error_exit "Failed to copy plan template"
else
    log "Implementation plan already exists: $PLAN_FILE"
fi

# Validate plan structure
log "Validating implementation plan..."

# Check for required sections
REQUIRED_SECTIONS=("## Implementation Plan:" "## Specification Reference" "## Phase -1: Pre-Implementation Gates" "## Implementation Phases")
MISSING_SECTIONS=()

for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$PLAN_FILE"; then
        MISSING_SECTIONS+=("$section")
    fi
done

if [ ${#MISSING_SECTIONS[@]} -gt 0 ]; then
    log "WARNING: Missing required sections: ${MISSING_SECTIONS[*]}"
fi

# Check Constitutional Gates
log "Checking Constitutional Gates..."

CONSTITUTIONAL_GATES=(
    "Simplicity Gate"
    "Anti-Abstraction Gate"
    "Test-First Gate"
    "Integration-First Gate"
    "Research Gate"
)

for gate in "${CONSTITUTIONAL_GATES[@]}"; do
    if ! grep -q "$gate" "$PLAN_FILE"; then
        log "WARNING: Missing constitutional gate: $gate"
    fi
done

# Check if specification has clarifications needed
if grep -q "NEEDS CLARIFICATION" "$SPEC_FILE"; then
    CLARIFICATION_COUNT=$(grep -c "NEEDS CLARIFICATION" "$SPEC_FILE")
    log "WARNING: Specification has $CLARIFICATION_COUNT clarifications needed - resolve before proceeding"
fi

# Validate gate compliance
GATE_STATUS=$(grep -A5 "Gate Status:" "$PLAN_FILE" | tail -1 | sed 's/.*\[\(.*\)\].*/\1/' || echo "PENDING")

if [ "$GATE_STATUS" != "COMPLETED" ]; then
    log "WARNING: Constitutional gates not completed. Status: $GATE_STATUS"
fi

log "Implementation plan processing completed successfully"

echo "PLAN_FILE=$PLAN_FILE"
echo "SPEC_FILE=$SPEC_FILE"
echo "MISSING_SECTIONS=${#MISSING_SECTIONS[@]}"
echo "CONSTITUTIONAL_GATES_STATUS=$GATE_STATUS"
echo "STATUS=ready"