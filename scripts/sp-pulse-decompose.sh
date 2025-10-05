#!/bin/bash

# SpecPulse Decomposition Orchestrator
# Validates decomposition request and returns status for AI processing

SPEC_ID="$1"
ACTION="${2:-validate}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[SpecPulse Decompose]${NC} Processing spec: ${SPEC_ID:-current}"

# Find specification
if [ -z "$SPEC_ID" ]; then
    SPEC_DIR=$(ls -d specs/* 2>/dev/null | sort -r | head -1)
else
    SPEC_DIR=$(ls -d specs/${SPEC_ID}* 2>/dev/null | head -1)
fi

if [ -z "$SPEC_DIR" ] || [ ! -d "$SPEC_DIR" ]; then
    echo "ERROR: No specification found"
    echo "SUGGESTION: Run /sp-spec create first"
    exit 1
fi

# Check complexity (simple heuristic)
SPEC_FILE=$(ls "$SPEC_DIR"/spec-*.md 2>/dev/null | sort | tail -1)
if [ -f "$SPEC_FILE" ]; then
    LINE_COUNT=$(wc -l < "$SPEC_FILE")
    echo "SPEC_FILE=$SPEC_FILE"
    echo "COMPLEXITY=$LINE_COUNT lines"
    
    if [ "$LINE_COUNT" -gt 100 ]; then
        echo "RECOMMENDATION=Decomposition advised (complex spec)"
    else
        echo "RECOMMENDATION=Single service may suffice"
    fi
fi

# Check for existing decomposition
if [ -d "$SPEC_DIR/decomposition" ]; then
    echo "STATUS=Decomposition exists"
    echo "PATH=$SPEC_DIR/decomposition"
else
    echo "STATUS=Ready for decomposition"
    echo "PATH=$SPEC_DIR"
fi

# Return template paths for AI
echo "TEMPLATES_DIR=templates/decomposition"
echo "MEMORY_FILE=memory/context.md"

exit 0