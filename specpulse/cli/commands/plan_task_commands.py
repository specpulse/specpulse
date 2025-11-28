"""
Plan and Task management commands for SpecPulse CLI v2.1.0
"""

from pathlib import Path
from datetime import datetime
import re
from typing import Optional


class PlanCommands:
    """Plan lifecycle management"""

    def __init__(self, console, project_root: Path):
        self.console = console
        self.project_root = project_root
        # Import PathManager for centralized path management
        from ...core.path_manager import PathManager
        self.path_manager = PathManager(project_root)

        self.plans_dir = self.path_manager.plans_dir
        self.specs_dir = self.path_manager.specs_dir
        self.templates_dir = self.path_manager.templates_dir
        self.memory_dir = self.path_manager.memory_dir

    def plan_create(self, description: str, feature_id: Optional[str] = None) -> bool:
        """Create implementation plan"""
        try:
            if not feature_id:
                feature_id = self._detect_current_feature()
                if not feature_id:
                    self.console.error("No active feature")
                    return False

            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                self.console.error(f"Feature not found: {feature_id}")
                return False

            plan_dir = self.plans_dir / feature_dir.name
            plan_dir.mkdir(parents=True, exist_ok=True)

            plan_number = self._get_next_plan_number(plan_dir)
            plan_file = plan_dir / f"plan-{plan_number:03d}.md"

            template_file = self.templates_dir / "plan.md"
            if not template_file.exists():
                self.console.error(f"Template not found: {template_file}")
                return False

            template_content = template_file.read_text(encoding='utf-8')

            plan_content = f"""# Implementation Plan: {description}

<!-- FEATURE_DIR: {feature_dir.name} -->
<!-- FEATURE_ID: {feature_id} -->
<!-- PLAN_NUMBER: {plan_number:03d} -->
<!-- CREATED: {datetime.now().isoformat()} -->

## Description
{description}

## [LLM: Generate implementation plan using the template below]

---

{template_content}
"""

            plan_file.write_text(plan_content, encoding='utf-8')

            self.console.success(f"Plan created: {plan_file.relative_to(self.project_root)}")
            self.console.info(f"  Feature: {feature_dir.name}")
            self.console.info("\nNext: LLM will generate implementation plan")

            return True

        except Exception as e:
            self.console.error(f"Plan creation failed: {e}")
            return False

    def plan_update(self, plan_id: str, description: str, feature_id: Optional[str] = None) -> bool:
        """Update existing plan"""
        try:
            if not feature_id:
                feature_id = self._detect_current_feature()

            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                return False

            plan_dir = self.plans_dir / feature_dir.name
            plan_file = plan_dir / f"plan-{plan_id}.md"

            if not plan_file.exists():
                self.console.error(f"Plan not found: {plan_file}")
                return False

            content = plan_file.read_text(encoding='utf-8')
            update_marker = f"""

---
## [UPDATE REQUEST - {datetime.now().isoformat()}]
{description}
---
"""
            content += update_marker
            plan_file.write_text(content, encoding='utf-8')

            self.console.success(f"Update marker added: {plan_file.relative_to(self.project_root)}")
            return True

        except Exception as e:
            self.console.error(f"Plan update failed: {e}")
            return False

    def _get_next_plan_number(self, plan_dir: Path) -> int:
        """Get next available plan number"""
        if not plan_dir.exists():
            return 1

        plans = list(plan_dir.glob("plan-*.md"))
        if not plans:
            return 1

        max_num = 0
        for plan_file in plans:
            match = re.search(r'plan-(\d{3})\.md', plan_file.name)
            if match:
                max_num = max(max_num, int(match.group(1)))

        return max_num + 1

    def _detect_current_feature(self) -> Optional[str]:
        """Detect current feature from context"""
        context_file = self.memory_dir / "context.md"
        if not context_file.exists():
            return None

        content = context_file.read_text(encoding='utf-8')
        matches = re.findall(r'### Active Feature:.*?\n- Feature ID: (\d{3})', content)
        return matches[-1] if matches else None

    def _find_feature_dir(self, feature_id: str) -> Optional[Path]:
        """Find feature directory"""
        if not self.plans_dir.exists():
            return None

        pattern = f"{feature_id}*"
        matches = list(self.plans_dir.glob(pattern))
        return matches[0] if matches else None


