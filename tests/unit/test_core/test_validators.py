"""
Tests for specialized validators

These tests verify the refactored validator modules.
"""

import pytest
from pathlib import Path
import tempfile

from specpulse.core.validators.spec_validator import SpecValidator
from specpulse.core.validators.plan_validator import PlanValidator
from specpulse.core.validators.sdd_validator import SddValidator


class TestSpecValidator:
    """Test SpecValidator functionality"""

    def test_spec_validator_initialization(self):
        """Test SpecValidator initializes correctly"""
        validator = SpecValidator()

        assert validator is not None
        assert validator.backup_manager is not None

    def test_spec_validator_with_project_root(self):
        """Test SpecValidator with project root"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            validator = SpecValidator(project_root)

            assert validator.project_root == project_root


class TestPlanValidator:
    """Test PlanValidator functionality"""

    def test_plan_validator_initialization(self):
        """Test PlanValidator initializes correctly"""
        validator = PlanValidator()

        assert validator is not None
        assert validator.backup_manager is not None

    def test_plan_validator_with_project_root(self):
        """Test PlanValidator with project root"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            validator = PlanValidator(project_root)

            assert validator.project_root == project_root


class TestSddValidator:
    """Test SddValidator functionality"""

    def test_sdd_validator_initialization(self):
        """Test SddValidator initializes correctly"""
        validator = SddValidator()

        assert validator is not None
        assert validator.SDD_PRINCIPLES is not None
        assert len(validator.SDD_PRINCIPLES) > 0

    def test_sdd_principles_defined(self):
        """Test that SDD principles are properly defined"""
        validator = SddValidator()

        expected_principles = [
            'specification_first',
            'clear_acceptance',
            'traceability',
            'iterative_refinement',
            'ai_collaboration',
            'phase_gates',
            'documentation'
        ]

        for principle in expected_principles:
            assert principle in validator.SDD_PRINCIPLES
            assert 'name' in validator.SDD_PRINCIPLES[principle]
            assert 'description' in validator.SDD_PRINCIPLES[principle]
            assert 'check' in validator.SDD_PRINCIPLES[principle]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
