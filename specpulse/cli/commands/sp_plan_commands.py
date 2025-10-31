#!/usr/bin/env python3
"""
sp-plan Commands - Implementation Plan Management
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


class SpPlanCommands:
    """Handler for sp-plan CLI commands"""

    def __init__(self, console: Console, project_root: Path):
        self.console = console
        self.project_root = project_root
        self.template_manager = TemplateManager(project_root)
        self.validator = Validator(project_root)
        self.specpulse = SpecPulse(project_root)
        self.error_handler = ErrorHandler()

    def create(self, description: str, feature_name: Optional[str] = None) -> bool:
        """
        Create a new implementation plan

        Args:
            description: Plan description
            feature_name: Optional feature name/ID, auto-detects from context if not provided

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Determine current feature
            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found. Run 'specpulse sp-pulse init <name>' first")
                return False

            feature_dir_name = feature_dir.name
            plans_dir = self.project_root / "plans" / feature_dir_name

            # Determine next plan number
            plan_number = self._get_next_plan_number(plans_dir)
            plan_filename = f"plan-{plan_number:03d}.md"
            plan_path = plans_dir / plan_filename

            self.console.header(f"Creating Implementation Plan: {plan_filename}", style="bright_cyan")

            # Check if spec exists
            specs_dir = self.project_root / "specs" / feature_dir_name
            spec_files = list(specs_dir.glob("spec-*.md"))

            if not spec_files:
                self.console.warning("No specification found. Consider creating a spec first with 'specpulse sp-spec create'")

            # Read template
            template_content = self.specpulse.get_plan_template()

            # Prepare metadata
            timestamp = datetime.now().strftime("%Y-%m-%d")
            feature_id = feature_dir_name.split('-')[0]

            # Replace template variables
            content = template_content
            content = content.replace("{{ feature_name }}", feature_dir_name)
            content = content.replace("{{ feature_id }}", feature_id)
            content = content.replace("{{ plan_id }}", f"{plan_number:03d}")
            content = content.replace("{{ date }}", timestamp)
            content = content.replace("{{ description }}", description)

            # Add metadata HTML comments for parsing
            metadata = f"""<!-- SPECPULSE_METADATA
FEATURE_DIR: {feature_dir_name}
FEATURE_ID: {feature_id}
PLAN_ID: {plan_number:03d}
CREATED: {datetime.now().isoformat()}
STATUS: draft
-->

"""
            content = metadata + content

            # SECURITY: Validate plan file path before writing
            try:
                safe_plan_path = PathValidator.validate_file_path(self.project_root, plan_path)
            except SecurityError as e:
                raise ValidationError(f"Security violation: {str(e)}")

            # Write plan file
            safe_plan_path.write_text(content, encoding='utf-8')

            self.console.success(f"Created: {safe_plan_path.relative_to(self.project_root)}")
            self.console.info(f"\nNext steps:")
            self.console.info(f"1. Edit the plan: {plan_path.relative_to(self.project_root)}")
            self.console.info(f"2. Expand with AI (Claude/Gemini): /sp-plan expand")
            self.console.info(f"3. Validate: specpulse sp-plan validate {plan_number:03d}")
            self.console.info(f"4. Create tasks: specpulse sp-task breakdown {plan_number:03d}")

            return True

        except Exception as e:
            self.console.error(f"Failed to create plan: {str(e)}")
            return False

    def update(self, plan_id: str, changes: str, feature_name: Optional[str] = None) -> bool:
        """
        Update an existing plan

        Args:
            plan_id: Plan ID (e.g., "001")
            changes: Description of changes to make
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate plan ID format
            try:
                PathValidator.validate_spec_id(plan_id)  # Reuse spec_id validation (3-digit format)
            except ValueError as e:
                raise ValidationError(f"Invalid plan ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            plan_path = self.project_root / "plans" / feature_dir.name / f"plan-{plan_id}.md"

            if not plan_path.exists():
                self.console.error(f"Plan not found: plan-{plan_id}.md")
                return False

            self.console.header(f"Updating Plan: plan-{plan_id}.md", style="bright_cyan")

            # Read current content
            content = plan_path.read_text(encoding='utf-8')

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

            plan_path.write_text(content, encoding='utf-8')

            self.console.success(f"Updated: {plan_path.relative_to(self.project_root)}")
            self.console.info(f"\nChanges logged: {changes}")

            return True

        except Exception as e:
            self.console.error(f"Failed to update plan: {str(e)}")
            return False

    def validate(self, plan_id: Optional[str] = None, feature_name: Optional[str] = None) -> bool:
        """
        Validate implementation plan(s)

        Args:
            plan_id: Optional specific plan ID, validates all if not provided
            feature_name: Optional feature name/ID

        Returns:
            bool: True if validation passes, False otherwise
        """
        try:
            # SECURITY: Validate plan ID if provided
            if plan_id:
                try:
                    PathValidator.validate_spec_id(plan_id)
                except ValueError as e:
                    raise ValidationError(f"Invalid plan ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            plans_dir = self.project_root / "plans" / feature_dir.name

            if plan_id:
                # Validate specific plan
                plan_path = plans_dir / f"plan-{plan_id}.md"
                if not plan_path.exists():
                    self.console.error(f"Plan not found: plan-{plan_id}.md")
                    return False

                plans_to_validate = [plan_path]
            else:
                # Validate all plans
                plans_to_validate = list(plans_dir.glob("plan-*.md"))

            if not plans_to_validate:
                self.console.warning("No plans found to validate")
                return False

            self.console.header("Validating Plans", style="bright_cyan")

            all_valid = True
            for plan_path in plans_to_validate:
                self.console.info(f"\nValidating: {plan_path.name}")

                content = plan_path.read_text(encoding='utf-8')

                # Check required sections
                required_sections = [
                    "## Architecture Overview",
                    "## Technology Stack",
                    "## Implementation Phases",
                    "## Testing Strategy"
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
                self.console.success("\n✓ All plans valid")
                return True
            else:
                self.console.warning("\n⚠ Some plans need attention")
                return False

        except Exception as e:
            self.console.error(f"Validation failed: {str(e)}")
            return False

    def list_plans(self, feature_name: Optional[str] = None) -> bool:
        """
        List all plans in current feature

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

            plans_dir = self.project_root / "plans" / feature_dir.name
            plans = sorted(plans_dir.glob("plan-*.md"))

            if not plans:
                self.console.warning(f"No plans found in {feature_dir.name}")
                return False

            self.console.header(f"Plans in {feature_dir.name}", style="bright_cyan")

            for plan_path in plans:
                # Extract metadata
                content = plan_path.read_text(encoding='utf-8')
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

                self.console.info(f"  • {plan_path.name} - Status: {status}, Created: {created}")

            return True

        except Exception as e:
            self.console.error(f"Failed to list plans: {str(e)}")
            return False

    def show(self, plan_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Display plan content

        Args:
            plan_id: Plan ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate plan ID
            try:
                PathValidator.validate_spec_id(plan_id)
            except ValueError as e:
                raise ValidationError(f"Invalid plan ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            plan_path = self.project_root / "plans" / feature_dir.name / f"plan-{plan_id}.md"

            if not plan_path.exists():
                self.console.error(f"Plan not found: plan-{plan_id}.md")
                return False

            content = plan_path.read_text(encoding='utf-8')

            self.console.header(f"Plan: plan-{plan_id}.md", style="bright_cyan")
            self.console.info(content)

            return True

        except Exception as e:
            self.console.error(f"Failed to show plan: {str(e)}")
            return False

    def progress(self, plan_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Show plan completion progress

        Args:
            plan_id: Plan ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate plan ID
            try:
                PathValidator.validate_spec_id(plan_id)
            except ValueError as e:
                raise ValidationError(f"Invalid plan ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            plan_path = self.project_root / "plans" / feature_dir.name / f"plan-{plan_id}.md"

            if not plan_path.exists():
                self.console.error(f"Plan not found: plan-{plan_id}.md")
                return False

            content = plan_path.read_text(encoding='utf-8')

            self.console.header(f"Progress: plan-{plan_id}.md", style="bright_cyan")

            # Check required sections
            required_sections = {
                "Architecture Overview": "## Architecture Overview" in content,
                "Technology Stack": "## Technology Stack" in content,
                "Implementation Phases": "## Implementation Phases" in content,
                "Testing Strategy": "## Testing Strategy" in content,
                "API Contracts": "## API Contracts" in content,
                "Data Models": "## Data Models" in content
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

    def phases(self, plan_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Show implementation phases

        Args:
            plan_id: Plan ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate plan ID
            try:
                PathValidator.validate_spec_id(plan_id)
            except ValueError as e:
                raise ValidationError(f"Invalid plan ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            plan_path = self.project_root / "plans" / feature_dir.name / f"plan-{plan_id}.md"

            if not plan_path.exists():
                self.console.error(f"Plan not found: plan-{plan_id}.md")
                return False

            content = plan_path.read_text(encoding='utf-8')

            self.console.header(f"Implementation Phases: plan-{plan_id}.md", style="bright_cyan")

            # Extract phases
            phase_pattern = r'### Phase \d+:([^\n]+)'
            phases = re.findall(phase_pattern, content)

            if phases:
                for i, phase in enumerate(phases, 1):
                    self.console.info(f"  Phase {i}: {phase.strip()}")
            else:
                self.console.warning("No phases found in plan")

            return True

        except Exception as e:
            self.console.error(f"Failed to show phases: {str(e)}")
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

    def _get_next_plan_number(self, plans_dir: Path) -> int:
        """Get next available plan number"""
        if not plans_dir.exists():
            return 1

        existing_plans = list(plans_dir.glob("plan-*.md"))

        if not existing_plans:
            return 1

        max_number = 0
        for plan_path in existing_plans:
            match = re.match(r'plan-(\d{3})\.md', plan_path.name)
            if match:
                plan_number = int(match.group(1))
                max_number = max(max_number, plan_number)

        return max_number + 1
