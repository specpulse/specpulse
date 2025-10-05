"""
Tests for progress_calculator module.
"""
import pytest
from specpulse.utils.progress_calculator import (
    ProgressCalculator,
    SectionStatus,
    calculate_progress,
)


@pytest.fixture
def calculator():
    """Create a ProgressCalculator instance."""
    return ProgressCalculator()


class TestSectionStatusCalculation:
    """Test section status determination."""

    def test_missing_section(self, calculator):
        """Test that empty content returns MISSING status."""
        status = calculator.calculate_section_status("Executive Summary", "")
        assert status == SectionStatus.MISSING

        status = calculator.calculate_section_status("Executive Summary", "   \n  \n  ")
        assert status == SectionStatus.MISSING

    def test_partial_executive_summary_too_short(self, calculator):
        """Test that short executive summary is PARTIAL."""
        short_content = "This is too short."
        status = calculator.calculate_section_status("Executive Summary", short_content)
        assert status == SectionStatus.PARTIAL

    def test_complete_executive_summary(self, calculator):
        """Test that adequate executive summary is COMPLETE."""
        good_content = """
        This is a comprehensive executive summary that provides sufficient detail
        about the feature. It explains what the feature does and why it's needed.
        The content meets the minimum character and line requirements.
        """
        status = calculator.calculate_section_status("Executive Summary", good_content)
        assert status == SectionStatus.COMPLETE

    def test_partial_functional_requirements_insufficient_items(self, calculator):
        """Test that functional requirements with too few items is PARTIAL."""
        content = """
        FR-001: First requirement
        FR-002: Second requirement
        """
        status = calculator.calculate_section_status("Functional Requirements", content)
        assert status == SectionStatus.PARTIAL

    def test_complete_functional_requirements(self, calculator):
        """Test that functional requirements with enough items is COMPLETE."""
        content = """
        FR-001: First requirement
        FR-002: Second requirement
        FR-003: Third requirement
        FR-004: Fourth requirement
        """
        status = calculator.calculate_section_status("Functional Requirements", content)
        assert status == SectionStatus.COMPLETE

    def test_partial_user_stories_insufficient(self, calculator):
        """Test that user stories with too few stories is PARTIAL."""
        content = """
        ### Story 1
        **As a** user
        **I want** something
        **So that** benefit
        """
        status = calculator.calculate_section_status("User Stories", content)
        assert status == SectionStatus.PARTIAL

    def test_complete_user_stories(self, calculator):
        """Test that user stories with enough stories is COMPLETE."""
        content = """
        ### Story 1
        **As a** user
        **I want** feature one
        **So that** benefit one

        ### Story 2
        **As a** developer
        **I want** feature two
        **So that** benefit two

        ### Story 3
        **As a** admin
        **I want** feature three
        **So that** benefit three
        """
        status = calculator.calculate_section_status("User Stories", content)
        assert status == SectionStatus.COMPLETE


class TestCompletionPercentage:
    """Test completion percentage calculation."""

    def test_empty_spec_zero_percent(self, calculator):
        """Test that empty spec returns 0% completion."""
        result = calculator.calculate_completion_percentage("")
        assert result.completion_percentage == 0

    def test_minimal_spec_low_percent(self, calculator):
        """Test that minimal spec returns low percentage."""
        minimal_content = """
        # Specification: Test

        ## Metadata
        - ID: SPEC-001

        ## Executive Summary
        This is a minimal executive summary.
        """
        result = calculator.calculate_completion_percentage(minimal_content)
        assert 0 < result.completion_percentage < 20  # Should be low but not zero

    def test_complete_spec_high_percent(self, calculator, valid_spec_content):
        """Test that complete spec returns high percentage."""
        result = calculator.calculate_completion_percentage(valid_spec_content)
        assert result.completion_percentage >= 80  # Should be high for complete spec

    def test_partial_spec_medium_percent(self, calculator, partial_spec_content):
        """Test that partial spec returns medium percentage."""
        result = calculator.calculate_completion_percentage(partial_spec_content)
        assert 30 <= result.completion_percentage <= 70  # Should be in middle range

    def test_completion_percentage_in_range(self, calculator, valid_spec_content):
        """Test that completion percentage is always 0-100."""
        result = calculator.calculate_completion_percentage(valid_spec_content)
        assert 0 <= result.completion_percentage <= 100


class TestSectionExtraction:
    """Test section extraction from spec content."""

    def test_extract_sections_valid_spec(self, calculator, valid_spec_content):
        """Test that sections are correctly extracted from valid spec."""
        sections = calculator._extract_sections(valid_spec_content)

        # Check that key sections are present
        assert "Executive Summary" in sections
        assert "Problem Statement" in sections
        assert "User Stories" in sections
        assert len(sections) > 5

    def test_extract_sections_empty_spec(self, calculator):
        """Test that empty spec returns empty dict."""
        sections = calculator._extract_sections("")
        assert sections == {}

    def test_extract_sections_preserves_content(self, calculator):
        """Test that section content is preserved correctly."""
        content = """
## Section One
Content for section one.
More content here.

## Section Two
Content for section two.
"""
        sections = calculator._extract_sections(content)

        assert "Section One" in sections
        assert "Content for section one" in sections["Section One"]
        assert "Section Two" in sections
        assert "Content for section two" in sections["Section Two"]


