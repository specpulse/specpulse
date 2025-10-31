"""
SpecPulse Template Manager - Enhanced template system with validation and versioning
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
import re
import yaml

# Template validation patterns for security
DANGEROUS_TEMPLATE_PATTERNS = [
    r'config\s*\.',                               # config attribute access
    r'env\s*\.',                                   # environment variable access
    r'request\s*\.',                               # request object access
    r'__\w+',                                      # dunder methods
    r'\.eval\s*\(',                               # eval method calls
    r'\.exec\s*\(',                               # exec method calls
    r'\.open\s*\(',                               # file open calls
    r'\.subprocess\s*\.',                          # subprocess access
    r'\.os\s*\.',                                  # os module access
    r'\.sys\s*\.',                                 # sys module access
    r'range\s*\(',                                 # range function (DoS)
    r'lipsum\s*\(',                                # lipsum function (DoS)
    r'cycler\s*\(',                                # cycler function
    r'joiner\s*\(',                                # joiner function
]

from ..utils.error_handler import (
    TemplateError, ValidationError, ErrorSeverity,
    validate_templates, suggest_recovery_for_error
)
from ..utils.console import Console
from ..utils.template_validator import TemplateValidator, ValidationResult


@dataclass
class TemplateMetadata:
    """Template metadata structure"""
    name: str
    version: str
    description: str
    category: str  # spec, plan, task, decomposition
    author: str
    created: str
    modified: str
    variables: List[str]
    sdd_principles: List[str]  # Which SDD principles this template enforces
    dependencies: List[str]  # Other templates this depends on
    tags: List[str]
    file_size: int = 0
    checksum: str = ""


@dataclass
class TemplateValidationResult:
    """Template validation result"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    missing_variables: List[str]
    extra_variables: List[str]
    sdd_compliance: Dict[str, bool]
    suggestions: List[str]


def validate_template_security(content: str) -> Tuple[bool, List[str]]:
    """
    Validate template content for security vulnerabilities.

    Args:
        content: Template content to validate

    Returns:
        Tuple of (is_safe, list_of_vulnerabilities)
    """
    vulnerabilities = []

    # Check dangerous patterns
    for pattern in DANGEROUS_TEMPLATE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL):
            vulnerabilities.append(f"Dangerous template pattern detected: {pattern}")

    # Check for excessive template complexity (DoS protection)
    lines = content.split('\n')
    if len(lines) > 1000:
        vulnerabilities.append("Template too large (potential DoS vector)")

    # Check for excessive variable usage
    var_count = len(re.findall(r'\{\{\s*\w+[\w\.]*\s*\}\}', content))
    if var_count > 200:
        vulnerabilities.append("Too many template variables (performance concern)")

    # Check for deep nesting using character count
    # Simple heuristic: count opening tags and closing tags
    opening_blocks = len(re.findall(r'\{\%\s*(if|for|block|macro|filter|with)', content))
    closing_blocks = len(re.findall(r'\{\%\s*end(if|for|block|macro|filter|with)?', content))

    # Estimate maximum nesting depth
    estimated_depth = max(0, opening_blocks - closing_blocks)

    # Also check for obvious deeply nested patterns
    if re.search(r'(\{\%\s*if.*\%\}){11,}', content) or opening_blocks > 10:
        vulnerabilities.append("Template nesting too deep (performance concern)")
    elif estimated_depth > 10:
        vulnerabilities.append("Template nesting too deep (performance concern)")

    is_safe = len(vulnerabilities) == 0
    return is_safe, vulnerabilities


