"""
Comprehensive test suite for SpecPulse Git utilities module.
Tests all Git functionality with proper subprocess mocking.
"""

import pytest
import unittest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import subprocess
import tempfile
import shutil
import os

from specpulse.utils.git_utils import GitUtils


class TestGitUtils(unittest.TestCase):
    """Comprehensive tests for GitUtils class"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.temp_dir)
        self.git_utils = GitUtils(self.repo_path)
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_init_with_default_path(self):
        """Test GitUtils initialization with default path"""
        with patch('specpulse.utils.git_utils.Path.cwd', return_value=self.repo_path):
            git_utils = GitUtils()
            self.assertEqual(git_utils.repo_path, self.repo_path)

    def test_init_with_custom_path(self):
        """Test GitUtils initialization with custom path"""
        git_utils = GitUtils(self.repo_path)
        self.assertEqual(git_utils.repo_path, self.repo_path)

    @patch('specpulse.utils.git_utils.subprocess.run')
    def test_run_git_command_success(self, mock_run):
        """Test successful git command execution"""
        mock_result = MagicMock()
        mock_result.stdout = "success output\n"
        mock_run.return_value = mock_result
        
        success, output = self.git_utils._run_git_command("status")
        
        self.assertTrue(success)
        self.assertEqual(output, "success output")
        mock_run.assert_called_once_with(
            ["git", "status"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )

    @patch('specpulse.utils.git_utils.subprocess.run')
    def test_run_git_command_failure(self, mock_run):
        """Test failed git command execution"""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "status"], stderr="error output"
        )
        
        success, output = self.git_utils._run_git_command("status")
        
        self.assertFalse(success)
        self.assertEqual(output, "error output")

    @patch('specpulse.utils.git_utils.subprocess.run')
    def test_run_git_command_file_not_found(self, mock_run):
        """Test git command when git is not installed"""
        mock_run.side_effect = FileNotFoundError("Git not found")
        
        success, output = self.git_utils._run_git_command("status")
        
        self.assertFalse(success)
        self.assertEqual(output, "Git is not installed or not in PATH")

    @patch('specpulse.utils.git_utils.subprocess.run')
    def test_run_git_command_multiple_args(self, mock_run):
        """Test git command with multiple arguments"""
        mock_result = MagicMock()
        mock_result.stdout = "output\n"
        mock_run.return_value = mock_result
        
        success, output = self.git_utils._run_git_command("checkout", "-b", "new-branch")
        
        self.assertTrue(success)
        mock_run.assert_called_once_with(
            ["git", "checkout", "-b", "new-branch"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )

    @patch.object(GitUtils, '_run_git_command')
    def test_check_git_installed_success(self, mock_run):
        """Test checking git installation when git is available"""
        mock_run.return_value = (True, "git version 2.30.0")
        
        result = self.git_utils.check_git_installed()
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("--version")

    @patch.object(GitUtils, '_run_git_command')
    def test_check_git_installed_failure(self, mock_run):
        """Test checking git installation when git is not available"""
        mock_run.return_value = (False, "Git not found")
        
        result = self.git_utils.check_git_installed()
        
        self.assertFalse(result)

    def test_is_git_repo_true(self):
        """Test is_git_repo when .git directory exists"""
        # Create .git directory
        git_dir = self.repo_path / ".git"
        git_dir.mkdir()
        
        result = self.git_utils.is_git_repo()
        
        self.assertTrue(result)

    def test_is_git_repo_false(self):
        """Test is_git_repo when .git directory doesn't exist"""
        result = self.git_utils.is_git_repo()
        
        self.assertFalse(result)

    def test_is_git_repo_custom_path(self):
        """Test is_git_repo with custom path"""
        custom_path = self.repo_path / "custom"
        custom_path.mkdir()
        git_dir = custom_path / ".git"
        git_dir.mkdir()
        
        result = self.git_utils.is_git_repo(custom_path)
        
        self.assertTrue(result)

    def test_is_git_repo_git_file_not_directory(self):
        """Test is_git_repo when .git is a file (not a directory)"""
        # Create .git as file instead of directory
        git_file = self.repo_path / ".git"
        git_file.touch()
        
        result = self.git_utils.is_git_repo()
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_init_repo_success(self, mock_run):
        """Test repository initialization success"""
        mock_run.return_value = (True, "Initialized empty Git repository")
        
        result = self.git_utils.init_repo()
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("init")

    @patch.object(GitUtils, '_run_git_command')
    def test_init_repo_failure(self, mock_run):
        """Test repository initialization failure"""
        mock_run.return_value = (False, "Failed to initialize")
        
        result = self.git_utils.init_repo()
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_current_branch_success(self, mock_run):
        """Test getting current branch name success"""
        mock_run.return_value = (True, "main")
        
        result = self.git_utils.get_current_branch()
        
        self.assertEqual(result, "main")
        mock_run.assert_called_once_with("branch", "--show-current")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_current_branch_failure(self, mock_run):
        """Test getting current branch name failure"""
        mock_run.return_value = (False, "Not a git repository")
        
        result = self.git_utils.get_current_branch()
        
        self.assertIsNone(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_create_branch_success(self, mock_run):
        """Test creating and checking out new branch success"""
        mock_run.return_value = (True, "Switched to a new branch 'feature-branch'")
        
        result = self.git_utils.create_branch("feature-branch")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("checkout", "-b", "feature-branch")

    @patch.object(GitUtils, '_run_git_command')
    def test_create_branch_failure(self, mock_run):
        """Test creating branch failure"""
        mock_run.return_value = (False, "Branch already exists")
        
        result = self.git_utils.create_branch("existing-branch")
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_checkout_branch_success(self, mock_run):
        """Test checking out existing branch success"""
        mock_run.return_value = (True, "Switched to branch 'existing-branch'")
        
        result = self.git_utils.checkout_branch("existing-branch")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("checkout", "existing-branch")

    @patch.object(GitUtils, '_run_git_command')
    def test_checkout_branch_failure(self, mock_run):
        """Test checking out branch failure"""
        mock_run.return_value = (False, "Branch not found")
        
        result = self.git_utils.checkout_branch("nonexistent-branch")
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_branches_success(self, mock_run):
        """Test getting list of branches success"""
        mock_run.return_value = (True, "* main\n  feature-branch\n  remotes/origin/main")
        
        result = self.git_utils.get_branches()
        
        expected = ["main", "feature-branch", "remotes/origin/main"]
        self.assertEqual(result, expected)
        mock_run.assert_called_once_with("branch", "-a")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_branches_current_branch_handling(self, mock_run):
        """Test getting branches properly handles current branch indicator"""
        mock_run.return_value = (True, "* current-branch\n  other-branch")
        
        result = self.git_utils.get_branches()
        
        expected = ["current-branch", "other-branch"]
        self.assertEqual(result, expected)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_branches_empty_lines(self, mock_run):
        """Test getting branches handles empty lines"""
        mock_run.return_value = (True, "* main\n\n  feature-branch\n")
        
        result = self.git_utils.get_branches()
        
        expected = ["main", "feature-branch"]
        self.assertEqual(result, expected)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_branches_failure(self, mock_run):
        """Test getting branches failure"""
        mock_run.return_value = (False, "Not a git repository")
        
        result = self.git_utils.get_branches()
        
        self.assertEqual(result, [])

    @patch.object(GitUtils, '_run_git_command')
    def test_add_files_specific_files(self, mock_run):
        """Test adding specific files to staging area"""
        mock_run.return_value = (True, "")
        
        files = ["file1.txt", "file2.py"]
        result = self.git_utils.add_files(files)
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("add", "file1.txt", "file2.py")

    @patch.object(GitUtils, '_run_git_command')
    def test_add_files_all_files(self, mock_run):
        """Test adding all files to staging area"""
        mock_run.return_value = (True, "")
        
        result = self.git_utils.add_files()
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("add", ".")

    @patch.object(GitUtils, '_run_git_command')
    def test_add_files_empty_list(self, mock_run):
        """Test adding files with empty list"""
        mock_run.return_value = (True, "")
        
        result = self.git_utils.add_files([])
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("add", ".")

    @patch.object(GitUtils, '_run_git_command')
    def test_add_files_failure(self, mock_run):
        """Test adding files failure"""
        mock_run.return_value = (False, "File not found")
        
        result = self.git_utils.add_files(["nonexistent.txt"])
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_commit_success(self, mock_run):
        """Test creating commit success"""
        mock_run.return_value = (True, "[main 1234567] Test commit")
        
        result = self.git_utils.commit("Test commit message")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("commit", "-m", "Test commit message")

    @patch.object(GitUtils, '_run_git_command')
    def test_commit_failure(self, mock_run):
        """Test creating commit failure"""
        mock_run.return_value = (False, "Nothing to commit")
        
        result = self.git_utils.commit("Empty commit")
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_status_success(self, mock_run):
        """Test getting git status success"""
        mock_run.return_value = (True, " M file1.txt\n?? file2.py")
        
        result = self.git_utils.get_status()
        
        self.assertEqual(result, " M file1.txt\n?? file2.py")
        mock_run.assert_called_once_with("status", "--short")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_status_failure(self, mock_run):
        """Test getting git status failure"""
        mock_run.return_value = (False, "Not a git repository")
        
        result = self.git_utils.get_status()
        
        self.assertIsNone(result)

    @patch.object(GitUtils, 'get_status')
    def test_has_changes_true(self, mock_get_status):
        """Test has_changes when there are changes"""
        mock_get_status.return_value = " M file1.txt\n?? file2.py"
        
        result = self.git_utils.has_changes()
        
        self.assertTrue(result)

    @patch.object(GitUtils, 'get_status')
    def test_has_changes_false(self, mock_get_status):
        """Test has_changes when there are no changes"""
        mock_get_status.return_value = ""
        
        result = self.git_utils.has_changes()
        
        self.assertFalse(result)

    @patch.object(GitUtils, 'get_status')
    def test_has_changes_status_none(self, mock_get_status):
        """Test has_changes when status returns None"""
        mock_get_status.return_value = None
        
        result = self.git_utils.has_changes()
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_log_success(self, mock_run):
        """Test getting commit log success"""
        log_output = "1234567 First commit\nabcdefg Second commit\n9876543 Third commit"
        mock_run.return_value = (True, log_output)
        
        result = self.git_utils.get_log(limit=5)
        
        expected = ["1234567 First commit", "abcdefg Second commit", "9876543 Third commit"]
        self.assertEqual(result, expected)
        mock_run.assert_called_once_with("log", "--oneline", "-5")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_log_default_limit(self, mock_run):
        """Test getting commit log with default limit"""
        mock_run.return_value = (True, "1234567 Commit")
        
        result = self.git_utils.get_log()
        
        mock_run.assert_called_once_with("log", "--oneline", "-10")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_log_empty_output(self, mock_run):
        """Test getting commit log with empty output"""
        mock_run.return_value = (True, "")
        
        result = self.git_utils.get_log()
        
        self.assertEqual(result, [])

    @patch.object(GitUtils, '_run_git_command')
    def test_get_log_failure(self, mock_run):
        """Test getting commit log failure"""
        mock_run.return_value = (False, "Not a git repository")
        
        result = self.git_utils.get_log()
        
        self.assertEqual(result, [])

    @patch.object(GitUtils, '_run_git_command')
    def test_stash_changes_with_message(self, mock_run):
        """Test stashing changes with message"""
        mock_run.return_value = (True, "Saved working directory")
        
        result = self.git_utils.stash_changes("Work in progress")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("stash", "push", "-m", "Work in progress")

    @patch.object(GitUtils, '_run_git_command')
    def test_stash_changes_without_message(self, mock_run):
        """Test stashing changes without message"""
        mock_run.return_value = (True, "Saved working directory")
        
        result = self.git_utils.stash_changes()
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("stash")

    @patch.object(GitUtils, '_run_git_command')
    def test_stash_changes_failure(self, mock_run):
        """Test stashing changes failure"""
        mock_run.return_value = (False, "Nothing to stash")
        
        result = self.git_utils.stash_changes("Test stash")
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_apply_stash_with_id(self, mock_run):
        """Test applying specific stash"""
        mock_run.return_value = (True, "Applied stash@{0}")
        
        result = self.git_utils.apply_stash("stash@{0}")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("stash", "apply", "stash@{0}")

    @patch.object(GitUtils, '_run_git_command')
    def test_apply_stash_latest(self, mock_run):
        """Test applying latest stash"""
        mock_run.return_value = (True, "Applied stash")
        
        result = self.git_utils.apply_stash()
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("stash", "apply")

    @patch.object(GitUtils, '_run_git_command')
    def test_apply_stash_failure(self, mock_run):
        """Test applying stash failure"""
        mock_run.return_value = (False, "No stash entries found")
        
        result = self.git_utils.apply_stash()
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_remote_url_success(self, mock_run):
        """Test getting remote URL success"""
        mock_run.return_value = (True, "https://github.com/user/repo.git")
        
        result = self.git_utils.get_remote_url("origin")
        
        self.assertEqual(result, "https://github.com/user/repo.git")
        mock_run.assert_called_once_with("remote", "get-url", "origin")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_remote_url_default_remote(self, mock_run):
        """Test getting remote URL with default remote"""
        mock_run.return_value = (True, "https://github.com/user/repo.git")
        
        result = self.git_utils.get_remote_url()
        
        mock_run.assert_called_once_with("remote", "get-url", "origin")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_remote_url_failure(self, mock_run):
        """Test getting remote URL failure"""
        mock_run.return_value = (False, "No such remote 'origin'")
        
        result = self.git_utils.get_remote_url()
        
        self.assertIsNone(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_push_default(self, mock_run):
        """Test pushing with default parameters"""
        mock_run.return_value = (True, "Everything up-to-date")
        
        result = self.git_utils.push()
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("push")

    @patch.object(GitUtils, '_run_git_command')
    def test_push_with_branch(self, mock_run):
        """Test pushing specific branch"""
        mock_run.return_value = (True, "Branch pushed")
        
        result = self.git_utils.push(branch="feature-branch")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("push", "origin", "feature-branch")

    @patch.object(GitUtils, '_run_git_command')
    def test_push_force(self, mock_run):
        """Test force pushing"""
        mock_run.return_value = (True, "Force pushed")
        
        result = self.git_utils.push(force=True)
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("push", "--force")

    @patch.object(GitUtils, '_run_git_command')
    def test_push_force_with_branch(self, mock_run):
        """Test force pushing specific branch"""
        mock_run.return_value = (True, "Force pushed")
        
        result = self.git_utils.push(branch="feature", force=True)
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("push", "--force", "origin", "feature")

    @patch.object(GitUtils, '_run_git_command')
    def test_push_failure(self, mock_run):
        """Test push failure"""
        mock_run.return_value = (False, "Push rejected")
        
        result = self.git_utils.push()
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_pull_default(self, mock_run):
        """Test pulling with default parameters"""
        mock_run.return_value = (True, "Already up to date")
        
        result = self.git_utils.pull()
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("pull")

    @patch.object(GitUtils, '_run_git_command')
    def test_pull_with_branch(self, mock_run):
        """Test pulling specific branch"""
        mock_run.return_value = (True, "Updated successfully")
        
        result = self.git_utils.pull(branch="main")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("pull", "origin", "main")

    @patch.object(GitUtils, '_run_git_command')
    def test_pull_failure(self, mock_run):
        """Test pull failure"""
        mock_run.return_value = (False, "Pull failed")
        
        result = self.git_utils.pull()
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_diff_unstaged(self, mock_run):
        """Test getting unstaged diff"""
        diff_output = "diff --git a/file.txt b/file.txt"
        mock_run.return_value = (True, diff_output)
        
        result = self.git_utils.get_diff()
        
        self.assertEqual(result, diff_output)
        mock_run.assert_called_once_with("diff")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_diff_staged(self, mock_run):
        """Test getting staged diff"""
        diff_output = "diff --git a/file.txt b/file.txt"
        mock_run.return_value = (True, diff_output)
        
        result = self.git_utils.get_diff(staged=True)
        
        self.assertEqual(result, diff_output)
        mock_run.assert_called_once_with("diff", "--staged")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_diff_failure(self, mock_run):
        """Test getting diff failure"""
        mock_run.return_value = (False, "Not a git repository")
        
        result = self.git_utils.get_diff()
        
        self.assertIsNone(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_tag_simple(self, mock_run):
        """Test creating simple tag"""
        mock_run.return_value = (True, "")
        
        result = self.git_utils.tag("v1.0.0")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("tag", "v1.0.0")

    @patch.object(GitUtils, '_run_git_command')
    def test_tag_with_message(self, mock_run):
        """Test creating annotated tag with message"""
        mock_run.return_value = (True, "")
        
        result = self.git_utils.tag("v1.0.0", message="Release version 1.0.0")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with("tag", "-a", "v1.0.0", "-m", "Release version 1.0.0")

    @patch.object(GitUtils, '_run_git_command')
    def test_tag_failure(self, mock_run):
        """Test creating tag failure"""
        mock_run.return_value = (False, "Tag already exists")
        
        result = self.git_utils.tag("existing-tag")
        
        self.assertFalse(result)

    @patch.object(GitUtils, '_run_git_command')
    def test_get_tags_success(self, mock_run):
        """Test getting list of tags success"""
        mock_run.return_value = (True, "v1.0.0\nv1.1.0\nv2.0.0")
        
        result = self.git_utils.get_tags()
        
        expected = ["v1.0.0", "v1.1.0", "v2.0.0"]
        self.assertEqual(result, expected)
        mock_run.assert_called_once_with("tag", "-l")

    @patch.object(GitUtils, '_run_git_command')
    def test_get_tags_empty(self, mock_run):
        """Test getting tags when no tags exist"""
        mock_run.return_value = (True, "")
        
        result = self.git_utils.get_tags()
        
        self.assertEqual(result, [])

    @patch.object(GitUtils, '_run_git_command')
    def test_get_tags_failure(self, mock_run):
        """Test getting tags failure"""
        mock_run.return_value = (False, "Not a git repository")
        
        result = self.git_utils.get_tags()
        
        self.assertEqual(result, [])

    def test_repo_path_property(self):
        """Test that repo_path property is accessible"""
        self.assertEqual(self.git_utils.repo_path, self.repo_path)
        
    @patch.object(GitUtils, '_run_git_command')
    def test_command_with_output_stripping(self, mock_run):
        """Test that command output is properly stripped"""
        mock_run.return_value = (True, "  output with spaces  \n\n")
        
        success, output = self.git_utils._run_git_command("status")
        
        self.assertEqual(output, "output with spaces")
        
    @patch.object(GitUtils, '_run_git_command')  
    def test_error_output_stripping(self, mock_run):
        """Test that error output is properly stripped"""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "status"], stderr="  error with spaces  \n\n"
        )
        
        success, output = self.git_utils._run_git_command("status")
        
        self.assertFalse(success)
        self.assertEqual(output, "error with spaces")


if __name__ == '__main__':
    unittest.main()