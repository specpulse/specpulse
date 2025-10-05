"""
Integration tests for SpecPulse
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import yaml

from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.cli.main import SpecPulseCLI


class TestIntegration:
    """Integration tests for SpecPulse workflow"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_complete_workflow(self):
        """Test complete SpecPulse workflow"""

        # 1. Initialize project structure
        self._create_project_structure()

        # 2. Validate project structure
        validator = Validator()
        results = validator.validate_all(self.project_path)
        assert isinstance(results, list)

        # 3. Check SDD compliance
        sdd_results = validator.validate_sdd_compliance(self.project_path)
        assert isinstance(sdd_results, list)

        # 4. Validate specific spec
        spec_results = validator.validate_spec(self.project_path)
        assert isinstance(spec_results, list)

        # 5. Validate specific plan
        plan_results = validator.validate_plan(self.project_path)
        assert isinstance(plan_results, list)

    def test_spec_to_plan_workflow(self):
        """Test specification to plan workflow"""

        # Create spec
        specs_dir = self.project_path / "specs" / "001-feature"
        specs_dir.mkdir(parents=True)
        spec_file = specs_dir / "spec.md"
        spec_file.write_text("""
# Feature Specification

## Requirements
- User authentication
- Data persistence
- API endpoints

## User Stories
- As a user, I want to log in
- As a user, I want to save data

## Acceptance Criteria
- Login works with email/password
- Data is saved to database
- API returns proper status codes
        """)

        # Validate spec
        validator = Validator()
        result = validator.validate_spec_file(spec_file)
        assert result["status"] == "valid"

        # Create corresponding plan
        plans_dir = self.project_path / "plans" / "001-feature"
        plans_dir.mkdir(parents=True)
        plan_file = plans_dir / "plan.md"
        plan_file.write_text("""
# Implementation Plan

## Architecture
- MVC pattern
- REST API
- PostgreSQL database

## Phases
### Phase 1: Setup
- Initialize project
- Set up database

### Phase 2: Implementation
- Create models
- Implement controllers
- Build API endpoints

## Technology Stack
- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
        """)

        # Validate plan
        result = validator.validate_plan_file(plan_file)
        assert result["status"] == "valid"

    def test_sdd_principles_validation(self):
        """Test SDD principles validation"""

        # Create constitution with all principles
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir(parents=True)
        constitution_file = memory_dir / "constitution.md"
        constitution_file.write_text("""
# Project Constitution

## Principle 1: SPECIFICATION FIRST
Every feature must begin with a clear, detailed specification.

## Principle 2: INCREMENTAL PLANNING
Development proceeds through well-defined, manageable phases.

## Principle 3: TASK DECOMPOSITION
Complex features are broken down into atomic, implementable tasks.

## Principle 4: TRACEABLE IMPLEMENTATION
Every line of code traces back to a specification requirement.

## Principle 5: CONTINUOUS VALIDATION
Quality gates ensure standards at every phase.

## Principle 6: QUALITY ASSURANCE
Comprehensive testing at all levels.

## Principle 7: ARCHITECTURE DOCUMENTATION
All architectural decisions are documented.

## Principle 8: ITERATIVE REFINEMENT
Continuous improvement through feedback loops.

## Principle 9: STAKEHOLDER ALIGNMENT
Regular communication and alignment with stakeholders.
        """)

        # Load and validate constitution
        validator = Validator()
        loaded = validator.load_constitution(self.project_path)
        assert loaded is True
        assert validator.constitution is not None

        # Check SDD compliance of a spec
        spec_content = """
# Feature Specification
This specification follows SDD principles.
All requirements are clearly defined.
        """

        result = validator.validate_sdd_principles(spec_content)
        assert result["status"] == "compliant"

    def test_project_validation(self):
        """Test complete project validation"""

        # Create complete project
        self._create_complete_project()

        # Validate entire project
        validator = Validator()
        result = validator.validate_all_project(self.project_path)

        assert isinstance(result, dict)
        assert "specs" in result
        assert "plans" in result
        assert "tasks" in result
        assert "sdd_compliance" in result

    def test_phase_gates(self):
        """Test phase gate checking"""

        validator = Validator()

        # Test specification gate
        context = {"spec_complete": True}
        result = validator.check_phase_gate("specification", context)
        assert result is True

        context = {"spec_complete": False}
        result = validator.check_phase_gate("specification", context)
        assert result is False

        # Test test-first gate
        context = {"tests_written": True}
        result = validator.check_phase_gate("test-first", context)
        assert result is True

    def _create_project_structure(self):
        """Helper to create basic project structure"""
        directories = [
            "specs",
            "plans",
            "tasks",
            "memory",
            "templates",
            "scripts",
            ".claude/commands",
            ".gemini/commands"
        ]

        for dir_path in directories:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

    def _create_complete_project(self):
        """Helper to create complete project with content"""
        self._create_project_structure()

        # Add constitution
        constitution = self.project_path / "memory" / "constitution.md"
        constitution.write_text("""
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

        # Add context and decisions
        (self.project_path / "memory" / "context.md").write_text("# Context\nProject context")
        (self.project_path / "memory" / "decisions.md").write_text("# Decisions\nArchitectural decisions")

        # Add specs
        spec_dir = self.project_path / "specs" / "001-auth"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("""
# Authentication Specification
## Requirements
- User login
- User registration
## User Stories
- As a user, I want to log in
## Acceptance Criteria
- Secure authentication
        """)

        # Add plans
        plan_dir = self.project_path / "plans" / "001-auth"
        plan_dir.mkdir(parents=True)
        (plan_dir / "plan.md").write_text("""
# Authentication Plan
## Architecture
- JWT tokens
## Phases
- Phase 1: Setup
## Technology Stack
- Python
        """)

        # Add tasks
        task_dir = self.project_path / "tasks" / "001-auth"
        task_dir.mkdir(parents=True)
        (task_dir / "tasks.md").write_text("""
# Tasks
## T001: Setup database
- Complexity: Simple
## T002: Create user model
- Complexity: Simple
## T003: Implement JWT
- Complexity: Medium
        """)

        # Add templates
        (self.project_path / "templates" / "spec.md").write_text("# Spec Template")
        (self.project_path / "templates" / "plan.md").write_text("# Plan Template")
        (self.project_path / "templates" / "task.md").write_text("# Task Template")

        # Add manifest
        manifest = self.project_path / ".specpulse.yaml"
        manifest.write_text(yaml.dump({
            "name": "test-project",
            "version": "1.0.0",
            "created": "2024-01-01"
        }))