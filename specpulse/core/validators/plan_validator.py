"""
Plan Validator

This module handles validation of implementation plan files,
including structure, phases, dependencies, and resource allocation.
"""

from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import re

from ..validation_rules import (
    validation_rules_registry, ValidationResult, ValidationSeverity
)
from ...utils.backup_manager import BackupManager


@dataclass
class PlanValidationResult:
    """Result of plan validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metadata: Dict
    phases: List[Dict]
    dependencies: List[str]


class PlanValidator:
    """Validator for implementation plan files"""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.backup_manager = BackupManager(self.project_root)
        self.results = []

    def validate_plan(self, plan_path: Path, fix: bool = False, verbose: bool = False) -> PlanValidationResult:
        """
        Validate a single implementation plan file

        Args:
            plan_path: Path to plan file
            fix: Whether to auto-fix issues
            verbose: Verbose output

        Returns:
            PlanValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        metadata = {}
        phases = []
        dependencies = []

        if not plan_path.exists():
            errors.append(f"Plan file not found: {plan_path}")
            return PlanValidationResult(
                valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                metadata=metadata,
                phases=phases,
                dependencies=dependencies
            )

        # Read plan content
        content = plan_path.read_text(encoding='utf-8')

        # Validate using validation rules
        validation_result = validation_rules_registry.validate('plan', content)

        # Convert to PlanValidationResult
        for issue in validation_result.issues:
            if issue.severity in [ValidationSeverity.CRITICAL, ValidationSeverity.ERROR]:
                errors.append(issue.message)
            elif issue.severity == ValidationSeverity.WARNING:
                warnings.append(issue.message)
            else:
                suggestions.append(issue.message)

        # Extract metadata
        metadata = self._extract_plan_metadata(content)

        # Extract phases
        phases = self._extract_phases(content)

        # Extract dependencies
        dependencies = self._extract_dependencies(content)

        # Check required sections
        required_sections = [
            "## Architecture Overview",
            "## Technology Stack",
            "## Implementation Phases"
        ]

        for section in required_sections:
            if section not in content:
                warnings.append(f"Missing required section: {section}")
                suggestions.append(f"Add '{section}' section to plan")

        # Validate phases
        if len(phases) == 0:
            warnings.append("No implementation phases found")
            suggestions.append("Add implementation phases with tasks and timelines")

        # Auto-fix if requested
        if fix and (errors or warnings):
            self._auto_fix_plan(plan_path, content, errors, warnings)

        is_valid = len(errors) == 0
        return PlanValidationResult(
            valid=is_valid,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata=metadata,
            phases=phases,
            dependencies=dependencies
        )

    def validate_all_plans(self, project_path: Path, fix: bool = False, verbose: bool = False) -> List[PlanValidationResult]:
        """
        Validate all plan files in project

        Args:
            project_path: Path to project root
            fix: Whether to auto-fix issues
            verbose: Verbose output

        Returns:
            List of PlanValidationResult for all plans
        """
        results = []
        plans_dir = project_path / "plans"

        if not plans_dir.exists():
            return results

        # Validate each plan directory
        for plan_dir in plans_dir.iterdir():
            if plan_dir.is_dir():
                plan_path = plan_dir / "plan.md"
                if plan_path.exists():
                    result = self.validate_plan(plan_path, fix, verbose)
                    results.append(result)

        return results

    def _extract_plan_metadata(self, content: str) -> Dict:
        """Extract metadata from plan"""
        metadata = {}

        # Extract HTML comment metadata
        meta_pattern = r'<!--\s*(\w+):\s*([^>]*)\s*-->'
        for match in re.finditer(meta_pattern, content, re.IGNORECASE):
            key, value = match.groups()
            metadata[key.lower()] = value.strip()

        return metadata

    def _extract_phases(self, content: str) -> List[Dict]:
        """Extract implementation phases from plan"""
        phases = []

        # Find phase sections (typically ### Phase N: or ## Phase N:)
        phase_pattern = r'###?\s+Phase\s+(\d+):\s*([^\n]+)'
        for match in re.finditer(phase_pattern, content, re.IGNORECASE):
            phase_num, phase_name = match.groups()
            phases.append({
                'number': int(phase_num),
                'name': phase_name.strip(),
                'position': match.start()
            })

        return phases

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from plan"""
        dependencies = []

        # Find dependency mentions
        dep_patterns = [
            r'Depends on:\s*([^\n]+)',
            r'Dependencies:\s*([^\n]+)',
            r'Requires:\s*([^\n]+)'
        ]

        for pattern in dep_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dependencies.extend(matches)

        return dependencies

    def _auto_fix_plan(self, plan_path: Path, content: str, errors: List[str], warnings: List[str]) -> None:
        """
        Attempt to auto-fix plan issues

        Args:
            plan_path: Path to plan file
            content: Current content
            errors: List of errors to fix
            warnings: List of warnings to fix
        """
        # Backup before fixing
        self.backup_manager.create_backup(plan_path)

        modified_content = content

        # Fix missing sections
        if any("Missing required section" in w for w in warnings):
            if "## Architecture Overview" not in content:
                modified_content += "\n\n## Architecture Overview\n\n[TODO: Add architecture overview]\n"

            if "## Technology Stack" not in content:
                modified_content += "\n\n## Technology Stack\n\n[TODO: Add technology stack]\n"

            if "## Implementation Phases" not in content:
                modified_content += "\n\n## Implementation Phases\n\n### Phase 1: [TODO]\n\n[TODO: Add phase details]\n"

        # Write fixed content
        if modified_content != content:
            plan_path.write_text(modified_content, encoding='utf-8')

    def check_plan_completeness(self, plan_path: Path) -> Dict:
        """
        Check completeness of implementation plan

        Returns:
            Dict with completeness metrics
        """
        content = plan_path.read_text(encoding='utf-8')

        completeness = {
            'has_architecture': '## Architecture' in content,
            'has_tech_stack': '## Technology' in content or '## Stack' in content,
            'has_phases': '## Implementation Phases' in content or '### Phase' in content,
            'has_dependencies': 'Dependencies:' in content or 'Depends on:' in content,
            'has_risks': '## Risks' in content or '## Risk' in content,
            'total_phases': len(re.findall(r'###?\s+Phase\s+\d+', content)),
            'total_tasks': len(re.findall(r'- \[[ x]\]', content)),
            'completion_percentage': 0
        }

        # Calculate completion percentage
        required_items = 3  # architecture, tech stack, phases
        completed_items = sum([
            completeness['has_architecture'],
            completeness['has_tech_stack'],
            completeness['has_phases']
        ])
        completeness['completion_percentage'] = (completed_items / required_items) * 100

        return completeness
