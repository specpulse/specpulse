"""Tests for TierManager module."""

import pytest
from pathlib import Path
from specpulse.core.tier_manager import TierManager


class TestTierManager:
    @pytest.fixture
    def tier_manager(self, tmp_path):
        """Create TierManager with temp directory."""
        # Set up temp project structure
        (tmp_path / "specs").mkdir()
        (tmp_path / "templates").mkdir()

        # Copy template resources
        resources_dir = Path(__file__).parent.parent / "specpulse" / "resources" / "templates"
        import shutil

        for template_file in resources_dir.glob("spec-tier*.md"):
            shutil.copy2(template_file, tmp_path / "templates" / template_file.name)

        return TierManager(tmp_path)

    @pytest.fixture
    def minimal_spec(self, tmp_path):
        """Create sample minimal spec."""
        spec_dir = tmp_path / "specs" / "001-test"
        spec_dir.mkdir(parents=True)
        spec_path = spec_dir / "spec-001.md"
        spec_path.write_text(
            """<!-- TIER: minimal -->
# Feature: Test Feature

## What
Build a payment system

## Why
Users need to pay for premium features

## Done When
- [ ] User can enter credit card
- [ ] Payment is processed securely
- [ ] Receipt is sent via email
"""
        )
        return spec_path

    @pytest.fixture
    def standard_spec(self, tmp_path):
        """Create sample standard spec."""
        spec_dir = tmp_path / "specs" / "002-test"
        spec_dir.mkdir(parents=True)
        spec_path = spec_dir / "spec-001.md"
        spec_path.write_text(
            """<!-- TIER: standard -->
# Feature: Test Feature

## Executive Summary
This is a test feature.

## What
Build something

## Why
Users need it

## User Stories
1. As a user, I want to do something

## Functional Requirements
- FR-001: Requirement

## Technical Approach
Some approach

## Acceptance Criteria
- [ ] It works
"""
        )
        return spec_path

    @pytest.fixture
    def complete_spec(self, tmp_path):
        """Create sample complete spec."""
        spec_dir = tmp_path / "specs" / "003-test"
        spec_dir.mkdir(parents=True)
        spec_path = spec_dir / "spec-001.md"
        spec_path.write_text(
            """<!-- TIER: complete -->
# Feature: Test Feature

## Executive Summary
Test

## What
Build

## Why
Need

## User Stories
1. Story

## Functional Requirements
- FR-001: Req

## Non-Functional Requirements
- NFR-001: Performance

## Technical Approach
Approach

## Edge Cases
1. Edge case

## Security Considerations
### Authentication & Authorization
Auth

## Performance Requirements
- Latency: 100ms

## Testing Strategy
### Unit Tests
Unit

## Deployment Considerations
### Deployment Strategy
Deploy

## Acceptance Criteria
- [ ] Done
"""
        )
        return spec_path

    def test_get_current_tier_minimal(self, tier_manager, minimal_spec):
        """Test tier detection for minimal spec."""
        tier = tier_manager.get_current_tier("001-test")
        assert tier == "minimal"

    def test_get_current_tier_standard(self, tier_manager, standard_spec):
        """Test tier detection for standard spec."""
        tier = tier_manager.get_current_tier("002-test")
        assert tier == "standard"

    def test_get_current_tier_complete(self, tier_manager, complete_spec):
        """Test tier detection for complete spec."""
        tier = tier_manager.get_current_tier("003-test")
        assert tier == "complete"

    def test_get_current_tier_by_marker(self, tier_manager, minimal_spec):
        """Test tier detection via marker."""
        content = minimal_spec.read_text()
        assert "<!-- TIER: minimal -->" in content
        tier = tier_manager.get_current_tier("001-test")
        assert tier == "minimal"

    def test_get_current_tier_missing_spec(self, tier_manager):
        """Test error when spec doesn't exist."""
        with pytest.raises(FileNotFoundError):
            tier_manager.get_current_tier("999-nonexistent")

    def test_expand_tier_minimal_to_standard(self, tier_manager, minimal_spec):
        """Test expansion from minimal to standard."""
        success = tier_manager.expand_tier("001-test", "standard")
        assert success

        # Verify tier changed
        new_tier = tier_manager.get_current_tier("001-test")
        assert new_tier == "standard"

        # Verify content preserved
        content = minimal_spec.read_text()
        assert "Build a payment system" in content

    def test_expand_tier_minimal_to_complete(self, tier_manager, minimal_spec):
        """Test expansion from minimal directly to complete."""
        success = tier_manager.expand_tier("001-test", "complete")
        assert success

        # Verify tier changed
        new_tier = tier_manager.get_current_tier("001-test")
        assert new_tier == "complete"

    def test_expand_tier_standard_to_complete(self, tier_manager, standard_spec):
        """Test expansion from standard to complete."""
        success = tier_manager.expand_tier("002-test", "complete")
        assert success

        # Verify tier changed
        new_tier = tier_manager.get_current_tier("002-test")
        assert new_tier == "complete"

    def test_expand_tier_preserves_user_content(self, tier_manager, minimal_spec):
        """Test that user content is preserved during expansion."""
        # Get original content
        original_content = minimal_spec.read_text()
        assert "Build a payment system" in original_content

        # Expand
        tier_manager.expand_tier("001-test", "standard")

        # Verify preserved
        new_content = minimal_spec.read_text()
        assert "Build a payment system" in new_content

    def test_expand_tier_adds_new_sections(self, tier_manager, minimal_spec):
        """Test that new sections are added."""
        # Expand minimal to standard
        tier_manager.expand_tier("001-test", "standard")

        # Check for new sections
        content = minimal_spec.read_text()
        assert "## Executive Summary" in content
        assert "## User Stories" in content
        assert "## Functional Requirements" in content

    def test_expand_tier_invalid_transition_complete_to_minimal(self, tier_manager, complete_spec):
        """Test error on invalid tier transition (complete to minimal)."""
        with pytest.raises(ValueError, match="Invalid tier transition"):
            tier_manager.expand_tier("003-test", "minimal")

    def test_expand_tier_invalid_transition_standard_to_minimal(self, tier_manager, standard_spec):
        """Test error on invalid tier transition (standard to minimal)."""
        with pytest.raises(ValueError, match="Invalid tier transition"):
            tier_manager.expand_tier("002-test", "minimal")

    def test_expand_tier_same_tier(self, tier_manager, minimal_spec):
        """Test expansion to same tier returns False."""
        # Minimal to minimal should return False
        success = tier_manager.expand_tier("001-test", "minimal")
        assert not success

    def test_expand_tier_creates_backup(self, tier_manager, minimal_spec, tmp_path):
        """Test that backup is created during expansion."""
        # Expand
        tier_manager.expand_tier("001-test", "standard", backup=True)

        # Check for backup file
        spec_dir = tmp_path / "specs" / "001-test"
        backup_files = list(spec_dir.glob("spec-001.backup-*.md"))
        assert len(backup_files) == 1

    def test_validate_tier_minimal(self, tier_manager, minimal_spec):
        """Test validation for minimal tier."""
        result = tier_manager.validate_tier(minimal_spec)
        assert result["tier"] == "minimal"
        assert result["valid"] is True

    def test_validate_tier_standard(self, tier_manager, standard_spec):
        """Test validation for standard tier."""
        result = tier_manager.validate_tier(standard_spec)
        assert result["tier"] == "standard"
        assert result["valid"] is True

    def test_validate_tier_missing_file(self, tier_manager, tmp_path):
        """Test validation fails with missing file."""
        missing_path = tmp_path / "specs" / "999-missing" / "spec-001.md"
        result = tier_manager.validate_tier(missing_path)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_tier_missing_sections(self, tier_manager, tmp_path):
        """Test validation fails with missing sections."""
        # Create incomplete minimal spec
        spec_dir = tmp_path / "specs" / "004-incomplete"
        spec_dir.mkdir(parents=True)
        spec_path = spec_dir / "spec-001.md"
        spec_path.write_text(
            """<!-- TIER: minimal -->
# Feature: Incomplete

## What
Something
"""
        )

        result = tier_manager.validate_tier(spec_path)
        # Should have errors about missing sections
        assert len(result["errors"]) > 0
        assert any("Why" in err for err in result["errors"])

    def test_validate_tier_with_placeholders(self, tier_manager, tmp_path):
        """Test validation warns about unfilled placeholders."""
        spec_dir = tmp_path / "specs" / "005-placeholder"
        spec_dir.mkdir(parents=True)
        spec_path = spec_dir / "spec-001.md"
        spec_path.write_text(
            """<!-- TIER: minimal -->
# Feature: {{ feature_name }}

## What
{{ what_description }}

## Why
{{ why_description }}

## Done When
- [ ] {{ acceptance_1 }}
"""
        )

        result = tier_manager.validate_tier(spec_path)
        # Should warn about placeholders
        assert len(result["warnings"]) > 0
        assert any("placeholder" in warn.lower() for warn in result["warnings"])

    def test_extract_tier_marker(self, tier_manager):
        """Test tier marker extraction."""
        content_minimal = "<!-- TIER: minimal -->\n# Test"
        assert tier_manager._extract_tier_marker(content_minimal) == "minimal"

        content_standard = "<!-- TIER: standard -->\n# Test"
        assert tier_manager._extract_tier_marker(content_standard) == "standard"

        content_complete = "<!-- TIER: complete -->\n# Test"
        assert tier_manager._extract_tier_marker(content_complete) == "complete"

        content_none = "# Test with no marker"
        assert tier_manager._extract_tier_marker(content_none) is None

    def test_detect_by_sections(self, tier_manager):
        """Test tier detection by section counting."""
        # Minimal (3 sections)
        minimal_content = """
# Feature
## What
Content
## Why
Content
## Done When
Content
"""
        assert tier_manager._detect_by_sections(minimal_content) == "minimal"

        # Standard (7+ sections)
        standard_content = """
# Feature
## What
## Why
## Executive Summary
## User Stories
## Functional Requirements
## Technical Approach
## Acceptance Criteria
"""
        assert tier_manager._detect_by_sections(standard_content) == "standard"

        # Complete (15+ sections)
        complete_content = """
# Feature
""" + "\n".join(
            [f"## Section {i}" for i in range(15)]
        )
        assert tier_manager._detect_by_sections(complete_content) == "complete"

    def test_valid_transition(self, tier_manager):
        """Test tier transition validation."""
        # Valid transitions
        assert tier_manager._valid_transition("minimal", "standard") is True
        assert tier_manager._valid_transition("minimal", "complete") is True
        assert tier_manager._valid_transition("standard", "complete") is True

        # Invalid transitions
        assert tier_manager._valid_transition("standard", "minimal") is False
        assert tier_manager._valid_transition("complete", "standard") is False
        assert tier_manager._valid_transition("complete", "minimal") is False

        # Same tier
        assert tier_manager._valid_transition("minimal", "minimal") is False
        assert tier_manager._valid_transition("standard", "standard") is False

    def test_merge_templates_preserves_content(self, tier_manager):
        """Test template merging logic."""
        current = """<!-- TIER: minimal -->
# Feature: Payment

## What
Build a payment system

## Why
Users need to pay

## Done When
- [ ] Works
"""

        target = """<!-- TIER: standard -->
# Feature: {{ feature_name }}

## Executive Summary
{{ executive_summary }}

## What
{{ what_description }}

## Why
{{ why_description }}

## User Stories
1. Story

## Done When
- [ ] {{ acceptance }}
"""

        merged = tier_manager._merge_templates(current, target)

        # Should preserve user content
        assert "Build a payment system" in merged
        assert "Users need to pay" in merged

        # Should add new sections
        assert "## Executive Summary" in merged
        assert "## User Stories" in merged

    def test_extract_sections(self, tier_manager):
        """Test section extraction from markdown."""
        content = """<!-- TIER: minimal -->
# Feature: Test

## What
This is the what section
with multiple lines

## Why
This is why
we need it

## Done When
- [ ] Criteria 1
- [ ] Criteria 2
"""

        sections = tier_manager._extract_sections(content)

        assert "What" in sections
        assert "This is the what section" in sections["What"]

        assert "Why" in sections
        assert "This is why" in sections["Why"]

        assert "Done When" in sections
