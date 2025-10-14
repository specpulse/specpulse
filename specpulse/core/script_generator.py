"""
Script Generator Service

Extracted from SpecPulse God Object - generates helper shell scripts.

Implements IScriptGenerator interface.
"""

from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ScriptGenerator:
    """Script generator service implementing IScriptGenerator"""

    def __init__(self, resources_dir: Path):
        self.resources_dir = resources_dir
        self.scripts_dir = resources_dir / "scripts"

    def get_setup_script(self) -> str:
        """Get feature initialization script"""
        return """#!/bin/bash
# SpecPulse Feature Initialization
FEATURE_NAME="$1"
FEATURE_NUM=$(find specs -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" | wc -l)
FEATURE_NUM=$((FEATURE_NUM + 1))
FEATURE_ID=$(printf "%03d" $FEATURE_NUM)
mkdir -p "specs/${FEATURE_ID}-${FEATURE_NAME}"
mkdir -p "plans/${FEATURE_ID}-${FEATURE_NAME}"
mkdir -p "tasks/${FEATURE_ID}-${FEATURE_NAME}"
"""

    def get_spec_script(self) -> str:
        """Get spec context script"""
        return """#!/bin/bash
# SpecPulse Spec Context
BRANCH=$(git branch --show-current)
echo "{\\"branch\\": \\"$BRANCH\\"}"
"""

    def get_plan_script(self) -> str:
        """Get plan context script"""
        return """#!/bin/bash
# SpecPulse Plan Context
BRANCH=$(git branch --show-current)
echo "{\\"branch\\": \\"$BRANCH\\"}"
"""

    def get_task_script(self) -> str:
        """Get task context script"""
        return """#!/bin/bash
# SpecPulse Task Context
BRANCH=$(git branch --show-current)
echo "{\\"branch\\": \\"$BRANCH\\"}"
"""

    def get_validate_script(self) -> str:
        """Get validation script"""
        return """#!/bin/bash
# SpecPulse Validation
grep -q "## Requirements" "$1" && echo "valid" || echo "invalid"
"""

    def get_generate_script(self) -> str:
        """Get generation script"""
        return """#!/bin/bash
# SpecPulse Generation
echo "Generate: $1"
"""


__all__ = ['ScriptGenerator']
