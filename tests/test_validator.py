"""
Tests for Validator module
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from specpulse.core.validator import Validator, ValidationExample


@pytest.mark.validation
class TestValidationExample:
    """Test ValidationExample dataclass."""

    def test_create_validation_example(self):
        """Test creating a ValidationExample instance."""
        example = ValidationExample(
            message="Missing: Acceptance Criteria",
            meaning="Acceptance criteria define when the feature is done",
            example="✓ User can login\n✓ Error shown for invalid credentials",
            suggestion="Add section '## Acceptance Criteria' with 3-5 checkboxes",
            help_command="specpulse help acceptance-criteria",
            auto_fix=True
        )

        assert example.message == "Missing: Acceptance Criteria"
        assert example.meaning == "Acceptance criteria define when the feature is done"
        assert "User can login" in example.example
        assert example.auto_fix is True

    def test_validation_example_default_auto_fix(self):
        """Test that auto_fix defaults to False."""
        example = ValidationExample(
            message="Test message",
            meaning="Test meaning",
            example="Test example",
            suggestion="Test suggestion",
            help_command="test command"
        )

        assert example.auto_fix is False

    def test_validation_example_str_representation(self):
        """Test string representation of ValidationExample."""
        example = ValidationExample(
            message="Missing: User Stories",
            meaning="User stories describe features from user perspective",
            example="As a user, I want to...",
            suggestion="Add user stories section",
            help_command="specpulse help user-stories"
        )

        str_repr = str(example)
        assert "Missing: User Stories" in str_repr
        assert "What this means:" in str_repr
        assert "User stories describe features from user perspective" in str_repr
        assert "Suggestion:" in str_repr
        assert "Add user stories section" in str_repr

    def test_validation_example_all_fields_required(self):
        """Test that all required fields must be provided."""
        # This should work
        example = ValidationExample(
            message="msg",
            meaning="mean",
            example="ex",
            suggestion="sug",
            help_command="help"
        )
        assert example is not None

        # Missing fields should raise TypeError
        with pytest.raises(TypeError):
            ValidationExample(
                message="msg",
                meaning="mean"
                # Missing: example, suggestion, help_command
            )

    def test_validation_example_multiline_example(self):
        """Test that multiline examples are supported."""
        multiline_example = """
        ✓ User can login with email/password
        ✓ Invalid credentials show error message
        ✓ Successful login redirects to dashboard
        ✓ Session expires after 30 minutes
        """

        example = ValidationExample(
            message="Test",
            meaning="Test",
            example=multiline_example,
            suggestion="Test",
            help_command="test"
        )

        assert "User can login" in example.example
        assert "Invalid credentials" in example.example
        assert "\n" in example.example  # Multiline preserved


@pytest.mark.validation
class TestLoadValidationExamples:
    """Test loading validation examples from YAML."""

    def test_load_validation_examples(self):
        """Test that validation examples load successfully."""
        examples = Validator.load_validation_examples()

        assert examples is not None
        assert isinstance(examples, dict)
        assert len(examples) > 0

    def test_validation_examples_cache(self):
        """Test that examples are cached after first load."""
        # Clear cache first
        Validator._validation_examples_cache = None

        # First load
        examples1 = Validator.load_validation_examples()

        # Second load should return cached version
        examples2 = Validator.load_validation_examples()

        assert examples1 is examples2  # Same object reference (cached)

    def test_validation_examples_have_required_fields(self):
        """Test that all loaded examples have required fields."""
        examples = Validator.load_validation_examples()

        for key, example in examples.items():
            assert isinstance(example, ValidationExample)
            assert example.message, f"Example {key} missing message"
            assert example.meaning, f"Example {key} missing meaning"
            assert example.example, f"Example {key} missing example"
            assert example.suggestion, f"Example {key} missing suggestion"
            assert example.help_command, f"Example {key} missing help_command"
            assert isinstance(example.auto_fix, bool), f"Example {key} auto_fix not bool"

    def test_validation_examples_contain_expected_keys(self):
        """Test that expected validation examples are present."""
        examples = Validator.load_validation_examples()

        expected_keys = [
            "missing_executive_summary",
            "missing_problem_statement",
            "missing_functional_requirements",
            "missing_user_stories",
            "missing_acceptance_criteria",
        ]

        for key in expected_keys:
            assert key in examples, f"Expected example key '{key}' not found"

    def test_get_validation_example(self):
        """Test getting a specific validation example."""
        validator = Validator()
        example = validator.get_validation_example("missing_acceptance_criteria")

        assert example is not None
        assert isinstance(example, ValidationExample)
        assert "Acceptance Criteria" in example.message

    def test_get_nonexistent_validation_example(self):
        """Test getting a validation example that doesn't exist."""
        validator = Validator()
        example = validator.get_validation_example("nonexistent_example")

        assert example is None

    def test_validation_examples_yaml_parsing(self):
        """Test that YAML parsing works correctly."""
        # Clear cache to force reload
        Validator._validation_examples_cache = None

        examples = Validator.load_validation_examples()

        # Check that multiline content is preserved
        problem_statement_ex = examples.get("missing_problem_statement")
        if problem_statement_ex:
            assert "\n" in problem_statement_ex.example  # Multiline preserved

    def test_validation_examples_auto_fix_flag(self):
        """Test that auto_fix flag is correctly parsed."""
        examples = Validator.load_validation_examples()

        # Some examples should have auto_fix = True
        auto_fixable = [ex for ex in examples.values() if ex.auto_fix]
        assert len(auto_fixable) > 0, "No auto-fixable examples found"

        # Some should have auto_fix = False
        not_auto_fixable = [ex for ex in examples.values() if not ex.auto_fix]
        assert len(not_auto_fixable) > 0, "All examples are auto-fixable (unexpected)"


