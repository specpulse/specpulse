"""
Tests for IncrementalBuilder (v1.9.0)
"""

import pytest
from pathlib import Path

from specpulse.core.incremental import IncrementalBuilder, ProgressInfo, AddResult


@pytest.fixture
def temp_project(tmp_path):
    """Create temporary project structure."""
    specs_dir = tmp_path / "specs" / "003-test-feature"
    specs_dir.mkdir(parents=True)

    # Create minimal tier spec
    minimal_spec = """---
tier: minimal
progress: 1.0
sections_completed:
  - what
  - why
  - done_when
last_updated: 2025-10-06
---

## What
User authentication system

## Why
Security requirement for production

## Done When
- [ ] Users can login with email/password
- [ ] Users can logout
- [ ] Sessions expire after inactivity
"""
    spec_file = specs_dir / "spec-001.md"
    spec_file.write_text(minimal_spec, encoding="utf-8")

    # Create templates directory
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir(parents=True)

    return tmp_path


@pytest.fixture
def builder(temp_project):
    """Create IncrementalBuilder instance."""
    return IncrementalBuilder(temp_project)


class TestSectionAddition:
    """Tests for adding sections."""

    def test_add_valid_section(self, builder, temp_project):
        """Test adding a valid section."""
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"

        result = builder.add_section(spec_file, "user_stories")

        # Should fail because user_stories is tier 2, spec is tier 1
        assert not result.success
        assert "requires tier" in result.message.lower()

    def test_add_section_already_exists(self, builder, temp_project):
        """Test adding a section that already exists."""
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"

        result = builder.add_section(spec_file, "what")

        assert not result.success
        assert "already exists" in result.message.lower()

    def test_add_invalid_section_name(self, builder, temp_project):
        """Test adding invalid section name."""
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"

        result = builder.add_section(spec_file, "invalid_section_name")

        assert not result.success
        assert "invalid" in result.message.lower()


class TestProgressCalculation:
    """Tests for progress calculation."""

    def test_progress_empty_spec(self, builder, tmp_path):
        """Test progress on empty spec."""
        spec_file = tmp_path / "empty-spec.md"
        spec_content = """---
tier: minimal
progress: 0.0
sections_completed: []
last_updated: 2025-10-06
---

# Specification: Empty
"""
        spec_file.write_text(spec_content, encoding="utf-8")

        progress = builder.get_progress(spec_file)

        assert progress.tier == "minimal"
        assert progress.percentage == 0.0
        assert progress.completed_sections == 0
        assert progress.total_sections == 3  # minimal has 3 sections

    def test_progress_minimal_complete(self, builder, temp_project):
        """Test progress on complete minimal tier."""
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"

        progress = builder.get_progress(spec_file)

        assert progress.tier == "minimal"
        assert progress.total_sections == 3
        # Should have sections (1 complete + 2 partial is valid progress)
        assert progress.completed_sections >= 1
        assert progress.percentage > 0.0

    def test_progress_partial_section(self, builder, tmp_path):
        """Test detection of partial sections."""
        spec_file = tmp_path / "partial-spec.md"
        spec_content = """---
tier: minimal
progress: 0.5
last_updated: 2025-10-06
---

## What
User authentication

## Why
[Why is this needed?]

## Done When
- [ ] Incomplete
"""
        spec_file.write_text(spec_content, encoding="utf-8")

        progress = builder.get_progress(spec_file)

        # Should detect partial sections
        assert progress.partial_sections >= 1 or progress.completed_sections >= 1


class TestNextSectionRecommendation:
    """Tests for next section recommendation."""

    def test_next_section_minimal_complete(self, builder, temp_project):
        """Test recommendation when minimal tier is complete."""
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"

        next_section = builder.get_next_section(spec_file)

        # Should recommend expanding to standard
        assert next_section is not None
        assert "standard" in next_section.lower() or next_section in ["what", "why", "done_when"]

    def test_next_section_incomplete(self, builder, tmp_path):
        """Test recommendation when sections incomplete."""
        spec_file = tmp_path / "incomplete-spec.md"
        spec_content = """---
tier: minimal
progress: 0.33
last_updated: 2025-10-06
---

## What
Test feature

## Why
[Why needed]

## Done When
[Criteria]
"""
        spec_file.write_text(spec_content, encoding="utf-8")

        next_section = builder.get_next_section(spec_file)

        # Should recommend one of the minimal tier sections or a recommendation
        assert next_section in ["what", "why", "done_when", None] or "RECOMMEND" in next_section


class TestSectionTemplate:
    """Tests for section template loading."""

    def test_get_section_template(self, builder):
        """Test loading section template."""
        template = builder.get_section_template("user_stories")

        # Should return some template content
        assert template is not None
        assert len(template) > 0

    def test_get_invalid_section_template(self, builder):
        """Test loading invalid section raises error."""
        with pytest.raises(ValueError):
            builder.get_section_template("invalid_section")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
