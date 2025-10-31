"""
SDD Compliance Validator

This module handles validation of Specification-Driven Development (SDD)
principles and compliance checks across the project.
"""

from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import yaml
import re

from ..validation_rules import ValidationSeverity


@dataclass
class SddComplianceResult:
    """Result of SDD compliance validation"""
    compliant: bool
    principles_checked: Dict[str, bool]
    violations: List[str]
    recommendations: List[str]
    score: float


class SddValidator:
    """Validator for SDD compliance"""

    # SDD Principles
    SDD_PRINCIPLES = {
        'specification_first': {
            'name': 'Specification First',
            'description': 'All features must have specifications before implementation',
            'check': 'spec_before_code'
        },
        'clear_acceptance': {
            'name': 'Clear Acceptance Criteria',
            'description': 'All specifications must have clear, testable acceptance criteria',
            'check': 'has_acceptance_criteria'
        },
        'traceability': {
            'name': 'Traceability',
            'description': 'Requirements must be traceable from spec to implementation',
            'check': 'has_traceability'
        },
        'iterative_refinement': {
            'name': 'Iterative Refinement',
            'description': 'Specifications can be refined iteratively based on feedback',
            'check': 'allows_refinement'
        },
        'ai_collaboration': {
            'name': 'AI Collaboration',
            'description': 'Specifications should be AI-friendly and machine-readable',
            'check': 'ai_friendly'
        },
        'phase_gates': {
            'name': 'Phase Gates',
            'description': 'Development follows defined phase gates',
            'check': 'has_phase_gates'
        },
        'documentation': {
            'name': 'Living Documentation',
            'description': 'Specifications serve as living documentation',
            'check': 'is_documented'
        }
    }

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.constitution_path = self.project_root / "memory" / "constitution.yaml"
        self.constitution = self._load_constitution()

    def validate_sdd_compliance(self, project_path: Path, verbose: bool = False) -> SddComplianceResult:
        """
        Validate project's SDD compliance

        Args:
            project_path: Path to project root
            verbose: Verbose output

        Returns:
            SddComplianceResult with compliance details
        """
        principles_checked = {}
        violations = []
        recommendations = []

        # Check each SDD principle
        for principle_id, principle in self.SDD_PRINCIPLES.items():
            is_compliant = self._check_principle(project_path, principle_id, principle)
            principles_checked[principle_id] = is_compliant

            if not is_compliant:
                violations.append(f"{principle['name']}: {principle['description']}")
                recommendations.append(f"Ensure {principle['name'].lower()} is followed in the project")

        # Calculate compliance score
        score = (sum(principles_checked.values()) / len(principles_checked)) * 100

        is_compliant = score >= 70  # 70% minimum compliance

        return SddComplianceResult(
            compliant=is_compliant,
            principles_checked=principles_checked,
            violations=violations,
            recommendations=recommendations,
            score=score
        )

    def _check_principle(self, project_path: Path, principle_id: str, principle: Dict) -> bool:
        """Check if a specific SDD principle is followed"""
        check_method = principle['check']

        if check_method == 'spec_before_code':
            return self._check_spec_before_code(project_path)
        elif check_method == 'has_acceptance_criteria':
            return self._check_acceptance_criteria(project_path)
        elif check_method == 'has_traceability':
            return self._check_traceability(project_path)
        elif check_method == 'allows_refinement':
            return self._check_refinement(project_path)
        elif check_method == 'ai_friendly':
            return self._check_ai_friendly(project_path)
        elif check_method == 'has_phase_gates':
            return self._check_phase_gates(project_path)
        elif check_method == 'is_documented':
            return self._check_documentation(project_path)

        return False

    def _check_spec_before_code(self, project_path: Path) -> bool:
        """Check if specs exist before code"""
        specs_dir = project_path / "specs"
        # If specs directory exists and has specs, consider compliant
        return specs_dir.exists() and any(specs_dir.iterdir())

    def _check_acceptance_criteria(self, project_path: Path) -> bool:
        """Check if specs have acceptance criteria"""
        specs_dir = project_path / "specs"
        if not specs_dir.exists():
            return False

        total_specs = 0
        specs_with_criteria = 0

        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_path = spec_dir / "spec.md"
                if spec_path.exists():
                    total_specs += 1
                    content = spec_path.read_text(encoding='utf-8')
                    if '## Acceptance Criteria' in content or '## Acceptance' in content:
                        specs_with_criteria += 1

        if total_specs == 0:
            return False

        # At least 80% of specs should have acceptance criteria
        return (specs_with_criteria / total_specs) >= 0.8

    def _check_traceability(self, project_path: Path) -> bool:
        """Check if requirements are traceable"""
        # Check for metadata linking specs to plans to tasks
        specs_dir = project_path / "specs"
        if not specs_dir.exists():
            return False

        total_specs = 0
        traceable_specs = 0

        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_path = spec_dir / "spec.md"
                if spec_path.exists():
                    total_specs += 1
                    content = spec_path.read_text(encoding='utf-8')
                    # Check for metadata
                    if '<!-- FEATURE_ID:' in content:
                        traceable_specs += 1

        if total_specs == 0:
            return False

        return (traceable_specs / total_specs) >= 0.8

    def _check_refinement(self, project_path: Path) -> bool:
        """Check if specifications support iterative refinement"""
        # Check for version control and status tracking
        specs_dir = project_path / "specs"
        if not specs_dir.exists():
            return False

        # Check if specs have status metadata
        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_path = spec_dir / "spec.md"
                if spec_path.exists():
                    content = spec_path.read_text(encoding='utf-8')
                    if '<!-- STATUS:' in content:
                        return True

        return False

    def _check_ai_friendly(self, project_path: Path) -> bool:
        """Check if specifications are AI-friendly"""
        # Check for structured metadata and clear formatting
        specs_dir = project_path / "specs"
        if not specs_dir.exists():
            return False

        ai_friendly_count = 0
        total_specs = 0

        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_path = spec_dir / "spec.md"
                if spec_path.exists():
                    total_specs += 1
                    content = spec_path.read_text(encoding='utf-8')

                    # Check for AI-friendly features
                    has_metadata = '<!--' in content
                    has_structure = '##' in content
                    has_variables = '{{' in content or 'AI:' in content

                    if has_metadata and has_structure:
                        ai_friendly_count += 1

        if total_specs == 0:
            return False

        return (ai_friendly_count / total_specs) >= 0.7

    def _check_phase_gates(self, project_path: Path) -> bool:
        """Check if phase gates are defined"""
        # Check for phase gates in constitution or plans
        if self.constitution and 'phase_gates' in self.constitution:
            return True

        plans_dir = project_path / "plans"
        if plans_dir.exists():
            for plan_dir in plans_dir.iterdir():
                if plan_dir.is_dir():
                    plan_path = plan_dir / "plan.md"
                    if plan_path.exists():
                        content = plan_path.read_text(encoding='utf-8')
                        if 'Phase' in content and 'Gate' in content:
                            return True

        return False

    def _check_documentation(self, project_path: Path) -> bool:
        """Check if specifications serve as living documentation"""
        # Check if specs are comprehensive and up-to-date
        specs_dir = project_path / "specs"
        if not specs_dir.exists():
            return False

        documented_specs = 0
        total_specs = 0

        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_path = spec_dir / "spec.md"
                if spec_path.exists():
                    total_specs += 1
                    content = spec_path.read_text(encoding='utf-8')

                    # Check for comprehensive documentation
                    word_count = len(content.split())
                    has_sections = len(re.findall(r'^##\s+', content, re.MULTILINE))

                    if word_count > 200 and has_sections >= 3:
                        documented_specs += 1

        if total_specs == 0:
            return False

        return (documented_specs / total_specs) >= 0.7

    def _load_constitution(self) -> Optional[Dict]:
        """Load project constitution if exists"""
        if self.constitution_path.exists():
            try:
                with open(self.constitution_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception:
                return None
        return None

    def validate_constitution(self, project_path: Path) -> Dict:
        """
        Validate project constitution file

        Args:
            project_path: Path to project root

        Returns:
            Dict with validation results
        """
        constitution_path = project_path / "memory" / "constitution.yaml"

        if not constitution_path.exists():
            return {
                'valid': False,
                'error': 'Constitution file not found',
                'suggestion': 'Create memory/constitution.yaml to define project SDD principles'
            }

        try:
            with open(constitution_path, 'r', encoding='utf-8') as f:
                constitution = yaml.safe_load(f)

            # Validate constitution structure
            required_keys = ['project_name', 'sdd_principles', 'phase_gates']
            missing_keys = [key for key in required_keys if key not in constitution]

            if missing_keys:
                return {
                    'valid': False,
                    'errors': [f"Missing required key: {key}" for key in missing_keys],
                    'suggestion': f"Add missing keys to constitution: {', '.join(missing_keys)}"
                }

            return {
                'valid': True,
                'principles_count': len(constitution.get('sdd_principles', [])),
                'phase_gates_count': len(constitution.get('phase_gates', []))
            }

        except yaml.YAMLError as e:
            return {
                'valid': False,
                'error': f'Invalid YAML: {e}',
                'suggestion': 'Fix YAML syntax errors in constitution.yaml'
            }
