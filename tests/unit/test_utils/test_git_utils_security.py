"""
Security tests for GitUtils module.

Tests cover:
- Command injection attempts
- Malicious branch names
- Malicious commit messages
- Malicious tag names
- Input validation
"""

import pytest
import tempfile
from pathlib import Path

from specpulse.utils.git_utils import GitUtils, GitSecurityError


class TestBranchNameSecurity:
    """Security tests for branch name validation"""

    @pytest.fixture
    def git_repo(self):
        """Create temporary git repository for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            git = GitUtils(repo_path)

            # Initialize git repo
            git.init_repo()

            # Create initial commit (required for branches)
            test_file = repo_path / "test.txt"
            test_file.write_text("test")
            git.add_files(["test.txt"])
            git.commit("Initial commit")

            yield git

    def test_valid_branch_names(self, git_repo):
        """Test that valid branch names are accepted"""
        valid_names = [
            "feature-branch",
            "bug_fix",
            "release/v1.0",
            "hotfix/security-patch",
            "ABC-123",
            "user123",
        ]

        for name in valid_names:
            # Should not raise exception
            result = git_repo.create_branch(name)
            # May fail if branch exists, but validation should pass
            # The important thing is no SecurityError

    def test_command_injection_semicolon(self, git_repo):
        """Test that semicolon command injection is blocked"""
        malicious_names = [
            "branch; rm -rf /",
            "feature; cat /etc/passwd",
            "test;whoami",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)

    def test_command_injection_ampersand(self, git_repo):
        """Test that ampersand command injection is blocked"""
        malicious_names = [
            "branch && rm -rf /",
            "feature & cat /etc/passwd",
            "test&whoami",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)

    def test_command_injection_pipe(self, git_repo):
        """Test that pipe command injection is blocked"""
        malicious_names = [
            "branch | rm -rf /",
            "feature || cat /etc/passwd",
            "test|whoami",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)

    def test_command_injection_dollar(self, git_repo):
        """Test that dollar sign command injection is blocked"""
        malicious_names = [
            "branch$(rm -rf /)",
            "feature$HOME",
            "test`whoami`",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)

    def test_command_injection_backticks(self, git_repo):
        """Test that backtick command injection is blocked"""
        malicious_names = [
            "branch`rm -rf /`",
            "feature`cat /etc/passwd`",
            "`whoami`",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)

    def test_command_injection_parentheses(self, git_repo):
        """Test that parentheses command injection is blocked"""
        malicious_names = [
            "branch(rm)",
            "feature)",
            "(malicious)",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)

    def test_command_injection_redirects(self, git_repo):
        """Test that redirect operators are blocked"""
        malicious_names = [
            "branch > /etc/passwd",
            "feature < /dev/null",
            "test >> log",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)

    def test_branch_name_too_long(self, git_repo):
        """Test that overly long branch names are rejected"""
        long_name = "a" * 256  # Over 255 char limit

        with pytest.raises(GitSecurityError, match="too long"):
            git_repo.create_branch(long_name)

    def test_empty_branch_name(self, git_repo):
        """Test that empty branch name is rejected"""
        with pytest.raises(GitSecurityError, match="cannot be empty"):
            git_repo.create_branch("")

    def test_branch_name_invalid_characters(self, git_repo):
        """Test that invalid characters are rejected"""
        invalid_names = [
            "feature branch",  # Space
            "feature@branch",  # @
            "feature#branch",  # #
            "feature!branch",  # !
            "feature~branch",  # ~ (allowed in git, but we block it)
        ]

        for name in invalid_names:
            with pytest.raises(GitSecurityError):
                git_repo.create_branch(name)

    def test_newline_in_branch_name(self, git_repo):
        """Test that newline characters are blocked"""
        malicious_names = [
            "branch\nrm -rf /",
            "feature\r\ncat /etc/passwd",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError, match="forbidden character"):
                git_repo.create_branch(name)


class TestCommitMessageSecurity:
    """Security tests for commit message validation"""

    @pytest.fixture
    def git_repo_with_changes(self):
        """Create temporary git repository with staged changes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            git = GitUtils(repo_path)

            # Initialize git repo
            git.init_repo()

            # Create and stage file
            test_file = repo_path / "test.txt"
            test_file.write_text("test")
            git.add_files(["test.txt"])

            yield git

    def test_valid_commit_messages(self, git_repo_with_changes):
        """Test that valid commit messages are accepted"""
        valid_messages = [
            "feat: add new feature",
            "fix: resolve bug #123",
            "docs: update README",
            "refactor: improve code structure",
            "test: add unit tests",
            "Multi-line commit\n\nWith detailed description",
        ]

        for message in valid_messages:
            # Create staged changes for each commit
            test_file = git_repo_with_changes.repo_path / "test.txt"
            test_file.write_text(f"test {message}")
            git_repo_with_changes.add_files(["test.txt"])

            # Should not raise exception
            result = git_repo_with_changes.commit(message)

    def test_command_injection_in_commit(self, git_repo_with_changes):
        """Test that command injection in commit messages is blocked"""
        malicious_messages = [
            "Commit message $(rm -rf /)",
            "Message with `whoami`",
        ]

        for message in malicious_messages:
            with pytest.raises(GitSecurityError, match="forbidden pattern"):
                git_repo_with_changes.commit(message)

    def test_null_bytes_in_commit(self, git_repo_with_changes):
        """Test that null bytes in commit messages are blocked"""
        with pytest.raises(GitSecurityError, match="forbidden pattern"):
            git_repo_with_changes.commit("Message\x00malicious")

    def test_commit_message_too_long(self, git_repo_with_changes):
        """Test that overly long commit messages are rejected"""
        long_message = "a" * 5001  # Over 5000 char limit

        with pytest.raises(GitSecurityError, match="too long"):
            git_repo_with_changes.commit(long_message)

    def test_empty_commit_message(self, git_repo_with_changes):
        """Test that empty commit message is rejected"""
        with pytest.raises(GitSecurityError, match="cannot be empty"):
            git_repo_with_changes.commit("")


