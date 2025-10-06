"""
SpecPulse Validator - Enhanced with comprehensive validation rules
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import yaml
import re
import difflib
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from ..utils.backup_manager import BackupManager
from ..utils.progress_calculator import SectionStatus, ProgressCalculator
from .validation_rules import (
    validation_rules_registry, ValidationResult, ValidationSeverity,
    ValidationCategory
)


@dataclass
class ValidationExample:
    """
    Enhanced validation error with actionable guidance.

    This dataclass represents a validation error with rich context including
    examples, suggestions, and help commands to guide LLMs in fixing issues.

    Attributes:
        message: Short error message (e.g., "Missing: Acceptance Criteria")
        meaning: Explanation of what this section means and why it's important
        example: Concrete example of valid content (multiline supported)
        suggestion: Actionable suggestion for fixing the issue
        help_command: Command to get more detailed help
        auto_fix: Whether this issue can be automatically fixed
    """
    message: str
    meaning: str
    example: str
    suggestion: str
    help_command: str
    auto_fix: bool = False

    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.message}\n\nWhat this means:\n  {self.meaning}\n\nSuggestion:\n  {self.suggestion}"


@dataclass
class ValidationProgress:
    """
    Result of partial/progressive validation.

    This dataclass represents the progress of an incomplete specification,
    showing completion percentage, section statuses, and suggestions for
    what to work on next.

    Attributes:
        completion_pct: Completion percentage (0-100)
        section_statuses: Dict mapping section names to SectionStatus (COMPLETE/PARTIAL/MISSING)
        next_suggestion: Suggested next section to work on (None if complete)
        total_sections: Total number of tracked sections
        complete_sections: Number of complete sections
        partial_sections: Number of partial sections
        missing_sections: Number of missing sections
    """
    completion_pct: int
    section_statuses: Dict[str, SectionStatus]
    next_suggestion: Optional[str]
    total_sections: int
    complete_sections: int
    partial_sections: int
    missing_sections: int

    def __str__(self) -> str:
        """String representation for display."""
        status_lines = []
        status_lines.append(f"Progress: {self.completion_pct}% complete\n")

        for section, status in self.section_statuses.items():
            icon = "✓" if status == SectionStatus.COMPLETE else ("⚠️" if status == SectionStatus.PARTIAL else "⭕")
            status_text = status.value
            status_lines.append(f"{icon} {section} ({status_text})")

        if self.next_suggestion:
            status_lines.append(f"\nNext suggested section: {self.next_suggestion}")

        return "\n".join(status_lines)


class Validator:
    """Validates SpecPulse project components with enhanced rules"""

    # Class-level cache for validation examples (shared across instances)
    _validation_examples_cache: Optional[Dict[str, ValidationExample]] = None

    def __init__(self, project_root: Optional[Path] = None):
        self.results = []
        self.constitution = None
        self.phase_gates = []
        self.rules_registry = validation_rules_registry

        if project_root:
            self._load_constitution(project_root)
    
    def validate_all(self, project_path: Path, fix: bool = False, verbose: bool = False,
                   strictness: str = "standard") -> List[Dict]:
        """Validate entire project with progressive strictness levels"""
        self.results = []

        # Check project structure
        self._validate_structure(project_path)

        # Validate based on strictness level
        if strictness == "basic":
            self._validate_basic(project_path, fix, verbose)
        elif strictness == "standard":
            self._validate_standard(project_path, fix, verbose)
        elif strictness == "comprehensive":
            self._validate_comprehensive(project_path, fix, verbose)
        elif strictness == "strict":
            self._validate_strict(project_path, fix, verbose)
        else:
            # Default to standard
            self._validate_standard(project_path, fix, verbose)

        # Validate SDD principles compliance
        self._validate_sdd_compliance(project_path, verbose)

        return self.results

    def _validate_basic(self, project_path: Path, fix: bool, verbose: bool):
        """Basic validation - check only critical errors"""
        self._validate_specs(project_path, fix, verbose, severity_filter="error")
        self._validate_plans(project_path, fix, verbose, severity_filter="error")

    def _validate_standard(self, project_path: Path, fix: bool, verbose: bool):
        """Standard validation - check errors and warnings"""
        self._validate_specs(project_path, fix, verbose)
        self._validate_plans(project_path, fix, verbose)

    def _validate_comprehensive(self, project_path: Path, fix: bool, verbose: bool):
        """Comprehensive validation - check all issues including info"""
        self._validate_specs(project_path, fix, verbose, severity_filter="all")
        self._validate_plans(project_path, fix, verbose, severity_filter="all")
        self._validate_tasks(project_path, fix, verbose, severity_filter="all")

    def _validate_strict(self, project_path: Path, fix: bool, verbose: bool):
        """Strict validation - enforce all rules strictly"""
        self._validate_specs(project_path, fix, verbose, severity_filter="all")
        self._validate_plans(project_path, fix, verbose, severity_filter="all")
        self._validate_tasks(project_path, fix, verbose, severity_filter="all")
        self._validate_cross_references(project_path, verbose)
        self._validate_naming_conventions(project_path, verbose)
    
    def validate_spec(self, project_path: Path, spec_name: Optional[str] = None, 
                     fix: bool = False, verbose: bool = False) -> List[Dict]:
        """Validate specification(s)"""
        self.results = []
        
        specs_dir = project_path / "specs"
        if not specs_dir.exists():
            self.results.append({
                "status": "error",
                "message": "No specs directory found"
            })
            return self.results
        
        if spec_name:
            spec_path = specs_dir / spec_name / "spec.md"
            if spec_path.exists():
                self._validate_single_spec(spec_path, fix, verbose)
            else:
                self.results.append({
                    "status": "error",
                    "message": f"Specification {spec_name} not found"
                })
        else:
            # Validate all specs
            for spec_dir in specs_dir.iterdir():
                if spec_dir.is_dir():
                    spec_path = spec_dir / "spec.md"
                    if spec_path.exists():
                        self._validate_single_spec(spec_path, fix, verbose)
        
        return self.results
    
    def validate_plan(self, project_path: Path, plan_name: Optional[str] = None,
                     fix: bool = False, verbose: bool = False) -> List[Dict]:
        """Validate implementation plan(s)"""
        self.results = []
        
        plans_dir = project_path / "plans"
        if not plans_dir.exists():
            self.results.append({
                "status": "warning",
                "message": "No plans directory found"
            })
            return self.results
        
        if plan_name:
            plan_path = plans_dir / plan_name / "plan.md"
            if plan_path.exists():
                self._validate_single_plan(plan_path, fix, verbose)
            else:
                self.results.append({
                    "status": "error",
                    "message": f"Plan {plan_name} not found"
                })
        else:
            # Validate all plans
            for plan_dir in plans_dir.iterdir():
                if plan_dir.is_dir():
                    plan_path = plan_dir / "plan.md"
                    if plan_path.exists():
                        self._validate_single_plan(plan_path, fix, verbose)
        
        return self.results
    
    def validate_sdd_compliance(self, project_path: Path, verbose: bool = False) -> List[Dict]:
        """Validate SDD principles compliance"""
        self.results = []
        self._validate_sdd_compliance(project_path, verbose)
        return self.results
    
    def _validate_structure(self, project_path: Path):
        """Validate project structure"""
        required_dirs = [
            ".specpulse",
            "memory",
            "specs",
            "templates",
            "scripts"
        ]
        
        for dir_name in required_dirs:
            dir_path = project_path / dir_name
            if dir_path.exists():
                self.results.append({
                    "status": "success",
                    "message": f"Directory {dir_name}/ exists"
                })
            else:
                self.results.append({
                    "status": "error",
                    "message": f"Missing directory: {dir_name}/"
                })
        
        # Check config file
        config_path = project_path / ".specpulse" / "config.yaml"
        if config_path.exists():
            self.results.append({
                "status": "success",
                "message": "Configuration file exists"
            })
        else:
            self.results.append({
                "status": "error",
                "message": "Missing configuration file"
            })
    
    def _validate_single_spec(self, spec_path: Path, fix: bool, verbose: bool):
        """Validate a single specification with enhanced rules"""
        spec_name = spec_path.parent.name

        try:
            # Read content
            content = spec_path.read_text(encoding='utf-8')

            # Apply validation rules
            validation_results = self.rules_registry.validate_file(spec_path, content)

            # Auto-fix if requested and possible
            if fix:
                fixed_content, fix_results = self.rules_registry.fix_file(spec_path, content)
                if fixed_content != content:
                    spec_path.write_text(fixed_content, encoding='utf-8')
                    validation_results.extend(fix_results)

            # Convert validation results to legacy format
            for result in validation_results:
                legacy_result = self._convert_validation_result(result, spec_name)
                self.results.append(legacy_result)

            # If no errors, add success message
            errors = [r for r in validation_results if r.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]]
            if not errors:
                self.results.append({
                    "status": "success",
                    "message": f"{spec_name}: Validation passed"
                })

        except Exception as e:
            self.results.append({
                "status": "error",
                "message": f"{spec_name}: Failed to validate - {str(e)}"
            })

    def _convert_validation_result(self, result: ValidationResult, context: str) -> Dict:
        """Convert ValidationResult to legacy format"""
        severity_map = {
            ValidationSeverity.INFO: "info",
            ValidationSeverity.WARNING: "warning",
            ValidationSeverity.ERROR: "error",
            ValidationSeverity.CRITICAL: "error"
        }

        status = severity_map.get(result.severity, "warning")
        message = result.message

        if result.suggestion:
            message += f" (Suggestion: {result.suggestion})"

        return {
            "status": status,
            "message": f"{context}: {message}",
            "severity": result.severity.value,
            "category": result.category.value,
            "auto_fixable": result.auto_fixable,
            "location": result.location
        }
    
    def _validate_single_plan(self, plan_path: Path, fix: bool, verbose: bool):
        """Validate a single implementation plan with enhanced rules"""
        plan_name = plan_path.parent.name

        try:
            # Read content
            content = plan_path.read_text(encoding='utf-8')

            # Apply validation rules
            validation_results = self.rules_registry.validate_file(plan_path, content)

            # Auto-fix if requested and possible
            if fix:
                fixed_content, fix_results = self.rules_registry.fix_file(plan_path, content)
                if fixed_content != content:
                    plan_path.write_text(fixed_content, encoding='utf-8')
                    validation_results.extend(fix_results)

            # Convert validation results to legacy format
            for result in validation_results:
                legacy_result = self._convert_validation_result(result, plan_name)
                self.results.append(legacy_result)

            # Additional plan-specific validations
            if "Spec ID" not in content and "Specification Reference" not in content:
                self.results.append({
                    "status": "warning",
                    "message": f"{plan_name}: No specification reference found"
                })

            # Check for implementation phases
            if "Implementation Phases" not in content:
                self.results.append({
                    "status": "warning",
                    "message": f"{plan_name}: No implementation phases defined"
                })

            # If no errors, add success message
            errors = [r for r in validation_results if r.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]]
            if not errors:
                self.results.append({
                    "status": "success",
                    "message": f"{plan_name}: Validation passed"
                })

        except Exception as e:
            self.results.append({
                "status": "error",
                "message": f"{plan_name}: Failed to validate - {str(e)}"
            })
    
    def _validate_specs(self, project_path: Path, fix: bool, verbose: bool):
        """Validate all specifications"""
        specs_dir = project_path / "specs"
        if specs_dir.exists():
            spec_count = 0
            for spec_dir in specs_dir.iterdir():
                if spec_dir.is_dir():
                    spec_path = spec_dir / "spec.md"
                    if spec_path.exists():
                        spec_count += 1
                        self._validate_single_spec(spec_path, fix, verbose)
            
            if spec_count == 0:
                self.results.append({
                    "status": "warning",
                    "message": "No specifications found"
                })
    
    def _validate_plans(self, project_path: Path, fix: bool, verbose: bool):
        """Validate all implementation plans"""
        plans_dir = project_path / "plans"
        if plans_dir.exists():
            plan_count = 0
            for plan_dir in plans_dir.iterdir():
                if plan_dir.is_dir():
                    plan_path = plan_dir / "plan.md"
                    if plan_path.exists():
                        plan_count += 1
                        self._validate_single_plan(plan_path, fix, verbose)
            
            if plan_count == 0:
                self.results.append({
                    "status": "info",
                    "message": "No implementation plans found"
                })
    
    def _validate_sdd_compliance(self, project_path: Path, verbose: bool):
        """Validate compliance with SDD principles"""
        constitution_path = project_path / "memory" / "constitution.md"
        
        if not constitution_path.exists():
            self.results.append({
                "status": "error",
                "message": "SDD principles file (constitution.md) not found"
            })
            return
        
        with open(constitution_path, 'r', encoding='utf-8') as f:
            constitution = f.read()
        
        # Check for key SDD principles
        principles = [
            "Specification First",
            "Incremental Planning",
            "Task Decomposition",
            "Traceable Implementation",
            "Continuous Validation",
            "Quality Assurance",
            "Architecture Documentation",
            "Iterative Refinement",
            "Stakeholder Alignment"
        ]
        
        for principle in principles:
            if principle in constitution:
                if verbose:
                    self.results.append({
                        "status": "success",
                        "message": f"SDD principle found: {principle}"
                    })
            else:
                self.results.append({
                    "status": "warning",
                    "message": f"Missing SDD principle: {principle}"
                })
        
        # Check config for constitution enforcement
        config_path = project_path / ".specpulse" / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config.get("sdd", {}).get("enforce", True):
                self.results.append({
                    "status": "success",
                    "message": "SDD principles enforcement enabled"
                })
            else:
                self.results.append({
                    "status": "warning",
                    "message": "SDD principles enforcement disabled"
                })
    
    def _load_constitution(self, project_root: Path):
        """Load constitution from project"""
        constitution_path = project_root / "memory" / "constitution.md"
        if constitution_path.exists():
            self.constitution = constitution_path.read_text()
            # Extract phase gates from constitution
            self._extract_phase_gates_from_constitution()

    def _extract_phase_gates_from_constitution(self):
        """Extract phase gates from constitution"""
        if not self.constitution:
            return

        # Simple extraction of phase gates from constitution text
        gates = []
        lines = self.constitution.split('\n')
        for line in lines:
            if 'Phase Gate' in line or 'phase gate' in line:
                gates.append(line.strip())
        self.phase_gates = gates
    
    def load_constitution(self, project_root: Path) -> bool:
        """Load constitution from a project"""
        self._load_constitution(project_root)
        return self.constitution is not None
    
    def validate_spec_file(self, spec_path: Path, verbose: bool = False) -> Dict:
        """Validate a single specification file"""
        if not spec_path.exists():
            return {"status": "error", "message": f"Spec file not found: {spec_path}"}
        
        content = spec_path.read_text()
        result = {"status": "valid", "issues": []}
        
        # Check required sections
        required_sections = ["## Requirements", "## User Stories", "## Acceptance Criteria"]
        for section in required_sections:
            if section not in content:
                result["issues"].append(f"Missing section: {section}")
        
        if result["issues"]:
            result["status"] = "invalid"
        
        return result
    
    def validate_plan_file(self, plan_path: Path, verbose: bool = False) -> Dict:
        """Validate a single plan file"""
        if not plan_path.exists():
            return {"status": "error", "message": f"Plan file not found: {plan_path}"}
        
        content = plan_path.read_text()
        result = {"status": "valid", "issues": []}
        
        # Check required sections
        required_sections = ["## Architecture", "## Phases", "## Technology Stack"]
        for section in required_sections:
            if section not in content:
                result["issues"].append(f"Missing section: {section}")
        
        if result["issues"]:
            result["status"] = "invalid"
        
        return result
    
    def validate_task_file(self, task_path: Path, verbose: bool = False) -> Dict:
        """Validate a single task file"""
        if not task_path.exists():
            return {"status": "error", "message": f"Task file not found: {task_path}"}
        
        content = task_path.read_text()
        result = {"status": "valid", "issues": []}
        
        # Check for task format
        if not re.search(r'T\d{3}', content):
            result["issues"].append("No task IDs found (T001 format)")
        
        if result["issues"]:
            result["status"] = "invalid"
        
        return result
    
    def validate_sdd_principles(self, spec_content: str, verbose: bool = False) -> Dict:
        """Validate that content complies with SDD principles"""
        result = {"status": "compliant", "violations": []}
        
        if not self.constitution:
            return result
        
        # Check for specification clarity
        if '[needs clarification]' in spec_content.lower():
            result["violations"].append("Specification First: Contains unresolved clarifications")
        
        if result["violations"]:
            result["status"] = "non-compliant"
        
        return result
    
    def check_phase_gate(self, gate_name: str, context: Dict) -> bool:
        """Check if a phase gate passes"""
        # Gate checking logic
        if gate_name == "specification":
            return context.get("spec_complete", False)
        elif gate_name == "test-first":
            return context.get("tests_written", False)
        return True
    
    def validate_all_project(self, project_root: Path, verbose: bool = False) -> Dict:
        """Validate entire project"""
        results = {
            "specs": [],
            "plans": [],
            "tasks": [],
            "sdd_compliance": True
        }
        
        # Validate specs
        specs_dir = project_root / "specs"
        if specs_dir.exists():
            for spec_file in specs_dir.glob("*/spec*.md"):
                results["specs"].append(self.validate_spec_file(spec_file, verbose))
        
        # Validate plans
        plans_dir = project_root / "plans"
        if plans_dir.exists():
            for plan_file in plans_dir.glob("*/plan*.md"):
                results["plans"].append(self.validate_plan_file(plan_file, verbose))
        
        # Validate tasks
        tasks_dir = project_root / "tasks"
        if tasks_dir.exists():
            for task_file in tasks_dir.glob("*/task*.md"):
                results["tasks"].append(self.validate_task_file(task_file, verbose))
        
        return results
    
    def format_validation_report(self, results: Dict) -> str:
        """Format validation results as a report"""
        report = "# Validation Report\n\n"
        
        # Specs section
        report += "## Specifications\n"
        for spec in results.get("specs", []):
            status = spec.get("status", "unknown")
            report += f"- Status: {status}\n"
            if spec.get("issues"):
                for issue in spec["issues"]:
                    report += f"  - Issue: {issue}\n"
        
        # Plans section
        report += "\n## Plans\n"
        for plan in results.get("plans", []):
            status = plan.get("status", "unknown")
            report += f"- Status: {status}\n"
            if plan.get("issues"):
                for issue in plan["issues"]:
                    report += f"  - Issue: {issue}\n"
        
        # Tasks section
        report += "\n## Tasks\n"
        for task in results.get("tasks", []):
            status = task.get("status", "unknown")
            report += f"- Status: {status}\n"
            if task.get("issues"):
                for issue in task["issues"]:
                    report += f"  - Issue: {issue}\n"
        
        return report

    def validate_constitution(self, project_path: Path) -> Dict:
        """Validate constitution file"""
        constitution_path = project_path / "memory" / "constitution.md"
        if not constitution_path.exists():
            return {
                "status": "error",
                "message": "Constitution file not found"
            }

        try:
            with open(constitution_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for required sections
            required_sections = [
                "Principles",
                "Specification First",
                "Quality Assurance"
            ]

            missing = []
            for section in required_sections:
                if section not in content:
                    missing.append(section)

            if missing:
                return {
                    "status": "warning",
                    "message": f"Missing sections: {', '.join(missing)}"
                }

            return {
                "status": "success",
                "message": "Constitution valid"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error reading constitution: {str(e)}"
            }

    def _check_phase_gates(self, plan_content: str) -> Dict[str, bool]:
        """Check phase gates in a plan"""
        gates = {}

        # Look for phase gate patterns
        lines = plan_content.split('\n')
        for line in lines:
            # Pattern: - [x] Gate Name
            if re.match(r'^\s*-\s*\[([x ])\]\s+(.+)', line):
                match = re.match(r'^\s*-\s*\[([x ])\]\s+(.+)', line)
                if match:
                    checked = match.group(1).lower() == 'x'
                    gate_name = match.group(2).strip()
                    gates[gate_name] = checked

        return gates

    def _extract_phase_gates(self, plan_content: str) -> List[Dict]:
        """Extract phase gates from plan content"""
        gates = []

        lines = plan_content.split('\n')
        for line in lines:
            # Pattern: - [x] Gate Name or - [ ] Gate Name
            if re.match(r'^\s*-\s*\[([x ])\]\s+(.+)', line):
                match = re.match(r'^\s*-\s*\[([x ])\]\s+(.+)', line)
                if match:
                    checked = match.group(1).lower() == 'x'
                    gate_name = match.group(2).strip()
                    gates.append({
                        "name": gate_name,
                        "checked": checked
                    })

        return gates

    def _fix_common_issues(self, content: str, doc_type: str) -> str:
        """Fix common issues in documents"""
        fixed_content = content

        if doc_type == "spec":
            # Ensure spec has required headers
            if "## Metadata" not in fixed_content:
                fixed_content = "## Metadata\n- **ID**: SPEC-XXX\n- **Created**: TBD\n\n" + fixed_content

            if "## Executive Summary" not in fixed_content:
                fixed_content += "\n\n## Executive Summary\n[To be completed]\n"

            if "## Functional Requirements" not in fixed_content:
                fixed_content += "\n\n## Functional Requirements\n- FR-001: [Requirement]\n"

        elif doc_type == "plan":
            # Ensure plan has phase gates
            if "## Phase -1: Pre-Implementation Gates" not in fixed_content:
                gates = """
