#!/bin/bash
# SpecPulse Task Breakdown Script

set -e

# Find current feature branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Look for plan
if [[ "$BRANCH" =~ ^[0-9]{3}- ]]; then
    PLAN_FILE="plans/$BRANCH/implementation.md"
    TASK_FILE="tasks/$BRANCH/tasks.md"
    
    if [ ! -f "$PLAN_FILE" ]; then
        echo "Error: Plan not found: $PLAN_FILE"
        exit 1
    fi
    
    # Create task directory if needed
    mkdir -p "tasks/$BRANCH"
    
    # Output for AI processing
    echo "{"
    echo "  \"action\": \"breakdown_tasks\","
    echo "  \"plan_file\": \"$PLAN_FILE\","
    echo "  \"task_file\": \"$TASK_FILE\","
    echo "  \"template\": \"templates/task.md\""
    echo "}"
else
    echo "Error: Not on a feature branch"
    exit 1
fi