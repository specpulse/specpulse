"""
Specification Validator

This module handles validation of specification files,
including structure, content, and SDD compliance checks.
"""

from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import yaml
import re

from ..validation_rules import (
    validation_rules_registry, ValidationResult, ValidationSeverity
)
from ...utils.backup_manager import BackupManager


@dataclass
class SpecValidationResult:
    """Result of specification validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metadata: Dict


class SpecValidator:
    """Validator for specification files"""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.backup_manager = BackupManager(self.project_root)
        self.results = []

    def validate_spec(self, spec_path: Path, fix: bool = False, verbose: bool = False) -> SpecValidationResult:
        """
        Validate a single specification file

        Args:
            spec_path: Path to specification file
            fix: Whether to auto-fix issues
            verbose: Verbose output

        Returns:
            SpecValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        metadata = {}

        if not spec_path.exists():
            errors.append(f"Specification file not found: {spec_path}")
            return SpecValidationResult(
                valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                metadata=metadata
            )

        # Read spec content
        content = spec_path.read_text(encoding='utf-8')

        # Validate using validation rules
        validation_result = validation_rules_registry.validate('spec', content)

        # Convert to SpecValidationResult
        for issue in validation_result.issues:
            if issue.severity in [ValidationSeverity.CRITICAL, ValidationSeverity.ERROR]:
                errors.append(issue.message)
            elif issue.severity == ValidationSeverity.WARNING:
                warnings.append(issue.message)
            else:
                suggestions.append(issue.message)

        # Extract metadata
        metadata = self._extract_spec_metadata(content)

        # Check required sections
        required_sections = [
            "## Specification",
            "## Functional Requirements",
            "## Acceptance Criteria"
        ]

        for section in required_sections:
            if section not in content:
                warnings.append(f"Missing required section: {section}")
                suggestions.append(f"Add '{section}' section to specification")

        # Auto-fix if requested
        if fix and (errors or warnings):
            self._auto_fix_spec(spec_path, content, errors, warnings)

        is_valid = len(errors) == 0
        return SpecValidationResult(
            valid=is_valid,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata=metadata
        )

    def validate_all_specs(self, project_path: Path, fix: bool = False, verbose: bool = False) -> List[SpecValidationResult]:
        """
        Validate all specification files in project

        Args:
            project_path: Path to project root
            fix: Whether to auto-fix issues
            verbose: Verbose output

        Returns:
            List of SpecValidationResult for all specs
        """
        results = []
        specs_dir = project_path / "specs"

        if not specs_dir.exists():
            return results

        # Validate each spec directory
        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_path = spec_dir / "spec.md"
                if spec_path.exists():
                    result = self.validate_spec(spec_path, fix, verbose)
                    results.append(result)

        return results

    def _extract_spec_metadata(self, content: str) -> Dict:
        """Extract metadata from specification"""
        metadata = {}

        # Extract HTML comment metadata
        meta_pattern = r'<!--\s*(\w+):\s*([^>]*)\s*-->'
        for match in re.finditer(meta_pattern, content, re.IGNORECASE):
            key, value = match.groups()
            metadata[key.lower()] = value.strip()

        return metadata

    def _auto_fix_spec(self, spec_path: Path, content: str, errors: List[str], warnings: List[str]) -> None:
        """
        Attempt to auto-fix specification issues

        Args:
            spec_path: Path to specification file
            content: Current content
            errors: List of errors to fix
            warnings: List of warnings to fix
        """
        # Backup before fixing
        self.backup_manager.create_backup(spec_path)

        modified_content = content

        # Fix missing sections
        if any("Missing required section" in w for w in warnings):
            # Add missing sections at the end
            if "## Functional Requirements" not in content:
                modified_content += "\n\n## Functional Requirements\n\n[TODO: Add functional requirements]\n"

            if "## Acceptance Criteria" not in content:
                modified_content += "\n\n## Acceptance Criteria\n\n- [ ] [TODO: Add acceptance criteria]\n"

        # Fix missing metadata
        if any("FEATURE_ID" in str(errors) or "FEATURE_ID" in str(warnings) for _ in [1]):
            if "<!-- FEATURE_ID:" not in content:
                # Extract feature ID from path
                feature_id = spec_path.parent.name.split('-')[0] if '-' in spec_path.parent.name else "001"
                modified_content += f"\n<!-- FEATURE_ID: {feature_id} -->\n"

        # Write fixed content
        if modified_content != content:
            spec_path.write_text(modified_content, encoding='utf-8')

    def check_spec_completeness(self, spec_path: Path) -> Dict:
        """
        Check completeness of specification

        Returns:
            Dict with completeness metrics
        """
        content = spec_path.read_text(encoding='utf-8')

        completeness = {
            'has_overview': '## Overview' in content or '## Specification' in content,
            'has_requirements': '## Functional Requirements' in content or '## Requirements' in content,
            'has_acceptance': '## Acceptance Criteria' in content or '## Acceptance' in content,
            'has_metadata': '<!-- FEATURE_ID:' in content,
            'has_technical': '## Technical' in content or '## Architecture' in content,
            'total_sections': len(re.findall(r'^##\s+', content, re.MULTILINE)),
            'total_tasks': len(re.findall(r'- \[[ x]\]', content)),
            'completion_percentage': 0
        }

        # Calculate completion percentage
        required_items = 3  # overview, requirements, acceptance
        completed_items = sum([
            completeness['has_overview'],
            completeness['has_requirements'],
            completeness['has_acceptance']
        ])
        completeness['completion_percentage'] = (completed_items / required_items) * 100

        return completeness