## Phase -1: Pre-Implementation Gates
- [ ] Specification First
- [ ] Quality Assurance
- [ ] Architecture Documentation
"""
                fixed_content = gates + "\n" + fixed_content

        elif doc_type == "task":
            # Ensure task has proper structure
            if "## Tasks" not in fixed_content:
                fixed_content += "\n\n## Tasks\n### T001: [Task Name]\n- **Status**: Pending\n"

        return fixed_content

    @classmethod
    def load_validation_examples(cls) -> Dict[str, ValidationExample]:
        """
        Load validation examples from YAML file with caching.

        This method loads the validation_examples.yaml file and converts
        it to ValidationExample objects. Results are cached at the class
        level to avoid repeated file I/O.

        Returns:
            Dictionary mapping example keys to ValidationExample objects

        Raises:
            FileNotFoundError: If validation_examples.yaml not found
            yaml.YAMLError: If YAML is malformed
        """
        # Return cached examples if available
        if cls._validation_examples_cache is not None:
            return cls._validation_examples_cache

        # Find the validation_examples.yaml file
        # It should be in specpulse/resources/validation_examples.yaml
        current_file = Path(__file__)
        resources_dir = current_file.parent.parent / "resources"
        examples_file = resources_dir / "validation_examples.yaml"

        if not examples_file.exists():
            raise FileNotFoundError(
                f"Validation examples file not found at {examples_file}"
            )

        try:
            with open(examples_file, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)

            # Convert YAML data to ValidationExample objects
            examples = {}
            for key, value in yaml_data.items():
                # Skip metadata section
                if key == "metadata":
                    continue

                # Create ValidationExample from YAML data
                if isinstance(value, dict) and 'message' in value:
                    examples[key] = ValidationExample(
                        message=value.get('message', ''),
                        meaning=value.get('meaning', ''),
                        example=value.get('example', ''),
                        suggestion=value.get('suggestion', ''),
                        help_command=value.get('help_command', ''),
                        auto_fix=value.get('auto_fix', False)
                    )

            # Cache the results
            cls._validation_examples_cache = examples
            return examples

        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse validation examples YAML: {e}")
        except Exception as e:
            raise Exception(f"Error loading validation examples: {e}")

    def get_validation_example(self, example_key: str) -> Optional[ValidationExample]:
        """
        Get a specific validation example by key.

        Args:
            example_key: Key for the validation example (e.g., 'missing_acceptance_criteria')

        Returns:
            ValidationExample if found, None otherwise
        """
        examples = self.load_validation_examples()
        return examples.get(example_key)

    def _check_section_exists(self, content: str, section_name: str) -> Optional[ValidationExample]:
        """
        Check if a section exists in spec content and return enhanced error if missing.

        This method replaces simple string error messages with rich ValidationExample
        objects that provide actionable guidance to LLMs.

        Args:
            content: Full specification content
            section_name: Name of section to check (e.g., "Acceptance Criteria")

        Returns:
            ValidationExample if section is missing, None if section exists

        Example:
            >>> validator = Validator()
            >>> content = "# Spec\\n## Executive Summary\\nText here"
            >>> error = validator._check_section_exists(content, "Acceptance Criteria")
            >>> if error:
            >>>     print(error.message)  # "Missing: Acceptance Criteria"
        """
        # Check if section exists (case-insensitive)
        section_marker = f"## {section_name}"
        if section_marker in content:
            return None  # Section exists, no error

        # Section is missing - get enhanced error message
        # Map section names to example keys
        section_to_key_map = {
            "Executive Summary": "missing_executive_summary",
            "Problem Statement": "missing_problem_statement",
            "Proposed Solution": "missing_proposed_solution",
            "Functional Requirements": "missing_functional_requirements",
            "Detailed Requirements": "missing_functional_requirements",  # Alias
            "Non-Functional Requirements": "missing_nfr_performance",  # Generic NFR
            "User Stories": "missing_user_stories",
            "Acceptance Criteria": "missing_acceptance_criteria",
            "Success Criteria": "missing_success_criteria",
            "Technical Constraints": "missing_technical_constraints",
            "Dependencies": "missing_dependencies",
            "Risks and Mitigations": "missing_risks",
        }

        # Get the validation example key
        example_key = section_to_key_map.get(section_name)

        if example_key:
            # Get pre-defined enhanced error
            example = self.get_validation_example(example_key)
            if example:
                return example

        # Fallback: create basic ValidationExample if no template found
        return ValidationExample(
            message=f"Missing: {section_name}",
            meaning=f"The '{section_name}' section is required but not found in the specification.",
            example=f"## {section_name}\\n[Content describing {section_name.lower()}]",
            suggestion=f"Add a section '## {section_name}' to your specification.",
            help_command=f"specpulse help {section_name.lower().replace(' ', '-')}",
            auto_fix=True
        )

    def format_enhanced_error(self, example: ValidationExample, console: Optional[Console] = None) -> str:
        """
        Format a ValidationExample into a beautiful, LLM-friendly error message using Rich.

        This method creates a formatted panel with color-coded sections that provide
        actionable guidance for fixing validation issues.

        Args:
            example: ValidationExample to format
            console: Optional Rich Console instance (creates one if not provided)

        Returns:
            Formatted error message as string (can be printed with Rich or as plain text)

        Example:
            >>> validator = Validator()
            >>> example = validator.get_validation_example("missing_acceptance_criteria")
            >>> formatted = validator.format_enhanced_error(example)
            >>> print(formatted)
        """
        if console is None:
            console = Console()

        # Create the formatted content
        content = Text()

        # Title (message) - bold red
        content.append(f"❌ {example.message}\n\n", style="bold red")

        # What this means section - cyan
        content.append("What this means:\n", style="bold cyan")
        content.append(f"  {example.meaning}\n\n", style="white")

        # Example section - green
        content.append("Example:\n", style="bold green")
        # Format example with slight indentation and different color
        for line in example.example.split("\n"):
            if line.strip():
                content.append(f"  {line}\n", style="green")
        content.append("\n")

        # Suggestion section - yellow
        content.append("Suggestion for LLM:\n", style="bold yellow")
        content.append(f"  {example.suggestion}\n\n", style="yellow")

        # Quick fix section (if auto-fixable) - magenta
        if example.auto_fix:
            content.append("Quick fix:\n", style="bold magenta")
            content.append("  specpulse validate <spec-id> --fix  # Adds template section\n\n", style="magenta")

        # Help command - blue
        content.append("Help:\n", style="bold blue")
        content.append(f"  {example.help_command}\n", style="blue")

        # Create a panel with the content
        panel = Panel(
            content,
            title=f"[bold white]Validation Error[/bold white]",
            border_style="red",
            padding=(1, 2)
        )

        # Render to string using console
        with console.capture() as capture:
            console.print(panel)

        return capture.get()

    def format_enhanced_error_plain(self, example: ValidationExample) -> str:
        """
        Format a ValidationExample into a plain text error message (no colors).

        This is useful for environments that don't support Rich formatting or
        for logging purposes.

        Args:
            example: ValidationExample to format

        Returns:
            Plain text formatted error message

        Example:
            >>> validator = Validator()
            >>> example = validator.get_validation_example("missing_user_stories")
            >>> plain_text = validator.format_enhanced_error_plain(example)
        """
        output = []
        output.append(f"❌ {example.message}")
        output.append("")
        output.append("What this means:")
        output.append(f"  {example.meaning}")
        output.append("")
        output.append("Example:")
        for line in example.example.split("\n"):
            if line.strip():
                output.append(f"  {line}")
        output.append("")
        output.append("Suggestion for LLM:")
        output.append(f"  {example.suggestion}")
        output.append("")

        if example.auto_fix:
            output.append("Quick fix:")
            output.append("  specpulse validate <spec-id> --fix  # Adds template section")
            output.append("")

        output.append("Help:")
        output.append(f"  {example.help_command}")
        output.append("")

        return "\n".join(output)

    def auto_fix_validation_issues(
        self,
        spec_path: Path,
        backup: bool = True,
        dry_run: bool = False
    ) -> Tuple[bool, List[str], Optional[Path]]:
        """
        Automatically fix common validation issues by adding missing sections.

        This method identifies auto-fixable validation errors and adds missing
        sections with template placeholders. It creates a backup before making
        changes and provides a diff report.

        Args:
            spec_path: Path to specification file to fix
            backup: Whether to create backup before fixing (default: True)
            dry_run: If True, only report what would be fixed without modifying (default: False)

        Returns:
            Tuple of (success: bool, changes: List[str], backup_path: Optional[Path])
            - success: True if fixes applied successfully
            - changes: List of changes made (for diff reporting)
            - backup_path: Path to backup file (if backup=True), None otherwise

        Raises:
            FileNotFoundError: If spec file doesn't exist
            IOError: If backup or file write fails

        Example:
            >>> validator = Validator()
            >>> success, changes, backup = validator.auto_fix_validation_issues(
            ...     Path("specs/001-feature/spec-001.md"),
            ...     backup=True
            ... )
            >>> if success:
            ...     print(f"Applied {len(changes)} fixes, backup at {backup}")
        """
        if not spec_path.exists():
            raise FileNotFoundError(f"Specification file not found: {spec_path}")

        # Read current content
        try:
            original_content = spec_path.read_text(encoding='utf-8')
        except Exception as e:
            raise IOError(f"Failed to read specification file: {e}")

        # Find all auto-fixable issues
        auto_fixable_issues = []
        required_sections = [
            "Executive Summary",
            "Problem Statement",
            "Proposed Solution",
            "Functional Requirements",
            "User Stories",
            "Acceptance Criteria",
            "Technical Constraints",
            "Dependencies",
            "Risks and Mitigations",
            "Success Criteria"
        ]

        for section in required_sections:
            error = self._check_section_exists(original_content, section)
            if error and error.auto_fix:
                auto_fixable_issues.append((section, error))

        # If no fixable issues, return early
        if not auto_fixable_issues:
            return (True, ["No auto-fixable issues found"], None)

        # Dry run: report what would be fixed
        if dry_run:
            changes = [f"Would add section: {section}" for section, _ in auto_fixable_issues]
            return (True, changes, None)

        # Create backup if requested
        backup_path = None
        if backup:
            try:
                backup_manager = BackupManager()
                backup_path = backup_manager.create_backup(spec_path)
            except Exception as e:
                raise IOError(f"Failed to create backup: {e}")

        # Apply fixes
        modified_content = original_content
        changes = []

        try:
            for section, error in auto_fixable_issues:
                # Get template content for this section from example
                section_template = self._get_section_template(section, error)

                # Add section to content
                modified_content = self._add_section_to_spec(modified_content, section, section_template)
                changes.append(f"Added section: {section}")

            # Write modified content back to file
            spec_path.write_text(modified_content, encoding='utf-8')

            return (True, changes, backup_path)

        except Exception as e:
            # Rollback if anything fails
            if backup and backup_path:
                try:
                    backup_manager = BackupManager()
                    backup_manager.restore_from_backup(backup_path, spec_path)
                    changes.append(f"ROLLBACK: Restored from backup due to error: {e}")
                except Exception as restore_error:
                    changes.append(f"CRITICAL: Rollback failed: {restore_error}")

            return (False, changes, backup_path)

    def _get_section_template(self, section_name: str, error: ValidationExample) -> str:
        """
        Get template content for a missing section.

        Args:
            section_name: Name of section to add
            error: ValidationExample with template information

        Returns:
            Template content for the section
        """
        # Extract example content as template
        # Remove any instructional text and keep just the structure
        template = error.example.strip()

        # If example doesn't start with ##, add section header
        if not template.startswith("##"):
            template = f"## {section_name}\n{template}"

        return template

    def _add_section_to_spec(self, content: str, section_name: str, section_template: str) -> str:
        """
        Add a section to specification content in the appropriate location.

        Sections are added in a logical order, not just appended to the end.

        Args:
            content: Current specification content
            section_name: Name of section to add
            section_template: Template content for the section

        Returns:
            Modified content with section added
        """
        # Define section order for insertion
        section_order = [
            "Metadata",
            "Executive Summary",
            "Problem Statement",
            "Proposed Solution",
            "Detailed Requirements",
            "Functional Requirements",
            "Non-Functional Requirements",
            "User Stories",
            "Acceptance Criteria",
            "Technical Constraints",
            "Dependencies",
            "Risks and Mitigations",
            "Success Criteria",
            "Open Questions",
            "Appendix"
        ]

        # Find insertion point
        lines = content.split("\n")
        insertion_index = len(lines)  # Default: append to end

        # Try to find the best insertion point based on section order
        section_index = section_order.index(section_name) if section_name in section_order else -1

        if section_index >= 0:
            # Find the section that should come after this one
            for i in range(section_index + 1, len(section_order)):
                next_section = section_order[i]
                marker = f"## {next_section}"

                for line_num, line in enumerate(lines):
                    if line.strip() == marker:
                        insertion_index = line_num
                        break

                if insertion_index < len(lines):
                    break

        # Insert the section
        lines.insert(insertion_index, "")
        lines.insert(insertion_index + 1, section_template)
        lines.insert(insertion_index + 2, "")

        return "\n".join(lines)

    def generate_diff(self, original_path: Path, modified_path: Path) -> str:
        """
        Generate a unified diff between original and modified files.

        Args:
            original_path: Path to original file
            modified_path: Path to modified file

        Returns:
            Unified diff as string
        """
        original_lines = original_path.read_text(encoding='utf-8').splitlines(keepends=True)
        modified_lines = modified_path.read_text(encoding='utf-8').splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=str(original_path),
            tofile=str(modified_path),
            lineterm=''
        )

        return ''.join(diff)

    def generate_diff_from_content(self, original_content: str, modified_content: str, filename: str = "spec") -> str:
        """
        Generate a unified diff from content strings.

        Args:
            original_content: Original content
            modified_content: Modified content
            filename: Name to use in diff header

        Returns:
            Unified diff as string
        """
        original_lines = original_content.splitlines(keepends=True)
        modified_lines = modified_content.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"{filename} (original)",
            tofile=f"{filename} (fixed)",
            lineterm=''
        )

        return ''.join(diff)

    def validate_partial(self, spec_path: Path) -> ValidationProgress:
        """
        Perform partial/progressive validation on an incomplete specification.

        This method validates a spec that may be incomplete, returning progress
        information instead of errors. It's designed for incremental spec building.

        Args:
            spec_path: Path to specification file

        Returns:
            ValidationProgress with completion percentage and section statuses

        Raises:
            FileNotFoundError: If spec file doesn't exist

        Example:
            >>> validator = Validator()
            >>> progress = validator.validate_partial(Path("specs/001-feature/spec-001.md"))
            >>> print(f"Spec is {progress.completion_pct}% complete")
            >>> print(f"Next: {progress.next_suggestion}")
        """
        if not spec_path.exists():
            raise FileNotFoundError(f"Specification file not found: {spec_path}")

        # Read spec content
        spec_content = spec_path.read_text(encoding='utf-8')

        # Use ProgressCalculator to analyze completion
        calculator = ProgressCalculator()
        progress_result = calculator.calculate_completion_percentage(spec_content)

        # Get next section suggestion
        next_suggestion = calculator.suggest_next_section(progress_result.section_statuses)

        # Count section statuses
        complete_count = sum(1 for status in progress_result.section_statuses.values() if status == SectionStatus.COMPLETE)
        partial_count = sum(1 for status in progress_result.section_statuses.values() if status == SectionStatus.PARTIAL)
        missing_count = sum(1 for status in progress_result.section_statuses.values() if status == SectionStatus.MISSING)

        return ValidationProgress(
            completion_pct=progress_result.completion_percentage,
            section_statuses=progress_result.section_statuses,
            next_suggestion=next_suggestion,
            total_sections=len(progress_result.section_statuses),
            complete_sections=complete_count,
            partial_sections=partial_count,
            missing_sections=missing_count
        )