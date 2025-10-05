"""
SpecPulse Validator - Enhanced with comprehensive validation rules
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
import yaml
import re
from .validation_rules import (
    validation_rules_registry, ValidationResult, ValidationSeverity,
    ValidationCategory
)


class Validator:
    """Validates SpecPulse project components with enhanced rules"""

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