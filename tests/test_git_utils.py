"""Tests for GitUtils module"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import subprocess
from pathlib import Path
import os

from specpulse.utils.git_utils import GitUtils


class TestGitUtils(unittest.TestCase):
    """Test GitUtils functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.git_utils = GitUtils()
    
    @patch('subprocess.run')
    def test_check_git_installed(self, mock_run):
        """Test Git installation check"""
        # Git installed
        mock_run.return_value = Mock(returncode=0)
        self.assertTrue(self.git_utils.check_git_installed())
        
        # Git not installed
        mock_run.side_effect = FileNotFoundError()
        self.assertFalse(self.git_utils.check_git_installed())
    
    @patch('subprocess.run')
    def test_is_git_repo(self, mock_run):
        """Test Git repository check"""
        # Is a Git repo
        mock_run.return_value = Mock(returncode=0)
        self.assertTrue(self.git_utils.is_git_repo())
        
        # Not a Git repo
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.is_git_repo())
        
        # Git command fails
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        self.assertFalse(self.git_utils.is_git_repo())
    
    @patch('subprocess.run')
    def test_init_repo(self, mock_run):
        """Test Git repository initialization"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.init_repo())
        mock_run.assert_called_with(
            ["git", "init"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Init fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.init_repo())
    
    @patch('subprocess.run')
    def test_add_files(self, mock_run):
        """Test adding files to Git"""
        mock_run.return_value = Mock(returncode=0)
        
        # Add single file
        self.assertTrue(self.git_utils.add_files("test.txt"))
        
        # Add multiple files
        self.assertTrue(self.git_utils.add_files(["file1.txt", "file2.txt"]))
        
        # Add fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.add_files("test.txt"))
    
    @patch('subprocess.run')
    def test_commit(self, mock_run):
        """Test Git commit"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.commit("Test commit"))
        mock_run.assert_called_with(
            ["git", "commit", "-m", "Test commit"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Commit fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.commit("Test commit"))
    
    @patch('subprocess.run')
    def test_get_current_branch(self, mock_run):
        """Test getting current branch"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="main\n"
        )
        
        self.assertEqual(self.git_utils.get_current_branch(), "main")
        
        # Command fails
        mock_run.return_value = Mock(returncode=1)
        self.assertEqual(self.git_utils.get_current_branch(), "main")
    
    @patch('subprocess.run')
    def test_create_branch(self, mock_run):
        """Test creating a new branch"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.create_branch("feature"))
        mock_run.assert_called_with(
            ["git", "checkout", "-b", "feature"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Branch creation fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.create_branch("feature"))
    
    @patch('subprocess.run')
    def test_checkout_branch(self, mock_run):
        """Test checking out a branch"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.checkout_branch("develop"))
        mock_run.assert_called_with(
            ["git", "checkout", "develop"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Checkout fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.checkout_branch("develop"))
    
    @patch('subprocess.run')
    def test_get_status(self, mock_run):
        """Test getting Git status"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="On branch main\nnothing to commit"
        )
        
        status = self.git_utils.get_status()
        self.assertIn("On branch main", status)
        
        # Status fails
        mock_run.return_value = Mock(returncode=1)
        self.assertEqual(self.git_utils.get_status(), "")
    
    @patch('subprocess.run')
    def test_get_log(self, mock_run):
        """Test getting Git log"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="commit abc123\nAuthor: Test"
        )
        
        log = self.git_utils.get_log(n=5)
        self.assertIn("commit abc123", log)
        
        # Log fails
        mock_run.return_value = Mock(returncode=1)
        self.assertEqual(self.git_utils.get_log(), "")
    
    @patch('subprocess.run')
    def test_push(self, mock_run):
        """Test Git push"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.push("origin", "main"))
        
        # Push fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.push())
    
    @patch('subprocess.run')
    def test_pull(self, mock_run):
        """Test Git pull"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.pull("origin", "main"))
        
        # Pull fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.pull())
    
    @patch('subprocess.run')
    def test_get_remote_url(self, mock_run):
        """Test getting remote URL"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="https://github.com/user/repo.git\n"
        )
        
        url = self.git_utils.get_remote_url()
        self.assertEqual(url, "https://github.com/user/repo.git")
        
        # No remote
        mock_run.return_value = Mock(returncode=1)
        self.assertEqual(self.git_utils.get_remote_url(), "")
    
    @patch('subprocess.run')
    def test_add_remote(self, mock_run):
        """Test adding remote"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.add_remote("origin", "https://github.com/user/repo.git"))
        
        # Add remote fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.add_remote("origin", "url"))
    
    @patch('subprocess.run')
    def test_tag(self, mock_run):
        """Test creating Git tag"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.tag("v1.0.0", "Release 1.0.0"))
        
        # Tag fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.tag("v1.0.0"))
    
    @patch('subprocess.run')
    def test_get_tags(self, mock_run):
        """Test getting Git tags"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="v1.0.0\nv1.0.1\nv1.0.2"
        )
        
        tags = self.git_utils.get_tags()
        self.assertEqual(tags, ["v1.0.0", "v1.0.1", "v1.0.2"])
        
        # No tags
        mock_run.return_value = Mock(returncode=1)
        self.assertEqual(self.git_utils.get_tags(), [])
    
    @patch('subprocess.run')
    def test_stash(self, mock_run):
        """Test Git stash"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.stash("WIP"))
        
        # Stash fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.stash())
    
    @patch('subprocess.run')
    def test_stash_pop(self, mock_run):
        """Test Git stash pop"""
        mock_run.return_value = Mock(returncode=0)
        
        self.assertTrue(self.git_utils.stash_pop())
        
        # Stash pop fails
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.git_utils.stash_pop())


if __name__ == '__main__':
    unittest.main()