#!/bin/bash
# Initialize a new feature with SpecPulse

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/script_utils.sh"

# Configuration
SCRIPT_NAME="$(basename "$0")"
# Script is in project-root/scripts/, so parent dir is project root
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Initialize script environment with error handling and rollback support
init_script_env "$SCRIPT_NAME" "$SCRIPT_DIR"

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        print_usage "$SCRIPT_NAME" "<feature-name> [feature-id]"
        exit 0
        ;;
    --version|-v)
        print_version "$SCRIPT_NAME" "1.0.0"
        exit 0
        ;;
    --verbose)
        export VERBOSE=true
        shift
        ;;
esac

# Validate arguments
if [ $# -eq 0 ]; then
    print_usage "$SCRIPT_NAME" "<feature-name> [feature-id]"
    exit 1
fi

FEATURE_NAME="$1"
CUSTOM_ID="${2:-}"

# Sanitize feature name using utility function
BRANCH_SAFE_NAME=$(sanitize_feature_name "$FEATURE_NAME")

# Get feature ID using utility function
FEATURE_ID=$(generate_feature_id "$PROJECT_ROOT" "$CUSTOM_ID")

BRANCH_NAME="${FEATURE_ID}-${BRANCH_SAFE_NAME}"

# Create directories
SPECS_DIR="$PROJECT_ROOT/specs/${BRANCH_NAME}"
PLANS_DIR="$PROJECT_ROOT/plans/${BRANCH_NAME}"
TASKS_DIR="$PROJECT_ROOT/tasks/${BRANCH_NAME}"

log_info "Creating feature directories for '$FEATURE_NAME'"

# Validate project structure first
validate_project_structure "$PROJECT_ROOT"

# Create directories with progress tracking
show_progress 1 4 "Creating directories"
mkdir -p "$SPECS_DIR"
show_progress 2 4 "Creating directories"
mkdir -p "$PLANS_DIR"
show_progress 3 4 "Creating directories"
mkdir -p "$TASKS_DIR"
show_progress 4 4 "Creating directories"

# Validate templates exist but don't copy them directly
TEMPLATE_DIR="$PROJECT_ROOT/templates"

# Validate all required templates exist
validate_templates "$TEMPLATE_DIR"

# Create marker files that indicate AI should use templates to generate content
# These are placeholder files that will be replaced by AI-generated content
echo "# Specification for $FEATURE_NAME" > "$SPECS_DIR/spec-001.md"
echo "# Implementation Plan for $FEATURE_NAME" > "$PLANS_DIR/plan-001.md"
echo "# Task Breakdown for $FEATURE_NAME" > "$TASKS_DIR/task-001.md"

# Add markers indicating these files need AI processing
echo "" >> "$SPECS_DIR/spec-001.md"
echo "<!-- INSTRUCTION: Generate specification content using template: $TEMPLATE_DIR/spec.md -->" >> "$SPECS_DIR/spec-001.md"
echo "<!-- FEATURE_DIR: $BRANCH_NAME -->" >> "$SPECS_DIR/spec-001.md"
echo "<!-- FEATURE_ID: $FEATURE_ID -->" >> "$SPECS_DIR/spec-001.md"

echo "" >> "$PLANS_DIR/plan-001.md"
echo "<!-- INSTRUCTION: Generate plan using template: $TEMPLATE_DIR/plan.md -->" >> "$PLANS_DIR/plan-001.md"
echo "<!-- SPEC_FILE: $SPECS_DIR/spec-001.md -->" >> "$PLANS_DIR/plan-001.md"
echo "<!-- FEATURE_DIR: $BRANCH_NAME -->" >> "$PLANS_DIR/plan-001.md"
echo "<!-- FEATURE_ID: $FEATURE_ID -->" >> "$PLANS_DIR/plan-001.md"

echo "" >> "$TASKS_DIR/task-001.md"
echo "<!-- INSTRUCTION: Generate tasks using template: $TEMPLATE_DIR/task.md -->" >> "$TASKS_DIR/task-001.md"
echo "<!-- SPEC_FILE: $SPECS_DIR/spec-001.md -->" >> "$TASKS_DIR/task-001.md"
echo "<!-- PLAN_FILE: $PLANS_DIR/plan-001.md -->" >> "$TASKS_DIR/task-001.md"
echo "<!-- FEATURE_DIR: $BRANCH_NAME -->" >> "$TASKS_DIR/task-001.md"
echo "<!-- FEATURE_ID: $FEATURE_ID -->" >> "$TASKS_DIR/task-001.md"

# Update context with backup
CONTEXT_FILE="$PROJECT_ROOT/memory/context.md"
mkdir -p "$(dirname "$CONTEXT_FILE")"

# Backup context file before modification
backup_file "$CONTEXT_FILE"

{
    echo ""
    echo "## Active Feature: $FEATURE_NAME"
    echo "- Feature ID: $FEATURE_ID"
    echo "- Branch: $BRANCH_NAME"
    echo "- Started: $(date -Iseconds)"
} >> "$CONTEXT_FILE"

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

log_success "Successfully initialized feature '$FEATURE_NAME' with ID $FEATURE_ID"

# Output results for consumption by other scripts
echo "BRANCH_NAME=$BRANCH_NAME"
echo "SPEC_DIR=$SPECS_DIR"
echo "FEATURE_ID=$FEATURE_ID"
echo "STATUS=initialized"
echo "BACKUP_DIR=$BACKUP_DIR"