class TestItemCounting:
    """Test various item counting methods."""

    def test_count_list_items_bullets(self, calculator):
        """Test counting bulleted list items."""
        content = """
        - Item one
        - Item two
        - Item three
        """
        count = calculator._count_list_items(content)
        assert count == 3

    def test_count_list_items_numbers(self, calculator):
        """Test counting numbered list items."""
        content = """
        1. First item
        2. Second item
        3. Third item
        """
        count = calculator._count_list_items(content)
        assert count == 3

    def test_count_list_items_mixed(self, calculator):
        """Test counting mixed list items."""
        content = """
        - Bullet item
        1. Numbered item
        * Asterisk item
        """
        count = calculator._count_list_items(content)
        assert count == 3

    def test_count_user_stories(self, calculator):
        """Test counting user stories."""
        content = """
        **As a** user
        **I want** something
        **So that** benefit

        **As a** developer
        **I want** another thing
        **So that** another benefit
        """
        count = calculator._count_user_stories(content)
        assert count == 2

    def test_count_risks(self, calculator):
        """Test counting risks."""
        content = """
        **Risk 1:** First risk
        **Risk 2:** Second risk
        **Risk 3:** Third risk
        """
        count = calculator._count_risks(content)
        assert count == 3

    def test_count_subsections(self, calculator):
        """Test counting subsections."""
        content = """
        ### Subsection 1
        Content

        ### Subsection 2
        Content

        #### Sub-subsection
        Content
        """
        count = calculator._count_subsections(content)
        assert count == 3  # Counts both ### and ####


class TestNextSectionSuggestion:
    """Test next section suggestion logic."""

    def test_suggest_next_when_all_missing(self, calculator):
        """Test that first section is suggested when all are missing."""
        current_sections = {section: SectionStatus.MISSING for section in calculator.section_weights.keys()}
        suggestion = calculator.suggest_next_section(current_sections)
        assert suggestion == "Executive Summary"

    def test_suggest_next_when_some_complete(self, calculator):
        """Test suggestion when some sections are complete."""
        current_sections = {
            "Executive Summary": SectionStatus.COMPLETE,
            "Problem Statement": SectionStatus.COMPLETE,
            "Proposed Solution": SectionStatus.MISSING,
            "Functional Requirements": SectionStatus.MISSING,
        }
        suggestion = calculator.suggest_next_section(current_sections)
        assert suggestion == "Proposed Solution"

    def test_suggest_next_when_partial(self, calculator):
        """Test that partial sections are suggested for completion."""
        current_sections = {
            "Executive Summary": SectionStatus.COMPLETE,
            "Problem Statement": SectionStatus.PARTIAL,
            "Proposed Solution": SectionStatus.MISSING,
        }
        suggestion = calculator.suggest_next_section(current_sections)
        assert suggestion == "Problem Statement"

    def test_suggest_none_when_all_complete(self, calculator):
        """Test that None is returned when all sections are complete."""
        current_sections = {section: SectionStatus.COMPLETE for section in calculator.section_weights.keys()}
        suggestion = calculator.suggest_next_section(current_sections)
        assert suggestion is None


class TestProgressResult:
    """Test ProgressResult dataclass."""

    def test_progress_result_structure(self, calculator, valid_spec_content):
        """Test that ProgressResult has expected structure."""
        result = calculator.calculate_completion_percentage(valid_spec_content)

        assert hasattr(result, "completion_percentage")
        assert hasattr(result, "section_statuses")
        assert hasattr(result, "total_weight")
        assert hasattr(result, "completed_weight")

        assert isinstance(result.completion_percentage, int)
        assert isinstance(result.section_statuses, dict)
        assert isinstance(result.total_weight, float)
        assert isinstance(result.completed_weight, float)

    def test_completed_weight_less_than_total(self, calculator, partial_spec_content):
        """Test that completed weight is less than total for partial spec."""
        result = calculator.calculate_completion_percentage(partial_spec_content)
        assert result.completed_weight < result.total_weight


class TestConvenienceFunction:
    """Test the convenience function."""

    def test_calculate_progress_function(self, valid_spec_content):
        """Test that convenience function works correctly."""
        result = calculate_progress(valid_spec_content)

        assert result.completion_percentage >= 0
        assert len(result.section_statuses) > 0


@pytest.mark.validation
class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_malformed_section_headers(self, calculator):
        """Test handling of malformed section headers."""
        content = """
        # Wrong level
        ### Also wrong level
        ## Correct Level
        Content here
        """
        sections = calculator._extract_sections(content)
        assert "Correct Level" in sections
        assert "Wrong level" not in sections

    def test_section_with_no_content(self, calculator):
        """Test handling of section with no content."""
        content = """
        ## Empty Section
        ## Next Section
        Some content
        """
        sections = calculator._extract_sections(content)
        assert "Empty Section" in sections
        # Empty section should have minimal content (just newline)

    def test_very_long_content(self, calculator):
        """Test that very long content doesn't cause issues."""
        long_content = "Lorem ipsum " * 10000  # Very long content
        content = f"## Test Section\n{long_content}"

        status = calculator.calculate_section_status("Test Section", long_content)
        assert status in [SectionStatus.COMPLETE, SectionStatus.PARTIAL, SectionStatus.MISSING]
