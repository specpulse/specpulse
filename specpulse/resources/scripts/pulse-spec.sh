#!/bin/bash
# SpecPulse Specification Generator Script

set -e

# Get description from argument
DESCRIPTION="$1"
if [ -z "$DESCRIPTION" ]; then
    echo "Error: Description required"
    exit 1
fi

# Find current feature branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
FEATURE_DIR=""

# Look for feature directory
if [[ "$BRANCH" =~ ^[0-9]{3}- ]]; then
    FEATURE_DIR="specs/$BRANCH"
    if [ ! -d "$FEATURE_DIR" ]; then
        echo "Error: Feature directory not found: $FEATURE_DIR"
        exit 1
    fi
else
    echo "Error: Not on a feature branch"
    exit 1
fi

# Create specification file
SPEC_FILE="$FEATURE_DIR/specification.md"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Output for AI processing
echo "{"
echo "  \"action\": \"create_specification\","
echo "  \"description\": \"$DESCRIPTION\","
echo "  \"spec_file\": \"$SPEC_FILE\","
echo "  \"template\": \"templates/spec.md\","
echo "  \"timestamp\": \"$TIMESTAMP\""
echo "}"