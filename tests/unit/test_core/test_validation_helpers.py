"""
Test helpers and utilities for validation testing.
"""
from typing import List, Dict, Any


class ValidationAssertions:
    """Helper class for common validation assertions."""

    @staticmethod
    def assert_has_section(content: str, section_name: str, msg: str = None):
        """Assert that spec content contains a specific section."""
        section_marker = f"## {section_name}"
        assert section_marker in content, msg or f"Expected section '{section_name}' not found in spec"

    @staticmethod
    def assert_missing_section(content: str, section_name: str, msg: str = None):
        """Assert that spec content is missing a specific section."""
        section_marker = f"## {section_name}"
        assert section_marker not in content, msg or f"Section '{section_name}' should not be present"

    @staticmethod
    def assert_validation_passed(result: Dict[str, Any]):
        """Assert that validation passed with no errors."""
        assert result.get("status") == "passed", "Validation should have passed"
        assert len(result.get("errors", [])) == 0, f"Expected no errors, found: {result.get('errors')}"

    @staticmethod
    def assert_validation_failed(result: Dict[str, Any]):
        """Assert that validation failed with errors."""
        assert result.get("status") == "failed", "Validation should have failed"
        assert len(result.get("errors", [])) > 0, "Expected validation errors, found none"

    @staticmethod
    def assert_has_error(errors: List[Dict[str, Any]], error_type: str):
        """Assert that error list contains a specific error type."""
        error_types = [e.get("type") for e in errors]
        assert error_type in error_types, f"Expected error type '{error_type}' not found in {error_types}"

    @staticmethod
    def assert_error_has_fields(error: Dict[str, Any], required_fields: List[str]):
        """Assert that error object has all required fields."""
        for field in required_fields:
            assert field in error, f"Error missing required field: {field}"
            assert error[field], f"Error field '{field}' is empty"

    @staticmethod
    def assert_completion_percentage(result: Dict[str, Any], expected: int, tolerance: int = 5):
        """Assert completion percentage is within tolerance of expected value."""
        actual = result.get("completion_percentage", 0)
        diff = abs(actual - expected)
        assert diff <= tolerance, f"Completion {actual}% not within {tolerance}% of expected {expected}%"

    @staticmethod
    def assert_section_status(result: Dict[str, Any], section: str, expected_status: str):
        """Assert that a section has the expected status (complete/partial/missing)."""
        sections = result.get("section_statuses", {})
        actual_status = sections.get(section)
        assert actual_status == expected_status, \
            f"Section '{section}' has status '{actual_status}', expected '{expected_status}'"


class ValidationTestHelpers:
    """Helper functions for creating test data."""

    @staticmethod
    def create_minimal_spec() -> str:
        """Create a minimal spec with just required metadata."""
        return """# Specification: Minimal Test Spec

## Metadata
- **ID**: SPEC-MIN-001
- **Created**: 2025-10-06

## Executive Summary
Minimal spec for testing.
"""

    @staticmethod
    def create_spec_with_sections(sections: List[str]) -> str:
        """Create a spec with specified sections."""
        content = """# Specification: Custom Test Spec

## Metadata
- **ID**: SPEC-CUSTOM-001
- **Created**: 2025-10-06

"""
        for section in sections:
            content += f"\n## {section}\nContent for {section} section.\n"

        return content

    @staticmethod
    def create_validation_error(error_type: str, message: str, section: str = None) -> Dict[str, Any]:
        """Create a mock validation error object."""
        error = {
            "type": error_type,
            "message": message,
            "severity": "error"
        }
        if section:
            error["section"] = section
        return error

    @staticmethod
    def count_sections(content: str) -> int:
        """Count the number of sections (##) in spec content."""
        return content.count("\n## ")

    @staticmethod
    def extract_sections(content: str) -> List[str]:
        """Extract all section names from spec content."""
        sections = []
        for line in content.split("\n"):
            if line.startswith("## "):
                section_name = line.replace("## ", "").strip()
                sections.append(section_name)
        return sections


# Convenience instances
validation_assert = ValidationAssertions()
validation_helpers = ValidationTestHelpers()


# Example test using these helpers (for documentation)
def test_validation_helpers_example(valid_spec_content):
    """Example test demonstrating helper usage."""
    # Assert spec has required sections
    validation_assert.assert_has_section(valid_spec_content, "Executive Summary")
    validation_assert.assert_has_section(valid_spec_content, "Problem Statement")

    # Extract sections
    sections = validation_helpers.extract_sections(valid_spec_content)
    assert len(sections) > 5, "Valid spec should have multiple sections"

    # Create custom test specs
    minimal = validation_helpers.create_minimal_spec()
    assert "Minimal Test Spec" in minimal

    custom = validation_helpers.create_spec_with_sections(["Requirements", "User Stories"])
    validation_assert.assert_has_section(custom, "Requirements")
    validation_assert.assert_has_section(custom, "User Stories")
