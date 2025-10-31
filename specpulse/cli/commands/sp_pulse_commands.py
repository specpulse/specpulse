#!/usr/bin/env python3
"""
sp-pulse Commands - Feature Initialization and Management
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import yaml
import re

from ...utils.console import Console
from ...utils.git_utils import GitUtils, GitSecurityError
from ...utils.path_validator import PathValidator, SecurityError
from ...utils.error_handler import (
    ErrorHandler, ValidationError, ProjectStructureError,
    GitError
)
from ...core.memory_manager import MemoryManager
from ...core.feature_id_generator import FeatureIDGenerator


class SpPulseCommands:
    """Handler for sp-pulse CLI commands"""

    def __init__(self, console: Console, project_root: Path):
        self.console = console
        self.project_root = project_root
        self.memory_manager = MemoryManager(project_root)
        self.git = GitUtils(project_root)
        self.error_handler = ErrorHandler()
        self.id_generator = FeatureIDGenerator(project_root)  # Thread-safe ID generation

    def init_feature(self, feature_name: str, feature_id: Optional[str] = None) -> bool:
        """
        Initialize a new feature with complete structure

        Args:
            feature_name: Name of the feature (e.g., "user-authentication")
            feature_id: Optional feature ID (e.g., "001"), auto-generated if not provided

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate feature name using PathValidator
            try:
                validated_name = PathValidator.validate_feature_name(feature_name)
            except (ValueError, SecurityError) as e:
                raise ValidationError(
                    f"Invalid feature name: {feature_name}. {str(e)}",
                    validation_type="feature_name",
                    missing_items=["Valid characters: alphanumeric, hyphen, underscore"]
                )

            # Sanitize for consistency (lowercase, clean format)
            sanitized_name = self._sanitize_feature_name(validated_name)

            # Determine feature ID (THREAD-SAFE)
            if not feature_id:
                # Use thread-safe ID generator instead of directory scanning
                feature_id = self.id_generator.get_next_id()

            # Create feature directory name
            feature_dir_name = f"{feature_id}-{sanitized_name}"

            self.console.header(f"Initializing Feature: {feature_dir_name}", style="bright_cyan")

            # Create directory structure
            directories = [
                self.project_root / "specs" / feature_dir_name,
                self.project_root / "plans" / feature_dir_name,
                self.project_root / "tasks" / feature_dir_name,
            ]

            with self.console.progress_bar("Creating feature structure", len(directories)) as progress:
                task = progress.add_task("Creating directories...", total=len(directories))

                for dir_path in directories:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    progress.update(task, advance=1)

            self.console.success(f"Created feature directories")

            # Update context
            self._update_context(feature_id, sanitized_name, feature_dir_name)

            # Create git branch (optional)
            if GitUtils.is_git_installed() and self.git.is_git_repo():
                try:
                    branch_name = feature_dir_name
                    # SECURITY: GitUtils now validates branch names internally
                    if self.git.create_branch(branch_name):
                        self.console.success(f"Created and switched to branch: {branch_name}")
                    else:
                        self.console.warning(f"Branch {branch_name} already exists, switched to it")
                except (GitError, GitSecurityError) as e:
                    self.console.warning(f"Git branch creation skipped: {str(e)}")

            # Display suggestions
            self._display_next_steps(feature_dir_name)

            return True

        except Exception as e:
            self.console.error(f"Failed to initialize feature: {str(e)}")
            return False

    def continue_feature(self, feature_name: str) -> bool:
        """
        Switch context to an existing feature

        Args:
            feature_name: Name or ID of the feature to continue

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Find matching feature directory
            feature_dir = self._find_feature_directory(feature_name)

            if not feature_dir:
                self.console.error(f"Feature not found: {feature_name}")
                self._list_features()
                return False

            feature_dir_name = feature_dir.name
            self.console.header(f"Switching to Feature: {feature_dir_name}", style="bright_cyan")

            # Extract feature ID from directory name (e.g., "001-user-auth" -> "001")
            feature_id = feature_dir_name.split("-")[0]
            feature_name_clean = "-".join(feature_dir_name.split("-")[1:])

            # Update context
            self._update_context(feature_id, feature_name_clean, feature_dir_name)

            # Switch git branch if available
            if GitUtils.is_git_installed() and self.git.is_git_repo():
                try:
                    # SECURITY: GitUtils now validates branch names internally
                    if self.git.checkout_branch(feature_dir_name):
                        self.console.success(f"Switched to branch: {feature_dir_name}")
                except (GitError, GitSecurityError) as e:
                    self.console.warning(f"Could not switch branch: {str(e)}")

            # Display feature status
            self._display_feature_status(feature_dir)

            return True

        except Exception as e:
            self.console.error(f"Failed to switch feature: {str(e)}")
            return False

    def list_features(self) -> bool:
        """
        List all features in the project

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._list_features()
            return True
        except Exception as e:
            self.console.error(f"Failed to list features: {str(e)}")
            return False

    def status(self) -> bool:
        """
        Show current feature status

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get current feature from context
            context_file = self.project_root / "memory" / "context.md"

            if not context_file.exists():
                self.console.warning("No active feature context found")
                return False

            content = context_file.read_text(encoding='utf-8')

            # Parse current feature from context
            current_feature = None
            for line in content.split('\n'):
                if 'current.feature_id' in line.lower() or 'active feature' in line.lower():
                    # Extract feature ID or name
                    parts = line.split(':')
                    if len(parts) > 1:
                        current_feature = parts[1].strip()
                        break

            if not current_feature:
                self.console.warning("No active feature in context")
                return False

            # Find and display feature status
            feature_dir = self._find_feature_directory(current_feature)
            if feature_dir:
                self._display_feature_status(feature_dir)
                return True
            else:
                self.console.warning(f"Feature directory not found for: {current_feature}")
                return False

        except Exception as e:
            self.console.error(f"Failed to get status: {str(e)}")
            return False

    def delete_feature(self, feature_name: str, force: bool = False) -> bool:
        """
        Delete a feature and its artifacts

        Args:
            feature_name: Name or ID of the feature to delete
            force: Skip confirmation prompt

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            feature_dir = self._find_feature_directory(feature_name)

            if not feature_dir:
                self.console.error(f"Feature not found: {feature_name}")
                return False

            feature_dir_name = feature_dir.name

            if not force:
                # Prompt for confirmation
                confirm = input(f"Delete feature '{feature_dir_name}' and all its artifacts? (yes/no): ")
                if confirm.lower() not in ['yes', 'y']:
                    self.console.info("Deletion cancelled")
                    return False

            self.console.header(f"Deleting Feature: {feature_dir_name}", style="bright_red")

            # Delete directories
            import shutil
            directories = [
                self.project_root / "specs" / feature_dir_name,
                self.project_root / "plans" / feature_dir_name,
                self.project_root / "tasks" / feature_dir_name,
            ]

            for dir_path in directories:
                # SECURITY: Validate path is within project before deletion
                try:
                    safe_path = PathValidator.validate_file_path(self.project_root, dir_path)
                    if safe_path.exists():
                        shutil.rmtree(safe_path)
                        self.console.info(f"Deleted: {safe_path.relative_to(self.project_root)}")
                except SecurityError as e:
                    self.console.error(f"Security violation: {str(e)}")
                    return False

            # Note: Git branch deletion skipped (manual operation recommended)
            # User should manually delete branch if needed: git branch -D <branch-name>

            self.console.success(f"Feature deleted: {feature_dir_name}")
            return True

        except Exception as e:
            self.console.error(f"Failed to delete feature: {str(e)}")
            return False

    # Helper methods

    def _sanitize_feature_name(self, name: str) -> str:
        """Sanitize feature name to valid format"""
        # Remove invalid characters, keep only alphanumeric and hyphens
        sanitized = re.sub(r'[^a-zA-Z0-9-]', '-', name)
        # Remove multiple consecutive hyphens
        sanitized = re.sub(r'-+', '-', sanitized)
        # Remove leading/trailing hyphens
        sanitized = sanitized.strip('-')
        # Convert to lowercase
        sanitized = sanitized.lower()
        return sanitized

    def _get_next_feature_id(self) -> str:
        """
        Get next available feature ID (DEPRECATED - use id_generator instead).

        This method is deprecated in favor of FeatureIDGenerator which provides
        thread-safe, race-condition-free ID generation.

        MIGRATION NOTE: This method is kept for backward compatibility but
        should not be used for new code. Use self.id_generator.get_next_id() instead.

        Returns:
            Next feature ID as 3-digit string
        """
        # Delegate to thread-safe generator
        return self.id_generator.get_next_id()

    def _update_context(self, feature_id: str, feature_name: str, feature_dir_name: str):
        """Update memory/context.md with current feature"""
        context_file = self.project_root / "memory" / "context.md"

        # Create context file if it doesn't exist
        if not context_file.exists():
            context_file.parent.mkdir(parents=True, exist_ok=True)
            context_file.write_text("# Project Context\n\n## Current State\n\n", encoding='utf-8')

        content = context_file.read_text(encoding='utf-8')

        # Update or add current feature section
        timestamp = datetime.now().isoformat()

        new_entry = f"""
## Active Feature
- **Feature ID**: {feature_id}
- **Feature Name**: {feature_name}
- **Directory**: {feature_dir_name}
- **Last Updated**: {timestamp}
- **Status**: initialized

"""

        # Replace existing active feature section or append
        if "## Active Feature" in content:
            # Replace existing section
            import re
            pattern = r'## Active Feature.*?(?=\n## |\Z)'
            content = re.sub(pattern, new_entry.strip(), content, flags=re.DOTALL)
        else:
            # Append new section
            if "## Current State" in content:
                content = content.replace("## Current State", f"## Current State\n{new_entry}")
            else:
                content += new_entry

        context_file.write_text(content, encoding='utf-8')
        self.console.success("Updated project context")

    def _find_feature_directory(self, identifier: str) -> Optional[Path]:
        """Find feature directory by ID or name"""
        specs_dir = self.project_root / "specs"

        if not specs_dir.exists():
            return None

        # Try exact match first
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

    def _list_features(self):
        """Display all features in a table"""
        specs_dir = self.project_root / "specs"

        if not specs_dir.exists() or not any(specs_dir.iterdir()):
            self.console.warning("No features found")
            return

        features = []
        for item in specs_dir.iterdir():
            if item.is_dir() and re.match(r'^\d{3}-', item.name):
                feature_id = item.name.split('-')[0]
                feature_name = "-".join(item.name.split('-')[1:])

                # Count artifacts
                specs_count = len(list((self.project_root / "specs" / item.name).glob("*.md")))
                plans_count = len(list((self.project_root / "plans" / item.name).glob("*.md")))
                tasks_count = len(list((self.project_root / "tasks" / item.name).glob("*.md")))

                features.append({
                    "ID": feature_id,
                    "Name": feature_name,
                    "Specs": specs_count,
                    "Plans": plans_count,
                    "Tasks": tasks_count
                })

        if not features:
            self.console.warning("No features found")
            return

        self.console.header("Features", style="bright_cyan")

        # Create table manually
        for f in features:
            self.console.info(f"  {f['ID']} - {f['Name']} | Specs: {f['Specs']}, Plans: {f['Plans']}, Tasks: {f['Tasks']}")

    def _display_feature_status(self, feature_dir: Path):
        """Display detailed status for a feature"""
        feature_dir_name = feature_dir.name

        self.console.header(f"Feature Status: {feature_dir_name}", style="bright_cyan")

        # Count artifacts
        specs_dir = self.project_root / "specs" / feature_dir_name
        plans_dir = self.project_root / "plans" / feature_dir_name
        tasks_dir = self.project_root / "tasks" / feature_dir_name

        specs = list(specs_dir.glob("*.md")) if specs_dir.exists() else []
        plans = list(plans_dir.glob("*.md")) if plans_dir.exists() else []
        tasks = list(tasks_dir.glob("*.md")) if tasks_dir.exists() else []

        # Display status
        self.console.info(f"  Specifications: {len(specs)}")
        self.console.info(f"  Plans: {len(plans)}")
        self.console.info(f"  Tasks: {len(tasks)}")

        # Show files if any
        if specs:
            self.console.info("\nSpecifications:")
            for spec in specs:
                self.console.info(f"  - {spec.name}")

        if plans:
            self.console.info("\nPlans:")
            for plan in plans:
                self.console.info(f"  - {plan.name}")

        if tasks:
            self.console.info("\nTasks:")
            for task in tasks:
                self.console.info(f"  - {task.name}")

    def _display_next_steps(self, feature_dir_name: str):
        """Display next steps after feature initialization"""
        self.console.header("Next Steps", style="bright_green")

        steps = [
            f"1. Create specification:",
            f"   specpulse sp-spec create \"<description>\"",
            f"",
            f"2. Or use slash command in Claude/Gemini:",
            f"   /sp-spec create <description>",
            f"",
            f"3. After specification, generate plan:",
            f"   specpulse sp-plan create \"<description>\"",
        ]

        for step in steps:
            self.console.info(step)
