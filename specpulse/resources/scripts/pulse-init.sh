#!/bin/bash
# SpecPulse Feature Initialization Script

set -e

# Get feature name from argument
FEATURE_NAME="$1"
if [ -z "$FEATURE_NAME" ]; then
    echo "Error: Feature name required"
    exit 1
fi

# Clean feature name (replace spaces with hyphens, lowercase)
CLEAN_NAME=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr '_' '-')

# Get next feature number
if [ -d "specs" ]; then
    FEATURE_NUM=$(find specs -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" | wc -l)
    FEATURE_NUM=$((FEATURE_NUM + 1))
else
    FEATURE_NUM=1
fi

# Format with leading zeros
FEATURE_ID=$(printf "%03d" $FEATURE_NUM)
BRANCH_NAME="${FEATURE_ID}-${CLEAN_NAME}"

# Create directories
mkdir -p "specs/${BRANCH_NAME}"
mkdir -p "plans/${BRANCH_NAME}"
mkdir -p "tasks/${BRANCH_NAME}"

# Create feature branch if git is available
if command -v git &> /dev/null && [ -d ".git" ]; then
    git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"
fi

# Output JSON result
echo "{"
echo "  \"branch_name\": \"$BRANCH_NAME\","
echo "  \"feature_id\": \"$FEATURE_ID\","
echo "  \"spec_dir\": \"specs/$BRANCH_NAME\","
echo "  \"plan_dir\": \"plans/$BRANCH_NAME\","
echo "  \"task_dir\": \"tasks/$BRANCH_NAME\""
echo "}"
