"""Tests for SpecPulse CLI"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil
import os

from specpulse.cli.main import SpecPulseCLI
from specpulse.utils.console import Console


class TestSpecPulseCLI(unittest.TestCase):
    """Test SpecPulse CLI functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.cli = SpecPulseCLI()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_init_creates_project_structure(self):
        """Test that init creates proper project structure"""
        result = self.cli.init("test-project", here=False, ai="claude", template="web")
        
        self.assertTrue(result)
        project_path = Path(self.temp_dir) / "test-project"
        
        # Check directories
        self.assertTrue((project_path / ".specpulse").exists())
        self.assertTrue((project_path / "memory").exists())
        self.assertTrue((project_path / "specs").exists())
        self.assertTrue((project_path / "plans").exists())
        self.assertTrue((project_path / "tasks").exists())
        self.assertTrue((project_path / "templates").exists())
        self.assertTrue((project_path / "scripts").exists())
        
        # Check files
        self.assertTrue((project_path / ".specpulse" / "config.yaml").exists())
        self.assertTrue((project_path / "PULSE.md").exists())
        # CLAUDE.md and GEMINI.md are no longer created by init
        
        # Check memory files
        self.assertTrue((project_path / "memory" / "constitution.md").exists())
        self.assertTrue((project_path / "memory" / "context.md").exists())
        self.assertTrue((project_path / "memory" / "decisions.md").exists())
        
        # Check templates
        self.assertTrue((project_path / "templates" / "spec.md").exists())
        self.assertTrue((project_path / "templates" / "plan.md").exists())
        self.assertTrue((project_path / "templates" / "task.md").exists())
    
    def test_init_here_uses_current_directory(self):
        """Test that init --here uses current directory"""
        result = self.cli.init(here=True, ai="gemini", template="api")
        
        self.assertTrue(result)
        
        # Check that files are created in current directory
        self.assertTrue(Path(".specpulse").exists())
        self.assertTrue(Path("memory").exists())
        self.assertTrue(Path("PULSE.md").exists())
        # CLAUDE.md and GEMINI.md are no longer created by init
    
    def test_init_adds_to_existing_directory(self):
        """Test that init adds SpecPulse to existing directory"""
        # Create directory first
        os.mkdir("existing-project")
        
        result = self.cli.init("existing-project")
        
        # Now init should succeed as it adds SpecPulse to existing projects
        self.assertTrue(result)
        self.assertTrue(Path("existing-project/.specpulse").exists())
    
    @patch('specpulse.cli.main.GitUtils')
    def test_doctor_checks_system(self, mock_git):
        """Test that doctor performs system checks"""
        mock_git_instance = mock_git.return_value
        mock_git_instance.check_git_installed.return_value = True
        mock_git_instance.is_git_repo.return_value = False
        
        # Create a SpecPulse project first
        self.cli.init(here=True)
        
        result = self.cli.doctor()
        
        # Should pass basic checks
        self.assertTrue(result)
        mock_git_instance.check_git_installed.assert_called_once()
    
    def test_validate_requires_specpulse_project(self):
        """Test that validate checks for SpecPulse project"""
        result = self.cli.validate()
        
        # Should fail without project
        self.assertFalse(result)
    
    def test_validate_works_with_project(self):
        """Test that validate works with initialized project"""
        # Initialize project first
        self.cli.init(here=True)
        
        result = self.cli.validate()
        
        # Should succeed with project
        self.assertTrue(result)
    
    @patch('specpulse.cli.main.GitUtils')
    def test_sync_updates_context(self, mock_git):
        """Test that sync updates context file"""
        mock_git_instance = mock_git.return_value
        mock_git_instance.is_git_repo.return_value = True
        mock_git_instance.get_current_branch.return_value = "main"
        
        # Initialize project
        self.cli.init(here=True)
        
        result = self.cli.sync()
        
        self.assertTrue(result)
        
        # Check that context was updated
        context_path = Path("memory") / "context.md"
        with open(context_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("Last Sync", content)


class TestConsole(unittest.TestCase):
    """Test Console utility"""
    
    def setUp(self):
        """Set up test console"""
        self.console = Console(no_color=True)
    
    def test_console_methods_dont_crash(self):
        """Test that console methods handle output correctly"""
        # These should not raise exceptions
        self.console.info("Test info")
        self.console.success("Test success")
        self.console.warning("Test warning")
        self.console.error("Test error")
        # progress method removed, using other visual methods
        self.console.header("Test header")
        # list_item and code_block methods changed
        self.console.section("Test section")
        self.console.code_block("print('test')", "python")
    
    def test_console_prompt(self):
        """Test console prompt with default"""
        with patch('builtins.input', return_value=''):
            result = self.console.prompt("Enter value", "default")
            self.assertEqual(result, "default")
        
        with patch('builtins.input', return_value='custom'):
            result = self.console.prompt("Enter value")
            self.assertEqual(result, "custom")
    
    def test_console_confirm(self):
        """Test console confirmation"""
        with patch('builtins.input', return_value='y'):
            result = self.console.confirm("Continue?")
            self.assertTrue(result)
        
        with patch('builtins.input', return_value='n'):
            result = self.console.confirm("Continue?")
            self.assertFalse(result)
        
        with patch('builtins.input', return_value=''):
            result = self.console.confirm("Continue?", default=True)
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()