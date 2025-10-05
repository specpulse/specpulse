#!/bin/bash
# Common utility functions for SpecPulse scripts
# This file provides standardized error handling and logging

# Configuration
SCRIPT_UTILS_VERSION="1.0.0"

# Colors for output
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    BOLD=''
    NC=''
fi

# Global variables
BACKUP_DIR=""
ROLLBACK_STACK=()

# Initialize script environment
init_script_env() {
    local script_name="$1"
    local script_dir="$2"

    # Create backup directory for rollback
    BACKUP_DIR="/tmp/specpulse_backup_$(date +%s)_$$"
    mkdir -p "$BACKUP_DIR"

    # Set strict mode
    set -euo pipefail

    # Trap errors and cleanup
    trap 'handle_error $? $LINENO' ERR
    trap 'cleanup_on_exit' EXIT
}

# Cleanup function called on exit
cleanup_on_exit() {
    local exit_code=$?
    if [ $exit_code -ne 0 ] && [ -n "$BACKUP_DIR" ] && [ -d "$BACKUP_DIR" ]; then
        echo -e "${YELLOW}Warning: Script exited with error $exit_code${NC}"
        echo -e "${YELLOW}Backup directory preserved at: $BACKUP_DIR${NC}"
    else
        rm -rf "$BACKUP_DIR" 2>/dev/null || true
    fi
}

