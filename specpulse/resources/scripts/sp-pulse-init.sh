#!/bin/bash
# Initialize a new feature with SpecPulse

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
    error_exit "Usage: $SCRIPT_NAME <feature-name> [feature-id]"
fi

FEATURE_NAME="$1"
CUSTOM_ID="${2:-}"

# Sanitize feature name
BRANCH_SAFE_NAME=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')

if [ -z "$BRANCH_SAFE_NAME" ]; then
    error_exit "Invalid feature name: '$FEATURE_NAME'"
fi

# Get feature ID
if [ -n "$CUSTOM_ID" ]; then
    FEATURE_ID=$(printf "%03d" "$CUSTOM_ID")
else
    FEATURE_ID=$(printf "%03d" $(find "$PROJECT_ROOT/specs" -maxdepth 1 -type d -name '[0-9]*' 2>/dev/null | wc -l | awk '{print $1 + 1}'))
fi

BRANCH_NAME="${FEATURE_ID}-${BRANCH_SAFE_NAME}"

# Create directories
SPECS_DIR="$PROJECT_ROOT/specs/${BRANCH_NAME}"
PLANS_DIR="$PROJECT_ROOT/plans/${BRANCH_NAME}"
TASKS_DIR="$PROJECT_ROOT/tasks/${BRANCH_NAME}"

log "Creating feature directories for '$FEATURE_NAME'"

mkdir -p "$SPECS_DIR" || error_exit "Failed to create specs directory: $SPECS_DIR"
mkdir -p "$PLANS_DIR" || error_exit "Failed to create plans directory: $PLANS_DIR"
mkdir -p "$TASKS_DIR" || error_exit "Failed to create tasks directory: $TASKS_DIR"

# Validate templates exist but don't copy them directly
TEMPLATE_DIR="$PROJECT_ROOT/templates"

# Validate all required templates exist
for template in spec.md plan.md task.md; do
    if [ ! -f "$TEMPLATE_DIR/$template" ]; then
        error_exit "Template not found: $TEMPLATE_DIR/$template. Please run 'specpulse init' to initialize templates."
    fi
done

# Create marker files that indicate AI should use templates to generate content
# These are placeholder files that will be replaced by AI-generated content
echo "# Specification for $FEATURE_NAME" > "$SPECS_DIR/spec-001.md"
echo "# Implementation Plan for $FEATURE_NAME" > "$PLANS_DIR/plan-001.md"
echo "# Task Breakdown for $FEATURE_NAME" > "$TASKS_DIR/task-001.md"

# Add markers indicating these files need AI processing
echo "" >> "$SPECS_DIR/spec-001.md"
echo "<!-- TO BE GENERATED FROM TEMPLATE: $TEMPLATE_DIR/spec.md -->" >> "$SPECS_DIR/spec-001.md"
echo "<!-- FEATURE: $FEATURE_NAME -->" >> "$SPECS_DIR/spec-001.md"
echo "<!-- ID: $FEATURE_ID -->" >> "$SPECS_DIR/spec-001.md"

echo "" >> "$PLANS_DIR/plan-001.md"
echo "<!-- TO BE GENERATED FROM TEMPLATE: $TEMPLATE_DIR/plan.md -->" >> "$PLANS_DIR/plan-001.md"
echo "<!-- FEATURE: $FEATURE_NAME -->" >> "$PLANS_DIR/plan-001.md"
echo "<!-- ID: $FEATURE_ID -->" >> "$PLANS_DIR/plan-001.md"

echo "" >> "$TASKS_DIR/task-001.md"
echo "<!-- TO BE GENERATED FROM TEMPLATE: $TEMPLATE_DIR/task.md -->" >> "$TASKS_DIR/task-001.md"
echo "<!-- FEATURE: $FEATURE_NAME -->" >> "$TASKS_DIR/task-001.md"
echo "<!-- ID: $FEATURE_ID -->" >> "$TASKS_DIR/task-001.md"

# Update context
CONTEXT_FILE="$PROJECT_ROOT/memory/context.md"
mkdir -p "$(dirname "$CONTEXT_FILE")"

{
    echo ""
    echo "## Active Feature: $FEATURE_NAME"
    echo "- Feature ID: $FEATURE_ID"
    echo "- Branch: $BRANCH_NAME"
    echo "- Started: $(date -Iseconds)"
} >> "$CONTEXT_FILE" || error_exit "Failed to update context file"

# Create git branch if in git repo
if [ -d "$PROJECT_ROOT/.git" ]; then
    cd "$PROJECT_ROOT"
    if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
        log "Git branch '$BRANCH_NAME' already exists, checking out"
        git checkout "$BRANCH_NAME" || error_exit "Failed to checkout existing branch"
    else
        log "Creating new git branch '$BRANCH_NAME'"
        git checkout -b "$BRANCH_NAME" || error_exit "Failed to create new branch"
    fi
fi

log "Successfully initialized feature '$FEATURE_NAME' with ID $FEATURE_ID"

echo "BRANCH_NAME=$BRANCH_NAME"
echo "SPEC_DIR=$SPECS_DIR"
echo "FEATURE_ID=$FEATURE_ID"
echo "STATUS=initialized"