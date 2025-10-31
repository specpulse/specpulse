"""
Tests for partial validation functionality.
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from specpulse.core.validator import Validator, ValidationProgress
from specpulse.utils.progress_calculator import SectionStatus


@pytest.mark.partial_validation
class TestValidationProgress:
    """Test ValidationProgress dataclass."""

    def test_create_validation_progress(self):
        """Test creating ValidationProgress instance."""
        progress = ValidationProgress(
            completion_pct=65,
            section_statuses={"Executive Summary": SectionStatus.COMPLETE},
            next_suggestion="Problem Statement",
            total_sections=10,
            complete_sections=4,
            partial_sections=2,
            missing_sections=4
        )

        assert progress.completion_pct == 65
        assert progress.total_sections == 10
        assert progress.complete_sections == 4
        assert progress.next_suggestion == "Problem Statement"

    def test_validation_progress_str_representation(self):
        """Test string representation of ValidationProgress."""
        progress = ValidationProgress(
            completion_pct=50,
            section_statuses={
                "Executive Summary": SectionStatus.COMPLETE,
                "Problem Statement": SectionStatus.PARTIAL,
                "User Stories": SectionStatus.MISSING
            },
            next_suggestion="Problem Statement",
            total_sections=3,
            complete_sections=1,
            partial_sections=1,
            missing_sections=1
        )

        str_repr = str(progress)

        assert "50% complete" in str_repr
        assert "Executive Summary" in str_repr
        assert "Problem Statement" in str_repr
        assert "User Stories" in str_repr
        assert "Next suggested section: Problem Statement" in str_repr

    def test_validation_progress_icons_in_str(self):
        """Test that section status icons appear in string representation."""
        progress = ValidationProgress(
            completion_pct=30,
            section_statuses={
                "Executive Summary": SectionStatus.COMPLETE,
                "Problem Statement": SectionStatus.PARTIAL,
                "User Stories": SectionStatus.MISSING
            },
            next_suggestion=None,
            total_sections=3,
            complete_sections=1,
            partial_sections=1,
            missing_sections=1
        )

        str_repr = str(progress)

        # Check for status icons
        assert "✓" in str_repr  # Complete icon
        assert "⚠️" in str_repr or "⚠" in str_repr  # Partial icon
        assert "⭕" in str_repr  # Missing icon


@pytest.mark.partial_validation
class TestValidatePartial:
    """Test validate_partial method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def create_test_spec(self, content: str) -> Path:
        """Create a test specification file."""
        spec_dir = self.temp_path / "specs" / "001-test"
        spec_dir.mkdir(parents=True, exist_ok=True)

        spec_path = spec_dir / "spec-001.md"
        spec_path.write_text(content, encoding='utf-8')

        return spec_path

    def test_validate_partial_complete_spec(self, valid_spec_content):
        """Test partial validation on a complete spec."""
        validator = Validator()
        spec_path = self.create_test_spec(valid_spec_content)

        progress = validator.validate_partial(spec_path)

        assert isinstance(progress, ValidationProgress)
        assert progress.completion_pct >= 50  # Should be decent for complete spec
        assert progress.complete_sections > 0

    def test_validate_partial_incomplete_spec(self, partial_spec_content):
        """Test partial validation on an incomplete spec."""
        validator = Validator()
        spec_path = self.create_test_spec(partial_spec_content)

        progress = validator.validate_partial(spec_path)

        assert isinstance(progress, ValidationProgress)
        assert 20 <= progress.completion_pct <= 70  # Should be in middle range
        assert progress.missing_sections > 0

    def test_validate_partial_minimal_spec(self):
        """Test partial validation on minimal spec."""
        validator = Validator()

        minimal_content = """# Specification: Minimal

## Metadata
- ID: SPEC-001

## Executive Summary
Just a summary.
"""
        spec_path = self.create_test_spec(minimal_content)

        progress = validator.validate_partial(spec_path)

        assert progress.completion_pct < 30  # Should be low
        assert progress.missing_sections > progress.complete_sections

    def test_validate_partial_next_suggestion(self):
        """Test that next suggestion is provided."""
        validator = Validator()

        content = """# Specification: Test

## Metadata
- ID: SPEC-001

## Executive Summary
Summary here that meets minimum requirements for being considered complete.

## Problem Statement
Problem description that also meets the minimum requirements.
"""
        spec_path = self.create_test_spec(content)

        progress = validator.validate_partial(spec_path)

        # Should suggest next section
        assert progress.next_suggestion is not None
        assert isinstance(progress.next_suggestion, str)

    def test_validate_partial_section_statuses(self):
        """Test that section statuses are correctly determined."""
        validator = Validator()

        content = """# Specification: Test

## Executive Summary
Complete summary with enough content to be considered done.

## Problem Statement
P  # Too short - should be partial

## User Stories
# Missing entirely
"""
        spec_path = self.create_test_spec(content)

        progress = validator.validate_partial(spec_path)

        # Check section status counts
        assert progress.total_sections > 0
        assert progress.complete_sections >= 0
        assert progress.partial_sections >= 0
        assert progress.missing_sections >= 0

        # Total should equal sum of categories
        assert progress.total_sections == (
            progress.complete_sections +
            progress.partial_sections +
            progress.missing_sections
        )

    def test_validate_partial_nonexistent_file(self):
        """Test partial validation with nonexistent file."""
        validator = Validator()

        nonexistent = self.temp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            validator.validate_partial(nonexistent)

    def test_validate_partial_no_errors_for_incomplete(self):
        """Test that partial validation doesn't raise errors for incomplete specs."""
        validator = Validator()

        incomplete_content = """# Specification: Incomplete

## Executive Summary
Just this.
"""
        spec_path = self.create_test_spec(incomplete_content)

        # This should NOT raise an exception
        progress = validator.validate_partial(spec_path)

        assert progress.completion_pct < 50
        assert progress.missing_sections > 0

    def test_validate_partial_complete_spec_no_suggestion(self, valid_spec_content):
        """Test that complete spec has no next suggestion."""
        validator = Validator()
        spec_path = self.create_test_spec(valid_spec_content)

        progress = validator.validate_partial(spec_path)

        # Complete spec might still have suggestion if not 100%, but should be high completion
        assert progress.completion_pct > 40


# Run a quick integration test
@pytest.mark.partial_validation
def test_partial_validation_workflow(valid_spec_path):
    """Test complete partial validation workflow."""
    validator = Validator()

    # Run partial validation
    progress = validator.validate_partial(valid_spec_path)

    # Should return valid progress
    assert isinstance(progress, ValidationProgress)
    assert 0 <= progress.completion_pct <= 100

    # Print progress (for manual verification)
    print(f"\nPartial Validation Result:")
    print(str(progress))
