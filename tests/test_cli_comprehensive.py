"""
Comprehensive test suite for SpecPulse CLI module.
Tests all CLI functionality with proper mocking for external dependencies.
"""

import pytest
import unittest
from unittest.mock import patch, mock_open, MagicMock, call
from pathlib import Path
import tempfile
import shutil
import sys
import os
import yaml
from datetime import datetime

from specpulse.cli.main import SpecPulseCLI, main
from specpulse.utils.console import Console
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.utils.git_utils import GitUtils


class TestSpecPulseCLI(unittest.TestCase):
    """Comprehensive tests for SpecPulseCLI class"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.cli = SpecPulseCLI(no_color=True, verbose=False)
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_init_with_defaults(self):
        """Test CLI initialization with default parameters"""
        self.assertIsInstance(self.cli.console, Console)
        self.assertIsInstance(self.cli.specpulse, SpecPulse)
        self.assertIsInstance(self.cli.validator, Validator)
        self.assertTrue(self.cli.console.no_color)
        self.assertFalse(self.cli.console.verbose)

    def test_init_with_custom_params(self):
        """Test CLI initialization with custom parameters"""
        cli = SpecPulseCLI(no_color=False, verbose=True)
        self.assertFalse(cli.console.no_color)
        self.assertTrue(cli.console.verbose)

    @patch('specpulse.cli.main.Path')
    @patch('specpulse.cli.main.open', new_callable=mock_open)
    @patch('specpulse.cli.main.yaml.dump')
    @patch('specpulse.cli.main.os.chmod')
    def test_init_here_flag(self, mock_chmod, mock_yaml_dump, mock_file, mock_path):
        """Test project initialization with --here flag"""
        # Create mock project path
        mock_project_path = MagicMock()
        mock_project_path.name = "test-project"
        
        # Mock directory creation
        mock_dir = MagicMock()
        mock_dir.mkdir = MagicMock()
        mock_project_path.__truediv__ = MagicMock(return_value=mock_dir)
        mock_path.cwd.return_value = mock_project_path
        
        result = self.cli.init(here=True)
        
        self.assertTrue(result)
        mock_yaml_dump.assert_called()

    @patch('specpulse.cli.main.Path')
    @patch('specpulse.cli.main.open', new_callable=mock_open)
    @patch('specpulse.cli.main.yaml.dump')
    @patch('specpulse.cli.main.os.chmod')
    def test_init_with_project_name(self, mock_chmod, mock_yaml_dump, mock_file, mock_path):
        """Test project initialization with project name"""
        mock_current_path = MagicMock()
        mock_path.cwd.return_value = mock_current_path
        
        # Mock new project path
        mock_project_path = MagicMock()
        mock_project_path.exists.return_value = False
        mock_project_path.mkdir = MagicMock()
        mock_current_path.__truediv__ = MagicMock(return_value=mock_project_path)
        
        # Mock directory creation within project
        mock_dir = MagicMock()
        mock_dir.mkdir = MagicMock()
        mock_project_path.__truediv__ = MagicMock(return_value=mock_dir)
        
        result = self.cli.init("new-project", ai="gemini", template="api")
        
        self.assertTrue(result)
        mock_yaml_dump.assert_called()

    @patch('specpulse.cli.main.Path')
    @patch('specpulse.cli.main.open', new_callable=mock_open)
    def test_init_no_project_name(self, mock_file, mock_path):
        """Test project initialization without project name"""
        mock_project_path = MagicMock()
        mock_project_path.name = "current-dir"
        mock_path.cwd.return_value = mock_project_path
        
        # Mock directory creation
        mock_dir = MagicMock()
        mock_dir.mkdir = MagicMock()
        mock_project_path.__truediv__ = MagicMock(return_value=mock_dir)
        
        with patch('specpulse.cli.main.yaml.dump'):
            with patch('specpulse.cli.main.os.chmod'):
                result = self.cli.init()
                
        self.assertTrue(result)

    def test_create_templates(self):
        """Test template creation method"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            templates_dir = project_path / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)
            
            self.cli._create_templates(project_path)
            
            # Check template files exist
            self.assertTrue((templates_dir / "spec.md").exists())
            self.assertTrue((templates_dir / "plan.md").exists())
            self.assertTrue((templates_dir / "task.md").exists())

    def test_create_memory_files(self):
        """Test memory files creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            memory_dir = project_path / "memory"
            memory_dir.mkdir(parents=True, exist_ok=True)
            
            self.cli._create_memory_files(project_path)
            
            # Check memory files exist
            self.assertTrue((memory_dir / "constitution.md").exists())
            self.assertTrue((memory_dir / "context.md").exists())
            self.assertTrue((memory_dir / "decisions.md").exists())

    def test_create_scripts(self):
        """Test script creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            scripts_dir = project_path / "scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            
            with patch('specpulse.cli.main.os.chmod'):
                self.cli._create_scripts(project_path)
            
            # Check script files exist
            self.assertTrue((scripts_dir / "pulse-init.sh").exists())
            self.assertTrue((scripts_dir / "pulse-spec.sh").exists())
            self.assertTrue((scripts_dir / "pulse-plan.sh").exists())
            self.assertTrue((scripts_dir / "pulse-task.sh").exists())

    def test_create_ai_commands(self):
        """Test AI command files creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            claude_dir = project_path / ".claude" / "commands"
            gemini_dir = project_path / ".gemini" / "commands" 
            claude_dir.mkdir(parents=True, exist_ok=True)
            gemini_dir.mkdir(parents=True, exist_ok=True)
            
            self.cli._create_ai_commands(project_path)
            
            # Check Claude command files
            self.assertTrue((claude_dir / "pulse.md").exists())
            self.assertTrue((claude_dir / "spec.md").exists())
            self.assertTrue((claude_dir / "plan.md").exists())
            self.assertTrue((claude_dir / "task.md").exists())
            
            # Check Gemini command files
            self.assertTrue((gemini_dir / "pulse.toml").exists())
            self.assertTrue((gemini_dir / "spec.toml").exists())
            self.assertTrue((gemini_dir / "plan.toml").exists())
            self.assertTrue((gemini_dir / "task.toml").exists())

    def test_create_manifest(self):
        """Test manifest creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            self.cli._create_manifest(project_path, "test-project")
            
            manifest_path = project_path / "PULSE.md"
            self.assertTrue(manifest_path.exists())
            
            # Check manifest content
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn("# test-project - SpecPulse Project", content)
            self.assertIn("SpecPulse for specification-driven development", content)

    @patch('specpulse.cli.main.Path')
    def test_update_not_specpulse_project(self, mock_path):
        """Test update when not in SpecPulse project"""
        mock_project_path = MagicMock()
        mock_path.cwd.return_value = mock_project_path
        
        # Mock config path that doesn't exist
        mock_config_path = MagicMock()
        mock_config_path.exists.return_value = False
        
        # Mock directory traversal
        mock_specpulse_dir = MagicMock()
        mock_specpulse_dir.__truediv__ = MagicMock(return_value=mock_config_path)
        mock_project_path.__truediv__ = MagicMock(return_value=mock_specpulse_dir)
        
        result = self.cli.update()
        
        self.assertFalse(result)

    @patch('specpulse.cli.main.Path')
    @patch('specpulse.cli.main.shutil.copytree')
    def test_update_success(self, mock_copytree, mock_path):
        """Test successful update"""
        mock_project_path = MagicMock()
        mock_path.cwd.return_value = mock_project_path
        
        # Mock config path exists
        mock_config_path = MagicMock()
        mock_config_path.exists.return_value = True
        
        # Mock templates directory
        mock_templates_dir = MagicMock()
        mock_templates_dir.exists.return_value = True
        
        # Mock backup directory
        mock_backup_dir = MagicMock()
        mock_backup_dir.mkdir = MagicMock()
        
        # Set up path mocking for different directories
        def project_div_side_effect(path_part):
            if path_part == ".specpulse":
                mock_specpulse_dir = MagicMock()
                def specpulse_div_side_effect(x):
                    if x == "config.yaml":
                        return mock_config_path
                    else:  # backups directory
                        return MagicMock(mkdir=MagicMock(), __truediv__=MagicMock(return_value=mock_backup_dir))
                mock_specpulse_dir.__truediv__ = MagicMock(side_effect=specpulse_div_side_effect)
                return mock_specpulse_dir
            elif path_part == "templates":
                return mock_templates_dir
            return MagicMock()
            
        mock_project_path.__truediv__ = MagicMock(side_effect=project_div_side_effect)
        
        with patch('specpulse.cli.main.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "20231201_120000"
            
            # Patch the _create_templates method to avoid actual file I/O
            with patch.object(self.cli, '_create_templates'):
                result = self.cli.update()
        
        self.assertTrue(result)

    def test_validate_all_components(self):
        """Test validation of all components"""
        with patch.object(self.cli.validator, 'validate_all') as mock_validate:
            mock_validate.return_value = [
                {"component": "specs", "status": "success"},
                {"component": "plans", "status": "success"}
            ]
            
            result = self.cli.validate("all")
            
            self.assertTrue(result)
            mock_validate.assert_called_once()

    def test_validate_specific_component(self):
        """Test validation of specific component"""
        with patch.object(self.cli.validator, 'validate_spec') as mock_validate:
            mock_validate.return_value = [{"component": "spec", "status": "success"}]
            
            result = self.cli.validate("spec")
            
            self.assertTrue(result)
            mock_validate.assert_called_once()

    def test_validate_unknown_component(self):
        """Test validation with unknown component"""
        result = self.cli.validate("unknown")
        self.assertFalse(result)

    def test_validate_with_errors(self):
        """Test validation with errors"""
        with patch.object(self.cli.validator, 'validate_all') as mock_validate:
            mock_validate.return_value = [
                {"component": "specs", "status": "error"},
                {"component": "plans", "status": "success"}
            ]
            
            result = self.cli.validate("all")
            
            self.assertFalse(result)

    @patch('specpulse.cli.main.Path')
    @patch('specpulse.cli.main.open', new_callable=mock_open)
    def test_sync_success(self, mock_file, mock_path):
        """Test successful sync"""
        mock_project_path = MagicMock()
        mock_path.cwd.return_value = mock_project_path
        
        # Mock context path
        mock_context_path = MagicMock()
        mock_context_path.exists.return_value = True
        
        # Mock specs directory
        mock_specs_dir = MagicMock()
        mock_specs_dir.exists.return_value = True
        mock_specs_dir.glob.return_value = [MagicMock(), MagicMock()]  # 2 specs
        
        def path_div_side_effect(path_part):
            if path_part == "memory":
                mock_memory_dir = MagicMock()
                mock_memory_dir.__truediv__ = MagicMock(return_value=mock_context_path)
                return mock_memory_dir
            elif path_part == "specs":
                return mock_specs_dir
            return MagicMock()
            
        mock_project_path.__truediv__ = MagicMock(side_effect=path_div_side_effect)
        
        with patch.object(self.cli, 'console'):
            result = self.cli.sync()
        
        self.assertTrue(result)

    @patch('specpulse.cli.main.sys')
    def test_doctor_all_checks_pass(self, mock_sys):
        """Test doctor when all checks pass"""
        # Mock sys.version_info as a proper named tuple-like object
        version_info = MagicMock()
        version_info.major = 3
        version_info.minor = 11
        version_info.micro = 0
        version_info.__ge__ = lambda self, other: True  # >= (3, 11)
        mock_sys.version_info = version_info
        
        with patch.object(GitUtils, 'check_git_installed', return_value=True):
            with patch('specpulse.cli.main.Path') as mock_path:
                mock_project_path = MagicMock()
                mock_path.cwd.return_value = mock_project_path
                
                mock_config_path = MagicMock()
                mock_config_path.exists.return_value = True
                
                def path_div_side_effect(path_part):
                    if path_part == ".specpulse":
                        mock_specpulse_dir = MagicMock()
                        mock_specpulse_dir.__truediv__ = MagicMock(return_value=mock_config_path)
                        return mock_specpulse_dir
                    else:
                        # Return existing directory for all required directories
                        mock_dir = MagicMock()
                        mock_dir.exists.return_value = True
                        return mock_dir
                
                mock_project_path.__truediv__ = MagicMock(side_effect=path_div_side_effect)
                
                result = self.cli.doctor()
                
        self.assertTrue(result)

    @patch('specpulse.cli.main.sys')
    def test_doctor_some_checks_fail(self, mock_sys):
        """Test doctor when some checks fail"""
        # Mock sys.version_info for old Python version
        version_info = MagicMock()
        version_info.major = 3
        version_info.minor = 8
        version_info.micro = 0
        version_info.__ge__ = lambda self, other: False  # < (3, 11)
        mock_sys.version_info = version_info
        
        with patch.object(GitUtils, 'check_git_installed', return_value=False):
            with patch('specpulse.cli.main.Path') as mock_path:
                mock_project_path = MagicMock()
                mock_path.cwd.return_value = mock_project_path
                
                mock_config_path = MagicMock()
                mock_config_path.exists.return_value = False
                
                def path_div_side_effect(path_part):
                    if path_part == ".specpulse":
                        mock_specpulse_dir = MagicMock()
                        mock_specpulse_dir.__truediv__ = MagicMock(return_value=mock_config_path)
                        return mock_specpulse_dir
                    else:
                        mock_dir = MagicMock()
                        mock_dir.exists.return_value = False
                        return mock_dir
                
                mock_project_path.__truediv__ = MagicMock(side_effect=path_div_side_effect)
                
                result = self.cli.doctor()
                
        self.assertFalse(result)

    @patch('specpulse.cli.main.Path')
    def test_doctor_missing_directories(self, mock_path):
        """Test doctor with missing directories"""
        with patch('specpulse.cli.main.sys') as mock_sys:
            # Mock proper version info
            version_info = MagicMock()
            version_info.major = 3
            version_info.minor = 11
            version_info.micro = 0
            version_info.__ge__ = lambda self, other: True
            mock_sys.version_info = version_info
            
            with patch.object(GitUtils, 'check_git_installed', return_value=True):
                mock_project_path = MagicMock()
                mock_path.cwd.return_value = mock_project_path
                
                mock_config_path = MagicMock()
                mock_config_path.exists.return_value = True
                
                def path_div_side_effect(path_part):
                    if path_part == ".specpulse":
                        mock_specpulse_dir = MagicMock()
                        mock_specpulse_dir.__truediv__ = MagicMock(return_value=mock_config_path)
                        return mock_specpulse_dir
                    elif path_part in ["memory", "specs"]:
                        # These directories exist
                        existing_dir = MagicMock()
                        existing_dir.exists.return_value = True
                        return existing_dir
                    else:
                        # Missing directories (plans, tasks)
                        missing_dir = MagicMock()
                        missing_dir.exists.return_value = False
                        return missing_dir
                
                mock_project_path.__truediv__ = MagicMock(side_effect=path_div_side_effect)
                
                result = self.cli.doctor()
                
        self.assertFalse(result)


class TestMainFunction(unittest.TestCase):
    """Test the main CLI entry point function"""

    @patch('specpulse.cli.main.argparse.ArgumentParser')
    def test_main_no_command(self, mock_parser):
        """Test main function with no command (shows help)"""
        mock_args = MagicMock()
        mock_args.command = None
        mock_args.no_color = False
        mock_args.verbose = False
        
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser.return_value = mock_parser_instance
        
        with patch('specpulse.cli.main.Console') as mock_console_class:
            mock_console = MagicMock()
            mock_console_class.return_value = mock_console
            
            main()
            
            # Should show banner and help
            mock_console.show_banner.assert_called_once()
            mock_parser_instance.print_help.assert_called_once()

    @patch('specpulse.cli.main.argparse.ArgumentParser')
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_init_command(self, mock_cli_class, mock_parser):
        """Test main function with init command"""
        mock_args = MagicMock()
        mock_args.command = "init"
        mock_args.project_name = "test-project"
        mock_args.here = False
        mock_args.ai = "claude"
        mock_args.template = "web"
        mock_args.no_color = False
        mock_args.verbose = False
        
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser.return_value = mock_parser_instance
        
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli_class.assert_called_once_with(no_color=False, verbose=False)
        mock_cli.init.assert_called_once_with("test-project", False, "claude", "web")

    @patch('specpulse.cli.main.argparse.ArgumentParser')
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_update_command(self, mock_cli_class, mock_parser):
        """Test main function with update command"""
        mock_args = MagicMock()
        mock_args.command = "update"
        mock_args.no_color = True
        mock_args.verbose = True
        
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser.return_value = mock_parser_instance
        
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli_class.assert_called_once_with(no_color=True, verbose=True)
        mock_cli.update.assert_called_once()

    @patch('specpulse.cli.main.argparse.ArgumentParser')
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_validate_command(self, mock_cli_class, mock_parser):
        """Test main function with validate command"""
        mock_args = MagicMock()
        mock_args.command = "validate"
        mock_args.component = "spec"
        mock_args.fix = True
        mock_args.verbose = False
        mock_args.no_color = False
        
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser.return_value = mock_parser_instance
        
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.validate.assert_called_once_with("spec", True, False)

    @patch('specpulse.cli.main.argparse.ArgumentParser')
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_sync_command(self, mock_cli_class, mock_parser):
        """Test main function with sync command"""
        mock_args = MagicMock()
        mock_args.command = "sync"
        mock_args.no_color = False
        mock_args.verbose = False
        
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser.return_value = mock_parser_instance
        
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.sync.assert_called_once()

    @patch('specpulse.cli.main.argparse.ArgumentParser')
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_doctor_command(self, mock_cli_class, mock_parser):
        """Test main function with doctor command"""
        mock_args = MagicMock()
        mock_args.command = "doctor"
        mock_args.no_color = False
        mock_args.verbose = False
        
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser.return_value = mock_parser_instance
        
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        mock_cli.doctor.assert_called_once()

    @patch('specpulse.cli.main.argparse.ArgumentParser')
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_hasattr_handling(self, mock_cli_class, mock_parser):
        """Test main function hasattr handling for optional arguments"""
        mock_args = MagicMock()
        mock_args.command = "init"
        mock_args.project_name = "test"
        mock_args.here = False
        mock_args.ai = "claude"
        mock_args.template = "web"
        
        # Simulate missing attributes
        del mock_args.no_color
        del mock_args.verbose
        
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser.return_value = mock_parser_instance
        
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        main()
        
        # Should use defaults when attributes are missing
        mock_cli_class.assert_called_once_with(no_color=False, verbose=False)


if __name__ == '__main__':
    unittest.main()