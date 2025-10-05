"""
Complete test suite for 100% coverage and success rate
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, call, PropertyMock
import tempfile
import shutil
import yaml
import json
import subprocess
from datetime import datetime, timedelta
from io import StringIO
import sys
import os

from specpulse.cli.main import SpecPulseCLI
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
from specpulse import __version__


class TestSpecPulseComplete:
    """Complete test suite for SpecPulse core functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        # Create .specpulse directory with config
        config_dir = self.project_path / ".specpulse"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.yaml"
        config_file.write_text(yaml.dump({
            "project_name": "test-project",
            "version": "1.0.0"
        }))
        # Change to temp directory
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_specpulse_initialization(self):
        """Test SpecPulse initialization"""
        sp = SpecPulse()
        assert sp is not None
        assert sp.resources_dir.exists()

    def test_specpulse_all_templates(self):
        """Test all template getter methods"""
        sp = SpecPulse()

        # Test all template methods
        assert isinstance(sp.get_spec_template(), str)
        assert isinstance(sp.get_plan_template(), str)
        assert isinstance(sp.get_task_template(), str)
        assert isinstance(sp.get_decomposition_template(), str)
        assert isinstance(sp.get_service_plan_template(), str)
        assert isinstance(sp.get_integration_plan_template(), str)
        assert isinstance(sp.get_api_contract_template(), str)
        assert isinstance(sp.get_interface_template(), str)

        # Verify template content
        assert "SPECIFICATION" in sp.get_spec_template()
        assert "PLAN" in sp.get_plan_template()
        assert "TASK" in sp.get_task_template()

    def test_specpulse_all_commands(self):
        """Test all command getter methods"""
        sp = SpecPulse()

        # Claude commands
        assert isinstance(sp.get_claude_pulse_command(), str)
        assert isinstance(sp.get_claude_spec_command(), str)
        assert isinstance(sp.get_claude_plan_command(), str)
        assert isinstance(sp.get_claude_task_command(), str)

        # Gemini commands
        assert isinstance(sp.get_gemini_pulse_command(), str)
        assert isinstance(sp.get_gemini_spec_command(), str)
        assert isinstance(sp.get_gemini_plan_command(), str)
        assert isinstance(sp.get_gemini_task_command(), str)

    def test_specpulse_project_initialization(self):
        """Test project initialization"""
        sp = SpecPulse()

        # Test directory creation
        new_project = self.project_path / "new-project"
        sp.initialize_project(new_project)

        assert new_project.exists()
        assert (new_project / "specs").exists()
        assert (new_project / "plans").exists()
        assert (new_project / "tasks").exists()
        assert (new_project / "memory").exists()
        assert (new_project / "templates").exists()
        assert (new_project / "scripts").exists()

    def test_specpulse_create_spec(self):
        """Test specification creation"""
        sp = SpecPulse()
        specs_dir = self.project_path / "specs" / "001-feature"
        specs_dir.mkdir(parents=True)

        sp.create_spec(specs_dir, "001", "Test Feature")

        spec_files = list(specs_dir.glob("spec-*.md"))
        assert len(spec_files) > 0

    def test_specpulse_create_plan(self):
        """Test plan creation"""
        sp = SpecPulse()
        plans_dir = self.project_path / "plans" / "001-feature"
        plans_dir.mkdir(parents=True)

        sp.create_plan(plans_dir, "001")

        plan_files = list(plans_dir.glob("plan-*.md"))
        assert len(plan_files) > 0

    def test_specpulse_create_tasks(self):
        """Test task creation"""
        sp = SpecPulse()
        tasks_dir = self.project_path / "tasks" / "001-feature"
        tasks_dir.mkdir(parents=True)

        sp.create_tasks(tasks_dir, "001")

        task_files = list(tasks_dir.glob("task-*.md"))
        assert len(task_files) > 0

    @patch('shutil.copy2')
    def test_specpulse_copy_resources(self, mock_copy):
        """Test resource copying"""
        sp = SpecPulse()
        sp.copy_resources(self.project_path)

        # Verify copy was called
        assert mock_copy.called


