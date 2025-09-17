#!/bin/bash
# Generate implementation plan

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

PLAN_DIR="$PROJECT_ROOT/plans/${FEATURE_DIR}"
SPEC_DIR="$PROJECT_ROOT/specs/${FEATURE_DIR}"
TEMPLATE_FILE="$PROJECT_ROOT/templates/plan.md"

# Ensure plans directory exists
mkdir -p "$PLAN_DIR"

# Find latest spec file
if [ -d "$SPEC_DIR" ]; then
    SPEC_FILE=$(find "$SPEC_DIR" -name "spec-*.md" -printf "%T@ %p\n" | sort -n | tail -1 | cut -d' ' -f2-)
    if [ -z "$SPEC_FILE" ]; then
        error_exit "No specification files found in $SPEC_DIR. Please create specification first."
    fi
else
    error_exit "Specifications directory not found: $SPEC_DIR. Please create specification first."
fi

# Find next available plan number or create new one
if [ -d "$PLAN_DIR" ]; then
    existing_plans=$(find "$PLAN_DIR" -name "plan-*.md" | wc -l)
    plan_number=$((existing_plans + 1))
else
    plan_number=1
fi
PLAN_FILE="$PLAN_DIR/plan-$(printf "%03d" $plan_number).md"

# Ensure plan template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    error_exit "Template not found: $TEMPLATE_FILE"
fi

# Create plan
log "Creating implementation plan from template: $PLAN_FILE"
cp "$TEMPLATE_FILE" "$PLAN_FILE" || error_exit "Failed to copy plan template"

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

# Check SDD Gates
log "Checking SDD Gates..."

SDD_GATES=(
    "Specification First"
    "Incremental Planning"
    "Task Decomposition"
    "Traceable Implementation"
    "Continuous Validation"
    "Quality Assurance"
    "Architecture Documentation"
    "Iterative Refinement"
    "Stakeholder Alignment"
)

for gate in "${SDD_GATES[@]}"; do
    if ! grep -q "$gate" "$PLAN_FILE"; then
        log "WARNING: Missing SDD gate: $gate"
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
    log "WARNING: SDD gates not completed. Status: $GATE_STATUS"
fi

log "Implementation plan processing completed successfully"

echo "PLAN_FILE=$PLAN_FILE"
echo "SPEC_FILE=$SPEC_FILE"
echo "MISSING_SECTIONS=${#MISSING_SECTIONS[@]}"
echo "SDD_GATES_STATUS=$GATE_STATUS"
echo "STATUS=ready"