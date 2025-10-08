"""
Tests for GitUtils
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import subprocess

from specpulse.utils.git_utils import GitUtils


class TestGitUtils:
    """Test GitUtils functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.run')
    def test_check_git_installed(self, mock_run):
        """Test checking if git is installed"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.check_git_installed() is True

    @patch('subprocess.run')
    def test_check_git_not_installed(self, mock_run):
        """Test when git is not installed"""
        mock_run.side_effect = FileNotFoundError

        git = GitUtils(self.project_path)
        assert git.check_git_installed() is False

    @patch('subprocess.run')
    def test_is_repo_true(self, mock_run):
        """Test checking if directory is a git repo"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.is_repo() is True

    @patch('subprocess.run')
    def test_is_repo_false(self, mock_run):
        """Test when directory is not a git repo"""
        mock_run.return_value.returncode = 1

        git = GitUtils(self.project_path)
        assert git.is_repo() is False

    @patch('subprocess.run')
    def test_init_repo(self, mock_run):
        """Test initializing a git repo"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.init_repo() is True

    @patch('subprocess.run')
    def test_init_repo_failure(self, mock_run):
        """Test init repo failure"""
        mock_run.return_value.returncode = 1

        git = GitUtils(self.project_path)
        assert git.init_repo() is False

    @patch('subprocess.run')
    def test_add_files(self, mock_run):
        """Test adding files to git"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.add_files([".gitignore", "README.md"]) is True

    @patch('subprocess.run')
    def test_add_all_files(self, mock_run):
        """Test adding all files"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.add_files() is True

        # Check that '.' was used for all files
        mock_run.assert_called_with(
            ["git", "add", "."],
            cwd=self.project_path,
            capture_output=True,
            text=True
        )

    @patch('subprocess.run')
    def test_commit(self, mock_run):
        """Test making a commit"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.commit("Test commit") is True

    @patch('subprocess.run')
    def test_commit_failure(self, mock_run):
        """Test commit failure"""
        mock_run.return_value.returncode = 1

        git = GitUtils(self.project_path)
        assert git.commit("Test commit") is False

    @patch('subprocess.run')
    def test_push(self, mock_run):
        """Test pushing to remote"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.push() is True

    @patch('subprocess.run')
    def test_push_with_branch(self, mock_run):
        """Test pushing specific branch"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.push(branch="main") is True

    @patch('subprocess.run')
    def test_pull(self, mock_run):
        """Test pulling from remote"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.pull() is True

    @patch('subprocess.run')
    def test_get_status(self, mock_run):
        """Test getting git status"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """
        M  file1.txt
        A  file2.txt
        ?? file3.txt
        """

        git = GitUtils(self.project_path)
        status = git.get_status()

        assert isinstance(status, dict)
        assert "modified" in status
        assert "staged" in status
        assert "untracked" in status

    @patch('subprocess.run')
    def test_get_status_clean(self, mock_run):
        """Test status when repo is clean"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""

        git = GitUtils(self.project_path)
        status = git.get_status()

        assert status["modified"] == []
        assert status["staged"] == []
        assert status["untracked"] == []

    @patch('subprocess.run')
    def test_get_current_branch(self, mock_run):
        """Test getting current branch"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "main\n"

        git = GitUtils(self.project_path)
        branch = git.get_current_branch()

        assert branch == "main"

    @patch('subprocess.run')
    def test_create_branch(self, mock_run):
        """Test creating a new branch"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.create_branch("feature-branch") is True

    @patch('subprocess.run')
    def test_checkout_branch(self, mock_run):
        """Test checking out a branch"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.checkout_branch("main") is True

    @patch('subprocess.run')
    def test_get_commits(self, mock_run):
        """Test getting commit history"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """abc123|Initial commit|2024-01-01
def456|Add feature|2024-01-02"""

        git = GitUtils(self.project_path)
        commits = git.get_commits(limit=2)

        assert isinstance(commits, list)
        assert len(commits) == 2
        assert "hash" in commits[0]
        assert "message" in commits[0]
        assert "date" in commits[0]

    @patch('subprocess.run')
    def test_get_remote_url(self, mock_run):
        """Test getting remote URL"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "https://github.com/user/repo.git\n"

        git = GitUtils(self.project_path)
        url = git.get_remote_url()

        assert url == "https://github.com/user/repo.git"

    @patch('subprocess.run')
    def test_get_remote_url_no_remote(self, mock_run):
        """Test when no remote is configured"""
        mock_run.return_value.returncode = 1

        git = GitUtils(self.project_path)
        url = git.get_remote_url()

        assert url == ""

    @patch('subprocess.run')
    def test_has_changes(self, mock_run):
        """Test checking if repo has changes"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "M file1.txt"

        git = GitUtils(self.project_path)
        assert git.has_changes() is True

    @patch('subprocess.run')
    def test_has_no_changes(self, mock_run):
        """Test when repo has no changes"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""

        git = GitUtils(self.project_path)
        assert git.has_changes() is False

    @patch('subprocess.run')
    def test_stash(self, mock_run):
        """Test stashing changes"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.stash() is True

    @patch('subprocess.run')
    def test_stash_pop(self, mock_run):
        """Test popping stash"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.stash_pop() is True

    @patch('subprocess.run')
    def test_tag(self, mock_run):
        """Test creating a tag"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.tag("v1.0.0", "Version 1.0.0") is True

    @patch('subprocess.run')
    def test_merge(self, mock_run):
        """Test merging branches"""
        mock_run.return_value.returncode = 0

        git = GitUtils(self.project_path)
        assert git.merge("feature-branch") is True

    def test_initialization_without_git(self):
        """Test GitUtils initialization when git is not available"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError

            git = GitUtils(self.project_path)
            assert git.git_available is False