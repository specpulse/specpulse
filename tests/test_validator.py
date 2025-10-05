"""
Tests for Validator module
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from specpulse.core.validator import Validator


class TestValidator:
    """Test Validator functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_init_without_project_root(self):
        """Test Validator initialization without project root"""
        validator = Validator()
        assert validator.results == []
        assert validator.constitution is None
        assert validator.phase_gates == []

    def test_init_with_project_root(self):
        """Test Validator initialization with project root"""
        # Create constitution file
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir(parents=True)
        constitution_path = memory_dir / "constitution.md"
        constitution_path.write_text("""
# Constitution
## Principle 1: Specification First
Every feature starts with clear specification.
        """)

        validator = Validator(self.project_path)
        assert validator.results == []
        assert validator.constitution is not None

    def test_validate_all(self):
        """Test validate_all method"""
        validator = Validator()

        # Create basic structure
        for dir_name in ["specs", "plans", "tasks", "memory", "templates", "scripts"]:
            (self.project_path / dir_name).mkdir()

        results = validator.validate_all(self.project_path)
        assert isinstance(results, list)

    def test_validate_spec_no_directory(self):
        """Test validate_spec with no specs directory"""
        validator = Validator()

        results = validator.validate_spec(self.project_path)
        assert len(results) > 0
        assert any(r["status"] == "error" for r in results)
        assert any("No specs directory" in r["message"] for r in results)

    def test_validate_spec_with_directory(self):
        """Test validate_spec with specs directory"""
        validator = Validator()

        specs_dir = self.project_path / "specs"
        specs_dir.mkdir()

        # Create a spec
        spec_dir = specs_dir / "001-test"
        spec_dir.mkdir()
        (spec_dir / "spec.md").write_text("""
# Specification
## Requirements
- Test requirement
## User Stories
- As a user
## Acceptance Criteria
- It works
        """)

        results = validator.validate_spec(self.project_path)
        assert isinstance(results, list)

    def test_validate_spec_with_name(self):
        """Test validate_spec with specific spec name"""
        validator = Validator()

        specs_dir = self.project_path / "specs"
        spec_dir = specs_dir / "001-test"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Test Spec")

        results = validator.validate_spec(self.project_path, spec_name="001-test")
        assert isinstance(results, list)

    def test_validate_plan_no_directory(self):
        """Test validate_plan with no plans directory"""
        validator = Validator()

        results = validator.validate_plan(self.project_path)
        assert len(results) > 0
        assert any("warning" in r.get("status", "") for r in results)

    def test_validate_plan_with_directory(self):
        """Test validate_plan with plans directory"""
        validator = Validator()

        plans_dir = self.project_path / "plans"
        plans_dir.mkdir()

        # Create a plan
        plan_dir = plans_dir / "001-test"
        plan_dir.mkdir()
        (plan_dir / "plan.md").write_text("""
# Plan
## Architecture
- Component design
## Phases
- Phase 1
## Technology Stack
- Python
        """)

        results = validator.validate_plan(self.project_path)
        assert isinstance(results, list)

    def test_validate_sdd_compliance(self):
        """Test validate_sdd_compliance method"""
        validator = Validator()

        # Create constitution
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text("""
# Constitution
## Principle 1: Specification First
## Principle 2: Incremental Planning
## Principle 3: Task Decomposition
## Principle 4: Traceable Implementation
## Principle 5: Continuous Validation
## Principle 6: Quality Assurance
## Principle 7: Architecture Documentation
## Principle 8: Iterative Refinement
## Principle 9: Stakeholder Alignment
        """)

        results = validator.validate_sdd_compliance(self.project_path)
        assert isinstance(results, list)

    def test_validate_spec_file(self):
        """Test validate_spec_file method"""
        validator = Validator()

        spec_path = self.project_path / "spec.md"
        spec_path.write_text("""
# Specification
## Requirements
- Requirement 1
## User Stories
- Story 1
## Acceptance Criteria
- Criteria 1
        """)

        result = validator.validate_spec_file(spec_path)
        assert isinstance(result, dict)
        assert "status" in result

    def test_validate_plan_file(self):
        """Test validate_plan_file method"""
        validator = Validator()

        plan_path = self.project_path / "plan.md"
        plan_path.write_text("""
# Plan
## Architecture
- Design
## Phases
- Phase 1
## Technology Stack
- Stack
        """)

        result = validator.validate_plan_file(plan_path)
        assert isinstance(result, dict)
        assert "status" in result

    def test_validate_task_file(self):
        """Test validate_task_file method"""
        validator = Validator()

        task_path = self.project_path / "task.md"
        task_path.write_text("""
# Tasks
## T001: First Task
- Description
- Complexity: Simple
        """)

        result = validator.validate_task_file(task_path)
        assert isinstance(result, dict)
        assert "status" in result

    def test_validate_sdd_principles(self):
        """Test validate_sdd_principles method"""
        validator = Validator()

        spec_content = """
# Specification
This follows SDD principles.
        """

        result = validator.validate_sdd_principles(spec_content)
        assert isinstance(result, dict)
        assert "status" in result

    def test_check_phase_gate(self):
        """Test check_phase_gate method"""
        validator = Validator()

        context = {"spec_complete": True}
        result = validator.check_phase_gate("specification", context)
        assert isinstance(result, bool)

    def test_validate_all_project(self):
        """Test validate_all_project method"""
        validator = Validator()

        # Create minimal structure
        (self.project_path / "specs").mkdir()
        (self.project_path / "plans").mkdir()
        (self.project_path / "memory").mkdir()

        result = validator.validate_all_project(self.project_path)
        assert isinstance(result, dict)
        assert "specs" in result
        assert "plans" in result
        assert "tasks" in result

    def test_load_constitution(self):
        """Test load_constitution method"""
        validator = Validator()

        # Create constitution
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text("""
# Constitution
## Principle 1: Test Principle
        """)

        result = validator.load_constitution(self.project_path)
        assert result is True
        assert validator.constitution is not None

    def test_load_constitution_missing(self):
        """Test load_constitution with missing file"""
        validator = Validator()

        result = validator.load_constitution(self.project_path)
        assert result is False