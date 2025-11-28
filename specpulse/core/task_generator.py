"""
Standardized Task Generator for SpecPulse

This module provides standardized task generation functionality
with strict adherence to the new task format requirements.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .path_manager import PathManager
from ..utils.console import Console


class TaskGenerator:
    """
    Generates tasks using the standardized format with strict validation.
    Ensures all tasks follow the exact YAML structure requirements.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.path_manager = PathManager(project_root)
        self.console = Console()

        # Load standard template
        self.template_path = self.path_manager.get_template_file("task_standard.md")
        self.template_content = self.template_path.read_text(encoding='utf-8') if self.template_path.exists() else self._get_default_template()

    def create_standard_task(self, task_id: str, title: str, description: str,
                           files_touched: List[Dict[str, str]],
                           goals: List[str], success_criteria: List[str],
                           dependencies: List[str] = None,
                           next_tasks: List[str] = None,
                           risk_level: str = "medium",
                           risk_notes: str = "",
                           moscow: Dict[str, List[str]] = None,
                           priority_overall: str = "should",
                           priority_reason: str = "",
                           feature_id: Optional[str] = None,
                           feature_name: Optional[str] = None) -> str:
        """
        Create a standardized task with all required fields.

        Args:
            task_id: Task identifier (e.g., "task-001")
            title: Short and clear task title
            description: Detailed description answering the 4 key questions
            files_touched: List of files to be modified with reasons
            goals: List of concrete goals this task achieves
            success_criteria: List of measurable success criteria
            dependencies: List of task IDs this task depends on
            next_tasks: List of task IDs that depend on this task
            risk_level: Risk level (low, medium, high)
            risk_notes: Risk notes and edge cases
            moscow: MoSCoW breakdown dict
            priority_overall: Overall priority (must, should, could, wont)
            priority_reason: Reason for this priority level
            feature_id: Feature identifier
            feature_name: Feature name

        Returns:
            Generated task content as string
        """
        # Validate required fields
        self._validate_task_inputs(task_id, title, description, files_touched, goals, success_criteria)

        # Set defaults
        if dependencies is None:
            dependencies = []
        if next_tasks is None:
            next_tasks = []
        if moscow is None:
            moscow = {"must": [], "should": [], "know": [], "wont": []}

        # Create YAML frontmatter
        frontmatter = {
            "id": task_id,
            "status": "todo",
            "title": title,
            "description": description,
            "files_touched": files_touched,
            "goals": goals,
            "success_criteria": success_criteria,
            "dependencies": dependencies,
            "next_tasks": next_tasks,
            "risk_level": risk_level,
            "risk_notes": risk_notes,
            "moscow": moscow,
            "priority_overall": priority_overall,
            "priority_reason": priority_reason
        }

        # Generate content
        content = self._generate_task_content(frontmatter, feature_id, feature_name)

        return content

    def create_task_from_plan_item(self, plan_item: Dict[str, Any], task_number: int,
                                  feature_id: str, feature_name: str) -> str:
        """
        Create a task from an implementation plan item.

        Args:
            plan_item: Plan item dictionary
            task_number: Task number for ID generation
            feature_id: Feature identifier
            feature_name: Feature name

        Returns:
            Generated task content
        """
        task_id = f"task-{task_number:03d}"

        # Extract information from plan item
        title = plan_item.get("title", f"Task {task_number}")
        description = self._format_description_from_plan_item(plan_item)

        # Default files based on plan item
        files_touched = plan_item.get("files", [])

        # Extract goals from plan item
        goals = plan_item.get("goals", [f"Complete {title}"])

        # Extract success criteria from plan item
        success_criteria = plan_item.get("acceptance", [f"{title} is working correctly"])

        # Extract dependencies
        dependencies = plan_item.get("dependencies", [])

        # Determine risk level based on complexity
        complexity = plan_item.get("complexity", "medium")
        risk_mapping = {"simple": "low", "medium": "medium", "complex": "high", "xl": "high"}
        risk_level = risk_mapping.get(complexity, "medium")

        # Default MoSCoW based on priority
        priority = plan_item.get("priority", "medium")
        moscow = self._get_default_moscow(priority)

        priority_overall = self._map_priority_to_overall(priority)
        priority_reason = f"Priority based on plan item: {priority}"

        return self.create_standard_task(
            task_id=task_id,
            title=title,
            description=description,
            files_touched=files_touched,
            goals=goals,
            success_criteria=success_criteria,
            dependencies=dependencies,
            risk_level=risk_level,
            moscow=moscow,
            priority_overall=priority_overall,
            priority_reason=priority_reason,
            feature_id=feature_id,
            feature_name=feature_name
        )

    def save_task_to_file(self, task_content: str, task_id: str,
                         feature_id: str, feature_name: str) -> Path:
        """
        Save task content to the appropriate file.

        Args:
            task_content: Task content to save
            task_id: Task identifier
            feature_id: Feature identifier
            feature_name: Feature name

        Returns:
            Path to saved task file
        """
        # Create task file path
        task_dir = self.path_manager.get_feature_dir(feature_id, feature_name, 'tasks')
        task_file = task_dir / f"{task_id}.md"

        # Ensure directory exists
        task_dir.mkdir(parents=True, exist_ok=True)

        # Write task content
        task_file.write_text(task_content, encoding='utf-8')

        return task_file

    def validate_task_format(self, task_content: str) -> Dict[str, Any]:
        """
        Validate that task content follows the standardized format.

        Args:
            task_content: Task content to validate

        Returns:
            Validation result with details
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "missing_fields": []
        }

        try:
            # Split frontmatter and content
            if not task_content.startswith("---"):
                result["errors"].append("Task must start with YAML frontmatter")
                result["valid"] = False
                return result

            parts = task_content.split("---", 2)
            if len(parts) < 3:
                result["errors"].append("Invalid YAML frontmatter format")
                result["valid"] = False
                return result

            frontmatter_content = parts[1]
            main_content = parts[2]

            # Parse YAML frontmatter
            try:
                frontmatter = yaml.safe_load(frontmatter_content)
            except yaml.YAMLError as e:
                result["errors"].append(f"Invalid YAML syntax: {e}")
                result["valid"] = False
                return result

            # Check required fields
            required_fields = [
                "id", "status", "title", "description", "files_touched",
                "goals", "success_criteria", "dependencies", "next_tasks",
                "risk_level", "moscow", "priority_overall", "priority_reason"
            ]

            for field in required_fields:
                if field not in frontmatter:
                    result["missing_fields"].append(field)
                    result["valid"] = False

            # Validate field formats
            if "id" in frontmatter and not frontmatter["id"].startswith("task-"):
                result["warnings"].append("Task ID should start with 'task-'")

            if "status" in frontmatter and frontmatter["status"] not in ["todo", "in-progress", "blocked", "done"]:
                result["errors"].append("Invalid status value")
                result["valid"] = False

            if "risk_level" in frontmatter and frontmatter["risk_level"] not in ["low", "medium", "high"]:
                result["errors"].append("Invalid risk_level value")
                result["valid"] = False

            if "priority_overall" in frontmatter and frontmatter["priority_overall"] not in ["must", "should", "could", "wont"]:
                result["errors"].append("Invalid priority_overall value")
                result["valid"] = False

            # Validate MoSCoW structure
            if "moscow" in frontmatter:
                moscow_required = ["must", "should", "know", "wont"]
                for key in moscow_required:
                    if key not in frontmatter["moscow"]:
                        result["missing_fields"].append(f"moscow.{key}")
                        result["valid"] = False

            # Validate description format (should answer 4 questions)
            if "description" in frontmatter:
                desc = frontmatter["description"]
                if isinstance(desc, str):
                    desc_lower = desc.lower()
                    required_keywords = ["çözüyor", "gerekli", "nasıl", "zaman"]
                    missing_keywords = [kw for kw in required_keywords if kw not in desc_lower]
                    if missing_keywords:
                        result["warnings"].append(f"Description might be missing answers to: {', '.join(missing_keywords)}")

        except Exception as e:
            result["errors"].append(f"Validation error: {e}")
            result["valid"] = False

        return result

    # Private helper methods
    def _validate_task_inputs(self, task_id: str, title: str, description: str,
                            files_touched: List[Dict[str, str]],
                            goals: List[str], success_criteria: List[str]) -> None:
        """Validate required task inputs"""
        if not task_id or not task_id.startswith("task-"):
            raise ValueError("Task ID must start with 'task-'")

        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")

        if not description or len(description.strip()) == 0:
            raise ValueError("Description is required")

        if not files_touched:
            raise ValueError("At least one file must be specified")

        if not goals:
            raise ValueError("At least one goal must be specified")

        if not success_criteria:
            raise ValueError("At least one success criterion must be specified")

    def _format_description_from_plan_item(self, plan_item: Dict[str, Any]) -> str:
        """Format description from plan item following the 4-question format"""
        title = plan_item.get("title", "Task")
        description = plan_item.get("description", "")
        implementation = plan_item.get("implementation", "")

        formatted = f"""- **What problem does this solve?**: {title}

