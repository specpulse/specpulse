"""
Tests for auto-fix functionality in Validator.
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from specpulse.core.validator import Validator, ValidationExample


@pytest.mark.validation
class TestAutoFix:
    """Test auto_fix_validation_issues method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def create_test_spec(self, content: str, filename: str = "spec-001.md") -> Path:
        """Create a test specification file."""
        spec_dir = self.temp_path / "specs" / "001-test-feature"
        spec_dir.mkdir(parents=True, exist_ok=True)

        spec_path = spec_dir / filename
        spec_path.write_text(content, encoding='utf-8')

        return spec_path

    def test_auto_fix_adds_missing_sections(self):
        """Test that auto-fix adds missing sections."""
        validator = Validator()

        # Create minimal spec missing several sections
        minimal_content = """# Specification: Test Feature

## Metadata
- ID: SPEC-001

## Executive Summary
Basic summary here.
"""
        spec_path = self.create_test_spec(minimal_content)

        # Run auto-fix
        success, changes, backup_path = validator.auto_fix_validation_issues(spec_path, backup=True)

        assert success is True
        assert len(changes) > 0
        assert backup_path is not None
        assert backup_path.exists()

        # Check that sections were added
        modified_content = spec_path.read_text()
        # Some sections should have been added
        assert len(modified_content) > len(minimal_content)

    def test_auto_fix_creates_backup(self):
        """Test that auto-fix creates a backup file."""
        validator = Validator()

        content = "# Spec\n## Metadata\nTest"
        spec_path = self.create_test_spec(content)

        success, changes, backup_path = validator.auto_fix_validation_issues(spec_path, backup=True)

        assert backup_path is not None
        assert backup_path.exists()
        # Backup should contain original content
        backup_content = backup_path.read_text()
        assert backup_content == content

    def test_auto_fix_without_backup(self):
        """Test auto-fix without creating backup."""
        validator = Validator()

        content = "# Spec\n## Metadata\nTest"
        spec_path = self.create_test_spec(content)

        success, changes, backup_path = validator.auto_fix_validation_issues(spec_path, backup=False)

        assert backup_path is None

    def test_auto_fix_dry_run(self):
        """Test dry run mode (no modifications)."""
        validator = Validator()

        original_content = "# Spec\n## Metadata\nTest"
        spec_path = self.create_test_spec(original_content)

        success, changes, backup_path = validator.auto_fix_validation_issues(spec_path, dry_run=True)

        assert success is True
        assert len(changes) > 0
        assert backup_path is None

        # Content should be unchanged
        current_content = spec_path.read_text()
        assert current_content == original_content

    def test_auto_fix_no_issues_to_fix(self):
        """Test auto-fix when spec is already valid."""
        validator = Validator()

        # Create a complete spec (using fixture)
        complete_content = """# Specification: Complete

## Metadata
- ID: SPEC-001

## Executive Summary
Complete summary.

## Problem Statement
Complete problem.

## Proposed Solution
Complete solution.

## Functional Requirements
FR-001: Requirement 1
FR-002: Requirement 2
FR-003: Requirement 3

## User Stories
### Story 1
**As a** user
**I want** something
**So that** benefit

### Story 2
**As a** developer
**I want** something
**So that** benefit

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Constraints
- Constraint 1
- Constraint 2

## Dependencies
- Dependency 1

## Risks and Mitigations
**Risk 1:** Problem
**Risk 2:** Another problem

## Success Criteria
- [ ] Success 1
- [ ] Success 2
- [ ] Success 3
"""
        spec_path = self.create_test_spec(complete_content)

        success, changes, backup_path = validator.auto_fix_validation_issues(spec_path)

        assert success is True
        assert len(changes) == 1
        assert "No auto-fixable issues found" in changes[0]

    def test_auto_fix_rollback_on_error(self):
        """Test that auto-fix rolls back on error."""
        validator = Validator()

        content = "# Spec\n## Metadata\nTest"
        spec_path = self.create_test_spec(content)

        # Make file read-only to trigger error during write
        import os
        os.chmod(spec_path, 0o444)

        try:
            success, changes, backup_path = validator.auto_fix_validation_issues(spec_path)

            # Should fail due to read-only file
            assert success is False
            # Changes should mention rollback
            rollback_mentioned = any("ROLLBACK" in change or "error" in change.lower() for change in changes)
            assert rollback_mentioned

        finally:
            # Restore permissions for cleanup
            os.chmod(spec_path, 0o644)
            # Also fix backup permissions if it exists
            if backup_path and backup_path.exists():
                os.chmod(backup_path, 0o644)

    def test_auto_fix_nonexistent_file(self):
        """Test auto-fix with nonexistent file."""
        validator = Validator()

        nonexistent_path = self.temp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            validator.auto_fix_validation_issues(nonexistent_path)

    def test_auto_fix_preserves_existing_content(self):
        """Test that auto-fix doesn't modify existing sections."""
        validator = Validator()

        content = """# Specification: Test

## Metadata
- ID: SPEC-001

## Executive Summary
This important content should be preserved.

## Problem Statement
This problem description should also be preserved.
"""
        spec_path = self.create_test_spec(content)

        success, changes, backup_path = validator.auto_fix_validation_issues(spec_path)

        modified_content = spec_path.read_text()

        # Existing content should be preserved
        assert "This important content should be preserved" in modified_content
        assert "This problem description should also be preserved" in modified_content


