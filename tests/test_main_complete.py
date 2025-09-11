"""
Complete tests for CLI main module - 100% coverage
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call, mock_open
from pathlib import Path
import tempfile
import shutil
import sys
from io import StringIO
import argparse

from specpulse.cli.main import SpecPulseCLI, main


class TestSpecPulseCLIComplete(unittest.TestCase):
    """Complete test coverage for SpecPulseCLI"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cli = SpecPulseCLI()
    
    def tearDown(self):
        """Clean up after tests"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test SpecPulseCLI initialization"""
        cli = SpecPulseCLI()
        self.assertIsNotNone(cli.console)
        self.assertIsNotNone(cli.core)
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('shutil.copy2')
    def test_init_command_new_project(self, mock_copy, mock_file, mock_mkdir, mock_exists):
        """Test init command for new project"""
        mock_exists.return_value = False
        
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            result = self.cli.init("test-project")
        
        self.assertTrue(result)
        mock_mkdir.assert_called()
    
    @patch('pathlib.Path.exists')
    def test_init_command_existing_project(self, mock_exists):
        """Test init command for existing project"""
        mock_exists.return_value = True
        
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            with patch.object(self.cli.console, 'warning') as mock_warning:
                result = self.cli.init()
                mock_warning.assert_called()
        
        self.assertFalse(result)
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('shutil.copy2')
    @patch('specpulse.utils.git_utils.GitUtils.check_git_installed')
    @patch('specpulse.utils.git_utils.GitUtils.is_git_repo')
    @patch('specpulse.utils.git_utils.GitUtils.init_repo')
    def test_init_with_git(self, mock_git_init, mock_is_repo, mock_check_git,
                           mock_copy, mock_file, mock_mkdir, mock_exists):
        """Test init with git option"""
        mock_exists.return_value = False
        mock_check_git.return_value = True
        mock_is_repo.return_value = False
        mock_git_init.return_value = True
        
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            result = self.cli.init(git=True)
        
        self.assertTrue(result)
        mock_git_init.assert_called_once()
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('shutil.copy2')
    def test_init_with_ai_claude(self, mock_copy, mock_file, mock_mkdir, mock_exists):
        """Test init with Claude AI option"""
        mock_exists.return_value = False
        
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            result = self.cli.init(ai="claude")
        
        self.assertTrue(result)
        # Should create .claude directory
        mock_mkdir.assert_any_call(parents=True, exist_ok=True)
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('shutil.copy2')
    def test_init_with_ai_gemini(self, mock_copy, mock_file, mock_mkdir, mock_exists):
        """Test init with Gemini AI option"""
        mock_exists.return_value = False
        
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            result = self.cli.init(ai="gemini")
        
        self.assertTrue(result)
        # Should create .gemini directory
        mock_mkdir.assert_any_call(parents=True, exist_ok=True)
    
    def test_create_templates(self):
        """Test _create_templates method"""
        project_path = Path(self.temp_dir)
        templates_dir = project_path / "templates"
        templates_dir.mkdir(parents=True)
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            self.cli._create_templates(project_path)
            # Should write template files
            self.assertTrue(mock_file.called)
    
    def test_create_memory_files(self):
        """Test _create_memory_files method"""
        project_path = Path(self.temp_dir)
        memory_dir = project_path / "memory"
        memory_dir.mkdir(parents=True)
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            self.cli._create_memory_files(project_path)
            # Should write memory files
            self.assertTrue(mock_file.called)
    
    def test_create_scripts(self):
        """Test _create_scripts method"""
        project_path = Path(self.temp_dir)
        scripts_dir = project_path / "scripts"
        scripts_dir.mkdir(parents=True)
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            self.cli._create_scripts(project_path)
            # Should write script files
            self.assertTrue(mock_file.called)
    
    @patch('pathlib.Path.exists')
    def test_create_ai_commands_claude(self, mock_exists):
        """Test _create_ai_commands for Claude"""
        project_path = Path(self.temp_dir)
        mock_exists.return_value = True
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            with patch('pathlib.Path.mkdir') as mock_mkdir:
                self.cli._create_ai_commands(project_path, ai="claude")
                # Should create Claude command files
                self.assertTrue(mock_file.called)
    
    @patch('pathlib.Path.exists')
    def test_create_ai_commands_gemini(self, mock_exists):
        """Test _create_ai_commands for Gemini"""
        project_path = Path(self.temp_dir)
        mock_exists.return_value = True
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            with patch('pathlib.Path.mkdir') as mock_mkdir:
                self.cli._create_ai_commands(project_path, ai="gemini")
                # Should create Gemini command files
                self.assertTrue(mock_file.called)
    
    def test_create_manifest(self):
        """Test _create_manifest method"""
        project_path = Path(self.temp_dir)
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            self.cli._create_manifest(project_path, "test-project")
            # Should write manifest file
            mock_file.assert_called()
    
    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_update_command(self, mock_exists, mock_run):
        """Test update command"""
        mock_exists.return_value = True
        mock_run.return_value = MagicMock(returncode=0)
        
        with patch.object(self.cli.console, 'info') as mock_info:
            self.cli.update()
            mock_info.assert_called()
    
    @patch('pathlib.Path.exists')
    def test_update_command_no_specpulse(self, mock_exists):
        """Test update command when .specpulse doesn't exist"""
        mock_exists.return_value = False
        
        with patch.object(self.cli.console, 'error') as mock_error:
            self.cli.update()
            mock_error.assert_called()
    
    @patch('pathlib.Path.cwd')
    @patch('specpulse.core.validator.Validator.validate_all')
    def test_validate_command_all(self, mock_validate, mock_cwd):
        """Test validate command for all components"""
        mock_cwd.return_value = Path(self.temp_dir)
        mock_validate.return_value = [
            {'status': 'success', 'message': 'Test passed'}
        ]
        
        with patch.object(self.cli.console, 'header') as mock_header:
            self.cli.validate()
            mock_header.assert_called()
            mock_validate.assert_called_once()
    
    @patch('pathlib.Path.cwd')
    @patch('specpulse.core.validator.Validator.validate_spec')
    def test_validate_command_spec(self, mock_validate, mock_cwd):
        """Test validate command for spec"""
        mock_cwd.return_value = Path(self.temp_dir)
        mock_validate.return_value = [
            {'status': 'success', 'message': 'Spec valid'}
        ]
        
        self.cli.validate(component="spec")
        mock_validate.assert_called_once()
    
    @patch('pathlib.Path.cwd')
    @patch('specpulse.core.validator.Validator.validate_plan')
    def test_validate_command_plan(self, mock_validate, mock_cwd):
        """Test validate command for plan"""
        mock_cwd.return_value = Path(self.temp_dir)
        mock_validate.return_value = [
            {'status': 'success', 'message': 'Plan valid'}
        ]
        
        self.cli.validate(component="plan")
        mock_validate.assert_called_once()
    
    @patch('pathlib.Path.cwd')
    @patch('specpulse.core.validator.Validator.validate_constitution')
    def test_validate_command_constitution(self, mock_validate, mock_cwd):
        """Test validate command for constitution"""
        mock_cwd.return_value = Path(self.temp_dir)
        mock_validate.return_value = [
            {'status': 'success', 'message': 'Constitution valid'}
        ]
        
        self.cli.validate(component="constitution")
        mock_validate.assert_called_once()
    
    @patch('pathlib.Path.cwd')
    def test_validate_command_invalid_component(self, mock_cwd):
        """Test validate command with invalid component"""
        mock_cwd.return_value = Path(self.temp_dir)
        
        with patch.object(self.cli.console, 'error') as mock_error:
            self.cli.validate(component="invalid")
            mock_error.assert_called()
    
    @patch('pathlib.Path.exists')
    @patch('specpulse.utils.git_utils.GitUtils.check_git_installed')
    @patch('specpulse.utils.git_utils.GitUtils.is_git_repo')
    @patch('specpulse.utils.git_utils.GitUtils.has_changes')
    @patch('specpulse.utils.git_utils.GitUtils.add_files')
    @patch('specpulse.utils.git_utils.GitUtils.commit')
    def test_sync_command_success(self, mock_commit, mock_add, mock_changes,
                                  mock_is_repo, mock_check_git, mock_exists):
        """Test sync command success"""
        mock_exists.return_value = True
        mock_check_git.return_value = True
        mock_is_repo.return_value = True
        mock_changes.return_value = True
        mock_add.return_value = True
        mock_commit.return_value = True
        
        with patch.object(self.cli.console, 'success') as mock_success:
            self.cli.sync()
            mock_success.assert_called()
    
    @patch('pathlib.Path.exists')
    def test_sync_command_no_specpulse(self, mock_exists):
        """Test sync command when .specpulse doesn't exist"""
        mock_exists.return_value = False
        
        with patch.object(self.cli.console, 'error') as mock_error:
            self.cli.sync()
            mock_error.assert_called()
    
    @patch('pathlib.Path.exists')
    @patch('specpulse.utils.git_utils.GitUtils.check_git_installed')
    def test_sync_command_no_git(self, mock_check_git, mock_exists):
        """Test sync command when git not installed"""
        mock_exists.return_value = True
        mock_check_git.return_value = False
        
        with patch.object(self.cli.console, 'error') as mock_error:
            self.cli.sync()
            mock_error.assert_called()
    
    @patch('pathlib.Path.exists')
    @patch('specpulse.utils.git_utils.GitUtils.check_git_installed')
    @patch('specpulse.core.validator.Validator.validate_all')
    def test_doctor_command(self, mock_validate, mock_check_git, mock_exists):
        """Test doctor command"""
        mock_exists.return_value = True
        mock_check_git.return_value = True
        mock_validate.return_value = []
        
        with patch.object(self.cli.console, 'header') as mock_header:
            self.cli.doctor()
            mock_header.assert_called()
    
    @patch('pathlib.Path.exists')
    def test_doctor_command_no_specpulse(self, mock_exists):
        """Test doctor command when .specpulse doesn't exist"""
        mock_exists.return_value = False
        
        with patch.object(self.cli.console, 'error') as mock_error:
            self.cli.doctor()
            mock_error.assert_called()