class TaskCommands:
    """Task lifecycle management"""

    def __init__(self, console, project_root: Path):
        self.console = console
        self.project_root = project_root
        # Import PathManager for centralized path management
        from ...core.path_manager import PathManager
        self.path_manager = PathManager(project_root)

        self.tasks_dir = self.path_manager.tasks_dir
        self.plans_dir = self.path_manager.plans_dir
        self.templates_dir = self.path_manager.templates_dir
        self.memory_dir = self.path_manager.memory_dir

    def task_create(self, description: str, feature_id: Optional[str] = None) -> bool:
        """Create new task"""
        try:
            if not feature_id:
                feature_id = self._detect_current_feature()
                if not feature_id:
                    self.console.error("No active feature")
                    return False

            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                self.console.error(f"Feature not found: {feature_id}")
                return False

            task_dir = self.tasks_dir / feature_dir.name
            task_dir.mkdir(parents=True, exist_ok=True)

            task_number = self._get_next_task_number(task_dir)
            task_file = task_dir / f"task-{task_number:03d}.md"

            template_file = self.templates_dir / "task.md"
            if not template_file.exists():
                self.console.error(f"Template not found: {template_file}")
                return False

            template_content = template_file.read_text(encoding='utf-8')

            task_content = f"""# Task: {description}

<!-- FEATURE_DIR: {feature_dir.name} -->
<!-- FEATURE_ID: {feature_id} -->
<!-- TASK_NUMBER: {task_number:03d} -->
<!-- STATUS: pending -->
<!-- CREATED: {datetime.now().isoformat()} -->

## Description
{description}

## [LLM: Expand this task using the template below]

---

{template_content}
"""

            task_file.write_text(task_content, encoding='utf-8')

            self.console.success(f"Task created: {task_file.relative_to(self.project_root)}")
            return True

        except Exception as e:
            self.console.error(f"Task creation failed: {e}")
            return False

    def task_breakdown(self, plan_id: str, feature_id: Optional[str] = None) -> bool:
        """Generate tasks from plan (placeholder for LLM)"""
        try:
            if not feature_id:
                feature_id = self._detect_current_feature()

            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                return False

            plan_dir = self.plans_dir / feature_dir.name
            plan_file = plan_dir / f"plan-{plan_id}.md"

            if not plan_file.exists():
                self.console.error(f"Plan not found: {plan_file}")
                return False

            # Read plan
            plan_content = plan_file.read_text(encoding='utf-8')

            # Create marker in tasks directory
            task_dir = self.tasks_dir / feature_dir.name
            task_dir.mkdir(parents=True, exist_ok=True)

            breakdown_marker = task_dir / f"_breakdown_from_plan-{plan_id}.md"
            marker_content = f"""# Task Breakdown Request

Source Plan: plan-{plan_id}.md
Created: {datetime.now().isoformat()}

## [LLM: Generate tasks based on the plan]

Read: {plan_file}
Create: task-001.md, task-002.md, etc.

---

{plan_content[:1000]}...

[LLM: Break this plan into individual tasks]
"""
            breakdown_marker.write_text(marker_content, encoding='utf-8')

            self.console.success(f"Breakdown marker created: {breakdown_marker.relative_to(self.project_root)}")
            self.console.info("Next: LLM will generate tasks from plan")

            return True

        except Exception as e:
            self.console.error(f"Task breakdown failed: {e}")
            return False

    def task_update(self, task_id: str, description: str, feature_id: Optional[str] = None) -> bool:
        """Update existing task"""
        try:
            if not feature_id:
                feature_id = self._detect_current_feature()

            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                return False

            task_dir = self.tasks_dir / feature_dir.name
            task_file = task_dir / f"task-{task_id}.md"

            if not task_file.exists():
                self.console.error(f"Task not found: {task_file}")
                return False

            content = task_file.read_text(encoding='utf-8')
            update_marker = f"""

---
## [UPDATE REQUEST - {datetime.now().isoformat()}]
{description}
---
"""
            content += update_marker
            task_file.write_text(content, encoding='utf-8')

            self.console.success(f"Update marker added: {task_file.relative_to(self.project_root)}")
            return True

        except Exception as e:
            self.console.error(f"Task update failed: {e}")
            return False

    def _get_next_task_number(self, task_dir: Path) -> int:
        """Get next available task number"""
        if not task_dir.exists():
            return 1

        tasks = list(task_dir.glob("task-*.md"))
        if not tasks:
            return 1

        max_num = 0
        for task_file in tasks:
            match = re.search(r'task-(\d{3})\.md', task_file.name)
            if match:
                max_num = max(max_num, int(match.group(1)))

        return max_num + 1

    def _detect_current_feature(self) -> Optional[str]:
        """Detect current feature"""
        context_file = self.memory_dir / "context.md"
        if not context_file.exists():
            return None

        content = context_file.read_text(encoding='utf-8')
        matches = re.findall(r'### Active Feature:.*?\n- Feature ID: (\d{3})', content)
        return matches[-1] if matches else None

    def _find_feature_dir(self, feature_id: str) -> Optional[Path]:
        """Find feature directory"""
        if not self.tasks_dir.exists():
            return None

        pattern = f"{feature_id}*"
        matches = list(self.tasks_dir.glob(pattern))
        return matches[0] if matches else None

    def task_list(self, **kwargs) -> bool:
        """
        List all tasks in the project with their status

        Returns:
            bool: Success status
        """
        try:
            self.console.info("Available tasks:")

            if not self.tasks_dir.exists():
                self.console.warning("  No tasks found (tasks directory doesn't exist)")
                return True

            # Get all feature directories
            features = sorted([
                d for d in self.tasks_dir.iterdir()
                if d.is_dir() and re.match(r'^\d{3}-', d.name)
            ])

            if not features:
                self.console.warning("  No tasks found")
                return True

            total_tasks = 0
            for feature in features:
                # Extract feature info
                match = re.match(r'^(\d{3})-(.+)$', feature.name)
                if match:
                    feature_id = match.group(1)
                    feature_name = match.group(2).replace('-', ' ').title()

                    # Count tasks
                    task_files = list(feature.glob("task-*.md"))
                    tasks_count = len(task_files)

                    if tasks_count > 0:
                        self.console.info(f"  {feature_id} - {feature_name}: {tasks_count} tasks")

                        # Show individual tasks
                        for task_file in sorted(task_files):
                            task_match = re.search(r'task-(\d{3})\.md', task_file.name)
                            if task_match:
                                task_num = task_match.group(1)
                                self.console.info(f"    - Task {task_num}: {task_file.name}")

                        total_tasks += tasks_count

            if total_tasks == 0:
                self.console.warning("  No tasks found")
            else:
                self.console.info(f"\nTotal: {total_tasks} tasks")

            return True

        except Exception as e:
            self.console.error(f"Failed to list tasks: {e}")
            return False


