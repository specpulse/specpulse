#!/usr/bin/env python3
"""
sp-spec Commands - Specification Management
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import yaml
import re

from ...utils.console import Console
from ...utils.path_validator import PathValidator, SecurityError
from ...utils.error_handler import (
    ErrorHandler, ValidationError, TemplateError
)
from ...core.template_manager import TemplateManager
from ...core.validator import Validator
from ...core.specpulse import SpecPulse


class SpSpecCommands:
    """Handler for sp-spec CLI commands"""

    def __init__(self, console: Console, project_root: Path):
        self.console = console
        self.project_root = project_root
        self.template_manager = TemplateManager(project_root)
        self.validator = Validator(project_root)
        self.specpulse = SpecPulse(project_root)
        self.error_handler = ErrorHandler()

    def create(self, description: str, feature_name: Optional[str] = None) -> bool:
        """
        Create a new specification

        Args:
            description: Specification description
            feature_name: Optional feature name/ID, auto-detects from context if not provided

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Determine current feature
            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found. Run 'specpulse sp-pulse <name>' first")
                return False

            feature_dir_name = feature_dir.name
            specs_dir = self.project_root / "specs" / feature_dir_name

            # Determine next spec number
            spec_number = self._get_next_spec_number(specs_dir)
            spec_filename = f"spec-{spec_number:03d}.md"
            spec_path = specs_dir / spec_filename

            self.console.header(f"Creating Specification: {spec_filename}", style="bright_cyan")

            # Read template
            template_content = self.specpulse.get_spec_template()

            # Prepare metadata
            timestamp = datetime.now().strftime("%Y-%m-%d")
            feature_id = feature_dir_name.split('-')[0]

            # Replace template variables
            content = template_content
            content = content.replace("{{ feature_name }}", feature_dir_name)
            content = content.replace("{{ feature_id }}", feature_id)
            content = content.replace("{{ spec_id }}", f"{spec_number:03d}")
            content = content.replace("{{ date }}", timestamp)
            content = content.replace("{{ description }}", description)

            # Add metadata HTML comments for parsing
            metadata = f"""<!-- SPECPULSE_METADATA
FEATURE_DIR: {feature_dir_name}
FEATURE_ID: {feature_id}
SPEC_ID: {spec_number:03d}
CREATED: {datetime.now().isoformat()}
STATUS: draft
-->

"""
            content = metadata + content

            # SECURITY: Validate spec file path before writing
            try:
                safe_spec_path = PathValidator.validate_file_path(self.project_root, spec_path)
            except SecurityError as e:
                raise ValidationError(f"Security violation: {str(e)}")

            # Write spec file
            safe_spec_path.write_text(content, encoding='utf-8')

            self.console.success(f"Created: {safe_spec_path.relative_to(self.project_root)}")
            self.console.info(f"\nNext steps:")
            self.console.info(f"1. Edit the specification: {spec_path.relative_to(self.project_root)}")
            self.console.info(f"2. Expand with AI (Claude/Gemini): /sp-spec expand")
            self.console.info(f"3. Validate: specpulse sp-spec validate {spec_number:03d}")

            return True

        except Exception as e:
            self.console.error(f"Failed to create specification: {str(e)}")
            return False

    def update(self, spec_id: str, changes: str, feature_name: Optional[str] = None) -> bool:
        """
        Update an existing specification

        Args:
            spec_id: Specification ID (e.g., "001")
            changes: Description of changes to make
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate spec ID format
            try:
                PathValidator.validate_spec_id(spec_id)
            except ValueError as e:
                raise ValidationError(f"Invalid spec ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            spec_path = self.project_root / "specs" / feature_dir.name / f"spec-{spec_id}.md"

            # SECURITY: Validate file path
            try:
                safe_spec_path = PathValidator.validate_file_path(self.project_root, spec_path)
            except SecurityError as e:
                raise ValidationError(f"Security violation: {str(e)}")

            spec_path = safe_spec_path

            if not spec_path.exists():
                self.console.error(f"Specification not found: spec-{spec_id}.md")
                return False

            self.console.header(f"Updating Specification: spec-{spec_id}.md", style="bright_cyan")

            # Read current content
            content = spec_path.read_text(encoding='utf-8')

            # Add update log
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_log = f"\n## Update Log\n- **{timestamp}**: {changes}\n"

            if "## Update Log" not in content:
                content += update_log
            else:
                # Append to existing log
                content = content.replace("## Update Log\n", f"## Update Log\n- **{timestamp}**: {changes}\n")

            # Update STATUS in metadata
            content = re.sub(
                r'STATUS: \w+',
                'STATUS: updated',
                content
            )

            spec_path.write_text(content, encoding='utf-8')

            self.console.success(f"Updated: {spec_path.relative_to(self.project_root)}")
            self.console.info(f"\nChanges logged: {changes}")

            return True

        except Exception as e:
            self.console.error(f"Failed to update specification: {str(e)}")
            return False

    def validate(self, spec_id: Optional[str] = None, feature_name: Optional[str] = None) -> bool:
        """
        Validate specification(s)

        Args:
            spec_id: Optional specific spec ID, validates all if not provided
            feature_name: Optional feature name/ID

        Returns:
            bool: True if validation passes, False otherwise
        """
        try:
            # SECURITY: Validate spec ID if provided
            if spec_id:
                try:
                    PathValidator.validate_spec_id(spec_id)
                except ValueError as e:
                    raise ValidationError(f"Invalid spec ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            specs_dir = self.project_root / "specs" / feature_dir.name

            if spec_id:
                # Validate specific spec
                spec_path = specs_dir / f"spec-{spec_id}.md"
                if not spec_path.exists():
                    self.console.error(f"Specification not found: spec-{spec_id}.md")
                    return False

                specs_to_validate = [spec_path]
            else:
                # Validate all specs
                specs_to_validate = list(specs_dir.glob("spec-*.md"))

            if not specs_to_validate:
                self.console.warning("No specifications found to validate")
                return False

            self.console.header("Validating Specifications", style="bright_cyan")

            all_valid = True
            for spec_path in specs_to_validate:
                self.console.info(f"\nValidating: {spec_path.name}")

                content = spec_path.read_text(encoding='utf-8')

                # Check required sections
                required_sections = [
                    "## Problem Statement",
                    "## Requirements",
                    "## User Stories",
                    "## Acceptance Criteria"
                ]

                missing_sections = []
                for section in required_sections:
                    if section not in content:
                        missing_sections.append(section)

                if missing_sections:
                    self.console.warning(f"  Missing sections:")
                    for section in missing_sections:
                        self.console.warning(f"    - {section}")
                    all_valid = False
                else:
                    self.console.success(f"  All required sections present")

                # Check for clarification markers
                clarification_count = content.count("[NEEDS CLARIFICATION")
                if clarification_count > 0:
                    self.console.warning(f"  Contains {clarification_count} clarification markers")
                    all_valid = False
                else:
                    self.console.success(f"  No clarifications needed")

            if all_valid:
                self.console.success("\n✓ All specifications valid")
                return True
            else:
                self.console.warning("\n⚠ Some specifications need attention")
                return False

        except Exception as e:
            self.console.error(f"Validation failed: {str(e)}")
            return False

    def clarify(self, spec_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Show clarification markers in a specification

        Args:
            spec_id: Specification ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate spec ID
            try:
                PathValidator.validate_spec_id(spec_id)
            except ValueError as e:
                raise ValidationError(f"Invalid spec ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            spec_path = self.project_root / "specs" / feature_dir.name / f"spec-{spec_id}.md"

            if not spec_path.exists():
                self.console.error(f"Specification not found: spec-{spec_id}.md")
                return False

            content = spec_path.read_text(encoding='utf-8')

            # Find all clarification markers
            clarifications = re.findall(r'\[NEEDS CLARIFICATION:([^\]]+)\]', content)

            if not clarifications:
                self.console.success("No clarifications needed - specification is complete!")
                return True

            self.console.header(f"Clarifications Needed: spec-{spec_id}.md", style="bright_yellow")

            for i, clarification in enumerate(clarifications, 1):
                self.console.warning(f"{i}. {clarification.strip()}")

            self.console.info(f"\nTotal: {len(clarifications)} items need clarification")
            self.console.info(f"\nTo address these, edit: {spec_path.relative_to(self.project_root)}")

            return True

        except Exception as e:
            self.console.error(f"Failed to check clarifications: {str(e)}")
            return False

    def list_specs(self, feature_name: Optional[str] = None) -> bool:
        """
        List all specifications in current feature

        Args:
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            specs_dir = self.project_root / "specs" / feature_dir.name
            specs = sorted(specs_dir.glob("spec-*.md"))

            if not specs:
                self.console.warning(f"No specifications found in {feature_dir.name}")
                return False

            self.console.header(f"Specifications in {feature_dir.name}", style="bright_cyan")

            for spec_path in specs:
                # Extract metadata
                content = spec_path.read_text(encoding='utf-8')
                status = "draft"
                created = "unknown"

                # Parse metadata
                metadata_match = re.search(r'STATUS: (\w+)', content)
                if metadata_match:
                    status = metadata_match.group(1)

                created_match = re.search(r'CREATED: ([^\n]+)', content)
                if created_match:
                    created_str = created_match.group(1).strip()
                    try:
                        created_dt = datetime.fromisoformat(created_str)
                        created = created_dt.strftime("%Y-%m-%d")
                    except:
                        created = created_str

                self.console.info(f"  • {spec_path.name} - Status: {status}, Created: {created}")

            return True

        except Exception as e:
            self.console.error(f"Failed to list specifications: {str(e)}")
            return False

    def show(self, spec_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Display specification content

        Args:
            spec_id: Specification ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate spec ID
            try:
                PathValidator.validate_spec_id(spec_id)
            except ValueError as e:
                raise ValidationError(f"Invalid spec ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            spec_path = self.project_root / "specs" / feature_dir.name / f"spec-{spec_id}.md"

            if not spec_path.exists():
                self.console.error(f"Specification not found: spec-{spec_id}.md")
                return False

            content = spec_path.read_text(encoding='utf-8')

            self.console.header(f"Specification: spec-{spec_id}.md", style="bright_cyan")
            self.console.info(content)

            return True

        except Exception as e:
            self.console.error(f"Failed to show specification: {str(e)}")
            return False

    def progress(self, spec_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Show specification completion progress

        Args:
            spec_id: Specification ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate spec ID
            try:
                PathValidator.validate_spec_id(spec_id)
            except ValueError as e:
                raise ValidationError(f"Invalid spec ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            spec_path = self.project_root / "specs" / feature_dir.name / f"spec-{spec_id}.md"

            if not spec_path.exists():
                self.console.error(f"Specification not found: spec-{spec_id}.md")
                return False

            content = spec_path.read_text(encoding='utf-8')

            self.console.header(f"Progress: spec-{spec_id}.md", style="bright_cyan")

            # Check required sections
            required_sections = {
                "Problem Statement": "## Problem Statement" in content,
                "Requirements": "## Requirements" in content,
                "User Stories": "## User Stories" in content,
                "Acceptance Criteria": "## Acceptance Criteria" in content,
                "Technical Constraints": "## Technical Constraints" in content,
                "Dependencies": "## Dependencies" in content
            }

            completed = sum(required_sections.values())
            total = len(required_sections)
            percentage = (completed / total) * 100

            # Display progress
            for section, is_complete in required_sections.items():
                if is_complete:
                    self.console.success(f"  {section}")
                else:
                    self.console.error(f"  {section}")

            self.console.info(f"\nCompletion: {completed}/{total} ({percentage:.0f}%)")

            # Check clarifications
            clarification_count = content.count("[NEEDS CLARIFICATION")
            if clarification_count > 0:
                self.console.warning(f"Clarifications needed: {clarification_count}")

            return True

        except Exception as e:
            self.console.error(f"Failed to show progress: {str(e)}")
            return False

    # Helper methods

    def _get_current_feature(self, feature_name: Optional[str] = None) -> Optional[Path]:
        """Get current feature directory from context or parameter"""

        if feature_name:
            # Find by name or ID
            return self._find_feature_directory(feature_name)

        # Try to get from context
        context_file = self.project_root / "memory" / "context.md"

        if context_file.exists():
            content = context_file.read_text(encoding='utf-8')

            # Parse active feature
            match = re.search(r'Feature ID[:\s]+(\d{3})', content)
            if match:
                feature_id = match.group(1)
                return self._find_feature_directory(feature_id)

            # Try directory name
            match = re.search(r'Directory[:\s]+([^\n]+)', content)
            if match:
                feature_dir_name = match.group(1).strip()
                specs_dir = self.project_root / "specs" / feature_dir_name
                if specs_dir.exists():
                    return specs_dir.parent / feature_dir_name

        # Fall back to most recent feature
        specs_dir = self.project_root / "specs"
        if specs_dir.exists():
            features = sorted([d for d in specs_dir.iterdir() if d.is_dir() and re.match(r'^\d{3}-', d.name)])
            if features:
                return features[-1]

        return None

    def _find_feature_directory(self, identifier: str) -> Optional[Path]:
        """Find feature directory by ID or name"""
        specs_dir = self.project_root / "specs"

        if not specs_dir.exists():
            return None

        # Try exact match
        for item in specs_dir.iterdir():
            if item.is_dir():
                if item.name == identifier or item.name.startswith(f"{identifier}-"):
                    return item

        # Try partial match
        identifier_lower = identifier.lower()
        for item in specs_dir.iterdir():
            if item.is_dir() and identifier_lower in item.name.lower():
                return item

        return None

    def _get_next_spec_number(self, specs_dir: Path) -> int:
        """Get next available specification number"""
        if not specs_dir.exists():
            return 1

        existing_specs = list(specs_dir.glob("spec-*.md"))

        if not existing_specs:
            return 1

        max_number = 0
        for spec_path in existing_specs:
            match = re.match(r'spec-(\d{3})\.md', spec_path.name)
            if match:
                spec_number = int(match.group(1))
                max_number = max(max_number, spec_number)

        return max_number + 1
