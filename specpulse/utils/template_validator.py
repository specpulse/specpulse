"""
Template Content Validator - Advanced security and content validation for templates
"""

import re
import yaml
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from .error_handler import TemplateError, ValidationError


class ValidationSeverity(Enum):
    """Severity levels for validation issues"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class TemplateCategory(Enum):
    """Template categories for different validation rules"""
    SPEC = "spec"
    PLAN = "plan"
    TASK = "task"
    DECOMPOSITION = "decomposition"
    UNKNOWN = "unknown"


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: ValidationSeverity
    category: str
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete template validation result"""
    is_valid: bool
    is_safe: bool
    issues: List[ValidationIssue]
    variables: Set[str]
    metadata: Dict[str, Any]
    suggestions: List[str]

    @property
    def critical_issues(self) -> List[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == ValidationSeverity.CRITICAL]

    @property
    def error_issues(self) -> List[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == ValidationSeverity.ERROR]

    @property
    def warning_issues(self) -> List[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == ValidationSeverity.WARNING]


class TemplateValidator:
    """Advanced template validator with comprehensive security and content checks"""

    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode

        # Security patterns - expanded from T001
        self.security_patterns = {
            'config_access': [
                r'config\s*\.',
                r'config\s*\[',
                r'config\s*\(',
            ],
            'environment_access': [
                r'env\s*\.',
                r'env\s*\[',
                r'env\s*\(',
                r'environ\s*\.',
                r'os\.environ',
            ],
            'dangerous_functions': [
                r'eval\s*\(',
                r'exec\s*\(',
                r'compile\s*\(',
                r'__import__\s*\(',
                r'open\s*\(',
                r'file\s*\(',
                r'input\s*\(',
                r'raw_input\s*\(',
            ],
            'module_access': [
                r'__builtins__',
                r'__globals__',
                r'__locals__',
                r'__dict__',
                r'__class__',
                r'__bases__',
                r'__subclasses__',
                r'__mro__',
            ],
            'file_system': [
                r'\.subprocess\s*\.',
                r'\.os\s*\.',
                r'\.sys\s*\.',
                r'\.path\s*\.',
                r'\.io\s*\.',
                r'\.shutil\s*\.',
            ],
            'network': [
                r'\.urllib\s*\.',
                r'\.requests\s*\.',
                r'\.http\s*\.',
                r'\.socket\s*\.',
                r'\.ftplib\s*\.',
            ],
            'code_execution': [
                r'range\s*\(',  # Potential DoS
                r'lipsum\s*\(',  # Jinja2 DoS function
                r'cycler\s*\(',
                r'joiner\s*\(',
            ],
        }

        # Content quality patterns
        self.quality_patterns = {
            'empty_sections': [
                r'^#+\s*$\s*^#+\s*$',
                r'^\s*$\s*^#+\s*$',
            ],
            'missing_metadata': [
                r'<!--\s*FEATURE_DIR:\s*-->',
                r'<!--\s*FEATURE_ID:\s*-->',
            ],
            'inconsistent_formatting': [
                r'\r\n',  # Windows line endings
                r'\t',    # Tabs (should use spaces)
            ],
        }

        # Required variables by category
        self.required_variables = {
            TemplateCategory.SPEC: {
                'feature_name', 'spec_id', 'date'
            },
            TemplateCategory.PLAN: {
                'feature_name', 'plan_id', 'date'
            },
            TemplateCategory.TASK: {
                'task_name', 'task_id', 'date'
            },
            TemplateCategory.DECOMPOSITION: {
                'feature_name', 'component_name', 'date'
            }
        }

        # Optional recommended variables
        self.recommended_variables = {
            TemplateCategory.SPEC: {
                'author', 'ai_assistant', 'priority', 'complexity'
            },
            TemplateCategory.PLAN: {
                'author', 'estimated_time', 'dependencies', 'risks'
            },
            TemplateCategory.TASK: {
                'assignee', 'estimated_hours', 'acceptance_criteria'
            },
            TemplateCategory.DECOMPOSITION: {
                'technologies', 'interfaces', 'data_flow'
            }
        }

    def validate_template(self, content: str, template_path: Optional[Path] = None) -> ValidationResult:
        """
        Validate template content comprehensively

        Args:
            content: Template content to validate
            template_path: Optional path for context

        Returns:
            ValidationResult with comprehensive analysis
        """
        issues = []
        variables = self._extract_variables(content)
        metadata = self._extract_metadata(content, template_path)
        suggestions = []

        # Security validation
        security_issues, security_suggestions = self._validate_security(content)
        issues.extend(security_issues)
        suggestions.extend(security_suggestions)

        # Content quality validation
        quality_issues, quality_suggestions = self._validate_quality(content)
        issues.extend(quality_issues)
        suggestions.extend(quality_suggestions)

        # Structure validation
        structure_issues, structure_suggestions = self._validate_structure(content, template_path)
        issues.extend(structure_issues)
        suggestions.extend(structure_suggestions)

        # Variable validation
        variable_issues, variable_suggestions = self._validate_variables(content, variables, template_path)
        issues.extend(variable_issues)
        suggestions.extend(variable_suggestions)

        # Determine validity and safety
        is_safe = not any(issue.severity in [ValidationSeverity.CRITICAL, ValidationSeverity.ERROR]
                        for issue in issues if 'security' in issue.category.lower())

        # For non-strict mode, allow warnings but not critical/error issues
        if not self.strict_mode:
            is_valid = not any(issue.severity in [ValidationSeverity.CRITICAL, ValidationSeverity.ERROR]
                              for issue in issues)
        else:
            # Strict mode: no issues allowed
            is_valid = len(issues) == 0

        # Special case: very short templates should not be valid even if no critical errors
        if len(content.strip()) < 50 and content.strip():
            is_valid = False
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="structure_too_short",
                message="Template is too short to be useful",
                suggestion="Add more comprehensive content"
            ))

        return ValidationResult(
            is_valid=is_valid,
            is_safe=is_safe,
            issues=issues,
            variables=variables,
            metadata=metadata,
            suggestions=list(set(suggestions))  # Remove duplicates
        )

    def _validate_security(self, content: str) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate security aspects of template"""
        issues = []
        suggestions = []

        for category, patterns in self.security_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1

                    severity = ValidationSeverity.CRITICAL if category in ['config_access', 'environment_access', 'dangerous_functions'] else ValidationSeverity.ERROR

                    issues.append(ValidationIssue(
                        severity=severity,
                        category=f"security_{category}",
                        message=f"Potentially dangerous {category.replace('_', ' ')} detected",
                        line_number=line_num,
                        suggestion=f"Remove or replace {category.replace('_', ' ')} usage"
                    ))

        # Additional security checks
        if len(content.split('\n')) > 1000:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="security_dos",
                message="Template too large (potential DoS vector)",
                suggestion="Break template into smaller components"
            ))

        var_count = len(re.findall(r'\{\{\s*\w+[\w\.]*\s*\}\}', content))
        if var_count > 200:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="security_performance",
                message="Too many template variables (performance concern)",
                suggestion="Consider simplifying template logic"
            ))

        return issues, suggestions

    def _validate_quality(self, content: str) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate content quality aspects"""
        issues = []
        suggestions = []

        # Check for empty sections
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip() == '' and i > 1 and i < len(lines):
                prev_line = lines[i-2].strip()
                next_line = lines[i].strip() if i < len(lines) else ''

                if (prev_line.startswith('#') and next_line.startswith('#')) or \
                   (prev_line == '' and next_line.startswith('#')):
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="quality_empty_section",
                        message="Empty section detected between headers",
                        line_number=i,
                        suggestion="Add content to empty section or remove empty lines"
                    ))

        # Check for formatting issues
        if '\r\n' in content:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.INFO,
                category="quality_formatting",
                message="Windows line endings detected",
                suggestion="Use Unix line endings (LF) for consistency"
            ))

        if '\t' in content:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.INFO,
                category="quality_formatting",
                message="Tab characters detected",
                suggestion="Use spaces for indentation (2 or 4 spaces)"
            ))

        return issues, suggestions

    def _validate_structure(self, content: str, template_path: Optional[Path] = None) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate template structure"""
        issues = []
        suggestions = []

        # Basic structure checks
        if not content.strip():
            issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                category="structure_empty",
                message="Template is empty",
                suggestion="Add template content"
            ))
            return issues, suggestions

        if len(content.strip()) < 50:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="structure_too_short",
                message="Template seems too short",
                suggestion="Add more comprehensive content"
            ))

        # Check for required metadata comments
        if template_path:
            category = self._detect_category(template_path, content)

            if category in [TemplateCategory.SPEC, TemplateCategory.PLAN, TemplateCategory.TASK]:
                required_metadata = ['FEATURE_DIR', 'FEATURE_ID']

                for meta in required_metadata:
                    pattern = f'<!--\\s*{meta}:\\s*[^>]+-->'
                    if not re.search(pattern, content, re.IGNORECASE):
                        issues.append(ValidationIssue(
                            severity=ValidationSeverity.WARNING,
                            category="structure_metadata",
                            message=f"Missing required metadata: {meta}",
                            suggestion=f"Add <!-- {meta}: VALUE --> comment to template"
                        ))

        # Check for markdown structure
        if not re.search(r'^#+\s+', content, re.MULTILINE):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="structure_headers",
                message="No markdown headers detected",
                suggestion="Add proper markdown headers for structure"
            ))

        return issues, suggestions

    def _validate_variables(self, content: str, variables: Set[str], template_path: Optional[Path] = None) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate template variables"""
        issues = []
        suggestions = []

        if template_path:
            category = self._detect_category(template_path, content)

            # Check required variables
            if category in self.required_variables:
                missing_vars = self.required_variables[category] - variables
                for var in missing_vars:
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="variables_missing",
                        message=f"Missing required variable: {var}",
                        suggestion=f"Add {{{{ {var} }}}} to template"
                    ))

            # Check recommended variables
            if category in self.recommended_variables:
                missing_recommended = self.recommended_variables[category] - variables
                if missing_recommended:
                    suggestions.append(f"Consider adding recommended variables: {', '.join(missing_recommended)}")

        # Check for unused variables (variables mentioned in comments but not used)
        commented_vars = set(re.findall(r'{{\s*(\w+[\w\.]*)\s*}}', re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)))
        unused_vars = commented_vars - variables

        if unused_vars:
            suggestions.append(f"Unused variables detected: {', '.join(unused_vars)}")

        return issues, suggestions

    def _extract_variables(self, content: str) -> Set[str]:
        """Extract all template variables from content"""
        # Remove comments first
        content_no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        # Find variables in {{ }} blocks
        variables = set(re.findall(r'{{\s*(\w+[\w\.]*)\s*}}', content_no_comments))

        return variables

    def _extract_metadata(self, content: str, template_path: Optional[Path] = None) -> Dict[str, Any]:
        """Extract metadata from template"""
        metadata = {}

        # Extract HTML comment metadata
        meta_pattern = r'<!--\s*(\w+):\s*([^>]*)\s*-->'
        for match in re.finditer(meta_pattern, content, re.IGNORECASE):
            key, value = match.groups()
            metadata[key.lower()] = value.strip()

        # Add file metadata
        if template_path:
            metadata['file_name'] = template_path.name
            metadata['file_size'] = len(content.encode('utf-8'))
            metadata['category'] = self._detect_category(template_path, content).value

        return metadata

    def _detect_category(self, template_path: Path, content: str) -> TemplateCategory:
        """Detect template category from path or content"""
        # Try to detect from file path first
        path_lower = str(template_path).lower()
        if 'spec' in path_lower:
            return TemplateCategory.SPEC
        elif 'plan' in path_lower:
            return TemplateCategory.PLAN
        elif 'task' in path_lower:
            return TemplateCategory.TASK
        elif 'decomposition' in path_lower:
            return TemplateCategory.DECOMPOSITION

        # Try to detect from content
        content_lower = content.lower()
        if any(word in content_lower for word in ['specification', 'functional requirements', 'technical spec']):
            return TemplateCategory.SPEC
        elif any(word in content_lower for word in ['implementation plan', 'project plan', 'sprint plan']):
            return TemplateCategory.PLAN
        elif any(word in content_lower for word in ['task', 'action item', 'todo']):
            return TemplateCategory.TASK
        elif any(word in content_lower for word in ['decomposition', 'component', 'microservice']):
            return TemplateCategory.DECOMPOSITION

        return TemplateCategory.UNKNOWN

    def validate_user_template(self, content: str, user_context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate user-provided templates with additional context

        Args:
            content: User-provided template content
            user_context: Additional context about the user/template

        Returns:
            ValidationResult with user-specific validations
        """
        result = self.validate_template(content)

        # Additional user-specific validations
        if user_context:
            # Check for user-specific restrictions
            if user_context.get('is_beginner', False):
                # More strict validation for beginners
                for issue in result.issues:
                    if issue.severity == ValidationSeverity.WARNING:
                        issue.severity = ValidationSeverity.ERROR

            # Check organization-specific patterns
            org_patterns = user_context.get('organization_patterns', [])
            for pattern in org_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    result.issues.append(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        category="organization_policy",
                        message=f"Template violates organization policy: {pattern}",
                        suggestion="Follow organization template guidelines"
                    ))
                    # Mark as invalid immediately
                    result.is_valid = False

        return result