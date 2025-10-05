"""
Integration tests for v1.8.0 validation feedback improvements.

Tests the complete workflow of all three components working together.
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from specpulse.core.validator import Validator, ValidationExample, ValidationProgress
from specpulse.core.custom_validation import RuleEngine, ProjectType
from specpulse.utils.project_detector import ProjectDetector


@pytest.mark.validation
class TestV180IntegrationWorkflow:
    """Integration tests for complete v1.8.0 validation workflow."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def create_spec(self, content: str) -> Path:
        """Create a test specification."""
        spec_dir = self.temp_path / "specs" / "001-test"
        spec_dir.mkdir(parents=True, exist_ok=True)
        spec_path = spec_dir / "spec-001.md"
        spec_path.write_text(content, encoding='utf-8')
        return spec_path

    def test_complete_validation_workflow(self):
        """Test complete workflow: validate → enhanced errors → partial → auto-fix."""
        validator = Validator()

        # Step 1: Create incomplete spec
        incomplete_spec = """# Specification: Test Feature

## Metadata
- ID: SPEC-001

## Executive Summary
Basic summary.
"""
        spec_path = self.create_spec(incomplete_spec)

        # Step 2: Check for missing sections (enhanced errors)
        error = validator._check_section_exists(incomplete_spec, "User Stories")
        assert error is not None
        assert isinstance(error, ValidationExample)
        assert len(error.meaning) > 50  # Enhanced error has detailed meaning

        # Step 3: Run partial validation
        progress = validator.validate_partial(spec_path)
        assert progress.completion_pct < 50  # Incomplete
        assert progress.missing_sections > 0
        assert progress.next_suggestion is not None

        # Step 4: Auto-fix missing sections
        success, changes, backup = validator.auto_fix_validation_issues(spec_path, backup=True)
        assert success is True
        assert len(changes) > 1  # Multiple sections added
        assert backup is not None and backup.exists()

        # Step 5: Validate again - should be better
        progress_after = validator.validate_partial(spec_path)
        assert progress_after.completion_pct > progress.completion_pct

    def test_enhanced_errors_with_partial_validation(self):
        """Test that enhanced errors work with partial validation."""
        validator = Validator()

        spec = """# Specification: Test

## Executive Summary
Summary here with enough content to be considered complete.

## Problem Statement
Problem description.
"""
        spec_path = self.create_spec(spec)

        # Get partial validation progress
        progress = validator.validate_partial(spec_path)

        # Should have some missing sections
        assert progress.missing_sections > 0

        # Check that missing sections return enhanced errors
        for section_name, status in progress.section_statuses.items():
            if status.name == "MISSING":
                error = validator._check_section_exists(spec, section_name)
                if error:
                    # Enhanced error should have all fields
                    assert error.message
                    assert error.meaning
                    assert error.example
                    assert error.suggestion

    def test_custom_rules_with_full_validation(self):
        """Test custom validation rules integration."""
        # Clear cache for clean test
        ProjectDetector.clear_cache()

        # Create spec
        spec = """# Specification: Test Web App

## Executive Summary
Web application spec.

## Functional Requirements
FR-001: User can login
"""
        spec_path = self.create_spec(spec)

        # Create project context for web-app
        context_dir = self.temp_path / ".specpulse"
        context_dir.mkdir(exist_ok=True)
        context_file = context_dir / "project_context.yaml"
        context_file.write_text("""
project:
  type: web-app
  name: test-project
""")

        # Detect project type
        project_type = ProjectDetector.detect_project_type(self.temp_path)
        assert project_type == ProjectType.WEB_APP

        # Load custom rules
        engine = RuleEngine()
        violations = engine.execute_rules(spec, project_type)

        # Violations should be a list (may be empty if rules disabled)
        assert isinstance(violations, list)

    def test_auto_fix_with_custom_rules(self):
        """Test that auto-fix works alongside custom rules."""
        validator = Validator()

        spec = """# Specification: Test

## Metadata
- ID: SPEC-001
"""
        spec_path = self.create_spec(spec)

        # Auto-fix missing sections
        success, changes, backup = validator.auto_fix_validation_issues(spec_path)

        assert success is True
        assert len(changes) > 0

        # Read fixed spec
        fixed_content = spec_path.read_text()

        # Should have more sections now
        assert len(fixed_content) > len(spec)

        # Custom rules should still work on fixed content
        engine = RuleEngine()
        violations = engine.execute_rules(fixed_content, ProjectType.WEB_APP)
        assert isinstance(violations, list)

    def test_partial_validation_with_custom_rules(self):
        """Test that partial validation and custom rules work together."""
        validator = Validator()

        spec = """# Specification: API Feature

## Executive Summary
API endpoint specification.

## Functional Requirements
FR-001: Endpoint /api/users
FR-002: Returns JSON
FR-003: Requires authentication
"""
        spec_path = self.create_spec(spec)

        # Run partial validation
        progress = validator.validate_partial(spec_path)

        # Should work without errors (even though spec is incomplete)
        assert progress.completion_pct > 0
        assert progress.completion_pct < 100

        # Custom rules can be applied separately
        engine = RuleEngine()
        violations = engine.execute_rules(spec, ProjectType.API)
        assert isinstance(violations, list)

    def test_formatting_enhanced_errors(self):
        """Test that enhanced error formatting works in workflow."""
        validator = Validator()

        # Get an enhanced error
        example = validator.get_validation_example("missing_acceptance_criteria")
        assert example is not None

        # Format with Rich
        formatted_rich = validator.format_enhanced_error(example)
        assert len(formatted_rich) > 100
        assert "What this means" in formatted_rich

        # Format plain
        formatted_plain = validator.format_enhanced_error_plain(example)
        assert len(formatted_plain) > 100
        assert "What this means:" in formatted_plain

    def test_end_to_end_incremental_spec_building(self):
        """Test complete end-to-end workflow of building a spec incrementally."""
        validator = Validator()

        # Start with minimal spec
        spec_content = """# Specification: Incremental Feature

## Metadata
- ID: SPEC-INC-001
- Created: 2025-10-06
"""
        spec_path = self.create_spec(spec_content)

        # Step 1: Check progress
        progress1 = validator.validate_partial(spec_path)
        initial_pct = progress1.completion_pct
        assert initial_pct < 20  # Very incomplete

        # Step 2: Add executive summary
        spec_content += """
## Executive Summary
This feature demonstrates the incremental spec building workflow with
progressive validation and auto-fix capabilities.
"""
        spec_path.write_text(spec_content)

        progress2 = validator.validate_partial(spec_path)
        assert progress2.completion_pct > initial_pct  # Progress increased

        # Step 3: Auto-fix remaining sections
        success, changes, backup = validator.auto_fix_validation_issues(spec_path)
        assert success is True

        # Step 4: Final validation shows major improvement
        progress3 = validator.validate_partial(spec_path)
        assert progress3.completion_pct > progress2.completion_pct
        assert progress3.completion_pct > 50  # Should be substantially improved


@pytest.mark.validation
def test_all_components_loaded():
    """Smoke test that all components load without errors."""
    # Load validation examples
    examples = Validator.load_validation_examples()
    assert len(examples) >= 15

    # Load custom rules
    engine = RuleEngine()
    assert engine.rules is not None

    # Detect project type
    project_type = ProjectDetector.detect_project_type()
    assert isinstance(project_type, ProjectType)

    # Create validator
    validator = Validator()
    assert validator is not None


@pytest.mark.validation
def test_v180_feature_checklist():
    """Verify all v1.8.0 features are implemented."""
    validator = Validator()

    # Component 3.1: Actionable Validation Messages
    assert hasattr(validator, 'format_enhanced_error')
    assert hasattr(validator, 'auto_fix_validation_issues')
    assert hasattr(Validator, 'load_validation_examples')

    # Component 3.2: Partial Validation
    assert hasattr(validator, 'validate_partial')

    # Component 3.3: Custom Rules
    assert RuleEngine is not None
    assert ProjectDetector is not None

    # All components present
    print("\n✅ All v1.8.0 components verified!")