- **Why is this necessary?**: {description if description else "This task is an important part of the implementation plan"}

- **How will this be done?**: {implementation if implementation else "Step-by-step implementation according to plan details"}

- **When is this considered complete?**: When all acceptance criteria are met and tests pass"""

        return formatted

    def _get_default_moscow(self, priority: str) -> Dict[str, List[str]]:
        """Get default MoSCoW breakdown based on priority"""
        if priority == "high":
            return {
                "must": ["Core functionality implementation"],
                "should": ["Performance improvements"],
                "know": ["Domain knowledge and technical requirements"],
                "wont": ["Advanced features (future release)"]
            }
        elif priority == "medium":
            return {
                "must": ["Core functionality"],
                "should": ["User experience improvements"],
                "know": ["Technical implementation details"],
                "wont": ["Out-of-scope features"]
            }
        else:  # low
            return {
                "must": ["Minimum functionality"],
                "should": ["Basic tests"],
                "know": ["Required documentation"],
                "wont": ["Extra features"]
            }

    def _map_priority_to_overall(self, priority: str) -> str:
        """Map task priority to overall priority"""
        priority_mapping = {
            "high": "must",
            "medium": "should",
            "low": "could"
        }
        return priority_mapping.get(priority, "should")

    def _generate_task_content(self, frontmatter: Dict[str, Any],
                             feature_id: Optional[str] = None,
                             feature_name: Optional[str] = None) -> str:
        """Generate complete task content from frontmatter"""
        # Convert frontmatter to YAML string
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)

        # Add metadata section
        metadata_section = f"""
## Metadata

- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Feature:** {feature_name} ({feature_id}) if feature_id and feature_name else "N/A"
- **Type:** Implementation"""

        # Combine all parts
        content = f"---\n{yaml_content}---\n\n{metadata_section}"

        return content

    def _get_default_template(self) -> str:
        """Get default task template"""
        return """# {title}

**Task ID:** {task_id}
**Status:** {status}
**Priority:** {priority_overall}
**Risk Level:** {risk_level}

## Description

{description}

## Files to Touch

{files_touched_list}

## Goals

{goals_list}

## Success Criteria

{success_criteria_list}

## Dependencies

{dependencies_list}

## Next Tasks

{next_tasks_list}

## Risk Notes

{risk_notes}

## MoSCoW Breakdown

### Must Have (Olmazsa Olmaz)

{must_list}

### Should Have (Vakit El Verirse)

{should_list}

### Know (Bilinmesi Gereken)

{know_list}

### Won't Have (Kapsım Dışı)

{wont_list}

## Priority Reason

{priority_reason}

## Metadata

- **Created:** {created_date}
- **Updated:** {updated_date}
- **Feature:** {feature_name} ({feature_id})
- **Type:** {task_type}"""


__all__ = ['TaskGenerator']