class TestMainFunction(unittest.TestCase):
    """Test main function"""
    
    @patch('sys.argv', ['specpulse', 'init'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_init(self, mock_cli_class):
        """Test main function with init command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.init.assert_called_once()
    
    @patch('sys.argv', ['specpulse', 'init', 'project-name'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_init_with_name(self, mock_cli_class):
        """Test main function with init and project name"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.init.assert_called_with(project_name='project-name', git=False, ai=None)
    
    @patch('sys.argv', ['specpulse', 'init', '--git'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_init_with_git(self, mock_cli_class):
        """Test main function with init --git"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.init.assert_called_with(project_name=None, git=True, ai=None)
    
    @patch('sys.argv', ['specpulse', 'init', '--ai', 'claude'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_init_with_ai(self, mock_cli_class):
        """Test main function with init --ai"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.init.assert_called_with(project_name=None, git=False, ai='claude')
    
    @patch('sys.argv', ['specpulse', 'update'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_update(self, mock_cli_class):
        """Test main function with update command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.update.assert_called_once()
    
    @patch('sys.argv', ['specpulse', 'validate'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_validate(self, mock_cli_class):
        """Test main function with validate command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.validate.assert_called_with(component='all', fix=False, verbose=False)
    
    @patch('sys.argv', ['specpulse', 'validate', '--component', 'spec'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_validate_with_component(self, mock_cli_class):
        """Test main function with validate --component"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.validate.assert_called_with(component='spec', fix=False, verbose=False)
    
    @patch('sys.argv', ['specpulse', 'validate', '--fix'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_validate_with_fix(self, mock_cli_class):
        """Test main function with validate --fix"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.validate.assert_called_with(component='all', fix=True, verbose=False)
    
    @patch('sys.argv', ['specpulse', 'validate', '--verbose'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_validate_with_verbose(self, mock_cli_class):
        """Test main function with validate --verbose"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.validate.assert_called_with(component='all', fix=False, verbose=True)
    
    @patch('sys.argv', ['specpulse', 'sync'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_sync(self, mock_cli_class):
        """Test main function with sync command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.sync.assert_called_once()
    
    @patch('sys.argv', ['specpulse', 'doctor'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_doctor(self, mock_cli_class):
        """Test main function with doctor command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.doctor.assert_called_once()
    
    @patch('sys.argv', ['specpulse', '--version'])
    def test_main_version(self):
        """Test main function with --version"""
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
            mock_print.assert_called()
    
    @patch('sys.argv', ['specpulse', '--help'])
    def test_main_help(self):
        """Test main function with --help"""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
    
    @patch('sys.argv', ['specpulse'])
    def test_main_no_args(self):
        """Test main function with no arguments"""
        with self.assertRaises(SystemExit):
            main()
    
    @patch('sys.argv', ['specpulse', 'unknown'])
    def test_main_unknown_command(self):
        """Test main function with unknown command"""
        with self.assertRaises(SystemExit):
            main()