"""
Unit tests for PathValidator security module.

Tests cover:
- Valid feature names
- Invalid feature names (security violations)
- Path traversal attempts
- File path validation
- Edge cases and boundary conditions
"""

import pytest
from pathlib import Path
import tempfile
import os

from specpulse.utils.path_validator import (
    PathValidator,
    SecurityError,
    validate_feature_name,
    validate_file_path,
    sanitize_filename,
)


class TestFeatureNameValidation:
    """Test suite for feature name validation"""

    def test_valid_feature_names(self):
        """Test that valid feature names pass validation"""
        valid_names = [
            "user-auth",
            "payment-gateway",
            "api-v2",
            "feature_123",
            "ABC-123-XYZ",
            "simple",
            "with-many-hyphens-between-words",
            "with_underscores_everywhere",
            "mixedCaseIsOk",
        ]

        for name in valid_names:
            result = PathValidator.validate_feature_name(name)
            assert result == name, f"Valid name '{name}' should pass unchanged"

    def test_empty_feature_name(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            PathValidator.validate_feature_name("")

    def test_feature_name_too_long(self):
        """Test that overly long names raise ValueError"""
        long_name = "a" * 256  # Over 255 char limit

        with pytest.raises(ValueError, match="too long"):
            PathValidator.validate_feature_name(long_name)

    def test_path_traversal_parent_directory(self):
        """Test that .. sequences are detected"""
        malicious_names = [
            "../etc/passwd",
            "feature/../../../secret",
            "..hidden",
            "normal..parent",
        ]

        for name in malicious_names:
            with pytest.raises(SecurityError, match="Path traversal"):
                PathValidator.validate_feature_name(name)

    def test_path_traversal_home_directory(self):
        """Test that ~ (home directory) is rejected"""
        malicious_names = [
            "~/secret",
            "feature~backup",
        ]

        for name in malicious_names:
            with pytest.raises(SecurityError, match="Path traversal"):
                PathValidator.validate_feature_name(name)

    def test_path_traversal_environment_variables(self):
        """Test that environment variable syntax is rejected"""
        malicious_names = [
            "$HOME/secret",
            "%USERPROFILE%/data",
            "feature$var",
        ]

        for name in malicious_names:
            with pytest.raises(SecurityError, match="Path traversal"):
                PathValidator.validate_feature_name(name)

    def test_path_separator_unix(self):
        """Test that Unix path separators are rejected"""
        malicious_names = [
            "/etc/passwd",
            "feature/subdir",
            "normal/feature",
        ]

        for name in malicious_names:
            with pytest.raises(SecurityError, match="separator"):
                PathValidator.validate_feature_name(name)

    def test_path_separator_windows(self):
        """Test that Windows path separators are rejected"""
        malicious_names = [
            "C:\\Windows\\System32",
            "feature\\subdir",
            "normal\\feature",
        ]

        for name in malicious_names:
            with pytest.raises(SecurityError, match="separator"):
                PathValidator.validate_feature_name(name)

    def test_absolute_path_unix(self):
        """Test that absolute Unix paths are rejected"""
        with pytest.raises(SecurityError, match="Absolute path"):
            PathValidator.validate_feature_name("/etc/passwd")

    def test_absolute_path_windows(self):
        """Test that absolute Windows paths are rejected"""
        malicious_names = [
            "C:/Windows",
            "D:\\Data",
        ]

        for name in malicious_names:
            with pytest.raises(SecurityError, match="Absolute path"):
                PathValidator.validate_feature_name(name)

    def test_invalid_characters(self):
        """Test that invalid characters are rejected"""
        invalid_names = [
            "feature with spaces",
            "feature@invalid",
            "feature#hashtag",
            "feature!exclaim",
            "feature(parens)",
            "feature[brackets]",
            "feature{braces}",
            "feature<angle>",
            "feature;semicolon",
            "feature&ampersand",
            "feature|pipe",
        ]

        for name in invalid_names:
            with pytest.raises(ValueError, match="invalid characters"):
                PathValidator.validate_feature_name(name)


class TestFilePathValidation:
    """Test suite for file path validation"""

    @pytest.fixture
    def temp_base_dir(self):
        """Create temporary base directory for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            yield base_path

    def test_valid_relative_path(self, temp_base_dir):
        """Test that valid relative paths are accepted"""
        # Create subdirectory
        subdir = temp_base_dir / "specs"
        subdir.mkdir()

        # Validate path within base
        result = PathValidator.validate_file_path(
            temp_base_dir,
            "specs/001-feature/spec.md"
        )

        # Should resolve to absolute path within base
        assert result.is_absolute()
        assert str(temp_base_dir) in str(result)

    def test_path_traversal_parent_escape(self, temp_base_dir):
        """Test that ../ path traversal is detected"""
        # Attempt to escape base directory
        with pytest.raises(SecurityError, match="Path traversal"):
            PathValidator.validate_file_path(
                temp_base_dir,
                "../../../etc/passwd"
            )

    def test_path_traversal_mixed(self, temp_base_dir):
        """Test that mixed path traversal (legit + malicious) is detected"""
        # Create subdirectory
        subdir = temp_base_dir / "specs" / "001-feature"
        subdir.mkdir(parents=True)

        # Attempt to escape via valid-looking path
        with pytest.raises(SecurityError, match="Path traversal"):
            PathValidator.validate_file_path(
                temp_base_dir,
                "specs/001-feature/../../../../etc/passwd"
            )

    def test_symlink_escape(self, temp_base_dir):
        """Test that symlinks escaping base are detected"""
        # Create a directory outside base
        with tempfile.TemporaryDirectory() as outside_dir:
            # Create symlink inside base pointing outside
            symlink_path = temp_base_dir / "escape_link"

            try:
                symlink_path.symlink_to(outside_dir)

                # Attempt to access via symlink
                with pytest.raises(SecurityError, match="Path traversal"):
                    PathValidator.validate_file_path(
                        temp_base_dir,
                        "escape_link/secret.txt"
                    )
            except OSError:
                # Symlink creation might fail on Windows without admin
                pytest.skip("Symlink test requires appropriate permissions")

    def test_absolute_path_within_base(self, temp_base_dir):
        """Test that absolute paths within base are accepted"""
        # Create file
        test_file = temp_base_dir / "test.md"
        test_file.touch()

        # Pass absolute path
        result = PathValidator.validate_file_path(
            temp_base_dir,
            str(test_file)
        )

        assert result == test_file.resolve()

    def test_base_directory_not_exists(self):
        """Test that non-existent base directory raises ValueError"""
        fake_base = Path("/nonexistent/directory")

        with pytest.raises(ValueError, match="does not exist"):
            PathValidator.validate_file_path(fake_base, "test.md")

    def test_base_directory_is_file(self, temp_base_dir):
        """Test that file as base directory raises ValueError"""
        # Create a file
        file_path = temp_base_dir / "notadir.txt"
        file_path.touch()

        with pytest.raises(ValueError, match="not a directory"):
            PathValidator.validate_file_path(file_path, "test.md")


class TestSanitizeFilename:
    """Test suite for filename sanitization"""

    def test_valid_filename_unchanged(self):
        """Test that valid filenames pass through unchanged"""
        valid_names = [
            "document.md",
            "spec-001.md",
            "my_file_123.txt",
            "README.MD",
        ]

        for name in valid_names:
            result = PathValidator.sanitize_filename(name)
            assert result == name

    def test_spaces_replaced(self):
        """Test that spaces are replaced with underscores"""
        assert PathValidator.sanitize_filename("my file.md") == "my_file.md"
        assert PathValidator.sanitize_filename("multiple   spaces.txt") == "multiple_spaces.txt"

    def test_special_chars_replaced(self):
        """Test that special characters are replaced"""
        assert PathValidator.sanitize_filename("file@name!.md") == "file_name_.md"
        assert PathValidator.sanitize_filename("my#file$.txt") == "my_file_.txt"

    def test_path_separators_removed(self):
        """Test that path separators are sanitized"""
        assert PathValidator.sanitize_filename("path/to/file.md") == "path_to_file.md"
        assert PathValidator.sanitize_filename("path\\to\\file.md") == "path_to_file.md"

    def test_empty_after_sanitization(self):
        """Test that empty result becomes 'unnamed'"""
        assert PathValidator.sanitize_filename("!!!") == "unnamed"
        assert PathValidator.sanitize_filename("@#$%") == "unnamed"

    def test_custom_replacement(self):
        """Test custom replacement character"""
        assert PathValidator.sanitize_filename("my file.md", "-") == "my-file.md"
        assert PathValidator.sanitize_filename("a@b#c.txt", "X") == "aXbXc.txt"


class TestSpecIDValidation:
    """Test suite for specification ID validation"""

    def test_valid_spec_ids(self):
        """Test that valid spec IDs pass"""
        valid_ids = ["001", "042", "999"]

        for spec_id in valid_ids:
            result = PathValidator.validate_spec_id(spec_id)
            assert result == spec_id

    def test_invalid_spec_id_too_short(self):
        """Test that short IDs are rejected"""
        with pytest.raises(ValueError, match="Invalid spec ID"):
            PathValidator.validate_spec_id("1")

        with pytest.raises(ValueError, match="Invalid spec ID"):
            PathValidator.validate_spec_id("01")

    def test_invalid_spec_id_too_long(self):
        """Test that long IDs are rejected"""
        with pytest.raises(ValueError, match="Invalid spec ID"):
            PathValidator.validate_spec_id("0001")

    def test_invalid_spec_id_non_numeric(self):
        """Test that non-numeric IDs are rejected"""
        with pytest.raises(ValueError, match="Invalid spec ID"):
            PathValidator.validate_spec_id("abc")

        with pytest.raises(ValueError, match="Invalid spec ID"):
            PathValidator.validate_spec_id("00a")


class TestIsSafePath:
    """Test suite for quick safety check"""

    def test_safe_paths(self):
        """Test that safe paths return True"""
        safe_paths = [
            "specs/001-feature",
            "plans/my-plan.md",
            "simple-name",
        ]

        for path in safe_paths:
            assert PathValidator.is_safe_path(path) is True

    def test_unsafe_paths(self):
        """Test that unsafe paths return False"""
        unsafe_paths = [
            "../../../etc/passwd",
            "/absolute/path",
            "C:\\Windows\\System32",
            "~/secret",
            "$HOME/data",
        ]

        for path in unsafe_paths:
            assert PathValidator.is_safe_path(path) is False


class TestConvenienceFunctions:
    """Test suite for convenience wrapper functions"""

    def test_validate_feature_name_wrapper(self):
        """Test convenience wrapper for feature name validation"""
        assert validate_feature_name("test-feature") == "test-feature"

        with pytest.raises(SecurityError):
            validate_feature_name("../bad")

    def test_validate_file_path_wrapper(self):
        """Test convenience wrapper for file path validation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            test_file = base / "test.md"
            test_file.touch()

            result = validate_file_path(base, "test.md")
            assert result.exists()

    def test_sanitize_filename_wrapper(self):
        """Test convenience wrapper for filename sanitization"""
        assert sanitize_filename("my file!.md") == "my_file_.md"


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions"""

    def test_exactly_255_chars(self):
        """Test feature name at exactly the length limit"""
        name_255 = "a" * 255
        result = PathValidator.validate_feature_name(name_255)
        assert result == name_255

    def test_unicode_characters(self):
        """Test that unicode characters are rejected"""
        with pytest.raises(ValueError, match="invalid characters"):
            PathValidator.validate_feature_name("café")

        with pytest.raises(ValueError, match="invalid characters"):
            PathValidator.validate_feature_name("日本語")

    def test_null_bytes(self):
        """Test that null bytes are rejected"""
        with pytest.raises(ValueError, match="invalid characters"):
            PathValidator.validate_feature_name("test\x00evil")

    def test_control_characters(self):
        """Test that control characters are rejected"""
        with pytest.raises(ValueError, match="invalid characters"):
            PathValidator.validate_feature_name("test\nline")

        with pytest.raises(ValueError, match="invalid characters"):
            PathValidator.validate_feature_name("test\rreturn")


# Performance/stress tests
class TestPerformance:
    """Performance and stress tests"""

    def test_validate_many_names(self):
        """Test that validation performs well with many names"""
        import time

        names = [f"feature-{i:03d}" for i in range(1000)]

        start = time.time()
        for name in names:
            PathValidator.validate_feature_name(name)
        duration = time.time() - start

        # Should complete in under 1 second
        assert duration < 1.0, f"Validation too slow: {duration:.2f}s"

    def test_validate_many_paths(self, temp_base_dir):
        """Test that path validation performs well"""
        import time

        # Create many paths
        paths = [f"specs/{i:03d}-feature/spec.md" for i in range(100)]

        start = time.time()
        for path in paths:
            try:
                PathValidator.validate_file_path(temp_base_dir, path)
            except SecurityError:
                pass  # Expected for non-existent paths
        duration = time.time() - start

        # Should complete in under 2 seconds
        assert duration < 2.0, f"Path validation too slow: {duration:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