class TestTagNameSecurity:
    """Security tests for tag name validation"""

    @pytest.fixture
    def git_repo_with_commits(self):
        """Create temporary git repository with commits"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            git = GitUtils(repo_path)

            # Initialize git repo and create commit
            git.init_repo()
            test_file = repo_path / "test.txt"
            test_file.write_text("test")
            git.add_files(["test.txt"])
            git.commit("Initial commit")

            yield git

    def test_valid_tag_names(self, git_repo_with_commits):
        """Test that valid tag names are accepted"""
        valid_tags = [
            "v1.0.0",
            "v2.1.3-beta",
            "release_2024",
            "stable-version",
        ]

        for tag in valid_tags:
            # Should not raise exception
            result = git_repo_with_commits.tag(tag)

    def test_command_injection_in_tag(self, git_repo_with_commits):
        """Test that command injection in tag names is blocked"""
        malicious_tags = [
            "v1.0; rm -rf /",
            "tag`whoami`",
            "v2$(cat /etc/passwd)",
        ]

        for tag in malicious_tags:
            with pytest.raises(GitSecurityError):
                git_repo_with_commits.tag(tag)

    def test_tag_name_too_long(self, git_repo_with_commits):
        """Test that overly long tag names are rejected"""
        long_tag = "v" * 256  # Over 255 char limit

        with pytest.raises(GitSecurityError, match="too long"):
            git_repo_with_commits.tag(long_tag)

    def test_empty_tag_name(self, git_repo_with_commits):
        """Test that empty tag name is rejected"""
        with pytest.raises(GitSecurityError, match="cannot be empty"):
            git_repo_with_commits.tag("")

    def test_tag_with_slashes(self, git_repo_with_commits):
        """Test that slashes in tag names are rejected"""
        with pytest.raises(GitSecurityError, match="invalid characters"):
            git_repo_with_commits.tag("v1/2/3")


class TestCheckoutSecurity:
    """Security tests for checkout operations"""

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

    def test_checkout_malicious_branch(self, git_repo):
        """Test that malicious checkout attempts are blocked"""
        malicious_names = [
            "branch; rm -rf /",
            "master && cat /etc/passwd",
            "feature | whoami",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError):
                git_repo.checkout_branch(name)


class TestMergeSecurity:
    """Security tests for merge operations"""

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

    def test_merge_malicious_branch(self, git_repo):
        """Test that malicious merge attempts are blocked"""
        malicious_names = [
            "branch; rm -rf /",
            "feature && cat /etc/passwd",
            "hotfix | whoami",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError):
                git_repo.merge(name)


class TestBranchExistsSecurity:
    """Security tests for branch_exists checks"""

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

    def test_branch_exists_malicious_name(self, git_repo):
        """Test that malicious branch names in checks are blocked"""
        malicious_names = [
            "branch; cat /etc/passwd",
            "feature && whoami",
        ]

        for name in malicious_names:
            with pytest.raises(GitSecurityError):
                git_repo.branch_exists(name)


# Integration tests
class TestIntegrationSecurity:
    """Integration tests for complete workflows"""

    def test_complete_secure_workflow(self):
        """Test a complete git workflow with security validation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            git = GitUtils(repo_path)

            # Initialize
            assert git.init_repo()

            # Create file and commit (secure)
            test_file = repo_path / "test.txt"
            test_file.write_text("content")
            git.add_files(["test.txt"])
            assert git.commit("feat: initial commit")

            # Create branch (secure)
            assert git.create_branch("feature-branch")

            # Create tag (secure)
            assert git.tag("v1.0.0")

            # All operations should succeed without security errors

    def test_reject_malicious_workflow(self):
        """Test that malicious workflow is completely blocked"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            git = GitUtils(repo_path)

            git.init_repo()

            # Attempt malicious branch creation
            with pytest.raises(GitSecurityError):
                git.create_branch("branch; rm -rf /")

            # Create legitimate commit
            test_file = repo_path / "test.txt"
            test_file.write_text("content")
            git.add_files(["test.txt"])
            git.commit("Initial commit")

            # Attempt malicious tag
            with pytest.raises(GitSecurityError):
                git.tag("tag$(whoami)")

            # Attempt malicious commit
            test_file.write_text("updated")
            git.add_files(["test.txt"])
            with pytest.raises(GitSecurityError):
                git.commit("Message`cat /etc/passwd`")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
