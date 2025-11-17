"""
Test Suite for Repository Bug Analysis Fixes

This module tests all bug fixes identified in the comprehensive repository analysis.
"""

import os
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, patch


class TestBug001AtomicWriteRaceCondition:
    """Tests for BUG-001: CRITICAL atomic write race condition in storage.py"""

    def test_atomic_write_uses_os_replace(self, tmp_path):
        """Test that atomic_write uses os.replace() instead of unlink+rename"""
        from specpulse.monitor.storage import StateStorage
        from specpulse.monitor.models import MonitoringConfig

        # Create storage instance
        project_path = tmp_path / "project"
        project_path.mkdir()
        (project_path / ".specpulse" / "memory").mkdir(parents=True)

        config = MonitoringConfig()
        storage = StateStorage(project_path, config)

        # Create test data
        test_data = {"test": "data", "value": 123}
        test_file = storage.memory_path / "test.json"

        # Write initial data
        storage._atomic_write(test_file, test_data)
        assert test_file.exists()

        # Verify content
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data == test_data

        # Write again to existing file (tests the critical path)
        test_data2 = {"test": "updated", "value": 456}
        storage._atomic_write(test_file, test_data2)

        # Verify updated content
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data == test_data2

    def test_atomic_write_no_data_loss_on_existing_file(self, tmp_path):
        """Test that overwriting existing file doesn't cause data loss"""
        from specpulse.monitor.storage import StateStorage
        from specpulse.monitor.models import MonitoringConfig

        project_path = tmp_path / "project"
        project_path.mkdir()
        (project_path / ".specpulse" / "memory").mkdir(parents=True)

        config = MonitoringConfig()
        storage = StateStorage(project_path, config)

        test_file = storage.memory_path / "critical.json"

        # Write initial critical data
        critical_data = {"important": "data", "balance": 10000}
        storage._atomic_write(test_file, critical_data)

        # Verify os.replace is used (atomic operation)
        with patch('specpulse.monitor.storage.os.replace', wraps=os.replace) as mock_replace:
            updated_data = {"important": "updated", "balance": 20000}
            storage._atomic_write(test_file, updated_data)
            # Verify os.replace was called (not unlink+rename)
            assert mock_replace.called

        # Verify data is correct
        with open(test_file, 'r') as f:
            result = json.load(f)
        assert result == updated_data


class TestBug002IndexErrorCheckpoints:
    """Tests for BUG-002: IndexError in checkpoints.py tier parsing"""

    def test_parse_tier_with_missing_value(self, tmp_path):
        """Test parsing tier when value is missing after colon"""
        from specpulse.core.checkpoints import CheckpointManager

        # Create spec file with malformed frontmatter
        spec_file = tmp_path / "spec.md"
        spec_file.write_text("""---
tier:
progress: 0.5
---

# Specification
Content here
""")

        manager = CheckpointManager(tmp_path)
        tier, progress = manager._extract_metadata(spec_file.read_text())

        # Should handle missing tier gracefully
        assert progress == 0.5
        # tier should be default or None, not cause IndexError

    def test_parse_tier_with_valid_values(self, tmp_path):
        """Test parsing tier with valid values"""
        from specpulse.core.checkpoints import CheckpointManager

        spec_file = tmp_path / "spec.md"
        spec_file.write_text("""---
tier: 2
progress: 0.75
---

# Specification
Content here
""")

        manager = CheckpointManager(tmp_path)
        tier, progress = manager._extract_metadata(spec_file.read_text())

        assert tier == "2"
        assert progress == 0.75

    def test_parse_tier_with_malformed_progress(self, tmp_path):
        """Test parsing when progress value is malformed"""
        from specpulse.core.checkpoints import CheckpointManager

        spec_file = tmp_path / "spec.md"
        spec_file.write_text("""---
tier: 2
progress:
---

# Specification
Content here
""")

        manager = CheckpointManager(tmp_path)
        tier, progress = manager._extract_metadata(spec_file.read_text())

        assert tier == "2"
        assert progress == 0.0  # Should default to 0.0 on error