@pytest.mark.validation
class TestSectionTemplate:
    """Test _get_section_template method."""

    def test_get_section_template(self):
        """Test getting section template from ValidationExample."""
        validator = Validator()

        error = ValidationExample(
            message="Test",
            meaning="Test",
            example="Template content here\nMore content",
            suggestion="Test",
            help_command="test",
            auto_fix=True
        )

        template = validator._get_section_template("Test Section", error)

        assert "Template content here" in template
        assert "## Test Section" in template or template.startswith("Template")

    def test_get_section_template_adds_header(self):
        """Test that section header is added if not present."""
        validator = Validator()

        error = ValidationExample(
            message="Test",
            meaning="Test",
            example="Content without header",
            suggestion="Test",
            help_command="test"
        )

        template = validator._get_section_template("My Section", error)

        assert "## My Section" in template


@pytest.mark.validation
class TestAddSectionToSpec:
    """Test _add_section_to_spec method."""

    def test_add_section_to_empty_spec(self):
        """Test adding section to empty spec."""
        validator = Validator()

        content = "# Specification: Test\n"
        template = "## User Stories\nContent here"

        modified = validator._add_section_to_spec(content, "User Stories", template)

        assert "## User Stories" in modified
        assert "Content here" in modified

    def test_add_section_in_correct_order(self):
        """Test that sections are added in logical order."""
        validator = Validator()

        content = """# Specification: Test

## Executive Summary
Summary here.

## User Stories
Stories here.
"""
        # Add Problem Statement (should go between Executive Summary and User Stories)
        template = "## Problem Statement\nProblem here."

        modified = validator._add_section_to_spec(content, "Problem Statement", template)

        # Find positions
        exec_pos = modified.find("## Executive Summary")
        problem_pos = modified.find("## Problem Statement")
        stories_pos = modified.find("## User Stories")

        # Problem should be between Executive and User Stories
        assert exec_pos < problem_pos < stories_pos

    def test_add_multiple_sections(self):
        """Test adding multiple sections."""
        validator = Validator()

        content = "# Specification: Test\n\n## Metadata\n- ID: TEST\n"

        # Add multiple sections
        content = validator._add_section_to_spec(content, "Executive Summary", "## Executive Summary\nSummary")
        content = validator._add_section_to_spec(content, "Problem Statement", "## Problem Statement\nProblem")
        content = validator._add_section_to_spec(content, "User Stories", "## User Stories\nStories")

        assert "## Executive Summary" in content
        assert "## Problem Statement" in content
        assert "## User Stories" in content


@pytest.mark.validation
class TestGenerateDiff:
    """Test diff generation methods."""

    def test_generate_diff_from_content(self):
        """Test generating diff from content strings."""
        validator = Validator()

        original = """# Spec
## Section 1
Content 1
"""
        modified = """# Spec
## Section 1
Content 1

## Section 2
Content 2
"""

        diff = validator.generate_diff_from_content(original, modified, "test-spec")

        assert isinstance(diff, str)
        # Diff should show the addition
        assert "+## Section 2" in diff or "Section 2" in diff

    def test_generate_diff_no_changes(self):
        """Test diff when there are no changes."""
        validator = Validator()

        content = "# Spec\nSame content"

        diff = validator.generate_diff_from_content(content, content, "test")

        # Empty diff or minimal output
        assert len(diff) < 100  # Should be very short if no changes