# Enhanced error handler
handle_error() {
    local exit_code=$1
    local line_number=$2

    echo -e "${RED}✖ ERROR: Script failed with exit code $exit_code at line $line_number${NC}" >&2

    # Show context if available
    if [ -n "${BASH_SOURCE[2]-}" ]; then
        echo -e "${RED}  In: ${BASH_SOURCE[2]}${NC}" >&2
    fi

    # Suggest recovery actions
    echo -e "${YELLOW}💡 Recovery suggestions:${NC}" >&2
    echo -e "${YELLOW}   1. Check file permissions and disk space${NC}" >&2
    echo -e "${YELLOW}   2. Verify all required directories exist${NC}" >&2
    echo -e "${YELLOW}   3. Run with --verbose for more details${NC}" >&2

    if [ ${#ROLLBACK_STACK[@]} -gt 0 ]; then
        echo -e "${YELLOW}   4. Run rollback to undo changes: echo 'rollback' | $0${NC}" >&2
    fi

    exit $exit_code
}

# Logging functions with levels
log_debug() {
    if [ "${VERBOSE:-false}" = "true" ]; then
        echo -e "${CYAN}[DEBUG]${NC} $1" >&2
    fi
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Progress indicator
show_progress() {
    local current=$1
    local total=$2
    local desc="${3:-Processing}"

    local percentage=$((current * 100 / total))
    local bar_length=30
    local filled_length=$((percentage * bar_length / 100))

    printf "\r${CYAN}%s${NC} [" "$desc"
    printf "%*s" $filled_length | tr ' ' '='
    printf "%*s" $((bar_length - filled_length)) | tr ' ' '-'
    printf "] %d%% (%d/%d)" $percentage $current $total

    if [ $current -eq $total ]; then
        echo
    fi
}

# File backup for rollback
backup_file() {
    local file_path="$1"

    if [ -f "$file_path" ]; then
        local backup_path="$BACKUP_DIR/$(echo "$file_path" | sed 's/\//_/g')"
        cp "$file_path" "$backup_path"
        ROLLBACK_STACK+=("$file_path:$backup_path")
        log_debug "Backed up: $file_path"
    fi
}

# Rollback function
rollback_changes() {
    log_info "Rolling back changes..."

    local rollback_count=0
    for item in "${ROLLBACK_STACK[@]}"; do
        IFS=':' read -r original_path backup_path <<< "$item"

        if [ -f "$backup_path" ]; then
            cp "$backup_path" "$original_path"
            log_info "Restored: $original_path"
            ((rollback_count++))
        fi
    done

    log_success "Rollback completed. Restored $rollback_count files."
}

# Validate project structure
validate_project_structure() {
    local project_root="$1"

    local required_dirs=("specs" "plans" "tasks" "memory" "templates")
    local missing_dirs=()

    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$project_root/$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done

    if [ ${#missing_dirs[@]} -gt 0 ]; then
        log_error "Missing required directories: ${missing_dirs[*]}"
        log_error "Run 'specpulse init' to initialize project structure"
        return 1
    fi

    return 0
}

# Validate templates exist
validate_templates() {
    local template_dir="$1"
    local required_templates=("spec.md" "plan.md" "task.md")

    for template in "${required_templates[@]}"; do
        if [ ! -f "$template_dir/$template" ]; then
            log_error "Template not found: $template_dir/$template"
            log_error "Run 'specpulse init' to initialize templates"
            return 1
        fi
    done

    return 0
}

# Sanitize input
sanitize_feature_name() {
    local feature_name="$1"

    # Remove special characters, convert to lowercase, replace spaces with hyphens
    local sanitized=$(echo "$feature_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')

    if [ -z "$sanitized" ]; then
        log_error "Invalid feature name: '$feature_name'"
        log_error "Feature names must contain at least one alphanumeric character"
        return 1
    fi

    echo "$sanitized"
}

# Generate unique feature ID
generate_feature_id() {
    local project_root="$1"
    local custom_id="${2:-}"

    if [ -n "$custom_id" ]; then
        printf "%03d" "$custom_id"
    else
        local specs_dir="$project_root/specs"
        if [ -d "$specs_dir" ]; then
            local count=$(find "$specs_dir" -maxdepth 1 -type d -name '[0-9]*' 2>/dev/null | wc -l | awk '{print $1}')
            printf "%03d" $((count + 1))
        else
            printf "001"
        fi
    fi
}

# Check dependencies
check_dependencies() {
    local deps=("${@}")
    local missing_deps=()

    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            missing_deps+=("$dep")
        fi
    done

    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install missing dependencies and try again"
        return 1
    fi

    return 0
}

# Get next file number in sequence
get_next_file_number() {
    local directory="$1"
    local prefix="$2"

    if [ -d "$directory" ]; then
        local highest=$(find "$directory" -name "${prefix}-*.md" -exec basename {} .md \; 2>/dev/null | sed "s/${prefix}-//" | sort -n | tail -1)
        if [ -n "$highest" ] && [[ "$highest" =~ ^[0-9]+$ ]]; then
            echo $((highest + 1))
        else
            echo "1"
        fi
    else
        echo "1"
    fi
}

# Print usage help
print_usage() {
    local script_name="$1"
    local usage_text="$2"

    echo -e "${BOLD}Usage:${NC}" >&2
    echo -e "  $script_name $usage_text" >&2
    echo >&2
    echo -e "${BOLD}Common options:${NC}" >&2
    echo -e "  ${CYAN}--verbose${NC}     Show detailed output" >&2
    echo -e "  ${CYAN}--help${NC}        Show this help message" >&2
    echo -e "  ${CYAN}--version${NC}     Show version information" >&2
}

# Print version info
print_version() {
    local script_name="$1"
    local script_version="${2:-unknown}"

    echo -e "${BOLD}$script_name${NC} version $script_version" >&2
    echo "SpecPulse Script Utils version $SCRIPT_UTILS_VERSION" >&2
}

# Export functions for use in other scripts
export -f init_script_env cleanup_on_exit handle_error
export -f log_debug log_info log_success log_warning log_error
export -f show_progress backup_file rollback_changes
export -f validate_project_structure validate_templates
export -f sanitize_feature_name generate_feature_id
export -f check_dependencies get_next_file_number
export -f print_usage print_version

# Export variables
export BACKUP_DIR ROLLBACK_STACK
export SCRIPT_UTILS_VERSION