class TestValidatorComplete:
    """Complete test suite for Validator"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.validator = Validator()

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_validator_initialization(self):
        """Test Validator initialization"""
        v = Validator()
        assert v is not None
        assert v.constitution is None

    def test_validator_load_constitution(self):
        """Test loading constitution"""
        # Create constitution file
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir(parents=True)
        constitution_file = memory_dir / "constitution.md"
        constitution_file.write_text("# Constitution\n## Principle 1: Test")

        loaded = self.validator.load_constitution(self.project_path)
        assert loaded is True
        assert self.validator.constitution is not None

    def test_validator_validate_spec_file(self):
        """Test spec file validation"""
        spec_file = self.project_path / "spec.md"
        spec_file.write_text("# Specification\n## Requirements\n- Test requirement")

        result = self.validator.validate_spec_file(spec_file)
        assert result["status"] == "valid"

    def test_validator_validate_plan_file(self):
        """Test plan file validation"""
        plan_file = self.project_path / "plan.md"
        plan_file.write_text("# Plan\n## Architecture\n## Phases\n## Technology Stack")

        result = self.validator.validate_plan_file(plan_file)
        assert result["status"] == "valid"

    def test_validator_validate_task_file(self):
        """Test task file validation"""
        task_file = self.project_path / "task.md"
        task_file.write_text("# Tasks\n## T001: Test Task\n- Complexity: Simple")

        result = self.validator.validate_task_file(task_file)
        assert result["status"] == "valid"

    def test_validator_validate_all(self):
        """Test validate all method"""
        results = self.validator.validate_all(self.project_path)
        assert isinstance(results, list)

    def test_validator_validate_sdd_compliance(self):
        """Test SDD compliance validation"""
        results = self.validator.validate_sdd_compliance(self.project_path)
        assert isinstance(results, list)

    def test_validator_validate_spec(self):
        """Test spec validation"""
        results = self.validator.validate_spec(self.project_path)
        assert isinstance(results, list)

    def test_validator_validate_plan(self):
        """Test plan validation"""
        results = self.validator.validate_plan(self.project_path)
        assert isinstance(results, list)

    def test_validator_validate_task(self):
        """Test task validation"""
        results = self.validator.validate_task(self.project_path)
        assert isinstance(results, list)

    def test_validator_validate_sdd_principles(self):
        """Test SDD principles validation"""
        content = "# Spec\nFollowing Principle 1: Specification First"
        result = self.validator.validate_sdd_principles(content)
        assert result["status"] == "compliant"

    def test_validator_check_phase_gate(self):
        """Test phase gate checking"""
        # Test different gates
        assert self.validator.check_phase_gate("specification", {"spec_complete": True})
        assert not self.validator.check_phase_gate("specification", {"spec_complete": False})

        assert self.validator.check_phase_gate("planning", {"plan_complete": True})
        assert not self.validator.check_phase_gate("planning", {"plan_complete": False})

        assert self.validator.check_phase_gate("test-first", {"tests_written": True})
        assert not self.validator.check_phase_gate("test-first", {"tests_written": False})

        assert self.validator.check_phase_gate("implementation", {"ready": True})
        assert not self.validator.check_phase_gate("implementation", {"ready": False})

        # Unknown gate should return False
        assert not self.validator.check_phase_gate("unknown", {})

    def test_validator_validate_all_project(self):
        """Test complete project validation"""
        result = self.validator.validate_all_project(self.project_path)
        assert isinstance(result, dict)
        assert "specs" in result
        assert "plans" in result
        assert "tasks" in result
        assert "sdd_compliance" in result

    def test_validator_fix_issues(self):
        """Test fixing validation issues"""
        issues = [
            {"type": "missing_section", "file": "test.md", "section": "Requirements"}
        ]

        # Create test file
        test_file = self.project_path / "test.md"
        test_file.write_text("# Test")

        fixed = self.validator.fix_issues(issues, self.project_path)
        assert fixed > 0

        # Verify fix was applied
        content = test_file.read_text()
        assert "## Requirements" in content


class TestCLIComplete:
    """Complete test suite for CLI"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        # Create .specpulse directory with config
        config_dir = self.project_path / ".specpulse"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.yaml"
        config_file.write_text(yaml.dump({
            "project_name": "test-project",
            "version": "1.0.0"
        }))
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_initialization(self, mock_should_check):
        """Test CLI initialization"""
        mock_should_check.return_value = False

        cli = SpecPulseCLI(no_color=True, verbose=False)
        assert cli.console is not None
        assert cli.specpulse is not None
        assert cli.validator is not None

    @patch('specpulse.utils.version_check.should_check_version')
    @patch('specpulse.utils.version_check.check_pypi_version')
    @patch('specpulse.utils.version_check.compare_versions')
    @patch('specpulse.utils.version_check.get_update_message')
    def test_cli_with_version_check(self, mock_get_msg, mock_compare, mock_check_pypi, mock_should_check):
        """Test CLI with version check"""
        mock_should_check.return_value = True
        mock_check_pypi.return_value = "2.0.0"
        mock_compare.return_value = (True, True)
        mock_get_msg.return_value = "Update available"

        cli = SpecPulseCLI(no_color=True, verbose=True)
        assert cli is not None

    @patch('specpulse.utils.version_check.should_check_version')
    @patch('shutil.copy2')
    def test_cli_init_new_project(self, mock_copy, mock_should_check):
        """Test initializing new project"""
        mock_should_check.return_value = False

        cli = SpecPulseCLI(no_color=True)

        # Create a new project in temp dir
        project_name = "test-new-project"
        result = cli.init(project_name)

        assert result is True
        assert (self.project_path / project_name).exists()
        assert (self.project_path / project_name / ".specpulse").exists()

    @patch('specpulse.utils.version_check.should_check_version')
    @patch('shutil.copy2')
    def test_cli_init_here(self, mock_copy, mock_should_check):
        """Test init in current directory"""
        mock_should_check.return_value = False

        cli = SpecPulseCLI(no_color=True)

        result = cli.init(here=True)

        assert result is True
        assert (self.project_path / "specs").exists()
        assert (self.project_path / "plans").exists()

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_init_invalid_name(self, mock_should_check):
        """Test init with invalid project name"""
        mock_should_check.return_value = False

        cli = SpecPulseCLI(no_color=True)
        result = cli.init("invalid@name!")

        assert result is False

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_validate(self, mock_should_check):
        """Test project validation"""
        mock_should_check.return_value = False

        # Create basic structure
        (self.project_path / "specs").mkdir()
        (self.project_path / "plans").mkdir()

        cli = SpecPulseCLI(no_color=True)
        result = cli.validate()

        assert isinstance(result, bool)

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_validate_with_fix(self, mock_should_check):
        """Test validation with fix option"""
        mock_should_check.return_value = False

        cli = SpecPulseCLI(no_color=True)
        result = cli.validate(fix=True, verbose=True)

        assert isinstance(result, bool)

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_list_specs(self, mock_should_check):
        """Test listing specifications"""
        mock_should_check.return_value = False

        # Create specs
        specs_dir = self.project_path / "specs"
        specs_dir.mkdir()
        (specs_dir / "001-auth").mkdir()
        (specs_dir / "002-payments").mkdir()

        cli = SpecPulseCLI(no_color=True)
        cli.list_specs()

        # Should not raise exception

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_doctor(self, mock_should_check):
        """Test doctor command"""
        mock_should_check.return_value = False

        # Create complete structure
        for dir_name in ["memory", "templates", "scripts", "specs", ".claude", ".gemini"]:
            (self.project_path / dir_name).mkdir(parents=True)

        cli = SpecPulseCLI(no_color=True)
        result = cli.doctor()

        assert result is True

    @patch('specpulse.utils.version_check.should_check_version')
    @patch('subprocess.run')
    def test_cli_update(self, mock_run, mock_should_check):
        """Test update command"""
        mock_should_check.return_value = False

        # First test successful update
        mock_run.return_value = MagicMock(returncode=0)

        cli = SpecPulseCLI(no_color=True)
        result = cli.update()

        assert result is True

        # Test failed update
        mock_run.return_value = MagicMock(returncode=1)
        result = cli.update()

        assert result is False

    @patch('specpulse.utils.version_check.should_check_version')
    @patch('specpulse.utils.git_utils.GitUtils.is_git_repo')
    @patch('specpulse.utils.git_utils.GitUtils.get_status')
    def test_cli_sync(self, mock_status, mock_is_repo, mock_should_check):
        """Test project sync"""
        mock_should_check.return_value = False
        mock_is_repo.return_value = True
        mock_status.return_value = "clean"

        # Create memory directory
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "context.md").write_text("# Context")

        cli = SpecPulseCLI(no_color=True)
        result = cli.sync()

        assert result is True

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_decompose(self, mock_should_check):
        """Test specification decomposition"""
        mock_should_check.return_value = False

        # Create spec structure
        spec_dir = self.project_path / "specs" / "001-feature"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Feature Spec")

        cli = SpecPulseCLI(no_color=True)
        result = cli.decompose("001")

        assert result is True

    @patch('specpulse.utils.version_check.should_check_version')
    def test_cli_create_manifest(self, mock_should_check):
        """Test manifest creation"""
        mock_should_check.return_value = False

        cli = SpecPulseCLI(no_color=True)
        cli._create_manifest(self.project_path, "test-project")

        manifest_file = self.project_path / ".specpulse.yaml"
        assert manifest_file.exists()


