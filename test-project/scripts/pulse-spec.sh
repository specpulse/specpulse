#!/bin/bash
# Generate or update specification

FEATURE_DIR="${1}"
SPEC_CONTENT="${2}"

if [ -z "$FEATURE_DIR" ]; then
    # Find current feature from context
    FEATURE_DIR=$(grep -A1 "Active Feature" memory/context.md | tail -1 | cut -d: -f2 | xargs)
fi

SPEC_FILE="specs/${FEATURE_DIR}/spec.md"

if [ -n "$SPEC_CONTENT" ]; then
    # Update specification with content
    echo "$SPEC_CONTENT" > "$SPEC_FILE"
else
    # Ensure template exists
    if [ ! -f "$SPEC_FILE" ]; then
        cp templates/spec.md "$SPEC_FILE"
    fi
fi

# Validate specification
echo "Validating specification..."
grep -q "NEEDS CLARIFICATION" "$SPEC_FILE" && echo "WARNING: Specification has clarifications needed"

echo "SPEC_FILE=$SPEC_FILE"
echo "STATUS=updated"