@pytest.mark.validation
class TestCheckSectionExists:
    """Test _check_section_exists method."""

    def test_section_exists_returns_none(self):
        """Test that method returns None when section exists."""
        validator = Validator()
        content = """
        # Specification: Test

        ## Executive Summary
        This is the executive summary.

        ## Problem Statement
        This is the problem.
        """

        error = validator._check_section_exists(content, "Executive Summary")
        assert error is None

        error = validator._check_section_exists(content, "Problem Statement")
        assert error is None

    def test_missing_section_returns_validation_example(self):
        """Test that method returns ValidationExample when section is missing."""
        validator = Validator()
        content = """
        # Specification: Test

        ## Executive Summary
        Summary here.
        """

        error = validator._check_section_exists(content, "Acceptance Criteria")
        assert error is not None
        assert isinstance(error, ValidationExample)
        assert "Acceptance Criteria" in error.message

    def test_uses_predefined_examples_for_known_sections(self):
        """Test that predefined examples are used for known sections."""
        validator = Validator()
        content = "# Spec\n## Executive Summary\nText"

        error = validator._check_section_exists(content, "User Stories")
        assert error is not None
        # Should use the rich example from validation_examples.yaml
        assert len(error.meaning) > 50  # Predefined examples have detailed meanings
        assert "As a" in error.example or "user" in error.example.lower()

    def test_fallback_for_unknown_sections(self):
        """Test fallback ValidationExample for unknown sections."""
        validator = Validator()
        content = "# Spec\n## Executive Summary\nText"

        error = validator._check_section_exists(content, "Unknown Custom Section")
        assert error is not None
        assert isinstance(error, ValidationExample)
        assert "Unknown Custom Section" in error.message
        assert error.auto_fix is True  # Fallback examples are auto-fixable

    def test_section_mapping_coverage(self):
        """Test that all important sections are mapped."""
        validator = Validator()
        content = "# Spec"

        important_sections = [
            "Executive Summary",
            "Problem Statement",
            "Proposed Solution",
            "Functional Requirements",
            "User Stories",
            "Acceptance Criteria",
            "Technical Constraints",
            "Dependencies",
            "Risks and Mitigations",
        ]

        for section in important_sections:
            error = validator._check_section_exists(content, section)
            assert error is not None, f"Should return error for missing {section}"
            assert isinstance(error, ValidationExample)

    def test_section_check_is_case_sensitive(self):
        """Test that section checking respects markdown ## format."""
        validator = Validator()

        # Correct format - should pass
        content_correct = "# Spec\n## Executive Summary\nText"
        error = validator._check_section_exists(content_correct, "Executive Summary")
        assert error is None

        # Wrong level (# instead of ##) - should fail
        content_wrong_level = "# Spec\n# Executive Summary\nText"
        error = validator._check_section_exists(content_wrong_level, "Executive Summary")
        assert error is not None

    def test_enhanced_error_has_all_fields(self):
        """Test that enhanced errors have all required fields."""
        validator = Validator()
        content = "# Spec"

        error = validator._check_section_exists(content, "Acceptance Criteria")
        assert error is not None
        assert error.message
        assert error.meaning
        assert error.example
        assert error.suggestion
        assert error.help_command
        assert isinstance(error.auto_fix, bool)

    def test_multiple_missing_sections(self):
        """Test checking multiple sections."""
        validator = Validator()
        content = """
        # Specification: Test

        ## Executive Summary
        Summary here.

        ## Problem Statement
        Problem here.
        """

        # Check multiple missing sections
        missing_sections = []
        for section in ["User Stories", "Acceptance Criteria", "Dependencies"]:
            error = validator._check_section_exists(content, section)
            if error:
                missing_sections.append(section)

        assert len(missing_sections) == 3
        assert "User Stories" in missing_sections
        assert "Acceptance Criteria" in missing_sections
        assert "Dependencies" in missing_sections


