#!/bin/bash
# SpecPulse Plan Generator Script

set -e

# Find current feature branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Look for specification
if [[ "$BRANCH" =~ ^[0-9]{3}- ]]; then
    SPEC_FILE="specs/$BRANCH/specification.md"
    PLAN_FILE="plans/$BRANCH/implementation.md"
    
    if [ ! -f "$SPEC_FILE" ]; then
        echo "Error: Specification not found: $SPEC_FILE"
        exit 1
    fi
    
    # Create plan directory if needed
    mkdir -p "plans/$BRANCH"
    
    # Output for AI processing
    echo "{"
    echo "  \"action\": \"generate_plan\","
    echo "  \"spec_file\": \"$SPEC_FILE\","
    echo "  \"plan_file\": \"$PLAN_FILE\","
    echo "  \"template\": \"templates/plan.md\""
    echo "}"
else
    echo "Error: Not on a feature branch"
    exit 1
fi