"""
Custom Validation Rule Engine for SpecPulse.

Provides project-specific validation rules that adapt based on project type.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Callable
import yaml


class RuleSeverity(Enum):
    """Severity level for validation rules."""
    ERROR = "error"      # Validation fails
    WARNING = "warning"  # Warning shown but validation passes
    INFO = "info"        # Informational message only


class ProjectType(Enum):
    """Supported project types for rule filtering."""
    WEB_APP = "web-app"
    API = "api"
    MOBILE_APP = "mobile-app"
    DESKTOP = "desktop"
    CLI = "cli"
    LIBRARY = "library"
    UNKNOWN = "unknown"


@dataclass
class ValidationRule:
    """
    Custom validation rule for project-specific checks.

    Attributes:
        name: Unique rule identifier (e.g., 'security_requirement')
        enabled: Whether this rule is active
        message: Error message shown when rule fails
        applies_to: List of project types this rule applies to
        severity: ERROR, WARNING, or INFO
        description: Explanation of why this rule exists
        section: Which spec section to check (optional)
        keywords: List of keywords that trigger this rule (optional)
    """
    name: str
    enabled: bool
    message: str
    applies_to: List[ProjectType]
    severity: RuleSeverity
    description: str = ""
    section: Optional[str] = None
    keywords: Optional[List[str]] = None

    def matches_project_type(self, project_type: ProjectType) -> bool:
        """Check if this rule applies to the given project type."""
        return project_type in self.applies_to

    def check(self, spec_content: str) -> bool:
        """
        Check if this rule is satisfied.

        Args:
            spec_content: Full specification content

        Returns:
            True if rule is satisfied, False if violated
        """
        # If rule specifies a section, check if section exists
        if self.section:
            section_marker = f"## {self.section}"
            if section_marker not in spec_content:
                return False

        # If rule specifies keywords, check if any are present
        if self.keywords:
            content_lower = spec_content.lower()
            keywords_found = any(keyword.lower() in content_lower for keyword in self.keywords)
            if not keywords_found:
                return False

        # If we got here, rule is satisfied
        return True


class RuleEngine:
    """
    Engine for loading, filtering, and executing custom validation rules.

    The RuleEngine loads rules from YAML configuration, filters them by
    project type, and executes them against specifications.
    """

    def __init__(self, rules_path: Optional[Path] = None):
        """
        Initialize RuleEngine.

        Args:
            rules_path: Path to validation_rules.yaml (auto-detects if None)
        """
        self.rules_path = rules_path
        self.rules: List[ValidationRule] = []
        self._load_rules()

    def _load_rules(self):
        """Load rules from YAML file."""
        if self.rules_path is None:
            # Auto-detect rules file
            # Try .specpulse/validation_rules.yaml first (project-specific)
            project_rules = Path.cwd() / ".specpulse" / "validation_rules.yaml"
            if project_rules.exists():
                self.rules_path = project_rules
            else:
                # Fall back to default rules in resources
                current_file = Path(__file__)
                resources_dir = current_file.parent.parent / "resources"
                self.rules_path = resources_dir / "validation_rules.yaml"

        if not self.rules_path or not self.rules_path.exists():
            # No rules file found - that's okay, just no custom rules
            return

        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)

            # Parse rules from YAML
            rules_data = yaml_data.get('rules', [])

            for rule_data in rules_data:
                # Convert project types from strings to enums
                applies_to_str = rule_data.get('applies_to', [])
                applies_to = []
                for pt_str in applies_to_str:
                    try:
                        applies_to.append(ProjectType(pt_str))
                    except ValueError:
                        # Unknown project type, skip
                        pass

                # Convert severity from string to enum
                severity_str = rule_data.get('severity', 'warning')
                try:
                    severity = RuleSeverity(severity_str)
                except ValueError:
                    severity = RuleSeverity.WARNING

                # Create ValidationRule
                rule = ValidationRule(
                    name=rule_data.get('name', ''),
                    enabled=rule_data.get('enabled', False),
                    message=rule_data.get('message', ''),
                    applies_to=applies_to,
                    severity=severity,
                    description=rule_data.get('description', ''),
                    section=rule_data.get('section'),
                    keywords=rule_data.get('keywords')
                )

                self.rules.append(rule)

        except Exception as e:
            # Log error but don't crash
            print(f"Warning: Failed to load custom rules: {e}")

    def filter_by_project_type(self, project_type: ProjectType) -> List[ValidationRule]:
        """
        Filter rules by project type.

        Args:
            project_type: Project type to filter by

        Returns:
            List of rules that apply to this project type
        """
        return [
            rule for rule in self.rules
            if rule.enabled and rule.matches_project_type(project_type)
        ]

    def execute_rules(
        self,
        spec_content: str,
        project_type: ProjectType
    ) -> List[Dict[str, any]]:
        """
        Execute all applicable rules against a specification.

        Args:
            spec_content: Full specification content
            project_type: Type of project being validated

        Returns:
            List of rule violations (empty if all rules pass)
        """
        violations = []

        # Get rules that apply to this project type
        applicable_rules = self.filter_by_project_type(project_type)

        for rule in applicable_rules:
            # Check if rule is satisfied
            if not rule.check(spec_content):
                violations.append({
                    "rule": rule.name,
                    "message": rule.message,
                    "severity": rule.severity.value,
                    "description": rule.description,
                    "section": rule.section
                })

        return violations

    def get_rule(self, rule_name: str) -> Optional[ValidationRule]:
        """
        Get a specific rule by name.

        Args:
            rule_name: Name of the rule

        Returns:
            ValidationRule if found, None otherwise
        """
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        return None

    def enable_rule(self, rule_name: str) -> bool:
        """
        Enable a rule by name.

        Args:
            rule_name: Name of rule to enable

        Returns:
            True if rule was found and enabled, False otherwise
        """
        rule = self.get_rule(rule_name)
        if rule:
            rule.enabled = True
            return True
        return False

    def disable_rule(self, rule_name: str) -> bool:
        """
        Disable a rule by name.

        Args:
            rule_name: Name of rule to disable

        Returns:
            True if rule was found and disabled, False otherwise
        """
        rule = self.get_rule(rule_name)
        if rule:
            rule.enabled = False
            return True
        return False

    def list_rules(
        self,
        enabled_only: bool = False,
        project_type: Optional[ProjectType] = None
    ) -> List[ValidationRule]:
        """
        List all rules, optionally filtered.

        Args:
            enabled_only: If True, only return enabled rules
            project_type: If provided, only return rules for this project type

        Returns:
            List of ValidationRule objects
        """
        rules = self.rules

        if enabled_only:
            rules = [r for r in rules if r.enabled]

        if project_type:
            rules = [r for r in rules if r.matches_project_type(project_type)]

        return rules

    def save_rules(self) -> bool:
        """
        Save current rules back to YAML file.

        Returns:
            True if successful, False otherwise
        """
        if not self.rules_path:
            return False

        try:
            # Read current YAML to preserve structure
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)

            # Update rules in YAML data
            rules_list = []
            for rule in self.rules:
                rule_dict = {
                    'name': rule.name,
                    'enabled': rule.enabled,
                    'message': rule.message,
                    'applies_to': [pt.value for pt in rule.applies_to],
                    'severity': rule.severity.value,
                    'description': rule.description
                }

                if rule.section:
                    rule_dict['section'] = rule.section
                if rule.keywords:
                    rule_dict['keywords'] = rule.keywords

                rules_list.append(rule_dict)

            yaml_data['rules'] = rules_list

            # Write back to file
            with open(self.rules_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True)

            return True

        except Exception as e:
            print(f"Error saving rules: {e}")
            return False