@pytest.mark.validation
class TestFormatEnhancedError:
    """Test format_enhanced_error and format_enhanced_error_plain methods."""

    def test_format_enhanced_error_returns_string(self):
        """Test that format_enhanced_error returns a string."""
        validator = Validator()
        example = ValidationExample(
            message="Missing: Test Section",
            meaning="This is what it means",
            example="Example content here",
            suggestion="Add this section",
            help_command="specpulse help test",
            auto_fix=True
        )

        formatted = validator.format_enhanced_error(example)
        assert isinstance(formatted, str)
        assert len(formatted) > 0

    def test_format_enhanced_error_contains_all_sections(self):
        """Test that formatted output contains all required sections."""
        validator = Validator()
        example = ValidationExample(
            message="Missing: Acceptance Criteria",
            meaning="Defines when feature is done",
            example="✓ Test example",
            suggestion="Add acceptance criteria",
            help_command="specpulse help acceptance-criteria",
            auto_fix=True
        )

        formatted = validator.format_enhanced_error(example)

        # Check all sections are present (may be escaped or have formatting)
        assert "Acceptance Criteria" in formatted or "Missing" in formatted
        assert "What this means" in formatted
        assert "Example" in formatted
        assert "Suggestion" in formatted
        assert "Quick fix" in formatted  # Because auto_fix=True
        assert "Help" in formatted

    def test_format_enhanced_error_without_auto_fix(self):
        """Test formatted output when auto_fix is False."""
        validator = Validator()
        example = ValidationExample(
            message="Warning: Incomplete Section",
            meaning="Section needs more detail",
            example="Add more content",
            suggestion="Expand this section",
            help_command="specpulse help section",
            auto_fix=False
        )

        formatted = validator.format_enhanced_error(example)

        # Should NOT contain quick fix section
        assert "Quick fix" not in formatted or "--fix" not in formatted

    def test_format_enhanced_error_plain(self):
        """Test plain text formatting."""
        validator = Validator()
        example = ValidationExample(
            message="Missing: User Stories",
            meaning="User stories describe features from user perspective",
            example="**As a** user\n**I want** feature\n**So that** benefit",
            suggestion="Add user stories section",
            help_command="specpulse help user-stories",
            auto_fix=True
        )

        plain = validator.format_enhanced_error_plain(example)

        assert isinstance(plain, str)
        assert "Missing: User Stories" in plain
        assert "What this means:" in plain
        assert "Example:" in plain
        assert "Suggestion for LLM:" in plain
        assert "Quick fix:" in plain
        assert "Help:" in plain

    def test_format_enhanced_error_plain_multiline_example(self):
        """Test that multiline examples are properly formatted in plain text."""
        validator = Validator()
        example = ValidationExample(
            message="Test",
            meaning="Test meaning",
            example="Line 1\nLine 2\nLine 3",
            suggestion="Test suggestion",
            help_command="test help",
            auto_fix=False
        )

        plain = validator.format_enhanced_error_plain(example)

        # All lines should be present with indentation
        assert "Line 1" in plain
        assert "Line 2" in plain
        assert "Line 3" in plain

    def test_format_enhanced_error_with_real_example(self):
        """Test formatting with a real validation example from YAML."""
        validator = Validator()
        example = validator.get_validation_example("missing_acceptance_criteria")

        assert example is not None

        # Test Rich formatting
        formatted_rich = validator.format_enhanced_error(example)
        assert len(formatted_rich) > 100  # Should be substantial
        assert "Acceptance Criteria" in formatted_rich

        # Test plain formatting
        formatted_plain = validator.format_enhanced_error_plain(example)
        assert len(formatted_plain) > 100
        assert "Acceptance Criteria" in formatted_plain

    def test_format_enhanced_error_preserves_special_characters(self):
        """Test that special characters in examples are preserved."""
        validator = Validator()
        example = ValidationExample(
            message="Test",
            meaning="Test",
            example="✓ Item 1\n✓ Item 2\n→ Arrow",
            suggestion="Test",
            help_command="test",
            auto_fix=True
        )

        plain = validator.format_enhanced_error_plain(example)

        assert "✓" in plain
        assert "→" in plain


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