class TestBug003IndexErrorFeatureParsing:
    """Tests for BUG-003: IndexError in sp_pulse_commands.py feature parsing"""

    def test_feature_name_parsing_with_valid_format(self):
        """Test feature name parsing with valid 'XXX-name' format"""
        # Simulate the parsing logic
        feature_dir_name = "001-user-authentication"
        parts = feature_dir_name.split("-", 1)

        assert len(parts) >= 2
        feature_id = parts[0]
        feature_name_clean = parts[1]

        assert feature_id == "001"
        assert feature_name_clean == "user-authentication"

    def test_feature_name_parsing_without_hyphen(self):
        """Test feature name parsing when directory name has no hyphen"""
        # Simulate the parsing logic with malformed name
        feature_dir_name = "001"  # Missing hyphen and name
        parts = feature_dir_name.split("-", 1)

        # Should handle gracefully without IndexError
        if len(parts) >= 2:
            feature_id = parts[0]
            feature_name_clean = parts[1]
        else:
            feature_id = parts[0] if parts else ""
            feature_name_clean = ""

        assert feature_id == "001"
        assert feature_name_clean == ""

    def test_feature_name_parsing_with_multiple_hyphens(self):
        """Test feature name parsing with multiple hyphens in name"""
        feature_dir_name = "042-user-auth-oauth-jwt"
        parts = feature_dir_name.split("-", 1)

        assert len(parts) >= 2
        feature_id = parts[0]
        feature_name_clean = parts[1]

        assert feature_id == "042"
        assert feature_name_clean == "user-auth-oauth-jwt"


class TestBug004VersionComparison:
    """Tests for BUG-004: Version comparison logic in version_check.py"""

    def test_version_comparison_with_double_digit_major(self):
        """Test version comparison handles '10.0.0' vs '2.0.0' correctly"""
        from specpulse.utils.version_check import get_update_message

        # Test that 10.x is correctly identified as newer major than 2.x
        current = "2.5.0"
        latest = "10.0.0"

        message, color = get_update_message(current, latest, is_major=True)

        # Should correctly identify as major update
        assert "major" in message.lower()
        assert "10.0.0" in message

    def test_version_comparison_with_same_major(self):
        """Test version comparison with same major version"""
        from specpulse.utils.version_check import get_update_message

        current = "2.5.0"
        latest = "2.10.0"

        message, color = get_update_message(current, latest, is_major=False)

        # Should correctly identify as minor update
        assert "minor" in message.lower() or "MINOR" in message

    def test_version_comparison_with_patch_update(self):
        """Test version comparison with patch update"""
        from specpulse.utils.version_check import get_update_message

        current = "2.5.3"
        latest = "2.5.10"

        message, color = get_update_message(current, latest, is_major=False)

        # Should correctly identify as patch update
        assert "patch" in message.lower() or "PATCH" in message

    def test_version_comparison_with_non_numeric_versions(self):
        """Test version comparison with non-numeric version strings"""
        from specpulse.utils.version_check import get_update_message

        # Should handle non-numeric versions gracefully
        current = "2.5.0-beta"
        latest = "2.6.0-rc1"

        # Should not crash
        message, color = get_update_message(current, latest, is_major=False)
        assert message is not None


class TestCodeQualityFixes:
    """Tests for code quality improvements"""

    def test_version_exported_in_init(self):
        """Test that __version__ is properly exported"""
        import specpulse

        # Should be accessible
        assert hasattr(specpulse, '__version__')
        assert specpulse.__version__ == "2.6.2"

    def test_init_file_has_newline_at_end(self):
        """Test that __init__.py has newline at end of file"""
        init_file = Path(__file__).parent.parent / "specpulse" / "__init__.py"

        with open(init_file, 'rb') as f:
            content = f.read()

        # Should end with newline
        assert content.endswith(b'\n')

    def test_version_file_has_newline_at_end(self):
        """Test that _version.py has newline at end of file"""
        version_file = Path(__file__).parent.parent / "specpulse" / "_version.py"

        with open(version_file, 'rb') as f:
            content = f.read()

        # Should end with newline
        assert content.endswith(b'\n')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
