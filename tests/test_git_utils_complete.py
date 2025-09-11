"""
Complete tests for Git utilities - 100% coverage
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import subprocess

from specpulse.utils.git_utils import GitUtils


class TestGitUtilsComplete(unittest.TestCase):
    """Complete test coverage for GitUtils"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.git_utils = GitUtils()
    
    def test_init_with_path(self):
        """Test initialization with custom path"""
        custom_path = Path("/custom/path")
        git_utils = GitUtils(custom_path)
        self.assertEqual(git_utils.repo_path, custom_path)
    
    def test_init_without_path(self):
        """Test initialization without path uses cwd"""
        with patch('pathlib.Path.cwd') as mock_cwd:
            mock_cwd.return_value = Path("/current/dir")
            git_utils = GitUtils()
            self.assertEqual(git_utils.repo_path, Path("/current/dir"))
    
    @patch('subprocess.run')
    def test_run_git_command_success(self, mock_run):
        """Test successful git command"""
        mock_run.return_value = MagicMock(stdout="success\n", stderr="")
        success, output = self.git_utils._run_git_command("status")
        self.assertTrue(success)
        self.assertEqual(output, "success")
    
    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_run):
        """Test failed git command"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git', stderr=b"error")
        success, output = self.git_utils._run_git_command("status")
        self.assertFalse(success)
    
    @patch('subprocess.run')
    def test_run_git_command_not_found(self, mock_run):
        """Test git not found"""
        mock_run.side_effect = FileNotFoundError()
        success, output = self.git_utils._run_git_command("status")
        self.assertFalse(success)
        self.assertEqual(output, "Git is not installed or not in PATH")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_check_git_installed_true(self, mock_run):
        """Test git is installed"""
        mock_run.return_value = (True, "git version 2.34.0")
        result = self.git_utils.check_git_installed()
        self.assertTrue(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_check_git_installed_false(self, mock_run):
        """Test git is not installed"""
        mock_run.return_value = (False, "")
        result = self.git_utils.check_git_installed()
        self.assertFalse(result)
    
    def test_is_git_repo_true(self):
        """Test directory is git repo"""
        with patch('pathlib.Path.exists') as mock_exists:
            with patch('pathlib.Path.is_dir') as mock_is_dir:
                mock_exists.return_value = True
                mock_is_dir.return_value = True
                result = self.git_utils.is_git_repo()
                self.assertTrue(result)
    
    def test_is_git_repo_false(self):
        """Test directory is not git repo"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            result = self.git_utils.is_git_repo()
            self.assertFalse(result)
    
    def test_is_git_repo_with_custom_path(self):
        """Test is_git_repo with custom path"""
        custom_path = Path("/custom")
        with patch('pathlib.Path.exists') as mock_exists:
            with patch('pathlib.Path.is_dir') as mock_is_dir:
                mock_exists.return_value = True
                mock_is_dir.return_value = True
                result = self.git_utils.is_git_repo(custom_path)
                self.assertTrue(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_init_repo_success(self, mock_run):
        """Test init repo success"""
        mock_run.return_value = (True, "Initialized")
        result = self.git_utils.init_repo()
        self.assertTrue(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_init_repo_failure(self, mock_run):
        """Test init repo failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.init_repo()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_current_branch_success(self, mock_run):
        """Test get current branch"""
        mock_run.return_value = (True, "main")
        result = self.git_utils.get_current_branch()
        self.assertEqual(result, "main")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_current_branch_none(self, mock_run):
        """Test get current branch returns None"""
        mock_run.return_value = (False, "")
        result = self.git_utils.get_current_branch()
        self.assertIsNone(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_create_branch_success(self, mock_run):
        """Test create branch"""
        mock_run.return_value = (True, "")
        result = self.git_utils.create_branch("feature")
        self.assertTrue(result)
        mock_run.assert_called_with("checkout", "-b", "feature")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_create_branch_failure(self, mock_run):
        """Test create branch failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.create_branch("feature")
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_checkout_branch_success(self, mock_run):
        """Test checkout branch"""
        mock_run.return_value = (True, "")
        result = self.git_utils.checkout_branch("main")
        self.assertTrue(result)
        mock_run.assert_called_with("checkout", "main")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_checkout_branch_failure(self, mock_run):
        """Test checkout branch failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.checkout_branch("main")
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_add_files_specific(self, mock_run):
        """Test add specific files"""
        mock_run.return_value = (True, "")
        result = self.git_utils.add_files(["file1.txt", "file2.txt"])
        self.assertTrue(result)
        mock_run.assert_called_with("add", "file1.txt", "file2.txt")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_add_files_all(self, mock_run):
        """Test add all files"""
        mock_run.return_value = (True, "")
        result = self.git_utils.add_files()
        self.assertTrue(result)
        mock_run.assert_called_with("add", ".")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_add_files_failure(self, mock_run):
        """Test add files failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.add_files()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_commit_success(self, mock_run):
        """Test commit"""
        mock_run.return_value = (True, "")
        result = self.git_utils.commit("Test commit")
        self.assertTrue(result)
        mock_run.assert_called_with("commit", "-m", "Test commit")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_commit_failure(self, mock_run):
        """Test commit failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.commit("Test")
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_status_success(self, mock_run):
        """Test get status"""
        mock_run.return_value = (True, "On branch main")
        result = self.git_utils.get_status()
        self.assertEqual(result, "On branch main")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_status_none(self, mock_run):
        """Test get status returns None"""
        mock_run.return_value = (False, "")
        result = self.git_utils.get_status()
        self.assertIsNone(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_log_success(self, mock_run):
        """Test get log"""
        mock_run.return_value = (True, "commit abc123")
        result = self.git_utils.get_log(5)
        self.assertEqual(result, ["commit abc123"])
        mock_run.assert_called_with("log", "--oneline", "-5")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_log_none(self, mock_run):
        """Test get log returns empty list"""
        mock_run.return_value = (False, "")
        result = self.git_utils.get_log()
        self.assertEqual(result, [])
    
    @patch.object(GitUtils, '_run_git_command')
    def test_has_changes_true(self, mock_run):
        """Test has changes"""
        mock_run.return_value = (True, "M file.txt")
        result = self.git_utils.has_changes()
        self.assertTrue(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_has_changes_false(self, mock_run):
        """Test no changes"""
        mock_run.return_value = (True, "")
        result = self.git_utils.has_changes()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_has_changes_error(self, mock_run):
        """Test changes check error"""
        mock_run.return_value = (False, "")
        result = self.git_utils.has_changes()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_remote_url_success(self, mock_run):
        """Test get remote URL"""
        mock_run.return_value = (True, "https://github.com/user/repo.git")
        result = self.git_utils.get_remote_url()
        self.assertEqual(result, "https://github.com/user/repo.git")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_remote_url_none(self, mock_run):
        """Test get remote URL returns None"""
        mock_run.return_value = (False, "")
        result = self.git_utils.get_remote_url()
        self.assertIsNone(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_push_success(self, mock_run):
        """Test push"""
        mock_run.return_value = (True, "")
        result = self.git_utils.push("main")
        self.assertTrue(result)
        mock_run.assert_called_with("push", "origin", "main")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_push_failure(self, mock_run):
        """Test push failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.push()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_pull_success(self, mock_run):
        """Test pull"""
        mock_run.return_value = (True, "")
        result = self.git_utils.pull()
        self.assertTrue(result)
        mock_run.assert_called_with("pull")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_pull_failure(self, mock_run):
        """Test pull failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.pull()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_stash_changes_success(self, mock_run):
        """Test stash changes"""
        mock_run.return_value = (True, "")
        result = self.git_utils.stash_changes()
        self.assertTrue(result)
        mock_run.assert_called_with("stash")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_stash_changes_failure(self, mock_run):
        """Test stash changes failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.stash_changes()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_apply_stash_success(self, mock_run):
        """Test apply stash"""
        mock_run.return_value = (True, "")
        result = self.git_utils.apply_stash()
        self.assertTrue(result)
        mock_run.assert_called_with("stash", "apply")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_apply_stash_failure(self, mock_run):
        """Test apply stash failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.apply_stash()
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_stash_changes_with_message(self, mock_run):
        """Test stash changes with message"""
        mock_run.return_value = (True, "")
        result = self.git_utils.stash_changes("WIP changes")
        self.assertTrue(result)
        mock_run.assert_called_with("stash", "push", "-m", "WIP changes")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_apply_stash_with_id(self, mock_run):
        """Test apply stash with specific ID"""
        mock_run.return_value = (True, "")
        result = self.git_utils.apply_stash("stash@{0}")
        self.assertTrue(result)
        mock_run.assert_called_with("stash", "apply", "stash@{0}")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_branches(self, mock_run):
        """Test get branches"""
        mock_run.return_value = (True, "* main\n  feature\n  develop")
        result = self.git_utils.get_branches()
        self.assertEqual(result, ["main", "feature", "develop"])
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_branches_empty(self, mock_run):
        """Test get branches returns empty list"""
        mock_run.return_value = (False, "")
        result = self.git_utils.get_branches()
        self.assertEqual(result, [])
    
    @patch.object(GitUtils, '_run_git_command')
    def test_push_with_force(self, mock_run):
        """Test push with force flag"""
        mock_run.return_value = (True, "")
        result = self.git_utils.push("main", force=True)
        self.assertTrue(result)
        mock_run.assert_called_with("push", "--force", "origin", "main")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_push_without_branch(self, mock_run):
        """Test push without branch specified"""
        mock_run.return_value = (True, "")
        result = self.git_utils.push()
        self.assertTrue(result)
        mock_run.assert_called_with("push")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_pull_with_branch(self, mock_run):
        """Test pull with branch"""
        mock_run.return_value = (True, "")
        result = self.git_utils.pull("develop")
        self.assertTrue(result)
        mock_run.assert_called_with("pull", "origin", "develop")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_diff_unstaged(self, mock_run):
        """Test get diff for unstaged changes"""
        mock_run.return_value = (True, "diff content")
        result = self.git_utils.get_diff()
        self.assertEqual(result, "diff content")
        mock_run.assert_called_with("diff")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_diff_staged(self, mock_run):
        """Test get diff for staged changes"""
        mock_run.return_value = (True, "staged diff")
        result = self.git_utils.get_diff(staged=True)
        self.assertEqual(result, "staged diff")
        mock_run.assert_called_with("diff", "--staged")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_diff_none(self, mock_run):
        """Test get diff returns None on failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.get_diff()
        self.assertIsNone(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_tag_simple(self, mock_run):
        """Test create simple tag"""
        mock_run.return_value = (True, "")
        result = self.git_utils.tag("v1.0.0")
        self.assertTrue(result)
        mock_run.assert_called_with("tag", "v1.0.0")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_tag_with_message(self, mock_run):
        """Test create annotated tag with message"""
        mock_run.return_value = (True, "")
        result = self.git_utils.tag("v1.0.0", "Release version 1.0.0")
        self.assertTrue(result)
        mock_run.assert_called_with("tag", "-a", "v1.0.0", "-m", "Release version 1.0.0")
    
    @patch.object(GitUtils, '_run_git_command')
    def test_tag_failure(self, mock_run):
        """Test tag creation failure"""
        mock_run.return_value = (False, "")
        result = self.git_utils.tag("v1.0.0")
        self.assertFalse(result)
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_tags(self, mock_run):
        """Test get tags list"""
        mock_run.return_value = (True, "v1.0.0\nv1.0.1\nv2.0.0")
        result = self.git_utils.get_tags()
        self.assertEqual(result, ["v1.0.0", "v1.0.1", "v2.0.0"])
    
    @patch.object(GitUtils, '_run_git_command')
    def test_get_tags_empty(self, mock_run):
        """Test get tags returns empty list"""
        mock_run.return_value = (False, "")
        result = self.git_utils.get_tags()
        self.assertEqual(result, [])