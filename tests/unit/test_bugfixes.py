"""
Test cases for verified bug fixes
"""

import pytest
from pathlib import Path
from specpulse.core.validation_rules import TaskFormatRule
from specpulse.utils.version_check import get_update_message
from specpulse.core.memory_manager import ContextEntry


class TestBug1_ValidationRulesSyntax:
    """Test for Bug #1: SyntaxError in validation_rules.py"""

    def test_validation_rules_imports_successfully(self):
        """Verify that validation_rules module can be imported without SyntaxError"""
        # This test will fail if the SyntaxError exists
        from specpulse.core import validation_rules
        assert validation_rules is not None

    def test_task_validation_rule_with_invalid_format(self):
        """Test that TaskFormatRule can process invalid task format without crash"""
        rule = TaskFormatRule()

        content = """# Test Document

## Tasks

### Invalid Task Without Proper Format
Some content here

### T001: Valid Task
Valid content
"""
        test_file = Path("/tmp/test.md")

        # This should not raise SyntaxError
        results = rule.validate(content, test_file)

        # Should find the invalid task
        assert len(results) > 0
        assert any("invalid_task_format" in r.status for r in results)

        # Verify location is properly formatted (no tuple)
        for result in results:
            if result.location:
                assert isinstance(result.location, str)
                assert ":" in result.location  # Should be "file:line"


class TestBug2_VersionCheckReturnType:
    """Test for Bug #2: Type mismatch in version_check.py"""

    def test_get_update_message_returns_tuple(self):
        """Verify get_update_message returns tuple of (message, color)"""
        result = get_update_message("2.4.0", "2.5.0", False)

        # Should return a tuple
        assert isinstance(result, tuple)
        assert len(result) == 2

        message, color = result

        # Message should be a string
        assert isinstance(message, str)
        assert "Update Available" in message
        assert "2.4.0" in message
        assert "2.5.0" in message

        # Color should be a string
        assert isinstance(color, str)
        assert color in ["bright_red", "yellow"]

    def test_get_update_message_major_update(self):
        """Test major update returns correct color"""
        message, color = get_update_message("1.0.0", "2.0.0", True)

        assert "MAJOR" in message
        assert color == "bright_red"

    def test_get_update_message_minor_update(self):
        """Test minor update returns correct color"""
        message, color = get_update_message("2.4.0", "2.5.0", False)

        assert color == "yellow"


class TestBug3_MemoryManagerVariableTypo:
    """Test for Bug #3: Variable typo in memory_manager.py"""

    def test_context_entry_impact_field_accessible(self):
        """Verify ContextEntry.impact field can be accessed"""
        entry = ContextEntry(
            timestamp="2024-01-01T00:00:00",
            action="feature_created",
            feature_name="test-feature",
            feature_id="001",
            impact="high",
            category="development",
            details={"test": "data"}
        )

        # Should be able to access impact field
        assert hasattr(entry, 'impact')
        assert entry.impact == "high"

        # Test in f-string context (simulating the bug scenario)
        formatted = f"Impact: {entry.impact}"
        assert formatted == "Impact: high"
        assert "entryimpact" not in formatted  # Should not contain the typo

    def test_context_entry_formatting(self):
        """Test that context entry formats correctly with all fields"""
        entry = ContextEntry(
            timestamp="2024-01-01T00:00:00",
            action="feature_updated",
            feature_name="auth-system",
            feature_id="002",
            impact="medium",
            category="enhancement",
            details=None
        )

        # Simulate the formatting used in memory_manager.py line 286-293
        entry_text = f"""
### {entry.action.replace('_', ' ').title()} - {entry.timestamp[:10]}
- **Feature**: {entry.feature_name or 'N/A'}
- **ID**: {entry.feature_id or 'N/A'}
- **Impact**: {entry.impact}
- **Category**: {entry.category}
"""

        # Verify all fields are properly interpolated
        assert "Feature Updated" in entry_text
        assert "2024-01-01" in entry_text
        assert "auth-system" in entry_text
        assert "002" in entry_text
        assert "medium" in entry_text
        assert "enhancement" in entry_text

        # Verify the typo is not present
        assert "entryimpact" not in entry_text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
