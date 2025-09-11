#!/bin/bash
# Generate or update specification

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
    error_exit "Usage: $SCRIPT_NAME <feature-dir> [spec-content]"
fi

FEATURE_DIR="$1"
SPEC_CONTENT="${2:-}"

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

SPEC_FILE="$PROJECT_ROOT/specs/${FEATURE_DIR}/spec.md"
TEMPLATE_FILE="$PROJECT_ROOT/templates/spec.md"

# Ensure specs directory exists
mkdir -p "$(dirname "$SPEC_FILE")"

if [ -n "$SPEC_CONTENT" ]; then
    # Update specification with provided content
    log "Updating specification: $SPEC_FILE"
    echo "$SPEC_CONTENT" > "$SPEC_FILE" || error_exit "Failed to write specification content"
else
    # Ensure specification exists from template
    if [ ! -f "$SPEC_FILE" ]; then
        if [ ! -f "$TEMPLATE_FILE" ]; then
            error_exit "Template not found: $TEMPLATE_FILE"
        fi
        log "Creating specification from template: $SPEC_FILE"
        cp "$TEMPLATE_FILE" "$SPEC_FILE" || error_exit "Failed to copy specification template"
    else
        log "Specification already exists: $SPEC_FILE"
    fi
fi

# Validate specification
log "Validating specification..."
if [ ! -f "$SPEC_FILE" ]; then
    error_exit "Specification file does not exist: $SPEC_FILE"
fi

# Check for required sections
REQUIRED_SECTIONS=("## Specification:" "## Metadata" "## Functional Requirements" "## Acceptance Scenarios")
MISSING_SECTIONS=()

for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$SPEC_FILE"; then
        MISSING_SECTIONS+=("$section")
    fi
done

if [ ${#MISSING_SECTIONS[@]} -gt 0 ]; then
    log "WARNING: Missing required sections: ${MISSING_SECTIONS[*]}"
fi

# Check for clarifications needed
if grep -q "NEEDS CLARIFICATION" "$SPEC_FILE"; then
    CLARIFICATION_COUNT=$(grep -c "NEEDS CLARIFICATION" "$SPEC_FILE")
    log "WARNING: Specification has $CLARIFICATION_COUNT clarifications needed"
fi

log "Specification processing completed successfully"

echo "SPEC_FILE=$SPEC_FILE"
echo "CLARIFICATIONS_NEEDED=${CLARIFICATION_COUNT:-0}"
echo "MISSING_SECTIONS=${#MISSING_SECTIONS[@]}"
echo "STATUS=updated"