class TemplateManager:
    """Enhanced template management system"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.templates_dir = project_root / "templates"
        self.template_registry = project_root / ".specpulse" / "template_registry.json"
        self.template_backup_dir = project_root / ".specpulse" / "template_backups"
        self.console = Console()

        # Ensure directories exist
        self.templates_dir.mkdir(exist_ok=True)
        self.template_registry.parent.mkdir(exist_ok=True)
        self.template_backup_dir.mkdir(exist_ok=True)

        # Initialize template registry
        self.registry = self._load_registry()

        # Initialize advanced template validator
        self.validator = TemplateValidator(strict_mode=False)

        # Standard template variables
        self.standard_variables = {
            "spec": [
                "feature_name", "spec_id", "date", "author", "ai_assistant",
                "executive_summary", "problem_statement", "proposed_solution"
            ],
            "plan": [
                "feature_name", "spec_id", "date", "optimization_focus",
                "architecture_pattern", "frontend_stack", "backend_stack",
                "database", "infrastructure", "team_size", "timeline"
            ],
            "task": [
                "feature_name", "spec_id", "date", "complexity",
                "estimated_hours", "team_members", "dependencies"
            ]
        }

        # SDD principle mappings
        self.sdd_principle_mappings = {
            "Specification First": ["functional_requirements", "acceptance_criteria", "user_stories"],
            "Incremental Planning": ["implementation_phases", "milestones", "checkpoints"],
            "Task Decomposition": ["tasks", "dependencies", "effort_estimates"],
            "Quality Assurance": ["testing_strategy", "quality_metrics", "acceptance_tests"],
            "Architecture Documentation": ["architecture_overview", "technical_decisions", "design_patterns"]
        }

    def _load_registry(self) -> Dict:
        """Load template registry from file"""
        if self.template_registry.exists():
            try:
                with open(self.template_registry, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.console.warning(f"Failed to load template registry: {e}")
                return {"templates": {}, "version": "1.0.0", "last_updated": datetime.now().isoformat()}
        else:
            return {"templates": {}, "version": "1.0.0", "last_updated": datetime.now().isoformat()}

    def _save_registry(self):
        """Save template registry to file"""
        self.registry["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.template_registry, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise TemplateError(f"Failed to save template registry: {e}")

    def _extract_variables(self, content: str) -> Set[str]:
        """Extract Jinja2 template variables from content"""
        # Find {{ variable_name }} patterns
        variables = set()
        pattern = r'\{\{\s*(\w+)\s*\}\}'
        matches = re.findall(pattern, content)
        variables.update(matches)

        # Find {% if variable %} patterns
        pattern = r'\{\%\s*if\s+(\w+)\s*\%\}'
        matches = re.findall(pattern, content)
        variables.update(matches)

        return variables

    def _calculate_checksum(self, content: str) -> str:
        """Calculate checksum for template content"""
        import hashlib
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _validate_template_variables(self, template_path: Path, metadata: TemplateMetadata) -> Tuple[List[str], List[str]]:
        """Validate template variables against standard variables"""
        content = template_path.read_text(encoding='utf-8')
        template_variables = self._extract_variables(content)

        # Determine template category from path
        category = self._get_template_category(template_path)

        if category in self.standard_variables:
            standard_vars = set(self.standard_variables[category])
            missing_vars = standard_vars - template_variables
            extra_vars = template_variables - standard_vars
        else:
            missing_vars = []
            extra_vars = list(template_variables)

        return list(missing_vars), list(extra_vars)

    def _get_template_category(self, template_path: Path) -> str:
        """Determine template category from path or content"""
        name = template_path.name.lower()
        if "spec" in name:
            return "spec"
        elif "plan" in name:
            return "plan"
        elif "task" in name:
            return "task"
        elif "decomposition" in name:
            return "decomposition"
        else:
            # Try to determine from content
            try:
                content = template_path.read_text(encoding='utf-8')
                if "Specification:" in content:
                    return "spec"
                elif "Implementation Plan:" in content:
                    return "plan"
                elif "Task Breakdown:" in content:
                    return "task"
            except:
                pass
            return "unknown"

    def _validate_sdd_compliance(self, template_path: Path) -> Dict[str, bool]:
        """Validate template compliance with SDD principles"""
        content = template_path.read_text(encoding='utf-8')
        compliance = {}

        for principle, keywords in self.sdd_principle_mappings.items():
            compliance[principle] = any(keyword.lower() in content.lower() for keyword in keywords)

        return compliance

    def validate_template(self, template_path: Path) -> TemplateValidationResult:
        """Comprehensive template validation"""
        if not template_path.exists():
            return TemplateValidationResult(
                valid=False,
                errors=[f"Template file not found: {template_path}"],
                warnings=[],
                missing_variables=[],
                extra_variables=[],
                sdd_compliance={},
                suggestions=["Check if template file exists in correct location"]
            )

        content = template_path.read_text(encoding='utf-8')

        # Use the advanced template validator
        validation_result = self.validator.validate_template(content, template_path)

        # Convert ValidationResult to the expected format
        errors = []
        warnings = []
        suggestions = []

        # Process validation issues
        for issue in validation_result.issues:
            message = issue.message
            if issue.line_number:
                message = f"Line {issue.line_number}: {message}"

            if issue.severity.value in ['critical', 'error']:
                errors.append(message)
            elif issue.severity.value == 'warning':
                warnings.append(message)
            else:  # info
                suggestions.append(message)

            # Add specific suggestions from issues
            if issue.suggestion:
                suggestions.append(issue.suggestion)

        # Add general suggestions from validation
        suggestions.extend(validation_result.suggestions)

        # Legacy variable extraction for compatibility
        variables = validation_result.variables
        category = self._get_template_category(template_path)

        # Check for required variables using legacy method for compatibility
        if category in self.standard_variables:
            standard_vars = set(self.standard_variables[category])
            missing_vars = standard_vars - variables
            extra_vars = variables - standard_vars

            if missing_vars:
                warnings.append(f"Missing standard variables: {', '.join(missing_vars)}")
                suggestions.append(f"Consider adding: {', '.join(missing_vars)}")

            if extra_vars:
                warnings.append(f"Extra variables not in standard set: {', '.join(extra_vars)}")

        # Legacy validation for backward compatibility
        # Validate Jinja2 syntax with secure environment
        try:
            from jinja2.sandbox import SandboxedEnvironment
            from jinja2 import meta

            # Use SandboxedEnvironment with autoescape for security
            env = SandboxedEnvironment(autoescape=True)
            env.parse(content)
        except Exception as e:
            errors.append(f"Jinja2 syntax error: {e}")
            suggestions.append("Check template syntax and variable formatting")

        # Check for required sections based on category
        required_sections = {
            "spec": ["## Specification:", "## Functional Requirements", "## Acceptance Criteria"],
            "plan": ["## Architecture Overview", "## Technology Stack", "## Implementation Phases"],
            "task": ["## Tasks", "### T001:", "## Progress Tracking"]
        }

        if category in required_sections:
            for section in required_sections[category]:
                if section not in content:
                    warnings.append(f"Missing recommended section: {section}")

        # Validate SDD compliance
        sdd_compliance = self._validate_sdd_compliance(template_path)

        return TemplateValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            missing_variables=list(missing_vars) if 'missing_vars' in locals() else [],
            extra_variables=list(extra_vars) if 'extra_vars' in locals() else [],
            sdd_compliance=sdd_compliance,
            suggestions=suggestions
        )

    def register_template(self, template_path: Path, metadata: Optional[TemplateMetadata] = None) -> bool:
        """Register a template in the registry"""
        try:
            if not template_path.exists():
                raise TemplateError(f"Template file not found: {template_path}")

            # Validate template first
            validation = self.validate_template(template_path)
            if not validation.valid:
                raise TemplateError(f"Template validation failed: {', '.join(validation.errors)}")

            # Auto-generate metadata if not provided
            if metadata is None:
                content = template_path.read_text(encoding='utf-8')
                category = self._get_template_category(template_path)
                variables = list(self._extract_variables(content))

                metadata = TemplateMetadata(
                    name=template_path.stem,
                    version="1.0.0",
                    description=f"Auto-generated {category} template",
                    category=category,
                    author="SpecPulse",
                    created=datetime.now().isoformat(),
                    modified=datetime.now().isoformat(),
                    variables=variables,
                    sdd_principles=list(self._validate_sdd_compliance(template_path).keys()),
                    dependencies=[],
                    tags=[category],
                    file_size=len(content),
                    checksum=self._calculate_checksum(content)
                )

            # Add to registry
            template_key = f"{metadata.category}/{metadata.name}"
            self.registry["templates"][template_key] = asdict(metadata)
            self._save_registry()

            self.console.success(f"Template registered: {template_key}")
            return True

        except Exception as e:
            self.console.error(f"Failed to register template: {e}")
            return False

    def backup_templates(self) -> str:
        """Create backup of all templates"""
        try:
            backup_name = f"templates_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path = self.template_backup_dir / backup_name
            backup_path.mkdir(exist_ok=True)

            # Copy all templates
            for template_file in self.templates_dir.rglob("*"):
                if template_file.is_file():
                    relative_path = template_file.relative_to(self.templates_dir)
                    backup_file = backup_path / relative_path
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(template_file, backup_file)

            # Copy registry
            registry_backup = backup_path / "template_registry.json"
            shutil.copy2(self.template_registry, registry_backup)

            self.console.success(f"Templates backed up to: {backup_path}")
            return str(backup_path)

        except Exception as e:
            raise TemplateError(f"Failed to backup templates: {e}")

    def restore_templates(self, backup_path: str) -> bool:
        """Restore templates from backup"""
        try:
            backup_dir = Path(backup_path)
            if not backup_dir.exists():
                raise TemplateError(f"Backup not found: {backup_path}")

            # Backup current templates first
            self.backup_templates()

            # Restore templates
            for backup_file in backup_dir.rglob("*"):
                if backup_file.is_file() and backup_file.name != "template_registry.json":
                    relative_path = backup_file.relative_to(backup_dir)
                    target_file = self.templates_dir / relative_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, target_file)

            # Restore registry if exists
            registry_backup = backup_dir / "template_registry.json"
            if registry_backup.exists():
                shutil.copy2(registry_backup, self.template_registry)
                self.registry = self._load_registry()

            self.console.success(f"Templates restored from: {backup_path}")
            return True

        except Exception as e:
            self.console.error(f"Failed to restore templates: {e}")
            return False

    def get_template_preview(self, template_path: Path, sample_data: Optional[Dict] = None) -> str:
        """Generate preview of template with sample data"""
        try:
            if not template_path.exists():
                raise TemplateError(f"Template not found: {template_path}")

            content = template_path.read_text(encoding='utf-8')

            # Provide sample data if not provided
            if sample_data is None:
                category = self._get_template_category(template_path)
                sample_data = self._get_sample_data(category)

            # Validate template with advanced validator before rendering
            validation_result = self.validator.validate_template(content, template_path)
            if not validation_result.is_safe:
                error_messages = [issue.message for issue in validation_result.critical_issues + validation_result.error_issues]
                raise TemplateError(f"Template contains security vulnerabilities: {'; '.join(error_messages)}")

            # Additional legacy security check for backward compatibility
            is_safe, vulnerabilities = validate_template_security(content)
            if not is_safe:
                raise TemplateError(f"Template contains security vulnerabilities: {'; '.join(vulnerabilities)}")

            # Render template with sample data using secure environment
            from jinja2.sandbox import SandboxedEnvironment
            from jinja2 import BaseLoader

            # Use SandboxedEnvironment with autoescape for maximum security
            env = SandboxedEnvironment(autoescape=True, loader=BaseLoader())
            template = env.from_string(content)
            rendered = template.render(**sample_data)

            return rendered

        except Exception as e:
            raise TemplateError(f"Failed to generate template preview: {e}")

    def _get_sample_data(self, category: str) -> Dict:
        """Get sample data for template preview"""
        base_data = {
            "feature_name": "User Authentication",
            "spec_id": "001",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "author": "Development Team",
            "ai_assistant": "Claude"
        }

        category_specific = {
            "spec": {
                "executive_summary": "Secure user authentication system",
                "problem_statement": "Users need to authenticate securely",
                "proposed_solution": "JWT-based authentication"
            },
            "plan": {
                "optimization_focus": "Security",
                "architecture_pattern": "Microservices",
                "frontend_stack": "React",
                "backend_stack": "Node.js",
                "database": "PostgreSQL",
                "infrastructure": "Docker",
                "team_size": "3",
                "timeline": "2 weeks"
            },
            "task": {
                "complexity": "Medium",
                "estimated_hours": "16",
                "team_members": "John, Jane",
                "dependencies": "Database schema"
            }
        }

        return {**base_data, **category_specific.get(category, {})}

    def list_templates(self, category: Optional[str] = None) -> List[Dict]:
        """List all registered templates"""
        templates = []
        for key, metadata in self.registry["templates"].items():
            if category is None or metadata["category"] == category:
                templates.append({"key": key, **metadata})
        return templates

    def get_template_info(self, template_key: str) -> Optional[Dict]:
        """Get detailed information about a specific template"""
        if template_key in self.registry["templates"]:
            return self.registry["templates"][template_key]
        return None

    def update_template_version(self, template_key: str, new_version: str, changes: str) -> bool:
        """Update template version with change log"""
        try:
            if template_key not in self.registry["templates"]:
                raise TemplateError(f"Template not found: {template_key}")

            metadata = self.registry["templates"][template_key]
            old_version = metadata["version"]

            # Backup before update
            self.backup_templates()

            # Update metadata
            metadata["version"] = new_version
            metadata["modified"] = datetime.now().isoformat()

            # Add change log entry
            if "change_log" not in metadata:
                metadata["change_log"] = []
            metadata["change_log"].append({
                "from_version": old_version,
                "to_version": new_version,
                "changes": changes,
                "date": datetime.now().isoformat()
            })

            self._save_registry()
            self.console.success(f"Template {template_key} updated to version {new_version}")
            return True

        except Exception as e:
            self.console.error(f"Failed to update template version: {e}")
            return False

    def validate_all_templates(self) -> Dict[str, TemplateValidationResult]:
        """Validate all registered templates"""
        results = {}
        template_dir = self.project_root / "templates"

        for template_file in template_dir.rglob("*.md"):
            relative_path = template_file.relative_to(template_dir)
            template_key = str(relative_path).replace("\\", "/")
            results[template_key] = self.validate_template(template_file)

        return results