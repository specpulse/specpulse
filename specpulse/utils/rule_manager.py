"""
Rule Manager for Custom Validation Rules.

Provides CRUD operations for managing validation rules.
"""
from pathlib import Path
from typing import List, Dict, Optional
import yaml

from ..core.custom_validation import ValidationRule, RuleEngine, RuleSeverity, ProjectType


class RuleManager:
    """
    Manages custom validation rules with CRUD operations.

    Provides a high-level interface for listing, enabling, disabling,
    and creating custom validation rules.
    """

    def __init__(self, rules_path: Optional[Path] = None):
        """
        Initialize RuleManager.

        Args:
            rules_path: Path to validation_rules.yaml (auto-detects if None)
        """
        self.engine = RuleEngine(rules_path)
        self.rules_path = self.engine.rules_path

    def list_rules(
        self,
        enabled_only: bool = False,
        project_type: Optional[ProjectType] = None
    ) -> List[ValidationRule]:
        """
        List all validation rules.

        Args:
            enabled_only: Only show enabled rules
            project_type: Filter by project type

        Returns:
            List of ValidationRule objects
        """
        return self.engine.list_rules(enabled_only, project_type)

    def enable_rule(self, rule_name: str) -> bool:
        """
        Enable a validation rule.

        Args:
            rule_name: Name of rule to enable

        Returns:
            True if successful, False if rule not found
        """
        success = self.engine.enable_rule(rule_name)
        if success:
            self.engine.save_rules()
        return success

    def disable_rule(self, rule_name: str) -> bool:
        """
        Disable a validation rule.

        Args:
            rule_name: Name of rule to disable

        Returns:
            True if successful, False if rule not found
        """
        success = self.engine.disable_rule(rule_name)
        if success:
            self.engine.save_rules()
        return success

    def add_custom_rule(
        self,
        name: str,
        message: str,
        applies_to: List[ProjectType],
        severity: RuleSeverity = RuleSeverity.WARNING,
        description: str = "",
        section: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        enabled: bool = False
    ) -> bool:
        """
        Add a new custom validation rule.

        Args:
            name: Unique rule identifier
            message: Error message
            applies_to: List of project types
            severity: ERROR, WARNING, or INFO
            description: Explanation of rule
            section: Section to check (optional)
            keywords: Keywords to look for (optional)
            enabled: Whether rule is enabled by default

        Returns:
            True if rule was added successfully
        """
        # Check if rule already exists
        if self.engine.get_rule(name):
            return False  # Rule already exists

        # Create new rule
        rule = ValidationRule(
            name=name,
            enabled=enabled,
            message=message,
            applies_to=applies_to,
            severity=severity,
            description=description,
            section=section,
            keywords=keywords
        )

        # Add to engine
        self.engine.rules.append(rule)

        # Save to file
        return self.engine.save_rules()

    def generate_rule_template(self) -> Dict[str, any]:
        """
        Generate a template for creating a new rule.

        Returns:
            Dictionary with rule template
        """
        return {
            "name": "my_custom_rule",
            "enabled": False,
            "message": "Description of what this rule checks",
            "applies_to": ["web-app", "api"],
            "severity": "warning",
            "description": "Detailed explanation of why this rule exists and what it checks for",
            "section": "Section Name",  # Optional
            "keywords": ["keyword1", "keyword2"]  # Optional
        }

    def validate_rule_structure(self, rule_dict: Dict) -> tuple[bool, Optional[str]]:
        """
        Validate that a rule dictionary has the correct structure.

        Args:
            rule_dict: Dictionary representing a rule

        Returns:
            Tuple of (is_valid: bool, error_message: Optional[str])
        """
        required_fields = ['name', 'enabled', 'message', 'applies_to', 'severity']

        for field in required_fields:
            if field not in rule_dict:
                return (False, f"Missing required field: {field}")

        # Validate field types
        if not isinstance(rule_dict['name'], str) or not rule_dict['name']:
            return (False, "Field 'name' must be a non-empty string")

        if not isinstance(rule_dict['enabled'], bool):
            return (False, "Field 'enabled' must be a boolean")

        if not isinstance(rule_dict['message'], str) or not rule_dict['message']:
            return (False, "Field 'message' must be a non-empty string")

        if not isinstance(rule_dict['applies_to'], list) or len(rule_dict['applies_to']) == 0:
            return (False, "Field 'applies_to' must be a non-empty list")

        # Validate severity
        valid_severities = ['error', 'warning', 'info']
        if rule_dict['severity'] not in valid_severities:
            return (False, f"Field 'severity' must be one of: {', '.join(valid_severities)}")

        # Validate project types
        valid_types = [pt.value for pt in ProjectType]
        for pt in rule_dict['applies_to']:
            if pt not in valid_types:
                return (False, f"Invalid project type: {pt}. Must be one of: {', '.join(valid_types)}")

        return (True, None)

    def get_rule_by_name(self, name: str) -> Optional[ValidationRule]:
        """
        Get a rule by name.

        Args:
            name: Rule name

        Returns:
            ValidationRule if found, None otherwise
        """
        return self.engine.get_rule(name)