class TestConsoleComplete:
    """Complete test suite for Console utilities"""

    def test_console_initialization(self):
        """Test Console initialization"""
        console = Console(no_color=False, verbose=True)
        assert console is not None

    def test_console_messages(self):
        """Test console message methods"""
        console = Console(no_color=True)

        # These should not raise exceptions
        console.info("Test info")
        console.success("Test success")
        console.warning("Test warning")
        console.error("Test error")
        console.header("Test header")
        console.section("Test section", "Content")

    def test_console_interactive(self):
        """Test interactive console methods"""
        console = Console(no_color=True)

        # Test prompt with mock input
        with patch('builtins.input', return_value="test"):
            result = console.prompt("Enter value")
            assert result == "test"

        # Test confirm
        with patch('builtins.input', return_value="y"):
            result = console.confirm("Confirm?")
            assert result is True

        with patch('builtins.input', return_value="n"):
            result = console.confirm("Confirm?")
            assert result is False

    def test_console_display(self):
        """Test console display methods"""
        console = Console(no_color=True)

        # Test table
        console.table("Title", ["Col1", "Col2"], [["Row1", "Data1"]])

        # Test tree
        console.tree("Tree", {"item1": {"sub1": "value"}})

        # Test code block
        console.code_block("print('test')", "python")

        # Test status panel
        console.status_panel("Status", [("Key", "Value")])

    def test_console_animations(self):
        """Test console animation methods"""
        console = Console(no_color=True)

        # These should not raise exceptions
        console.animated_text("Test")
        console.animated_success("Success")
        console.pulse_animation("Pulse", 0.01)
        console.rocket_launch("Launch")
        console.celebration()

    def test_console_formatting(self):
        """Test console formatting methods"""
        console = Console(no_color=True)

        # Test divider
        console.divider()

        # Test gradient text
        console.gradient_text("Test")

        # Test validation results
        results = {"test1": True, "test2": False}
        console.validation_results(results)

        # Test feature showcase
        features = [{"name": "Feature", "description": "Desc"}]
        console.feature_showcase(features)

    def test_console_progress_bar(self):
        """Test progress bar"""
        console = Console(no_color=True)

        with console.progress_bar("Test", 10) as progress:
            task = progress.add_task("Task", total=10)
            progress.update(task, advance=5)

    def test_console_spinner(self):
        """Test spinner"""
        console = Console(no_color=True)

        with console.spinner("Loading"):
            pass  # Spinner context


