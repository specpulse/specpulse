"""
Feature management commands for SpecPulse CLI v2.1.0

These commands replace bash/ps1 scripts with pure Python implementation.
AI assistants (Claude/Gemini) call these via custom slash commands.
"""

from pathlib import Path
from datetime import datetime
import re
from typing import Optional
import yaml


class FeatureCommands:
    """Feature lifecycle management commands"""

    def __init__(self, console, project_root: Path):
        self.console = console
        self.project_root = project_root
        # Import PathManager for centralized path management
        from ...core.path_manager import PathManager
        self.path_manager = PathManager(project_root, use_legacy_structure=False)

        self.specs_dir = self.path_manager.specs_dir
        self.plans_dir = self.path_manager.plans_dir
        self.tasks_dir = self.path_manager.tasks_dir
        self.memory_dir = self.path_manager.memory_dir
        self.templates_dir = self.path_manager.templates_dir

    def feature_init(self, feature_name: str, **kwargs) -> bool:
        """
        Initialize a new feature with directory structure.

        Creates:
        - .specpulse/specs/XXX-feature-name/
        - .specpulse/plans/XXX-feature-name/
        - .specpulse/tasks/XXX-feature-name/
        Updates:
        - .specpulse/memory/context.md

        Args:
            feature_name: Feature name (e.g., "user-authentication")

        Returns:
            bool: Success status
        """
        try:
            # Find next feature number
            feature_id = self._get_next_feature_id()

            # Sanitize feature name
            sanitized_name = re.sub(r'[^a-z0-9-]', '-', feature_name.lower())
            sanitized_name = re.sub(r'-+', '-', sanitized_name).strip('-')

            # Full feature directory name: 001-feature-name
            full_name = f"{feature_id:03d}-{sanitized_name}"

            self.console.header(f"Initializing Feature: {full_name}")

            # Create directories
            dirs_created = []
            for base_dir in [self.specs_dir, self.plans_dir, self.tasks_dir]:
                feature_dir = base_dir / full_name
                feature_dir.mkdir(parents=True, exist_ok=True)
                dirs_created.append(str(feature_dir.relative_to(self.project_root)))

            # Update .specpulse/memory/context.md
            self._update_context_for_feature(full_name, feature_id)

            # Display results
            self.console.success(f"Feature initialized: {full_name}")
            for dir_path in dirs_created:
                self.console.info(f"  Created: {dir_path}/")
            self.console.info(f"  Updated: .specpulse/memory/context.md")

            # Next steps
            self.console.info("\nNext steps:")
            self.console.info(f"  1. Create specification: /sp-spec <description>")
            self.console.info(f"  2. Or manually: .specpulse/specs/{full_name}/spec-001.md")

            return True

        except Exception as e:
            self.console.error(f"Feature initialization failed: {e}")
            return False

    def feature_continue(self, feature_name: str, **kwargs) -> bool:
        """
        Switch context to an existing feature.

        Args:
            feature_name: Feature name or ID (e.g., "001" or "user-authentication")

        Returns:
            bool: Success status
        """
        try:
            # Find matching feature directory
            feature_dir = self._find_feature_dir(feature_name)

            if not feature_dir:
                self.console.error(f"Feature not found: {feature_name}")
                self.console.info("Available features:")
                self._list_features()
                return False

            # Extract feature ID from directory name
            match = re.match(r'^(\d{3})-', feature_dir.name)
            if not match:
                self.console.error(f"Invalid feature directory format: {feature_dir.name}")
                return False

            feature_id = int(match.group(1))

            # Update context
            self._update_context_for_feature(feature_dir.name, feature_id)

            self.console.success(f"Switched to feature: {feature_dir.name}")
            self.console.info(f"  Context updated in: .specpulse/memory/context.md")

            # Show feature status
            self._show_feature_status(feature_dir)

            return True

        except Exception as e:
            self.console.error(f"Feature switch failed: {e}")
            return False

    def _get_next_feature_id(self) -> int:
        """Get next available feature ID by scanning directories"""
        max_id = 0

        for base_dir in [self.specs_dir, self.plans_dir, self.tasks_dir]:
            if not base_dir.exists():
                continue

            for item in base_dir.iterdir():
                if item.is_dir():
                    match = re.match(r'^(\d{3})-', item.name)
                    if match:
                        feature_id = int(match.group(1))
                        max_id = max(max_id, feature_id)

        return max_id + 1

    def _find_feature_dir(self, feature_name: str) -> Optional[Path]:
        """Find feature directory by name or ID"""
        # If numeric, treat as ID
        if feature_name.isdigit():
            feature_id = int(feature_name)
            pattern = f"{feature_id:03d}-*"
        else:
            # Sanitize and search by name
            sanitized = re.sub(r'[^a-z0-9-]', '-', feature_name.lower())
            pattern = f"*-{sanitized}"

        # Search in specs directory
        if self.specs_dir.exists():
            matches = list(self.specs_dir.glob(pattern))
            if matches:
                return matches[0]

        return None

    def _update_context_for_feature(self, full_name: str, feature_id: int):
        """Update .specpulse/memory/context.md with active feature"""
        context_file = self.memory_dir / "context.md"

        # Read current context
        if context_file.exists():
            content = context_file.read_text(encoding='utf-8')
        else:
            # Create from template
            content = """# Project Context

## Current State
- **Active Feature**: None
- **Last Updated**: [AUTO-GENERATED]
- **Phase**: Initialization

## Active Features
<!-- Format:
1. **[feature-name]** (SPEC-XXX)
   - Status: [Specification|Planning|Implementation|Testing|Deployed]
   - Branch: [branch-name]
-->

## Recent Decisions

## Completed Features
"""

        # Update active feature section
        timestamp = datetime.now().isoformat()

        # Add to workflow history
        history_entry = f"""
### Active Feature: {full_name}
- Feature ID: {feature_id:03d}
- Branch: {full_name}
- Started: {timestamp}
"""

        if "## Workflow History" not in content:
            content += "\n## Workflow History\n"

        content += history_entry

        # Write back
        context_file.write_text(content, encoding='utf-8')

    def _list_features(self):
        """List all available features"""
        if not self.specs_dir.exists():
            return

        features = sorted([
            d for d in self.specs_dir.iterdir()
            if d.is_dir() and re.match(r'^\d{3}-', d.name)
        ])

        for feature in features:
            self.console.info(f"  - {feature.name}")

    def _show_feature_status(self, feature_dir: Path):
        """Show status of feature (specs, plans, tasks)"""
        self.console.info("\nFeature status:")

        # Count specs
        specs_count = len(list((self.specs_dir / feature_dir.name).glob("spec-*.md")))
        self.console.info(f"  Specs: {specs_count}")

        # Count plans
        plans_count = len(list((self.plans_dir / feature_dir.name).glob("plan-*.md")))
        self.console.info(f"  Plans: {plans_count}")

        # Count tasks
        tasks_count = len(list((self.tasks_dir / feature_dir.name).glob("task-*.md")))
        self.console.info(f"  Tasks: {tasks_count}")

    def feature_list(self, **kwargs) -> bool:
        """
        List all features in the project with their status

        Returns:
            bool: Success status
        """
        try:
            self.console.info("Available features:")

            if not self.specs_dir.exists():
                self.console.warning("  No features found (specs directory doesn't exist)")
                return True

            features = sorted([
                d for d in self.specs_dir.iterdir()
                if d.is_dir() and re.match(r'^\d{3}-', d.name)
            ])

            if not features:
                self.console.warning("  No features found")
                return True

            for feature in features:
                # Extract feature info
                match = re.match(r'^(\d{3})-(.+)$', feature.name)
                if match:
                    feature_id = match.group(1)
                    feature_name = match.group(2).replace('-', ' ').title()

                    # Count files
                    specs_count = len(list((self.specs_dir / feature.name).glob("spec-*.md")))
                    plans_count = len(list((self.plans_dir / feature.name).glob("plan-*.md")))
                    tasks_count = len(list((self.tasks_dir / feature.name).glob("task-*.md")))

                    # Show status
                    self.console.info(f"  {feature_id} - {feature_name}")
                    self.console.info(f"    Specs: {specs_count}, Plans: {plans_count}, Tasks: {tasks_count}")

            return True

        except Exception as e:
            self.console.error(f"Failed to list features: {e}")
            return False
