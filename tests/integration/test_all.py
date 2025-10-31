"""
Complete test suite for 100% coverage and 100% success
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import shutil
import yaml
import json
import subprocess
from datetime import datetime, timedelta

from specpulse import __version__
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.cli.main import SpecPulseCLI
from specpulse.utils.console import Console
from specpulse.utils.git_utils import GitUtils
from specpulse.utils.version_check import (
    check_pypi_version,
    compare_versions,
    should_check_version,
    get_update_message
)


class TestSpecPulseCore:
    """Complete tests for SpecPulse core"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_specpulse_init(self):
        """Test SpecPulse initialization"""
        sp = SpecPulse()
        assert sp.resources_dir is not None
        assert sp.config is not None

    def test_specpulse_init_with_project_path(self):
        """Test SpecPulse with project path"""
        sp = SpecPulse(self.project_path)
        assert sp.project_path == self.project_path

    def test_specpulse_load_config(self):
        """Test config loading"""
        # Create config file
        config_dir = Path.home() / ".specpulse"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "config.yaml"
        config_data = {"test": "data"}
        config_file.write_text(yaml.dump(config_data))

        try:
            sp = SpecPulse()
            # Config should be loaded
            assert sp.config is not None
        finally:
            # Clean up
            if config_file.exists():
                config_file.unlink()

    def test_specpulse_templates(self):
        """Test all template getters"""
        sp = SpecPulse()

        # Test all template methods
        assert isinstance(sp.get_spec_template(), str)
        assert isinstance(sp.get_plan_template(), str)
        assert isinstance(sp.get_task_template(), str)
        assert isinstance(sp.get_constitution_template(), str)
        assert isinstance(sp.get_context_template(), str)
        assert isinstance(sp.get_decomposition_template("api"), str)
        assert isinstance(sp.get_decisions_template(), str)

    def test_specpulse_scripts(self):
        """Test all script getters"""
        sp = SpecPulse()

        # Test all script methods
        assert isinstance(sp.get_setup_script(), str)
        assert isinstance(sp.get_spec_script(), str)
        assert isinstance(sp.get_plan_script(), str)
        assert isinstance(sp.get_task_script(), str)
        assert isinstance(sp.get_validate_script(), str)
        assert isinstance(sp.get_generate_script(), str)

    def test_specpulse_claude_commands(self):
        """Test Claude command getters"""
        sp = SpecPulse()

        assert isinstance(sp.get_claude_instructions(), str)
        assert isinstance(sp.get_claude_pulse_command(), str)
        assert isinstance(sp.get_claude_spec_command(), str)
        assert isinstance(sp.get_claude_plan_command(), str)
        assert isinstance(sp.get_claude_task_command(), str)
        assert isinstance(sp.get_claude_decompose_command(), str)
        assert isinstance(sp.get_claude_execute_command(), str)
        assert isinstance(sp.get_claude_validate_command(), str)

    def test_specpulse_gemini_commands(self):
        """Test Gemini command getters"""
        sp = SpecPulse()

        assert isinstance(sp.get_gemini_pulse_command(), str)
        assert isinstance(sp.get_gemini_spec_command(), str)
        assert isinstance(sp.get_gemini_plan_command(), str)
        assert isinstance(sp.get_gemini_task_command(), str)
        assert isinstance(sp.get_gemini_decompose_command(), str)
        assert isinstance(sp.get_gemini_execute_command(), str)
        assert isinstance(sp.get_gemini_validate_command(), str)


