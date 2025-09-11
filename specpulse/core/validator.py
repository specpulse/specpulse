"""
SpecPulse Validator
"""

from pathlib import Path
from typing import List, Dict, Optional
import yaml
import re


class Validator:
    """Validates SpecPulse project components"""
    
    def __init__(self):
        self.results = []
    
    def validate_all(self, project_path: Path, fix: bool = False, verbose: bool = False) -> List[Dict]:
        """Validate entire project"""
        self.results = []
        
        # Check project structure
        self._validate_structure(project_path)
        
        # Validate specifications
        self._validate_specs(project_path, fix, verbose)
        
        # Validate plans
        self._validate_plans(project_path, fix, verbose)
        
        # Validate constitution compliance
        self._validate_constitution_compliance(project_path, verbose)
        
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
    
    def validate_constitution(self, project_path: Path, verbose: bool = False) -> List[Dict]:
        """Validate constitution compliance"""
        self.results = []
        self._validate_constitution_compliance(project_path, verbose)
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
    
    def _validate_constitution_compliance(self, project_path: Path, verbose: bool):
        """Validate compliance with constitution principles"""
        constitution_path = project_path / "memory" / "constitution.md"
        
        if not constitution_path.exists():
            self.results.append({
                "status": "error",
                "message": "Constitution file not found"
            })
            return
        
        with open(constitution_path, 'r', encoding='utf-8') as f:
            constitution = f.read()
        
        # Check for key principles
        principles = [
            "Simplicity First",
            "Test-Driven Development",
            "Single Responsibility",
            "Documentation as Code",
            "Security by Design"
        ]
        
        for principle in principles:
            if principle in constitution:
                if verbose:
                    self.results.append({
                        "status": "success",
                        "message": f"Constitution includes: {principle}"
                    })
            else:
                self.results.append({
                    "status": "warning",
                    "message": f"Constitution missing principle: {principle}"
                })
        
        # Check config for constitution enforcement
        config_path = project_path / ".specpulse" / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config.get("constitution", {}).get("enforce", False):
                self.results.append({
                    "status": "success",
                    "message": "Constitution enforcement enabled"
                })
            else:
                self.results.append({
                    "status": "warning",
                    "message": "Constitution enforcement disabled"
                })