class TestGitUtilsComplete:
    """Complete test suite for GitUtils"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.git_utils = GitUtils(Path(self.temp_dir))

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.run')
    def test_git_check_installed(self, mock_run):
        """Test checking if git is installed"""
        mock_run.return_value = MagicMock(returncode=0)

        result = self.git_utils.check_git_installed()
        assert result is True

        mock_run.return_value = MagicMock(returncode=1)
        result = self.git_utils.check_git_installed()
        assert result is False

    @patch('subprocess.run')
    def test_git_is_repo(self, mock_run):
        """Test checking if directory is a git repo"""
        mock_run.return_value = MagicMock(returncode=0, stdout="true")

        result = self.git_utils.is_git_repo()
        assert result is True

        mock_run.return_value = MagicMock(returncode=1)
        result = self.git_utils.is_git_repo()
        assert result is False

    @patch('subprocess.run')
    def test_git_init_repo(self, mock_run):
        """Test initializing git repo"""
        mock_run.return_value = MagicMock(returncode=0)

        result = self.git_utils.init_repo()
        assert result is True

    @patch('subprocess.run')
    def test_git_branch_operations(self, mock_run):
        """Test branch operations"""
        mock_run.return_value = MagicMock(returncode=0, stdout="main")

        # Get current branch
        branch = self.git_utils.get_current_branch()
        assert branch == "main"

        # Create branch
        result = self.git_utils.create_branch("feature")
        assert result is True

        # Checkout branch
        result = self.git_utils.checkout_branch("feature")
        assert result is True

        # Get branches
        mock_run.return_value = MagicMock(returncode=0, stdout="* main\n  feature")
        branches = self.git_utils.get_branches()
        assert isinstance(branches, list)

    @patch('subprocess.run')
    def test_git_file_operations(self, mock_run):
        """Test file operations"""
        mock_run.return_value = MagicMock(returncode=0)

        # Add files
        result = self.git_utils.add_files()
        assert result is True

        # Commit
        result = self.git_utils.commit("Test commit")
        assert result is True

        # Get status
        mock_run.return_value = MagicMock(returncode=0, stdout="M file.txt")
        status = self.git_utils.get_status()
        assert status is not None

        # Has changes
        result = self.git_utils.has_changes()
        assert result is True

    @patch('subprocess.run')
    def test_git_history(self, mock_run):
        """Test history operations"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="commit1\ncommit2"
        )

        # Get log
        log = self.git_utils.get_log()
        assert isinstance(log, list)
        assert len(log) == 2

    @patch('subprocess.run')
    def test_git_stash(self, mock_run):
        """Test stash operations"""
        mock_run.return_value = MagicMock(returncode=0)

        # Stash changes
        result = self.git_utils.stash_changes()
        assert result is True

        # Apply stash
        result = self.git_utils.apply_stash()
        assert result is True

    @patch('subprocess.run')
    def test_git_remote(self, mock_run):
        """Test remote operations"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="https://github.com/user/repo.git"
        )

        # Get remote URL
        url = self.git_utils.get_remote_url()
        assert url == "https://github.com/user/repo.git"

        # Push
        mock_run.return_value = MagicMock(returncode=0)
        result = self.git_utils.push()
        assert result is True

        # Pull
        result = self.git_utils.pull()
        assert result is True

    @patch('subprocess.run')
    def test_git_diff(self, mock_run):
        """Test diff operations"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="diff content"
        )

        # Get diff
        diff = self.git_utils.get_diff()
        assert diff == "diff content"

        # Get staged diff
        diff = self.git_utils.get_diff(staged=True)
        assert diff == "diff content"

    @patch('subprocess.run')
    def test_git_tags(self, mock_run):
        """Test tag operations"""
        mock_run.return_value = MagicMock(returncode=0)

        # Create tag
        result = self.git_utils.tag("v1.0.0")
        assert result is True

        # Get tags
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="v1.0.0\nv1.0.1"
        )
        tags = self.git_utils.get_tags()
        assert isinstance(tags, list)
        assert len(tags) == 2


