"""
SpecPulse Validator
"""

from pathlib import Path
from typing import List, Dict, Optional
import yaml
import re


class Validator:
    """Validates SpecPulse project components"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.results = []
        self.constitution = None
        self.phase_gates = []
        
        if project_root:
            self._load_constitution(project_root)
    
    def validate_all(self, project_path: Path, fix: bool = False, verbose: bool = False) -> List[Dict]:
        """Validate entire project"""
        self.results = []
        
        # Check project structure
        self._validate_structure(project_path)
        
        # Validate specifications
        self._validate_specs(project_path, fix, verbose)
        
        # Validate plans
        self._validate_plans(project_path, fix, verbose)
        
        # Validate SDD principles compliance
        self._validate_sdd_compliance(project_path, verbose)
        
        return self.results
    
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
        """Validate a single specification"""
        with open(spec_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        spec_name = spec_path.parent.name
        
        # Check required sections
        required_sections = [
            "## Requirements",
            "## User Stories",
            "## Acceptance Criteria"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            if fix:
                # Attempt to add missing sections
                for section in missing_sections:
                    content += f"\n\n{section}\n[To be completed]\n"
                with open(spec_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.results.append({
                    "status": "warning",
                    "message": f"Fixed missing sections in {spec_name}"
                })
            else:
                self.results.append({
                    "status": "error",
                    "message": f"{spec_name}: Missing sections: {', '.join(missing_sections)}"
                })
        else:
            self.results.append({
                "status": "success",
                "message": f"{spec_name}: All required sections present"
            })
        
        # Check for clarification markers
        if "[NEEDS CLARIFICATION]" in content:
            clarifications = re.findall(r'\[NEEDS CLARIFICATION\].*', content)
            if verbose:
                for clarification in clarifications:
                    self.results.append({
                        "status": "warning",
                        "message": f"{spec_name}: {clarification}"
                    })
            else:
                self.results.append({
                    "status": "warning",
                    "message": f"{spec_name}: Contains {len(clarifications)} items needing clarification"
                })
    
    def _validate_single_plan(self, plan_path: Path, fix: bool, verbose: bool):
        """Validate a single implementation plan"""
        with open(plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        plan_name = plan_path.parent.name
        
        # Check required sections
        required_sections = [
            "## Architecture",
            "## Technology Stack",
            "## Implementation Phases"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            if fix:
                # Attempt to add missing sections
                for section in missing_sections:
                    content += f"\n\n{section}\n[To be completed]\n"
                with open(plan_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.results.append({
                    "status": "warning",
                    "message": f"Fixed missing sections in {plan_name}"
                })
            else:
                self.results.append({
                    "status": "error",
                    "message": f"{plan_name}: Missing sections: {', '.join(missing_sections)}"
                })
        else:
            self.results.append({
                "status": "success",
                "message": f"{plan_name}: All required sections present"
            })
        
        # Check for specification reference
        if "Spec ID" not in content:
            self.results.append({
                "status": "warning",
                "message": f"{plan_name}: No specification reference found"
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