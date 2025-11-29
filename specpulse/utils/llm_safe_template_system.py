"""
LLM-SAFE Template System

This module provides a template system that prevents LLM from creating
arbitrary file names and structures while allowing content generation.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime
from .llm_safe_file_operations import LLMSafeFileOperations

class LLMSafeTemplateSystem:
    """
    LLM-safe template system with strict validation.

    This system ensures that:
    1. Templates cannot be modified by LLM
    2. File names are always validated
    3. Content can be generated safely
    4. Structure is always consistent
    """

    def __init__(self, project_root: Path):
        """
        Initialize template system.

        Args:
            project_root: Project root directory
        """
        self.file_ops = LLMSafeFileOperations(project_root)
        self.templates_dir = project_root / "specpulse" / "resources" / "templates"
        self.project_root = project_root

        # Pre-compiled validation patterns
        self.template_var_pattern = re.compile(r'\{\{([A-Z_]+)\}\}')
        self.directive_pattern = re.compile(r'<!--\s*(\w+):\s*([^-->]+)\s*-->')

    def load_template(self, template_name: str) -> str:
        """
        Load template with validation.

        Args:
            template_name: Name of template file (without path)

        Returns:
            Template content

        Raises:
            FileNotFoundError: If template doesn't exist
            ValueError: If template path is invalid
        """
        # Validate template name
        if not re.match(r'^[a-z0-9_-]+\.md$', template_name):
            raise ValueError(f"Invalid template name: {template_name}")

        template_path = self.templates_dir / template_name

        # Validate path is within templates directory
        try:
            template_path.relative_to(self.templates_dir)
        except ValueError:
            raise ValueError(f"Template path outside templates directory: {template_path}")

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        return template_path.read_text(encoding='utf-8')

    def extract_template_metadata(self, template_content: str) -> Dict[str, str]:
        """
        Extract metadata from template content.

        Looks for HTML comments like:
        <!-- TEMPLATE_TYPE: spec -->
        <!-- REQUIRED_VARS: FEATURE_ID,FEATURE_NAME -->
        <!-- DESCRIPTION: Feature specification template -->

        Args:
            template_content: Template content

        Returns:
            Dictionary of metadata
        """
        metadata = {
            "template_type": "unknown",
            "required_vars": [],
            "optional_vars": [],
            "description": "",
            "version": "1.0"
        }

        # Extract directives from content
        for match in self.directive_pattern.finditer(template_content):
            key = match.group(1).upper()
            value = match.group(2).strip()

            if key == "TEMPLATE_TYPE":
                metadata["template_type"] = value
            elif key == "REQUIRED_VARS":
                metadata["required_vars"] = [v.strip() for v in value.split(",")]
            elif key == "OPTIONAL_VARS":
                metadata["optional_vars"] = [v.strip() for v in value.split(",")]
            elif key == "DESCRIPTION":
                metadata["description"] = value
            elif key == "VERSION":
                metadata["version"] = value

        return metadata

    def validate_template_variables(self, template_content: str,
                                   provided_vars: Dict[str, str]) -> Tuple[bool, List[str]]:
        """
        Validate that all required template variables are provided.

        Args:
            template_content: Template content
            provided_vars: Variables provided by user/LLM

        Returns:
            Tuple of (is_valid, list_of_missing_variables)
        """
        metadata = self.extract_template_metadata(template_content)
        required_vars = metadata.get("required_vars", [])

        # Find all template variables in content
        content_vars = set(self.template_var_pattern.findall(template_content))

        # Check required variables
        missing_vars = []
        for var in required_vars:
            if var not in provided_vars and var in content_vars:
                missing_vars.append(var)

        return len(missing_vars) == 0, missing_vars

    def render_template_safe(self, template_name: str, variables: Dict[str, str],
                           validate_only: bool = False) -> Tuple[bool, str, Dict[str, str]]:
        """
        Render template with strict validation.

        Args:
            template_name: Template file name
            variables: Template variables
            validate_only: If True, only validate without rendering

        Returns:
            Tuple of (success, result_content_or_error, metadata)

        Raises:
            ValueError: If validation fails
        """
        try:
            # Load template
            template_content = self.load_template(template_name)
            metadata = self.extract_template_metadata(template_content)

            # Validate required variables
            is_valid, missing_vars = self.validate_template_variables(template_content, variables)
            if not is_valid:
                error_msg = f"Missing required variables: {', '.join(missing_vars)}"
                return False, error_msg, metadata

            # Sanitize variables
            sanitized_vars = self._sanitize_template_variables(variables, metadata)

            if validate_only:
                return True, "Template validation passed", metadata

            # Render template
            rendered_content = template_content
            for var_name, var_value in sanitized_vars.items():
                placeholder = f"{{{{{var_name}}}}}"
                rendered_content = rendered_content.replace(placeholder, str(var_value))

            # Add rendering metadata
            rendering_metadata = {
                "rendered_at": datetime.now().isoformat(),
                "template_name": template_name,
                "template_version": metadata.get("version", "1.0"),
                "variables_count": len(sanitized_vars)
            }

            return True, rendered_content, rendering_metadata

        except Exception as e:
            return False, f"Template rendering failed: {str(e)}", {}

    def _sanitize_template_variables(self, variables: Dict[str, str],
                                    metadata: Dict[str, str]) -> Dict[str, str]:
        """
        Sanitize template variables based on type.

        Args:
            variables: Raw variables
            metadata: Template metadata

        Returns:
            Sanitized variables
        """
        sanitized = {}

        # Common sanitizations
        for key, value in variables.items():
            if isinstance(value, str):
                # Remove potentially dangerous content
                value = value.strip()
                # Limit length for safety
                if len(value) > 10000:  # 10KB limit per variable
                    value = value[:10000] + "... [truncated]"

            sanitized[key] = value

        # Template-specific sanitizations
        template_type = metadata.get("template_type", "")

        if template_type == "spec":
            # Feature name sanitization
            if "FEATURE_NAME" in sanitized:
                sanitized["FEATURE_NAME"] = self.file_ops.sanitize_feature_name(
                    sanitized["FEATURE_NAME"]
                )

        return sanitized

    def create_specification_safe(self, feature_name: str, description: str,
                                additional_vars: Optional[Dict[str, str]] = None) -> Tuple[bool, str]:
        """
        Create specification with full validation.

        This is the ONLY approved way to create specifications.

        Args:
            feature_name: Feature name (will be sanitized)
            description: Specification description
            additional_vars: Additional template variables

        Returns:
            Tuple of (success, file_path_or_error_message)
        """
        try:
            # Create feature directories
            feature_id, created_dirs = self.file_ops.create_feature_directories(feature_name)
            feature_dir_name = f"{feature_id}-{self.file_ops.sanitize_feature_name(feature_name)}"

            # Generate spec file path
            spec_path = self.file_ops.generate_spec_file_path(feature_dir_name)

            # Prepare template variables
            variables = {
                "FEATURE_ID": feature_id,
                "FEATURE_NAME": self.file_ops.sanitize_feature_name(feature_name),
                "FEATURE_DIR": feature_dir_name,
                "SPEC_NUMBER": "001",
                "DESCRIPTION": description,
                "CREATED_AT": datetime.now().strftime("%Y-%m-%d"),
                "CREATED_BY": "LLM-Assisted"
            }

            # Add additional variables
            if additional_vars:
                variables.update(additional_vars)

            # Render template
            success, content, metadata = self.render_template_safe("spec.md", variables)
            if not success:
                return False, f"Template rendering failed: {content}"

            # Write file atomically
            self.file_ops.atomic_write_file(spec_path, content)

            return True, str(spec_path)

        except Exception as e:
            return False, f"Specification creation failed: {str(e)}"

    def create_plan_safe(self, feature_dir: str, plan_description: str,
                        additional_vars: Optional[Dict[str, str]] = None) -> Tuple[bool, str]:
        """
        Create implementation plan with full validation.

        Args:
            feature_dir: Feature directory name (must exist)
            plan_description: Plan description
            additional_vars: Additional template variables

        Returns:
            Tuple of (success, file_path_or_error_message)
        """
        try:
            # Validate feature directory
            if not self.file_ops.validate_feature_dir_name(feature_dir):
                return False, f"Invalid feature directory: {feature_dir}"

            # Generate plan file path
            plan_path = self.file_ops.generate_plan_file_path(feature_dir)

            # Extract feature info from directory name
            feature_id = feature_dir.split("-")[0]
            feature_name = "-".join(feature_dir.split("-")[1:])

            # Prepare template variables
            variables = {
                "FEATURE_ID": feature_id,
                "FEATURE_NAME": feature_name,
                "FEATURE_DIR": feature_dir,
                "PLAN_NUMBER": plan_path.stem.split("-")[1],
                "DESCRIPTION": plan_description,
                "CREATED_AT": datetime.now().strftime("%Y-%m-%d"),
                "CREATED_BY": "LLM-Assisted"
            }

            # Add additional variables
            if additional_vars:
                variables.update(additional_vars)

            # Render template
            success, content, metadata = self.render_template_safe("plan.md", variables)
            if not success:
                return False, f"Template rendering failed: {content}"

            # Write file atomically
            self.file_ops.atomic_write_file(plan_path, content)

            return True, str(plan_path)

        except Exception as e:
            return False, f"Plan creation failed: {str(e)}"

    def create_task_safe(self, feature_dir: str, task_description: str,
                        additional_vars: Optional[Dict[str, str]] = None,
                        service_prefix: Optional[str] = None) -> Tuple[bool, str]:
        """
        Create task with full validation.

        Args:
            feature_dir: Feature directory name
            task_description: Task description
            additional_vars: Additional template variables
            service_prefix: Optional service prefix for microservices

        Returns:
            Tuple of (success, file_path_or_error_message)
        """
        try:
            # Validate feature directory
            if not self.file_ops.validate_feature_dir_name(feature_dir):
                return False, f"Invalid feature directory: {feature_dir}"

            # Generate task file path
            task_path = self.file_ops.generate_task_file_path(
                feature_dir, service_prefix=service_prefix
            )

            # Extract feature info from directory name
            feature_id = feature_dir.split("-")[0]
            feature_name = "-".join(feature_dir.split("-")[1:])

            # Prepare template variables
            variables = {
                "FEATURE_ID": feature_id,
                "FEATURE_NAME": feature_name,
                "FEATURE_DIR": feature_dir,
                "TASK_NUMBER": task_path.stem.split("-")[-1].replace("T", ""),
                "TASK_PREFIX": f"{service_prefix}-" if service_prefix else "",
                "DESCRIPTION": task_description,
                "CREATED_AT": datetime.now().strftime("%Y-%m-%d"),
                "CREATED_BY": "LLM-Assisted",
                "STATUS": "pending"
            }

            # Add additional variables
            if additional_vars:
                variables.update(additional_vars)

            # Render template
            success, content, metadata = self.render_template_safe("task.md", variables)
            if not success:
                return False, f"Template rendering failed: {content}"

            # Write file atomically
            self.file_ops.atomic_write_file(task_path, content)

            return True, str(task_path)

        except Exception as e:
            return False, f"Task creation failed: {str(e)}"

    def list_templates(self) -> Dict[str, Dict[str, str]]:
        """
        List all available templates with metadata.

        Returns:
            Dictionary of template_name -> metadata
        """
        templates = {}

        if not self.templates_dir.exists():
            return templates

        for template_file in self.templates_dir.glob("*.md"):
            try:
                content = template_file.read_text(encoding='utf-8')
                metadata = self.extract_template_metadata(content)
                templates[template_file.name] = metadata
            except Exception:
                # Skip invalid templates
                continue

        return templates


# Singleton instance for easy access
_template_system = None

def get_template_system(project_root: Path) -> LLMSafeTemplateSystem:
    """Get or create template system instance."""
    global _template_system
    if _template_system is None or _template_system.project_root != Path(project_root).resolve():
        _template_system = LLMSafeTemplateSystem(project_root)
    return _template_system