class TestVersionCheckComplete:
    """Complete test suite for version checking"""

    def test_compare_versions(self):
        """Test version comparison"""
        # Equal versions
        is_newer, is_major = compare_versions("1.0.0", "1.0.0")
        assert is_newer is False
        assert is_major is False

        # Patch difference
        is_newer, is_major = compare_versions("1.0.0", "1.0.1")
        assert is_newer is True
        assert is_major is False

        # Minor difference
        is_newer, is_major = compare_versions("1.0.0", "1.1.0")
        assert is_newer is True
        assert is_major is False

        # Major difference
        is_newer, is_major = compare_versions("1.0.0", "2.0.0")
        assert is_newer is True
        assert is_major is True

        # Older version
        is_newer, is_major = compare_versions("2.0.0", "1.0.0")
        assert is_newer is False
        assert is_major is False

        # Invalid versions
        is_newer, is_major = compare_versions("invalid", "1.0.0")
        assert is_newer is False
        assert is_major is False

    def test_should_check_version(self):
        """Test version check timing"""
        result = should_check_version()
        assert isinstance(result, bool)

    @patch('requests.get')
    def test_check_pypi_version(self, mock_get):
        """Test PyPI version checking"""
        # Successful check
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "1.2.3"}}
        mock_get.return_value = mock_response

        version = check_pypi_version("specpulse")
        assert version == "1.2.3"

        # Failed check
        mock_get.side_effect = Exception("Network error")
        version = check_pypi_version("specpulse")
        assert version is None

        # 404 response
        mock_get.side_effect = None
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        version = check_pypi_version("nonexistent")
        assert version is None

    def test_get_update_message(self):
        """Test update message generation"""
        # Patch update
        msg = get_update_message("1.0.0", "1.0.1", False)
        assert "1.0.1" in msg

        # Major update
        msg = get_update_message("1.0.0", "2.0.0", True)
        if isinstance(msg, tuple):
            msg = msg[0]  # Extract message from tuple
        assert "2.0.0" in msg

        # No update
        msg = get_update_message("1.0.0", "1.0.0", False)
        assert isinstance(msg, (str, tuple))


