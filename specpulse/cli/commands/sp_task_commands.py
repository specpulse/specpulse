#!/usr/bin/env python3
"""
sp-task Commands - Task Management and Execution
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
from ...core.specpulse import SpecPulse


class SpTaskCommands:
    """Handler for sp-task CLI commands"""

    def __init__(self, console: Console, project_root: Path):
        self.console = console
        self.project_root = project_root
        self.template_manager = TemplateManager(project_root)
        self.specpulse = SpecPulse(project_root)
        self.error_handler = ErrorHandler()

    def breakdown(self, plan_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Generate tasks from implementation plan

        Args:
            plan_id: Plan ID to break down into tasks
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate plan ID format
            try:
                PathValidator.validate_spec_id(plan_id)  # 3-digit format
            except ValueError as e:
                raise ValidationError(f"Invalid plan ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            feature_dir_name = feature_dir.name

            # Check if plan exists
            plan_path = self.project_root / "plans" / feature_dir_name / f"plan-{plan_id}.md"

            if not plan_path.exists():
                self.console.error(f"Plan not found: plan-{plan_id}.md")
                return False

            tasks_dir = self.project_root / "tasks" / feature_dir_name

            # Determine next task number
            task_number = self._get_next_task_number(tasks_dir)
            task_filename = f"tasks-{task_number:03d}.md"
            task_path = tasks_dir / task_filename

            self.console.header(f"Creating Task Breakdown: {task_filename}", style="bright_cyan")

            # Read plan content for context
            plan_content = plan_path.read_text(encoding='utf-8')

            # Read template
            template_content = self.specpulse.get_task_template()

            # Prepare metadata
            timestamp = datetime.now().strftime("%Y-%m-%d")
            feature_id = feature_dir_name.split('-')[0]

            # Replace template variables
            content = template_content
            content = content.replace("{{ feature_name }}", feature_dir_name)
            content = content.replace("{{ feature_id }}", feature_id)
            content = content.replace("{{ plan_id }}", plan_id)
            content = content.replace("{{ task_id }}", f"{task_number:03d}")
            content = content.replace("{{ date }}", timestamp)

            # Add metadata HTML comments for parsing
            metadata = f"""<!-- SPECPULSE_METADATA
FEATURE_DIR: {feature_dir_name}
FEATURE_ID: {feature_id}
PLAN_ID: {plan_id}
TASK_ID: {task_number:03d}
CREATED: {datetime.now().isoformat()}
STATUS: pending
PROGRESS: 0
-->

"""
            content = metadata + content

            # Add reference to plan
            plan_reference = f"""# Task Breakdown

**Plan Reference**: plan-{plan_id}.md
**Feature**: {feature_dir_name}

