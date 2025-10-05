"""
SpecPulse Validation Rules - Comprehensive validation rules for SDD compliance
"""

from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
import re
from dataclasses import dataclass


class ValidationSeverity(Enum):
    """Validation severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationCategory(Enum):
    """Validation categories"""
    STRUCTURE = "structure"
    CONTENT = "content"
    SDD_COMPLIANCE = "sdd_compliance"
    FORMATTING = "formatting"
    NAMING = "naming"
    CROSS_REFERENCE = "cross_reference"


@dataclass
class ValidationResult:
    """Validation result with detailed information"""
    status: str
    message: str
    severity: ValidationSeverity
    category: ValidationCategory
    suggestion: Optional[str] = None
    location: Optional[str] = None
    auto_fixable: bool = False
    fix_action: Optional[str] = None


class ValidationRule:
    """Base class for validation rules"""

    def __init__(self, name: str, description: str, severity: ValidationSeverity,
                 category: ValidationCategory, auto_fixable: bool = False):
        self.name = name
        self.description = description
        self.severity = severity
        self.category = category
        self.auto_fixable = auto_fixable

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        """Validate content against this rule"""
        raise NotImplementedError

    def fix(self, content: str, file_path: Path) -> Tuple[str, bool]:
        """Auto-fix content if possible"""
        return content, False


class SpecValidationRule(ValidationRule):
    """Base class for specification validation rules"""

    def __init__(self, name: str, description: str, severity: ValidationSeverity,
                 auto_fixable: bool = False):
        super().__init__(name, description, severity,
                        ValidationCategory.CONTENT, auto_fixable)


class PlanValidationRule(ValidationRule):
    """Base class for plan validation rules"""

    def __init__(self, name: str, description: str, severity: ValidationSeverity,
                 auto_fixable: bool = False):
        super().__init__(name, description, severity,
                        ValidationCategory.CONTENT, auto_fixable)


class TaskValidationRule(ValidationRule):
    """Base class for task validation rules"""

    def __init__(self, name: str, description: str, severity: ValidationSeverity,
                 auto_fixable: bool = False):
        super().__init__(name, description, severity,
                        ValidationCategory.CONTENT, auto_fixable)


# === SPECIFICATION VALIDATION RULES ===

class RequiredSectionsRule(SpecValidationRule):
    """Validate that required sections are present"""

    def __init__(self):
        super().__init__(
            "required_sections",
            "All required sections must be present",
            ValidationSeverity.ERROR,
            auto_fixable=True
        )
        self.required_sections = {
            "spec": [
                "## Specification:",
                "## Metadata",
                "## Functional Requirements",
                "## User Stories",
                "## Acceptance Criteria"
            ],
            "plan": [
                "## Architecture Overview",
                "## Technology Stack",
                "## Implementation Phases",
                "## Risk Management"
            ],
            "task": [
                "## Tasks",
                "### T001:",
                "## Progress Tracking"
            ]
        }

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        results = []
        file_type = self._detect_file_type(file_path)

        if file_type in self.required_sections:
            required = self.required_sections[file_type]
            missing = []

            for section in required:
                if section not in content:
                    missing.append(section)

            if missing:
                results.append(ValidationResult(
                    status="missing_sections",
                    message=f"Missing required sections: {', '.join(missing)}",
                    severity=self.severity,
                    category=self.category,
                    suggestion=f"Add missing sections to your {file_type}",
                    location=str(file_path),
                    auto_fixable=self.auto_fixable,
                    fix_action="add_missing_sections"
                ))

        return results

    def _detect_file_type(self, file_path: Path) -> Optional[str]:
        """Detect file type from path"""
        name = file_path.name.lower()
        if "spec" in name:
            return "spec"
        elif "plan" in name:
            return "plan"
        elif "task" in name:
            return "task"
        return None

    def fix(self, content: str, file_path: Path) -> Tuple[str, bool]:
        """Add missing sections"""
        file_type = self._detect_file_type(file_path)
        if not file_type or file_type not in self.required_sections:
            return content, False

        missing_sections = []
        for section in self.required_sections[file_type]:
            if section not in content:
                missing_sections.append(section)

        if not missing_sections:
            return content, False

        # Add missing sections at the end
        for section in missing_sections:
            content += f"\n\n{section}\n[To be completed]\n"

        return content, True


class ClarificationMarkerRule(SpecValidationRule):
    """Validate clarification markers are properly formatted"""

    def __init__(self):
        super().__init__(
            "clarification_markers",
            "Clarification markers should be properly formatted",
            ValidationSeverity.WARNING,
            auto_fixable=True
        )

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        results = []

        # Check for various clarification marker formats
        invalid_formats = [
            (r'\[needs clarification\]', '[NEEDS CLARIFICATION]'),
            (r'\[Needs Clarification\]', '[NEEDS CLARIFICATION]'),
            (r'needs clarification', '[NEEDS CLARIFICATION]'),
            (r'Needs Clarification', '[NEEDS CLARIFICATION]')
        ]

        for pattern, correct_format in invalid_formats:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                results.append(ValidationResult(
                    status="invalid_clarification_format",
                    message=f"Invalid clarification format at position {match.start()}: {match.group()}",
                    severity=self.severity,
                    category=ValidationCategory.FORMATTING,
                    suggestion=f"Use format: {correct_format}",
                    location=f"{file_path}:{match.start()}",
                    auto_fixable=self.auto_fixable,
                    fix_action="fix_clarification_format"
                ))

        # Count total clarifications needed
        total_clarifications = len(re.findall(r'\[NEEDS CLARIFICATION\]', content))
        if total_clarifications > 0:
            results.append(ValidationResult(
                status="clarifications_needed",
                message=f"Specification has {total_clarifications} items needing clarification",
                severity=ValidationSeverity.INFO,
                category=ValidationCategory.CONTENT,
                suggestion="Resolve clarifications before proceeding to implementation"
            ))

        return results

    def fix(self, content: str, file_path: Path) -> Tuple[str, bool]:
        """Fix clarification marker formats"""
        original_content = content

        # Replace various invalid formats with the correct one
        content = re.sub(r'\[needs clarification\]', '[NEEDS CLARIFICATION]', content, flags=re.IGNORECASE)
        content = re.sub(r'\[Needs Clarification\]', '[NEEDS CLARIFICATION]', content)
        content = re.sub(r'needs clarification(?!\])', '[NEEDS CLARIFICATION]', content, flags=re.IGNORECASE)
        content = re.sub(r'Needs Clarification(?!\])', '[NEEDS CLARIFICATION]', content)

        return content, content != original_content


class UserStoryFormatRule(SpecValidationRule):
    """Validate user stories follow proper format"""

    def __init__(self):
        super().__init__(
            "user_story_format",
            "User stories should follow standard format",
            ValidationSeverity.WARNING,
            auto_fixable=False
        )

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        results = []

        # Look for user story sections
        user_story_section = re.search(r'## User Stories.*?(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if user_story_section:
            stories = re.findall(r'### .*?\n\n.*?(?=###|\n##|\Z)', user_story_section.group(), re.DOTALL)

            for story in stories:
                # Check if story has required components
                has_as = bool(re.search(r'as a', story, re.IGNORECASE))
                has_want = bool(re.search(r'i want', story, re.IGNORECASE))
                has_so_that = bool(re.search(r'so that', story, re.IGNORECASE))
                has_acceptance = bool(re.search(r'acceptance criteria', story, re.IGNORECASE))

                if not (has_as and has_want and has_so_that):
                    results.append(ValidationResult(
                        status="incomplete_user_story",
                        message="User story missing required components (As a/I want/So that)",
                        severity=self.severity,
                        category=ValidationCategory.CONTENT,
                        suggestion="Format: As a [user type], I want [action] so that [benefit]",
                        location=f"{file_path}:User Stories section"
                    ))

                if not has_acceptance:
                    results.append(ValidationResult(
                        status="missing_acceptance_criteria",
                        message="User story missing acceptance criteria",
                        severity=self.severity,
                        category=ValidationCategory.CONTENT,
                        suggestion="Add acceptance criteria with checkbox format",
                        location=f"{file_path}:User Stories section"
                    ))

        return results


class AcceptanceCriteriaRule(SpecValidationRule):
    """Validate acceptance criteria are testable and specific"""

    def __init__(self):
        super().__init__(
            "acceptance_criteria",
            "Acceptance criteria should be testable and specific",
            ValidationSeverity.WARNING,
            auto_fixable=False
        )

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        results = []

        # Find acceptance criteria sections
        ac_sections = re.finditer(r'## Acceptance Criteria.*?(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)

        for ac_match in ac_sections:
            ac_content = ac_match.group()

            # Check for vague criteria
            vague_patterns = [
                r'should work',
                r'must be good',
                r'needs to be proper',
                r'should be correct',
                r'must be appropriate'
            ]

            for pattern in vague_patterns:
                matches = re.finditer(pattern, ac_content, re.IGNORECASE)
                for match in matches:
                    results.append(ValidationResult(
                        status="vague_acceptance_criteria",
                        message=f"Vague acceptance criteria: {match.group()}",
                        severity=self.severity,
                        category=ValidationCategory.CONTENT,
                        suggestion="Make criteria specific and measurable",
                        location=f"{file_path}:Acceptance Criteria:{match.start()}"
                    ))

            # Check for testability indicators
            has_checkboxes = bool(re.search(r'- \[ \]', ac_content))
            has_measurable = bool(re.search(r'\\d+|can|will|should|must', ac_content, re.IGNORECASE))

            if not has_checkboxes:
                results.append(ValidationResult(
                    status="untestable_criteria",
                    message="Acceptance criteria not in testable format",
                    severity=self.severity,
                    category=ValidationCategory.FORMATTING,
                    suggestion="Use checkbox format: - [ ] Criteria description",
                    location=f"{file_path}:Acceptance Criteria"
                ))

        return results


# === PLAN VALIDATION RULES ===

class PhaseGateRule(PlanValidationRule):
    """Validate phase gates are properly configured"""

    def __init__(self):
        super().__init__(
            "phase_gates",
            "Phase gates should be properly configured",
            ValidationSeverity.ERROR,
            auto_fixable=True
        )

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        results = []

        # Check for phase gates section
        if "Phase -1: Pre-Implementation Gates" not in content:
            results.append(ValidationResult(
                status="missing_phase_gates",
                message="Missing Phase -1: Pre-Implementation Gates",
                severity=self.severity,
                category=ValidationCategory.CONTENT,
                suggestion="Add phase gates section before implementation",
                location=str(file_path),
                auto_fixable=self.auto_fixable,
                fix_action="add_phase_gates"
            ))

        # Check for required SDD principle gates
        required_gates = [
            "Specification First",
            "Incremental Planning",
            "Task Decomposition",
            "Quality Assurance",
            "Architecture Documentation"
        ]

        for gate in required_gates:
            if gate not in content:
                results.append(ValidationResult(
                    status="missing_sdd_gate",
                    message=f"Missing SDD principle gate: {gate}",
                    severity=ValidationSeverity.WARNING,
                    category=ValidationCategory.SDD_COMPLIANCE,
                    suggestion=f"Add {gate} gate to phase gates"
                ))

        return results

    def fix(self, content: str, file_path: Path) -> Tuple[str, bool]:
        """Add missing phase gates section"""
        if "Phase -1: Pre-Implementation Gates" in content:
            return content, False

        phase_gates = """