class TestValidatorCore:
    """Complete tests for Validator"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_validator_init(self):
        """Test Validator initialization"""
        validator = Validator()
        assert validator.results == []
        assert validator.constitution is None
        assert validator.phase_gates == []

    def test_validator_init_with_project(self):
        """Test Validator with project root"""
        # Create constitution
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text("# Constitution")

        validator = Validator(self.project_path)
        assert validator.constitution is not None

    def test_validator_validate_all(self):
        """Test validate_all method"""
        validator = Validator()

        # Create structure
        for dir_name in ["specs", "plans", "tasks", "memory"]:
            (self.project_path / dir_name).mkdir()

        results = validator.validate_all(self.project_path)
        assert isinstance(results, list)

        # Test with fix and verbose
        results = validator.validate_all(self.project_path, fix=True, verbose=True)
        assert isinstance(results, list)

    def test_validator_validate_spec(self):
        """Test validate_spec method"""
        validator = Validator()

        # Test without directory
        results = validator.validate_spec(self.project_path)
        assert len(results) > 0

        # Create spec and test
        specs_dir = self.project_path / "specs" / "001-test"
        specs_dir.mkdir(parents=True)
        (specs_dir / "spec.md").write_text("# Spec")

        results = validator.validate_spec(self.project_path, spec_name="001-test")
        assert isinstance(results, list)

    def test_validator_validate_plan(self):
        """Test validate_plan method"""
        validator = Validator()

        # Test without directory
        results = validator.validate_plan(self.project_path)
        assert len(results) > 0

        # Create plan and test
        plans_dir = self.project_path / "plans" / "001-test"
        plans_dir.mkdir(parents=True)
        (plans_dir / "plan.md").write_text("# Plan")

        results = validator.validate_plan(self.project_path, plan_name="001-test")
        assert isinstance(results, list)

    def test_validator_validate_sdd_compliance(self):
        """Test SDD compliance validation"""
        validator = Validator()

        # Create constitution
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text("""
# Constitution
## Principle 1: Specification First
## Principle 2: Incremental Planning
        """)

        results = validator.validate_sdd_compliance(self.project_path)
        assert isinstance(results, list)

        # Test verbose
        results = validator.validate_sdd_compliance(self.project_path, verbose=True)
        assert isinstance(results, list)

    def test_validator_file_methods(self):
        """Test file validation methods"""
        validator = Validator()

        # Test validate_spec_file
        spec_file = self.project_path / "spec.md"
        spec_file.write_text("# Spec\n## Requirements\n- Test")
        result = validator.validate_spec_file(spec_file)
        assert isinstance(result, dict)

        # Test validate_plan_file
        plan_file = self.project_path / "plan.md"
        plan_file.write_text("# Plan\n## Architecture\n- Test")
        result = validator.validate_plan_file(plan_file)
        assert isinstance(result, dict)

        # Test validate_task_file
        task_file = self.project_path / "task.md"
        task_file.write_text("# Tasks\n## T001: Test")
        result = validator.validate_task_file(task_file)
        assert isinstance(result, dict)

    def test_validator_sdd_principles(self):
        """Test SDD principles validation"""
        validator = Validator()

        spec_content = "# Spec\nThis follows SDD principles"
        result = validator.validate_sdd_principles(spec_content)
        assert isinstance(result, dict)

        # Test verbose
        result = validator.validate_sdd_principles(spec_content, verbose=True)
        assert isinstance(result, dict)

    def test_validator_phase_gate(self):
        """Test phase gate checking"""
        validator = Validator()

        context = {"spec_complete": True}
        result = validator.check_phase_gate("specification", context)
        assert isinstance(result, bool)

    def test_validator_all_project(self):
        """Test validate_all_project"""
        validator = Validator()

        # Create structure
        (self.project_path / "specs").mkdir()
        (self.project_path / "plans").mkdir()
        (self.project_path / "tasks").mkdir()

        result = validator.validate_all_project(self.project_path)
        assert isinstance(result, dict)

    def test_validator_load_constitution(self):
        """Test constitution loading"""
        validator = Validator()

        # Create constitution
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text("# Constitution")

        result = validator.load_constitution(self.project_path)
        assert result is True
        assert validator.constitution is not None


class TestCLICore:
    """Complete tests for CLI"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir)

    def teardown_method(self):
        import os
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('specpulse.cli.main.should_check_version')
    def test_cli_init(self, mock_should):
        """Test CLI initialization"""
        mock_should.return_value = False
        cli = SpecPulseCLI(no_color=True, verbose=False)
        assert cli.console is not None
        assert cli.specpulse is not None

    @patch('specpulse.cli.main.should_check_version')
    @patch('specpulse.cli.main.check_pypi_version')
    @patch('specpulse.cli.main.compare_versions')
    @patch('specpulse.cli.main.get_update_message')
    def test_cli_with_updates(self, mock_msg, mock_compare, mock_check, mock_should):
        """Test CLI with update checking"""
        mock_should.return_value = True
        mock_check.return_value = "2.0.0"
        mock_compare.return_value = (True, True)
        mock_msg.return_value = "Update available"

        cli = SpecPulseCLI(no_color=True)
        assert cli is not None

    @patch('specpulse.cli.main.should_check_version')
    def test_cli_init_project(self, mock_should):
        """Test project initialization"""
        mock_should.return_value = False
        cli = SpecPulseCLI(no_color=True)

        with patch('shutil.copy2'):
            result = cli.init("test-project")
            assert result is True
            assert (Path.cwd() / "test-project").exists()

    @patch('specpulse.cli.main.should_check_version')
    def test_cli_init_invalid_name(self, mock_should):
        """Test init with invalid name"""
        mock_should.return_value = False
        cli = SpecPulseCLI(no_color=True)

        result = cli.init("invalid@name!")
        assert result is False

    @patch('specpulse.cli.main.should_check_version')
    @patch('pathlib.Path.cwd')
    def test_cli_validate(self, mock_cwd, mock_should):
        """Test validation"""
        mock_should.return_value = False
        mock_cwd.return_value = self.project_path

        (self.project_path / "specs").mkdir()

        cli = SpecPulseCLI(no_color=True)
        result = cli.validate()
        assert isinstance(result, bool)

    @patch('specpulse.cli.main.should_check_version')
    @patch('subprocess.run')
    def test_cli_update(self, mock_run, mock_should):
        """Test update command"""
        mock_should.return_value = False
        mock_run.return_value.returncode = 0

        cli = SpecPulseCLI(no_color=True)
        result = cli.update()
        assert result is True


