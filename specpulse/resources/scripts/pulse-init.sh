#!/bin/bash
# Initialize a new feature with SpecPulse

FEATURE_NAME="${1:-feature}"

# Get next feature ID
FEATURE_ID=$(printf "%03d" $(ls -d specs/[0-9]* 2>/dev/null | wc -l | xargs expr 1 +))

# Create branch name
BRANCH_NAME="${FEATURE_ID}-${FEATURE_NAME}"

# Create directories
mkdir -p "specs/${BRANCH_NAME}"
mkdir -p "plans/${BRANCH_NAME}"
mkdir -p "tasks/${BRANCH_NAME}"

# Create initial files from templates
cp templates/spec.md "specs/${BRANCH_NAME}/spec.md"
cp templates/plan.md "plans/${BRANCH_NAME}/plan.md"
cp templates/task.md "tasks/${BRANCH_NAME}/tasks.md"

# Update context
echo "" >> memory/context.md
echo "## Active Feature: ${FEATURE_NAME}" >> memory/context.md
echo "- Feature ID: ${FEATURE_ID}" >> memory/context.md
echo "- Branch: ${BRANCH_NAME}" >> memory/context.md
echo "- Started: $(date -Iseconds)" >> memory/context.md

# Create git branch if in git repo
if [ -d .git ]; then
    git checkout -b "${BRANCH_NAME}" 2>/dev/null || git checkout "${BRANCH_NAME}"
fi

echo "BRANCH_NAME=${BRANCH_NAME}"
echo "SPEC_DIR=specs/${BRANCH_NAME}"
echo "FEATURE_ID=${FEATURE_ID}"
echo "STATUS=initialized"