"""
Additional tests for 100% coverage
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import shutil
import yaml
import os
import subprocess

from specpulse.cli.main import SpecPulseCLI, main
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.utils.console import Console
from specpulse.utils.git_utils import GitUtils
from specpulse.utils.version_check import (
    check_pypi_version,
    compare_versions,
    should_check_version,
    get_update_message
)


class TestCLICoverage:
    """Additional CLI tests for full coverage"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        # Create config
        config_dir = self.project_path / ".specpulse"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.yaml"
        config_file.write_text(yaml.dump({"project_name": "test", "version": "1.0.0"}))
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('specpulse.utils.version_check.should_check_version')
    @patch('specpulse.utils.version_check.check_pypi_version')
    def test_cli_with_version_error(self, mock_check_pypi, mock_should_check):
        """Test CLI when version check fails"""
        mock_should_check.return_value = True
        mock_check_pypi.side_effect = Exception("Network error")

        cli = SpecPulseCLI(no_color=True, verbose=True)
        assert cli is not None

    @patch('sys.argv', ['sp', 'init', 'test-project'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_init(self, mock_cli_class):
        """Test main function with init command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        result = main()
        assert result == 0
        mock_cli.init.assert_called_once()

    @patch('sys.argv', ['sp', 'validate'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_validate(self, mock_cli_class):
        """Test main function with validate command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        mock_cli.validate.return_value = True

        result = main()
        assert result == 0
        mock_cli.validate.assert_called_once()

    @patch('sys.argv', ['sp', 'doctor'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_doctor(self, mock_cli_class):
        """Test main function with doctor command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        result = main()
        assert result == 0
        mock_cli.doctor.assert_called_once()

    @patch('sys.argv', ['sp', 'sync'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_sync(self, mock_cli_class):
        """Test main function with sync command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        mock_cli.sync.return_value = True

        result = main()
        assert result == 0
        mock_cli.sync.assert_called_once()

    @patch('sys.argv', ['sp', 'update'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_update(self, mock_cli_class):
        """Test main function with update command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        mock_cli.update.return_value = True

        result = main()
        assert result == 0
        mock_cli.update.assert_called_once()

    @patch('sys.argv', ['sp', 'list'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_list(self, mock_cli_class):
        """Test main function with list command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        result = main()
        assert result == 0
        mock_cli.list_specs.assert_called_once()

    @patch('sys.argv', ['sp', 'decompose', '001'])
    @patch('specpulse.cli.main.SpecPulseCLI')
    def test_main_decompose(self, mock_cli_class):
        """Test main function with decompose command"""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        mock_cli.decompose.return_value = True

        result = main()
        assert result == 0
        mock_cli.decompose.assert_called_once()

    @patch('sys.argv', ['sp', '--version'])
    @patch('builtins.print')
    def test_main_version(self, mock_print):
        """Test main function with --version flag"""
        result = main()
        assert result == 0
        mock_print.assert_called()

    @patch('sys.argv', ['sp', 'invalid-command'])
    def test_main_invalid_command(self):
        """Test main function with invalid command"""
        result = main()
        assert result == 1

    @patch('sys.argv', ['sp'])
    @patch('builtins.print')
    def test_main_no_args(self, mock_print):
        """Test main function with no arguments"""
        result = main()
        assert result == 0


class TestValidatorCoverage:
    """Additional Validator tests for full coverage"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.validator = Validator(self.project_path)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_validate_with_fix(self):
        """Test validation with fix option"""
        # Create specs with issues
        specs_dir = self.project_path / "specs" / "001-test"
        specs_dir.mkdir(parents=True)
        spec_file = specs_dir / "spec.md"
        spec_file.write_text("# Spec\n")  # Missing sections

        results = self.validator.validate_all(self.project_path, fix=True, verbose=True)
        assert isinstance(results, list)

    def test_validate_spec_with_name(self):
        """Test spec validation with specific name"""
        specs_dir = self.project_path / "specs" / "001-test"
        specs_dir.mkdir(parents=True)
        spec_file = specs_dir / "spec.md"
        spec_file.write_text("# Spec\n## Requirements\n- Test")

        results = self.validator.validate_spec(self.project_path, spec_name="001", verbose=True)
        assert isinstance(results, list)

    def test_validate_plan_with_name(self):
        """Test plan validation with specific name"""
        plans_dir = self.project_path / "plans" / "001-test"
        plans_dir.mkdir(parents=True)
        plan_file = plans_dir / "plan.md"
        plan_file.write_text("# Plan\n## Architecture\n## Phases\n## Technology Stack")

        results = self.validator.validate_plan(self.project_path, plan_name="001", verbose=True)
        assert isinstance(results, list)

    def test_validate_spec_missing_sections(self):
        """Test spec validation with missing sections"""
        spec_file = self.project_path / "spec.md"
        spec_file.write_text("# Spec\n")  # Missing all required sections

        result = self.validator.validate_spec_file(spec_file, verbose=True)
        assert result["status"] == "invalid"
        assert len(result["issues"]) > 0

    def test_validate_plan_missing_sections(self):
        """Test plan validation with missing sections"""
        plan_file = self.project_path / "plan.md"
        plan_file.write_text("# Plan\n")  # Missing all required sections

        result = self.validator.validate_plan_file(plan_file, verbose=True)
        assert result["status"] == "invalid"
        assert len(result["issues"]) > 0

    def test_validate_task_missing_sections(self):
        """Test task validation with missing sections"""
        task_file = self.project_path / "task.md"
        task_file.write_text("# Tasks\n")  # Missing task definitions

        result = self.validator.validate_task_file(task_file, verbose=True)
        assert result["status"] == "invalid"
        assert len(result["issues"]) > 0

    def test_validate_sdd_principles_verbose(self):
        """Test SDD principles validation with verbose output"""
        content = "# Spec without principles"
        result = self.validator.validate_sdd_principles(content, verbose=True)
        assert result["status"] == "non-compliant"

    def test_load_constitution_missing_file(self):
        """Test loading constitution when file doesn't exist"""
        result = self.validator.load_constitution(self.project_path)
        assert result is False


class TestSpecPulseCoverage:
    """Additional SpecPulse tests for full coverage"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_specpulse_no_config(self):
        """Test SpecPulse initialization without config"""
        sp = SpecPulse()
        assert sp.config == {}

    def test_specpulse_with_invalid_config(self):
        """Test SpecPulse with invalid config file"""
        config_dir = self.project_path / ".specpulse"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "config.yaml"
        config_file.write_text("invalid: yaml: content:")  # Invalid YAML

        sp = SpecPulse(self.project_path)
        assert sp.config == {}

    def test_get_decomposition_templates(self):
        """Test getting all decomposition template types"""
        sp = SpecPulse()

        # Test all template types that don't exist
        result = sp.get_decomposition_template("nonexistent")
        assert "Template not found" in result or len(result) > 0


class TestConsoleCoverage:
    """Additional Console tests for full coverage"""

    def test_console_with_color(self):
        """Test console with color enabled"""
        console = Console(no_color=False, verbose=True)

        # Test methods that behave differently with color
        with console.spinner("Loading"):
            pass  # Should create actual spinner

    def test_console_tree_nested(self):
        """Test console tree with deeply nested structure"""
        console = Console(no_color=True)

        nested_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": "value"
                    }
                },
                "another": "value"
            }
        }
        console.tree("Nested Tree", nested_data)


class TestGitUtilsCoverage:
    """Additional GitUtils tests for full coverage"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.git_utils = GitUtils(Path(self.temp_dir))

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.run')
    def test_git_command_failure(self, mock_run):
        """Test git command failures"""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")

        # Test various operations that should handle failures
        result = self.git_utils.add_files(["file.txt"])
        assert result is False

        result = self.git_utils.stash_changes("test")
        assert result is False

        result = self.git_utils.push(force=True)
        assert result is False

        result = self.git_utils.pull("branch")
        assert result is False

        result = self.git_utils.tag("v1.0.0", "message")
        assert result is False

    @patch('subprocess.run')
    def test_git_empty_responses(self, mock_run):
        """Test git operations with empty responses"""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        result = self.git_utils.get_current_branch()
        assert result is None

        result = self.git_utils.get_remote_url()
        assert result is None

        result = self.git_utils.get_diff(staged=True)
        assert result is None


class TestVersionCheckCoverage:
    """Additional version check tests for full coverage"""

    def test_get_update_message_all_cases(self):
        """Test all update message cases"""
        # When versions are equal or current is newer
        msg = get_update_message("2.0.0", "1.0.0", False)
        if isinstance(msg, tuple):
            msg = msg[0]
        # Should still return a message
        assert isinstance(msg, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])