class ExecuteCommands:
    """Task execution tracking"""

    def __init__(self, console, project_root: Path):
        self.console = console
        self.project_root = project_root
        self.tasks_dir = project_root / "tasks"
        self.memory_dir = project_root / "memory"

    def execute_start(self, task_id: str, feature_id: Optional[str] = None) -> bool:
        """Mark task as started"""
        return self._update_task_status(task_id, "in_progress", feature_id)

    def execute_done(self, task_id: str, feature_id: Optional[str] = None) -> bool:
        """Mark task as completed"""
        return self._update_task_status(task_id, "completed", feature_id)

    def _update_task_status(self, task_id: str, status: str, feature_id: Optional[str]) -> bool:
        """Update task status"""
        try:
            if not feature_id:
                feature_id = self._detect_current_feature()

            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                self.console.error(f"Feature not found")
                return False

            task_dir = self.tasks_dir / feature_dir.name
            task_file = task_dir / f"task-{task_id}.md"

            if not task_file.exists():
                self.console.error(f"Task not found: {task_file}")
                return False

            content = task_file.read_text(encoding='utf-8')

            # Update status in metadata
            content = re.sub(
                r'<!-- STATUS: \w+ -->',
                f'<!-- STATUS: {status} -->',
                content
            )

            # Add timestamp
            timestamp_marker = f"\n<!-- {status.upper()}_AT: {datetime.now().isoformat()} -->\n"
            if timestamp_marker not in content:
                # Add after STATUS line
                content = re.sub(
                    r'(<!-- STATUS: \w+ -->)',
                    r'\1' + timestamp_marker,
                    content
                )

            task_file.write_text(content, encoding='utf-8')

            self.console.success(f"Task {task_id}: {status}")
            self.console.info(f"  File: {task_file.relative_to(self.project_root)}")

            return True

        except Exception as e:
            self.console.error(f"Status update failed: {e}")
            return False

    def _detect_current_feature(self) -> Optional[str]:
        """Detect current feature"""
        context_file = self.memory_dir / "context.md"
        if not context_file.exists():
            return None

        content = context_file.read_text(encoding='utf-8')
        matches = re.findall(r'### Active Feature:.*?\n- Feature ID: (\d{3})', content)
        return matches[-1] if matches else None

    def _find_feature_dir(self, feature_id: str) -> Optional[Path]:
        """Find feature directory"""
        if not self.tasks_dir.exists():
            return None

        pattern = f"{feature_id}*"
        matches = list(self.tasks_dir.glob(pattern))
        return matches[0] if matches else None

    def execute_status(self, target: Optional[str] = None, **kwargs) -> bool:
        """Show execution status of tasks"""
        try:
            self.console.info("Execution Status:")
            if not self.tasks_dir.exists():
                self.console.warning("  No tasks directory found")
                return True
            features = sorted([d for d in self.tasks_dir.iterdir() if d.is_dir() and re.match(r'^\d{3}-', d.name)])
            if not features:
                self.console.warning("  No tasks found")
                return True
            total_tasks = 0
            for feature in features:
                match = re.match(r'^(\d{3})-(.+)$', feature.name)
                if match:
                    feature_id = match.group(1)
                    feature_name = match.group(2).replace('-', ' ').title()
                    task_files = list(feature.glob("task-*.md"))
                    if task_files:
                        self.console.info(f"  {feature_id} - {feature_name}: {len(task_files)} tasks")
                        total_tasks += len(task_files)
            self.console.info(f"\nTotal: {total_tasks} tasks")
            return True
        except Exception as e:
            self.console.error(f"Failed to show execution status: {e}")
            return False