## Phase -1: Pre-Implementation Gates
**SDD Compliance Check** - Must pass before coding:
- [ ] Specification First - Complete spec with no ambiguities
- [ ] Incremental Planning - Phases clearly defined
- [ ] Task Decomposition - Tasks are concrete and executable
- [ ] Quality Assurance - Testing strategy defined
- [ ] Architecture Documentation - Technical decisions recorded
"""

        # Insert after metadata or at the beginning
        metadata_match = re.search(r'## Metadata.*?(?=\n##|\Z)', content, re.DOTALL)
        if metadata_match:
            content = content[:metadata_match.end()] + phase_gates + content[metadata_match.end():]
        else:
            content = phase_gates + content

        return content, True


# === TASK VALIDATION RULES ===

class TaskFormatRule(TaskValidationRule):
    """Validate tasks follow proper numbering and status format"""

    def __init__(self):
        super().__init__(
            "task_format",
            "Tasks should follow proper T### format with status",
            ValidationSeverity.ERROR,
            auto_fixable=True
        )

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        results = []

        # Check for task headers
        task_headers = re.finditer(r'^### (T\d{3}):', content, re.MULTILINE)

        for match in task_headers:
            task_id = match.group(1)
            start_pos = match.start()
            lines_before = content[:start_pos].count('\n')

            # Look for status in next few lines
            remaining_content = content[match.end():]
            next_lines = remaining_content.split('\n')[:5]

            has_status = any('**Status**:' in line for line in next_lines)

            if not has_status:
                results.append(ValidationResult(
                    status="missing_task_status",
                    message=f"Task {task_id} missing status indicator",
                    severity=self.severity,
                    category=ValidationCategory.FORMATTING,
                    suggestion="Add **Status**: [ ], [>], [x], or [!]",
                    location=f"{file_path}:{lines_before + 1}",
                    auto_fixable=self.auto_fixable,
                    fix_action="add_task_status"
                ))

        # Check for tasks without proper numbering
        invalid_tasks = re.finditer(r'^### (?!T\d{3}:).*', content, re.MULTILINE)
        for match in invalid_tasks:
            results.append(ValidationResult(
                status="invalid_task_format",
                message=f"Invalid task format: {match.group()}",
                severity=self.severity,
                category=ValidationCategory.FORMATTING,
                suggestion="Use format: ### T001: Task Name",
                location=f"{file_path}:{content[:match.start()].count('\n') + 1}",
                auto_fixable=self.auto_fixable,
                fix_action="fix_task_format"
            ))

        return results

    def fix(self, content: str, file_path: Path) -> Tuple[str, bool]:
        """Fix task formatting issues"""
        original_content = content
        fixed = False

        # Fix task headers without proper format
        def fix_task_header(match):
            nonlocal fixed
            fixed = True
            task_name = match.group(1).strip()
            # Find next available task number
            existing_tasks = re.findall(r'T(\d{3}):', content)
            next_num = max([int(n) for n in existing_tasks], default=0) + 1
            return f"### T{next_num:03d}: {task_name}"

        content = re.sub(r'^### (?!T\d{3}:)(.+)$', fix_task_header, content, flags=re.MULTILINE)

        return content, fixed


class TaskDependencyRule(TaskValidationRule):
    """Validate task dependencies are properly specified"""

    def __init__(self):
        super().__init__(
            "task_dependencies",
            "Task dependencies should be clearly specified",
            ValidationSeverity.WARNING,
            auto_fixable=False
        )

    def validate(self, content: str, file_path: Path) -> List[ValidationResult]:
        results = []

        # Find all tasks
        tasks = re.finditer(r'^### (T\d{3}):.*?(?=\n### T\d{3}:|\n##|\Z)', content, re.DOTALL | re.MULTILINE)

        for task_match in tasks:
            task_id = task_match.group(1)
            task_content = task_match.group()

            # Check for dependency specification
            has_dependencies = bool(re.search(r'dependencies?', task_content, re.IGNORECASE))
            has_status = bool(re.search(r'\*\*Status\*\*:', task_content))

            if has_status and not has_dependencies:
                # Check if this task depends on others (should be explicit)
                # This is more complex and might require cross-referencing
                pass

        return results


# === VALIDATION RULES REGISTRY ===

class ValidationRulesRegistry:
    """Registry for all validation rules"""

    def __init__(self):
        self.spec_rules = [
            RequiredSectionsRule(),
            ClarificationMarkerRule(),
            UserStoryFormatRule(),
            AcceptanceCriteriaRule()
        ]

        self.plan_rules = [
            RequiredSectionsRule(),
            PhaseGateRule()
        ]

        self.task_rules = [
            RequiredSectionsRule(),
            TaskFormatRule(),
            TaskDependencyRule()
        ]

    def get_rules_for_file(self, file_path: Path) -> List[ValidationRule]:
        """Get applicable rules for a file"""
        name = file_path.name.lower()

        if "spec" in name:
            return self.spec_rules
        elif "plan" in name:
            return self.plan_rules
        elif "task" in name:
            return self.task_rules
        else:
            return self.spec_rules  # Default to spec rules

    def validate_file(self, file_path: Path, content: str = None) -> List[ValidationResult]:
        """Validate a file with all applicable rules"""
        if content is None:
            if not file_path.exists():
                return [ValidationResult(
                    status="file_not_found",
                    message=f"File not found: {file_path}",
                    severity=ValidationSeverity.ERROR,
                    category=ValidationCategory.STRUCTURE
                )]
            content = file_path.read_text(encoding='utf-8')

        results = []
        rules = self.get_rules_for_file(file_path)

        for rule in rules:
            try:
                rule_results = rule.validate(content, file_path)
                results.extend(rule_results)
            except Exception as e:
                results.append(ValidationResult(
                    status="validation_error",
                    message=f"Error applying rule {rule.name}: {str(e)}",
                    severity=ValidationSeverity.ERROR,
                    category=ValidationCategory.STRUCTURE,
                    location=str(file_path)
                ))

        return results

    def fix_file(self, file_path: Path, content: str = None) -> Tuple[str, List[ValidationResult]]:
        """Auto-fix a file if possible"""
        if content is None:
            content = file_path.read_text(encoding='utf-8')

        original_content = content
        fix_results = []

        rules = self.get_rules_for_file(file_path)
        applicable_rules = [rule for rule in rules if rule.auto_fixable]

        for rule in applicable_rules:
            try:
                content, was_fixed = rule.fix(content, file_path)
                if was_fixed:
                    fix_results.append(ValidationResult(
                        status="auto_fixed",
                        message=f"Applied auto-fix for rule: {rule.name}",
                        severity=ValidationSeverity.INFO,
                        category=rule.category,
                        location=str(file_path)
                    ))
            except Exception as e:
                fix_results.append(ValidationResult(
                    status="fix_failed",
                    message=f"Failed to apply fix for rule {rule.name}: {str(e)}",
                    severity=ValidationSeverity.WARNING,
                    category=rule.category,
                    location=str(file_path)
                ))

        return content, fix_results


# Global registry instance
validation_rules_registry = ValidationRulesRegistry()