class TestIntegrationComplete:
    """Complete integration tests"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        # Create .specpulse directory with config
        config_dir = self.project_path / ".specpulse"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.yaml"
        config_file.write_text(yaml.dump({
            "project_name": "test-project",
            "version": "1.0.0"
        }))
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('specpulse.utils.version_check.should_check_version')
    @patch('shutil.copy2')
    def test_complete_workflow(self, mock_copy, mock_should_check):
        """Test complete SpecPulse workflow"""
        mock_should_check.return_value = False

        # 1. Initialize CLI
        cli = SpecPulseCLI(no_color=True)

        # 2. Initialize project
        result = cli.init(here=True)
        assert result is True

        # 3. Create specification
        specs_dir = self.project_path / "specs" / "001-auth"
        specs_dir.mkdir(parents=True)
        spec_file = specs_dir / "spec.md"
        spec_file.write_text("# Auth Spec\n## Requirements\n- User login")

        # 4. Validate project
        result = cli.validate()
        assert isinstance(result, bool)

        # 5. Run doctor
        result = cli.doctor()
        assert isinstance(result, bool)

        # 6. List specs
        cli.list_specs()

        # 7. Decompose spec
        result = cli.decompose("001")
        assert result is True

    def test_validator_workflow(self):
        """Test validator workflow"""
        # Create project structure
        self._create_project_structure()

        # Initialize validator
        validator = Validator()

        # Validate all
        results = validator.validate_all(self.project_path)
        assert isinstance(results, list)

        # Check SDD compliance
        results = validator.validate_sdd_compliance(self.project_path)
        assert isinstance(results, list)

        # Validate complete project
        result = validator.validate_all_project(self.project_path)
        assert isinstance(result, dict)

    def test_specpulse_workflow(self):
        """Test SpecPulse core workflow"""
        sp = SpecPulse()

        # Initialize project
        sp.initialize_project(self.project_path)

        # Create spec
        specs_dir = self.project_path / "specs" / "001-feature"
        specs_dir.mkdir(parents=True)
        sp.create_spec(specs_dir, "001", "Test Feature")

        # Create plan
        plans_dir = self.project_path / "plans" / "001-feature"
        plans_dir.mkdir(parents=True)
        sp.create_plan(plans_dir, "001")

        # Create tasks
        tasks_dir = self.project_path / "tasks" / "001-feature"
        tasks_dir.mkdir(parents=True)
        sp.create_tasks(tasks_dir, "001")

        # Verify all created
        assert list(specs_dir.glob("*.md"))
        assert list(plans_dir.glob("*.md"))
        assert list(tasks_dir.glob("*.md"))

    def _create_project_structure(self):
        """Helper to create project structure"""
        directories = [
            "specs", "plans", "tasks", "memory",
            "templates", "scripts", ".claude", ".gemini"
        ]

        for dir_name in directories:
            (self.project_path / dir_name).mkdir(parents=True, exist_ok=True)

        # Add constitution
        constitution = self.project_path / "memory" / "constitution.md"
        constitution.write_text("""
# Constitution
## Principle 1: Specification First
## Principle 2: Incremental Planning
## Principle 3: Task Decomposition
## Principle 4: Traceable Implementation
## Principle 5: Continuous Validation
## Principle 6: Quality Assurance
## Principle 7: Architecture Documentation
## Principle 8: Iterative Refinement
## Principle 9: Stakeholder Alignment
        """)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])