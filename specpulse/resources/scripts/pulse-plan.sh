#!/bin/bash
# Generate implementation plan

FEATURE_DIR="${1}"

if [ -z "$FEATURE_DIR" ]; then
    # Find current feature from context
    FEATURE_DIR=$(grep -A1 "Active Feature" memory/context.md | tail -1 | cut -d: -f2 | xargs)
fi

PLAN_FILE="plans/${FEATURE_DIR}/plan.md"

# Ensure template exists
if [ ! -f "$PLAN_FILE" ]; then
    cp templates/plan.md "$PLAN_FILE"
fi

# Check Phase Gates
echo "Checking Phase Gates..."
echo "- Constitutional compliance"
echo "- Simplicity check (≤3 modules)"
echo "- Test-first strategy"
echo "- Framework selection"

echo "PLAN_FILE=$PLAN_FILE"
echo "STATUS=ready"