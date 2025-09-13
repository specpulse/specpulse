#!/bin/bash
# Generate or update specification

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

SPEC_DIR="$PROJECT_ROOT/specs/${FEATURE_DIR}"
TEMPLATE_FILE="$PROJECT_ROOT/templates/spec.md"

# Ensure specs directory exists
mkdir -p "$SPEC_DIR"

# Find latest spec file or create new one
if [ -n "$SPEC_CONTENT" ]; then
    # Find next available spec number
    if [ -d "$SPEC_DIR" ]; then
        existing_specs=$(find "$SPEC_DIR" -name "spec-*.md" | wc -l)
        spec_number=$((existing_specs + 1))
    else
        spec_number=1
    fi
    SPEC_FILE="$SPEC_DIR/spec-$(printf "%03d" $spec_number).md"
    
    # Update specification with provided content
    log "Creating specification: $SPEC_FILE"
    echo "$SPEC_CONTENT" > "$SPEC_FILE" || error_exit "Failed to write specification content"
else
    # Find latest spec file
    if [ -d "$SPEC_DIR" ]; then
        SPEC_FILE=$(find "$SPEC_DIR" -name "spec-*.md" -printf "%T@ %p\n" | sort -n | tail -1 | cut -d' ' -f2-)
        if [ -z "$SPEC_FILE" ]; then
            # No spec files found, create first one
            SPEC_FILE="$SPEC_DIR/spec-001.md"
            if [ ! -f "$TEMPLATE_FILE" ]; then
                error_exit "Template not found: $TEMPLATE_FILE"
            fi
            log "Creating specification from template: $SPEC_FILE"
            cp "$TEMPLATE_FILE" "$SPEC_FILE" || error_exit "Failed to copy specification template"
        else
            log "Using latest specification: $SPEC_FILE"
        fi
    else
        # Create directory and first spec
        SPEC_FILE="$SPEC_DIR/spec-001.md"
        if [ ! -f "$TEMPLATE_FILE" ]; then
            error_exit "Template not found: $TEMPLATE_FILE"
        fi
        log "Creating specification from template: $SPEC_FILE"
        cp "$TEMPLATE_FILE" "$SPEC_FILE" || error_exit "Failed to copy specification template"
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