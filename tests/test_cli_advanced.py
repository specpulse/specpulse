"""Advanced tests for SpecPulse CLI"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import tempfile
import shutil
import os
import sys
import argparse

from specpulse.cli.main import SpecPulseCLI, main


class TestCLIAdvanced(unittest.TestCase):
    """Advanced CLI tests for edge cases and error handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.cli = SpecPulseCLI(no_color=True, verbose=True)
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_init_with_invalid_template(self):
        """Test init with invalid template"""
        # Should use default template
        result = self.cli.init("test", template="invalid")
        self.assertTrue(result)
    
    def test_update_command(self):
        """Test update command"""
        # First init a project
        self.cli.init(here=True)
        
        # Test update
        result = self.cli.update()
        self.assertTrue(result)
        
        # Check that templates are updated
        self.assertTrue(Path("templates/spec.md").exists())
    
    def test_update_without_project(self):
        """Test update without initialized project"""
        result = self.cli.update()
        self.assertFalse(result)
    
    @patch('sys.argv', ['specpulse', '--version'])
    @patch('sys.exit')
    def test_main_version(self, mock_exit):
        """Test main function with --version"""
        with self.assertRaises(SystemExit):
            main()
    
    @patch('sys.argv', ['specpulse', 'init', 'test'])
    def test_main_init(self):
        """Test main function with init command"""
        result = main()
        self.assertIsNone(result)  # main returns None on success
        self.assertTrue(Path("test/.specpulse").exists())
    
    @patch('sys.argv', ['specpulse', 'doctor'])
    def test_main_doctor(self):
        """Test main function with doctor command"""
        # First init
        self.cli.init(here=True)
        result = main()
        self.assertIsNone(result)
    
    @patch('sys.argv', ['specpulse', 'validate'])
    def test_main_validate(self):
        """Test main function with validate command"""
        # First init
        self.cli.init(here=True)
        result = main()
        self.assertIsNone(result)
    
    @patch('sys.argv', ['specpulse', 'sync'])
    def test_main_sync(self):
        """Test main function with sync command"""
        # First init
        self.cli.init(here=True)
        result = main()
        self.assertIsNone(result)
    
    @patch('sys.argv', ['specpulse', 'update'])
    def test_main_update(self):
        """Test main function with update command"""
        # First init
        self.cli.init(here=True)
        result = main()
        self.assertIsNone(result)
    
    def test_init_creates_claude_commands(self):
        """Test that init creates Claude command files"""
        self.cli.init("test", ai="claude")
        
        project_path = Path("test")
        claude_path = project_path / ".claude" / "commands"
        
        self.assertTrue((claude_path / "pulse.md").exists())
        self.assertTrue((claude_path / "spec.md").exists())
        self.assertTrue((claude_path / "plan.md").exists())
        self.assertTrue((claude_path / "task.md").exists())
    
    def test_init_creates_gemini_commands(self):
        """Test that init creates Gemini command files"""
        self.cli.init("test", ai="gemini")
        
        project_path = Path("test")
        gemini_path = project_path / ".gemini" / "commands"
        
        self.assertTrue((gemini_path / "pulse.toml").exists())
        self.assertTrue((gemini_path / "spec.toml").exists())
        self.assertTrue((gemini_path / "plan.toml").exists())
        self.assertTrue((gemini_path / "task.toml").exists())
    
    def test_init_creates_scripts(self):
        """Test that init creates shell scripts"""
        self.cli.init("test")
        
        project_path = Path("test")
        scripts_path = project_path / "scripts"
        
        self.assertTrue((scripts_path / "pulse-init.sh").exists())
        self.assertTrue((scripts_path / "pulse-spec.sh").exists())
        self.assertTrue((scripts_path / "pulse-plan.sh").exists())
        self.assertTrue((scripts_path / "pulse-task.sh").exists())
    
    def test_doctor_verbose_output(self):
        """Test doctor with verbose output"""
        cli = SpecPulseCLI(verbose=True)
        cli.init(here=True)
        
        result = cli.doctor()
        self.assertTrue(result)
    
    def test_validate_with_components(self):
        """Test validate with specific components"""
        self.cli.init(here=True)
        
        # Test each component
        result = self.cli.validate(component="spec")
        self.assertTrue(result)
        
        result = self.cli.validate(component="plan")
        self.assertTrue(result)
        
        result = self.cli.validate(component="task")
        self.assertTrue(result)
        
        result = self.cli.validate(component="constitution")
        self.assertTrue(result)
    
    def test_validate_verbose(self):
        """Test validate with verbose output"""
        cli = SpecPulseCLI(verbose=True)
        cli.init(here=True)
        
        result = cli.validate(verbose=True)
        self.assertTrue(result)
    
    def test_validate_with_auto_fix(self):
        """Test validate with auto-fix"""
        self.cli.init(here=True)
        
        result = self.cli.validate(auto_fix=True)
        self.assertTrue(result)
    
    @patch('specpulse.cli.main.GitUtils')
    def test_sync_with_git(self, mock_git):
        """Test sync with Git repository"""
        mock_git_instance = mock_git.return_value
        mock_git_instance.is_git_repo.return_value = True
        mock_git_instance.get_current_branch.return_value = "feature"
        mock_git_instance.get_status.return_value = "modified: test.txt"
        
        self.cli.init(here=True)
        result = self.cli.sync()
        
        self.assertTrue(result)
        
        # Check context was updated with Git info
        context_path = Path("memory/context.md")
        with open(context_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("Git Branch", content)
    
    def test_cli_with_no_color(self):
        """Test CLI with no-color option"""
        cli = SpecPulseCLI(no_color=True)
        cli.init(here=True)
        
        # Should work without color output
        result = cli.doctor()
        self.assertTrue(result)
    
    @patch('sys.argv', ['specpulse', 'init', '--help'])
    def test_help_command(self):
        """Test help command"""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
    
    @patch('sys.argv', ['specpulse', '--no-color', 'init', 'test'])
    def test_main_with_flags(self):
        """Test main with global flags"""
        result = main()
        self.assertIsNone(result)
        self.assertTrue(Path("test/.specpulse").exists())
    
    @patch('sys.argv', ['specpulse', '-v', 'doctor'])
    def test_main_verbose(self):
        """Test main with verbose flag"""
        self.cli.init(here=True)
        result = main()
        self.assertIsNone(result)


class TestCLIErrorHandling(unittest.TestCase):
    """Test error handling in CLI"""
    
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
    
    @patch('pathlib.Path.mkdir')
    def test_init_mkdir_error(self, mock_mkdir):
        """Test init when mkdir fails"""
        mock_mkdir.side_effect = OSError("Permission denied")
        
        result = self.cli.init("test")
        # Should handle error gracefully
        self.assertFalse(result)
    
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_init_file_write_error(self, mock_open):
        """Test init when file write fails"""
        result = self.cli.init("test")
        # Should handle error gracefully
        self.assertFalse(result)
    
    def test_doctor_without_project(self):
        """Test doctor without initialized project"""
        result = self.cli.doctor()
        self.assertFalse(result)
    
    def test_sync_without_project(self):
        """Test sync without initialized project"""
        result = self.cli.sync()
        self.assertFalse(result)
    
    @patch('pathlib.Path.exists', return_value=False)
    def test_update_missing_templates(self, mock_exists):
        """Test update when templates are missing"""
        self.cli.init(here=True)
        result = self.cli.update()
        # Should still succeed by copying templates
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()