"""
            content = plan_reference + content

            # SECURITY: Validate task file path before writing
            try:
                safe_task_path = PathValidator.validate_file_path(self.project_root, task_path)
            except SecurityError as e:
                raise ValidationError(f"Security violation: {str(e)}")

            # Write task file
            safe_task_path.write_text(content, encoding='utf-8')

            self.console.success(f"Created: {safe_task_path.relative_to(self.project_root)}")
            self.console.info(f"\nNext steps:")
            self.console.info(f"1. Edit the task breakdown: {task_path.relative_to(self.project_root)}")
            self.console.info(f"2. Expand with AI (Claude/Gemini): /sp-task expand")
            self.console.info(f"3. Start first task: specpulse sp-task start 001")

            return True

        except Exception as e:
            self.console.error(f"Failed to create task breakdown: {str(e)}")
            return False

    def create(self, description: str, feature_name: Optional[str] = None) -> bool:
        """
        Create a single manual task

        Args:
            description: Task description
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            feature_dir_name = feature_dir.name
            tasks_dir = self.project_root / "tasks" / feature_dir_name

            # Find tasks file or create new
            task_files = list(tasks_dir.glob("tasks-*.md"))

            if task_files:
                # Add to existing tasks file
                task_file = sorted(task_files)[-1]
                content = task_file.read_text(encoding='utf-8')

                # Add new task
                new_task = f"""

### Task: {description}
- **Status**: pending
- **Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Description**: {description}

"""
                content += new_task
                task_file.write_text(content, encoding='utf-8')

                self.console.success(f"Added task to: {task_file.relative_to(self.project_root)}")
            else:
                # Create new tasks file
                self.console.warning("No tasks file found. Use 'specpulse sp-task breakdown <plan-id>' first")
                return False

            return True

        except Exception as e:
            self.console.error(f"Failed to create task: {str(e)}")
            return False

    def update(self, task_id: str, changes: str, feature_name: Optional[str] = None) -> bool:
        """
        Update a task

        Args:
            task_id: Task ID
            changes: Description of changes
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate task ID format
            try:
                PathValidator.validate_spec_id(task_id)  # 3-digit format
            except ValueError as e:
                raise ValidationError(f"Invalid task ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            task_path = self.project_root / "tasks" / feature_dir.name / f"tasks-{task_id}.md"

            if not task_path.exists():
                self.console.error(f"Task file not found: tasks-{task_id}.md")
                return False

            self.console.header(f"Updating Tasks: tasks-{task_id}.md", style="bright_cyan")

            # Read current content
            content = task_path.read_text(encoding='utf-8')

            # Add update log
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_log = f"\n## Update Log\n- **{timestamp}**: {changes}\n"

            if "## Update Log" not in content:
                content += update_log
            else:
                content = content.replace("## Update Log\n", f"## Update Log\n- **{timestamp}**: {changes}\n")

            task_path.write_text(content, encoding='utf-8')

            self.console.success(f"Updated: {task_path.relative_to(self.project_root)}")
            self.console.info(f"\nChanges logged: {changes}")

            return True

        except Exception as e:
            self.console.error(f"Failed to update task: {str(e)}")
            return False

    def start(self, task_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Mark a task as started

        Args:
            task_id: Task ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate task ID format
            try:
                PathValidator.validate_spec_id(task_id)
            except ValueError as e:
                raise ValidationError(f"Invalid task ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            task_path = self.project_root / "tasks" / feature_dir.name / f"tasks-{task_id}.md"

            if not task_path.exists():
                self.console.error(f"Task file not found: tasks-{task_id}.md")
                return False

            content = task_path.read_text(encoding='utf-8')

            # Update STATUS in metadata
            content = re.sub(
                r'STATUS: \w+',
                'STATUS: in_progress',
                content
            )

            # Add started timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            started_marker = f"\n**Started**: {timestamp}\n"

            if "**Started**:" not in content:
                # Add after metadata
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('-->'):
                        lines.insert(i + 1, started_marker)
                        break
                content = '\n'.join(lines)

            task_path.write_text(content, encoding='utf-8')

            self.console.success(f"Task started: tasks-{task_id}.md")
            self.console.info(f"Status: in_progress")

            return True

        except Exception as e:
            self.console.error(f"Failed to start task: {str(e)}")
            return False

    def done(self, task_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Mark a task as completed

        Args:
            task_id: Task ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate task ID format
            try:
                PathValidator.validate_spec_id(task_id)
            except ValueError as e:
                raise ValidationError(f"Invalid task ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            task_path = self.project_root / "tasks" / feature_dir.name / f"tasks-{task_id}.md"

            if not task_path.exists():
                self.console.error(f"Task file not found: tasks-{task_id}.md")
                return False

            content = task_path.read_text(encoding='utf-8')

            # Update STATUS in metadata
            content = re.sub(
                r'STATUS: \w+',
                'STATUS: completed',
                content
            )

            # Update PROGRESS to 100
            content = re.sub(
                r'PROGRESS: \d+',
                'PROGRESS: 100',
                content
            )

            # Add completed timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            completed_marker = f"\n**Completed**: {timestamp}\n"

            if "**Completed**:" not in content:
                # Add after metadata
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('-->'):
                        lines.insert(i + 1, completed_marker)
                        break
                content = '\n'.join(lines)

            task_path.write_text(content, encoding='utf-8')

            self.console.success(f"Task completed: tasks-{task_id}.md")
            self.console.info(f"Status: completed")
            self.console.info(f"Progress: 100%")

            return True

        except Exception as e:
            self.console.error(f"Failed to complete task: {str(e)}")
            return False

    def list_tasks(self, feature_name: Optional[str] = None) -> bool:
        """
        List all tasks in current feature

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

            tasks_dir = self.project_root / "tasks" / feature_dir.name
            tasks = sorted(tasks_dir.glob("tasks-*.md"))

            if not tasks:
                self.console.warning(f"No tasks found in {feature_dir.name}")
                return False

            self.console.header(f"Tasks in {feature_dir.name}", style="bright_cyan")

            for task_path in tasks:
                # Extract metadata
                content = task_path.read_text(encoding='utf-8')
                status = "pending"
                progress = 0

                # Parse metadata
                status_match = re.search(r'STATUS: (\w+)', content)
                if status_match:
                    status = status_match.group(1)

                progress_match = re.search(r'PROGRESS: (\d+)', content)
                if progress_match:
                    progress = int(progress_match.group(1))

                self.console.info(f"  • {task_path.name} - Status: {status}, Progress: {progress}%")

            return True

        except Exception as e:
            self.console.error(f"Failed to list tasks: {str(e)}")
            return False

    def show(self, task_id: str, feature_name: Optional[str] = None) -> bool:
        """
        Display task content

        Args:
            task_id: Task ID
            feature_name: Optional feature name/ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # SECURITY: Validate task ID format
            try:
                PathValidator.validate_spec_id(task_id)
            except ValueError as e:
                raise ValidationError(f"Invalid task ID: {str(e)}")

            feature_dir = self._get_current_feature(feature_name)

            if not feature_dir:
                self.console.error("No active feature found")
                return False

            task_path = self.project_root / "tasks" / feature_dir.name / f"tasks-{task_id}.md"

            if not task_path.exists():
                self.console.error(f"Task not found: tasks-{task_id}.md")
                return False

            content = task_path.read_text(encoding='utf-8')

            self.console.header(f"Tasks: tasks-{task_id}.md", style="bright_cyan")
            self.console.info(content)

            return True

        except Exception as e:
            self.console.error(f"Failed to show task: {str(e)}")
            return False

    def progress(self, feature_name: Optional[str] = None) -> bool:
        """
        Show overall task progress

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

            tasks_dir = self.project_root / "tasks" / feature_dir.name
            task_files = list(tasks_dir.glob("tasks-*.md"))

            if not task_files:
                self.console.warning("No tasks found")
                return False

            self.console.header(f"Task Progress: {feature_dir.name}", style="bright_cyan")

            total_tasks = 0
            completed_tasks = 0
            in_progress_tasks = 0
            pending_tasks = 0

            for task_file in task_files:
                content = task_file.read_text(encoding='utf-8')

                # Count individual tasks (look for task markers)
                task_count = content.count("### Task:")
                total_tasks += task_count

                # Count statuses
                completed_tasks += content.count('**Status**: completed')
                in_progress_tasks += content.count('**Status**: in_progress')
                pending_tasks += content.count('**Status**: pending')

            # Calculate percentage
            if total_tasks > 0:
                completion_percentage = (completed_tasks / total_tasks) * 100
            else:
                completion_percentage = 0

            # Display progress
            self.console.info(f"  Total Tasks: {total_tasks}")
            self.console.success(f"  Completed: {completed_tasks}")
            self.console.warning(f"  In Progress: {in_progress_tasks}")
            self.console.error(f"  Pending: {pending_tasks}")
            self.console.info(f"\n  Overall Completion: {completion_percentage:.1f}%")

            return True

        except Exception as e:
            self.console.error(f"Failed to show progress: {str(e)}")
            return False

    # Helper methods

    def _get_current_feature(self, feature_name: Optional[str] = None) -> Optional[Path]:
        """Get current feature directory from context or parameter"""

        if feature_name:
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

    def _get_next_task_number(self, tasks_dir: Path) -> int:
        """Get next available task number"""
        if not tasks_dir.exists():
            return 1

        existing_tasks = list(tasks_dir.glob("tasks-*.md"))

        if not existing_tasks:
            return 1

        max_number = 0
        for task_path in existing_tasks:
            match = re.match(r'tasks-(\d{3})\.md', task_path.name)
            if match:
                task_number = int(match.group(1))
                max_number = max(max_number, task_number)

        return max_number + 1