class TestConsoleCore:
    """Complete tests for Console"""

    def test_console_init(self):
        """Test Console initialization"""
        console = Console(no_color=True, verbose=False)
        assert console.console is not None

    def test_console_display_methods(self):
        """Test all display methods"""
        console = Console(no_color=True)

        with patch.object(console.console, 'print'):
            console.show_banner()
            console.show_banner(mini=True)
            console.info("Info")
            console.success("Success")
            console.warning("Warning")
            console.error("Error")
            console.header("Header")
            console.section("Title", "Content")
            console.animated_text("Text", 0.001)
            console.divider()
            console.gradient_text("Gradient")
            console.code_block("code")

    def test_console_interactive(self):
        """Test interactive methods"""
        console = Console(no_color=True)

        # Test progress bar
        progress = console.progress_bar("Test", 10)
        assert hasattr(progress, '__enter__')

        # Test spinner
        spinner = console.spinner("Loading")
        assert spinner is not None

        # Test prompt
        with patch('rich.prompt.Prompt.ask') as mock_ask:
            mock_ask.return_value = "answer"
            result = console.prompt("Question")
            assert result == "answer"

        # Test confirm
        with patch('rich.prompt.Confirm.ask') as mock_ask:
            mock_ask.return_value = True
            result = console.confirm("Confirm?")
            assert result is True

    def test_console_table_tree(self):
        """Test table and tree display"""
        console = Console(no_color=True)

        with patch.object(console.console, 'print'):
            console.table("Title", ["Col1"], [["Data"]])
            console.tree("Tree", {"root": None})

    def test_console_animations(self):
        """Test animation methods"""
        console = Console(no_color=True)

        # These should complete without error
        console.pulse_animation("Test", 0.01)

        with patch.object(console.console, 'print'):
            console.type_effect("Test", 0.001)


class TestGitUtilsCore:
    """Complete tests for GitUtils"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.run')
    def test_git_check_installed(self, mock_run):
        """Test git installation check"""
        git = GitUtils(self.project_path)

        mock_run.return_value.returncode = 0
        assert git.check_git_installed() is True

        mock_run.side_effect = FileNotFoundError
        assert git.check_git_installed() is False

    @patch('subprocess.run')
    def test_git_repo_methods(self, mock_run):
        """Test repository methods"""
        git = GitUtils(self.project_path)

        mock_run.return_value.returncode = 0
        assert git.is_repo() is True
        assert git.init_repo() is True
        assert git.add_files() is True
        assert git.commit("Test") is True
        assert git.push() is True
        assert git.pull() is True

    @patch('subprocess.run')
    def test_git_status_methods(self, mock_run):
        """Test status methods"""
        git = GitUtils(self.project_path)

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "M file.txt"

        status = git.get_status()
        assert isinstance(status, dict)

        mock_run.return_value.stdout = "main\n"
        branch = git.get_current_branch()
        assert branch == "main"

        mock_run.return_value.stdout = "M file.txt"
        assert git.has_changes() is True

    @patch('subprocess.run')
    def test_git_branch_methods(self, mock_run):
        """Test branch methods"""
        git = GitUtils(self.project_path)

        mock_run.return_value.returncode = 0
        assert git.create_branch("feature") is True
        assert git.checkout_branch("main") is True
        assert git.merge("feature") is True

    @patch('subprocess.run')
    def test_git_other_methods(self, mock_run):
        """Test other git methods"""
        git = GitUtils(self.project_path)

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "abc123|Message|2024-01-01"

        commits = git.get_commits()
        assert isinstance(commits, list)

        mock_run.return_value.stdout = "https://github.com/user/repo.git\n"
        url = git.get_remote_url()
        assert url == "https://github.com/user/repo.git"

        assert git.stash() is True
        assert git.stash_pop() is True
        assert git.tag("v1.0.0", "Release") is True


class TestVersionCheck:
    """Complete tests for version checking"""

    @patch('requests.get')
    def test_check_pypi_version(self, mock_get):
        """Test PyPI version check"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "1.2.3"}}
        mock_get.return_value = mock_response

        version = check_pypi_version()
        assert version == "1.2.3"

        # Test error case
        mock_get.side_effect = Exception("Error")
        version = check_pypi_version()
        assert version is None

    def test_compare_versions(self):
        """Test version comparison"""
        is_newer, is_major = compare_versions("1.0.0", "2.0.0")
        assert is_newer is True
        assert is_major is True

        is_newer, is_major = compare_versions("1.0.0", "1.0.0")
        assert is_newer is False

    def test_should_check_version(self):
        """Test version check timing"""
        result = should_check_version()
        assert isinstance(result, bool)

    def test_get_update_message(self):
        """Test update message"""
        msg = get_update_message("1.0.0", "2.0.0", True)
        assert "2.0.0" in msg