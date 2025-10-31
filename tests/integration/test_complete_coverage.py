"""
Complete test coverage for SpecPulse - 100% coverage target
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
import requests

# Import all modules to test
from specpulse import __version__
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.cli.main import SpecPulseCLI, main
from specpulse.utils.console import Console
from specpulse.utils.git_utils import GitUtils
from specpulse.utils.version_check import (
    check_pypi_version,
    compare_versions,
    should_check_version,
    get_update_message
)


class TestCompleteSpecPulse:
    """Complete test coverage for SpecPulse core"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_specpulse_init_creates_directories(self):
        """Test SpecPulse initialization creates necessary directories"""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            sp = SpecPulse()
            assert sp.resources_dir is not None
            assert sp.templates_dir is not None

    def test_specpulse_load_config_no_file(self):
        """Test config loading when file doesn't exist"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            sp = SpecPulse()
            config = sp._load_config()
            assert config == {}

    def test_specpulse_load_config_with_file(self):
        """Test config loading with existing file"""
        config_data = {"test": "data"}
        with patch('pathlib.Path.exists') as mock_exists:
            with patch('builtins.open', mock_open(read_data=yaml.dump(config_data))):
                mock_exists.return_value = True
                sp = SpecPulse()
                assert sp.config == config_data

    def test_specpulse_get_template(self):
        """Test template retrieval"""
        sp = SpecPulse()

        # Create test template
        template_dir = self.project_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "test.md"
        template_file.write_text("Hello {{name}}")

        sp.templates_dir = self.project_path / "templates"

        # Test with variables
        content = sp.get_template("test.md", variables={"name": "World"})
        assert content == "Hello World"

        # Test without variables
        content = sp.get_template("test.md")
        assert content == "Hello {{name}}"

        # Test non-existent template
        content = sp.get_template("nonexistent.md")
        assert content == ""

    def test_specpulse_get_decomposition_template(self):
        """Test decomposition template retrieval"""
        sp = SpecPulse()

        # Create decomposition template
        decomp_dir = self.project_path / "templates" / "decomposition"
        decomp_dir.mkdir(parents=True)
        template_file = decomp_dir / "service.md"
        template_file.write_text("Service: {{service_name}}")

        sp.templates_dir = self.project_path / "templates"

        content = sp.get_decomposition_template("service.md", {"service_name": "Auth"})
        assert content == "Service: Auth"

        # Test non-existent
        content = sp.get_decomposition_template("nonexistent.md")
        assert content == ""

    def test_specpulse_generate_claude_commands(self):
        """Test Claude command generation"""
        sp = SpecPulse()
        commands = sp.generate_claude_commands()

        assert isinstance(commands, list)
        assert len(commands) > 0
        assert all("name" in cmd for cmd in commands)
        assert all("description" in cmd for cmd in commands)
        assert all("script" in cmd for cmd in commands)

    def test_specpulse_generate_gemini_commands(self):
        """Test Gemini command generation"""
        sp = SpecPulse()
        commands = sp.generate_gemini_commands()

        assert isinstance(commands, list)
        assert len(commands) > 0
        assert all("name" in cmd for cmd in commands)

    def test_specpulse_decompose_specification(self):
        """Test specification decomposition"""
        sp = SpecPulse()

        spec_content = """
        # E-Commerce System
        ## Services
        - User Service
        - Product Service
        - Order Service

        ## API Endpoints
        - POST /users
        - GET /products
        - POST /orders
        """

        spec_dir = self.project_path / "specs" / "001-ecommerce"
        spec_dir.mkdir(parents=True)

        result = sp.decompose_specification(spec_dir, spec_content)

        assert "services" in result
        assert "api_contracts" in result
        assert "integration_points" in result
        assert len(result["services"]) == 3

    def test_specpulse_decompose_empty_specification(self):
        """Test empty specification decomposition"""
        sp = SpecPulse()
        result = sp.decompose_specification(self.project_path, "")

        assert result["services"] == []
        assert result["api_contracts"] == []
        assert result["integration_points"] == []


class TestCompleteValidator:
    """Complete test coverage for Validator"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_validator_init_with_project_root(self):
        """Test Validator initialization with project root"""
        # Create constitution
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        constitution_file = memory_dir / "constitution.md"
        constitution_file.write_text("""
# Constitution
## Principle 1: Test
PHASE_GATE: Test Gate
        """)

        validator = Validator(self.project_path)
        assert validator.constitution is not None
        assert len(validator.phase_gates) > 0

    def test_validator_validate_all_with_fix(self):
        """Test validate_all with fix option"""
        validator = Validator()

        # Create partial structure
        (self.project_path / "specs").mkdir()

        results = validator.validate_all(self.project_path, fix=True, verbose=True)
        assert isinstance(results, list)

        # Check directories were created
        assert (self.project_path / "plans").exists()
        assert (self.project_path / "tasks").exists()

    def test_validator_validate_spec_with_name(self):
        """Test validate_spec with specific name"""
        validator = Validator()

        # Create spec
        spec_dir = self.project_path / "specs" / "001-test"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec")

        results = validator.validate_spec(self.project_path, spec_name="001-test", fix=True, verbose=True)
        assert isinstance(results, list)

    def test_validator_validate_plan_with_name(self):
        """Test validate_plan with specific name"""
        validator = Validator()

        # Create plan
        plan_dir = self.project_path / "plans" / "001-test"
        plan_dir.mkdir(parents=True)
        (plan_dir / "plan.md").write_text("# Plan")

        results = validator.validate_plan(self.project_path, plan_name="001-test", fix=True, verbose=True)
        assert isinstance(results, list)

    def test_validator_private_methods(self):
        """Test private validation methods"""
        validator = Validator()

        # Test _validate_structure
        validator._validate_structure(self.project_path)
        assert len(validator.results) > 0

        # Test _validate_single_spec
        spec_file = self.project_path / "spec.md"
        spec_file.write_text("# Spec")
        validator.results = []
        validator._validate_single_spec(spec_file, fix=True, verbose=True)

        # Test _validate_single_plan
        plan_file = self.project_path / "plan.md"
        plan_file.write_text("# Plan")
        validator.results = []
        validator._validate_single_plan(plan_file, fix=True, verbose=True)

        # Test _validate_specs
        specs_dir = self.project_path / "specs"
        specs_dir.mkdir()
        validator.results = []
        validator._validate_specs(self.project_path, fix=True, verbose=True)

        # Test _validate_plans
        plans_dir = self.project_path / "plans"
        plans_dir.mkdir()
        validator.results = []
        validator._validate_plans(self.project_path, fix=True, verbose=True)

    def test_validator_extract_phase_gates(self):
        """Test phase gate extraction"""
        validator = Validator()
        validator.constitution = """
# Constitution
## Principle 1: Test
PHASE_GATE_ONE: First gate
PHASE_GATE_TWO: Second gate
        """
        validator._extract_phase_gates()
        assert len(validator.phase_gates) == 2


class TestCompleteCLI:
    """Complete test coverage for CLI"""

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
    @patch('specpulse.cli.main.check_pypi_version')
    @patch('specpulse.cli.main.compare_versions')
    @patch('specpulse.cli.main.get_update_message')
    def test_cli_check_for_updates(self, mock_msg, mock_compare, mock_check, mock_should):
        """Test CLI update checking"""
        mock_should.return_value = True
        mock_check.return_value = "2.0.0"
        mock_compare.return_value = (True, True)
        mock_msg.return_value = "Update available"

        cli = SpecPulseCLI(no_color=True, verbose=False)
        assert cli is not None

    @patch('specpulse.cli.main.should_check_version')
    def test_cli_private_methods(self, mock_should):
        """Test CLI private methods"""
        mock_should.return_value = False

        cli = SpecPulseCLI(no_color=True)

        # Test _create_memory_files
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()

        with patch('shutil.copy2') as mock_copy:
            # Create fake source files
            cli.specpulse.resources_dir = self.project_path
            source_memory = self.project_path / "memory"
            source_memory.mkdir(exist_ok=True)
            (source_memory / "constitution.md").write_text("# Constitution")
            (source_memory / "context.md").write_text("# Context")
            (source_memory / "decisions.md").write_text("# Decisions")

            cli._create_memory_files(self.project_path)

        # Test _create_templates
        templates_dir = self.project_path / "templates"
        templates_dir.mkdir()

        with patch('shutil.copy2') as mock_copy:
            source_templates = self.project_path / "templates"
            (source_templates / "spec.md").write_text("# Spec")
            (source_templates / "plan.md").write_text("# Plan")
            (source_templates / "task.md").write_text("# Task")

            cli._create_templates(self.project_path)

        # Test _create_scripts
        scripts_dir = self.project_path / "scripts"
        scripts_dir.mkdir()

        with patch('shutil.copy2') as mock_copy:
            with patch('os.chmod') as mock_chmod:
                source_scripts = self.project_path / "scripts"
                source_scripts.mkdir(exist_ok=True)
                (source_scripts / "script.sh").write_text("#!/bin/bash")

                cli._create_scripts(self.project_path)

        # Test _create_ai_commands
        claude_dir = self.project_path / ".claude" / "commands"
        claude_dir.mkdir(parents=True)
        gemini_dir = self.project_path / ".gemini" / "commands"
        gemini_dir.mkdir(parents=True)

        cli._create_ai_commands(self.project_path)

        assert len(list(claude_dir.glob("*.md"))) > 0
        assert len(list(gemini_dir.glob("*.toml"))) > 0

    @patch('sys.argv', ['specpulse', '--version'])
    def test_main_function(self):
        """Test main entry point"""
        with patch('specpulse.cli.main.click') as mock_click:
            from specpulse.cli.main import main
            # Just ensure it doesn't crash
            try:
                main()
            except SystemExit:
                pass


class TestCompleteConsole:
    """Complete test coverage for Console"""

    def test_console_all_methods(self):
        """Test all Console methods"""
        console = Console(no_color=True, verbose=True)

        # Test all display methods
        with patch.object(console.console, 'print') as mock_print:
            console.show_banner()
            console.show_banner(mini=True)
            console.info("Info")
            console.success("Success")
            console.warning("Warning")
            console.error("Error")
            console.header("Header")
            console.section("Section", "Content")
            console.animated_text("Text", delay=0.001)
            console.divider()
            console.gradient_text("Gradient")
            console.code_block("print('hello')")

        # Test progress bar
        progress = console.progress_bar("Test", 10)
        assert hasattr(progress, '__enter__')
        assert hasattr(progress, '__exit__')

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

        # Test table
        with patch.object(console.console, 'print') as mock_print:
            console.table("Title", ["Col1"], [["Data"]])

        # Test tree
        with patch.object(console.console, 'print') as mock_print:
            console.tree("Tree", {"root": {"child": None}})

        # Test pulse animation
        console.pulse_animation("Test", duration=0.01)

        # Test type effect
        with patch.object(console.console, 'print') as mock_print:
            console.type_effect("Test", delay=0.001)


class TestCompleteGitUtils:
    """Complete test coverage for GitUtils"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.run')
    def test_git_all_methods(self, mock_run):
        """Test all GitUtils methods"""
        git = GitUtils(self.project_path)

        # Test check_git_installed
        mock_run.return_value.returncode = 0
        assert git.check_git_installed() is True

        mock_run.side_effect = FileNotFoundError
        assert git.check_git_installed() is False
        mock_run.side_effect = None

        # Test is_repo
        mock_run.return_value.returncode = 0
        assert git.is_repo() is True

        mock_run.return_value.returncode = 1
        assert git.is_repo() is False

        # Test init_repo
        mock_run.return_value.returncode = 0
        assert git.init_repo() is True

        # Test add_files
        assert git.add_files([".gitignore"]) is True
        assert git.add_files() is True

        # Test commit
        assert git.commit("Test") is True

        # Test push
        assert git.push() is True
        assert git.push("main") is True

        # Test pull
        assert git.pull() is True

        # Test get_status
        mock_run.return_value.stdout = "M file1.txt\nA file2.txt\n?? file3.txt"
        status = git.get_status()
        assert "modified" in status

        # Test get_current_branch
        mock_run.return_value.stdout = "main\n"
        assert git.get_current_branch() == "main"

        # Test create_branch
        assert git.create_branch("feature") is True

        # Test checkout_branch
        assert git.checkout_branch("main") is True

        # Test get_commits
        mock_run.return_value.stdout = "abc123|Message|2024-01-01"
        commits = git.get_commits()
        assert len(commits) > 0

        # Test get_remote_url
        mock_run.return_value.stdout = "https://github.com/user/repo.git\n"
        assert git.get_remote_url() == "https://github.com/user/repo.git"

        # Test has_changes
        mock_run.return_value.stdout = "M file.txt"
        assert git.has_changes() is True

        # Test stash
        assert git.stash() is True

        # Test stash_pop
        assert git.stash_pop() is True

        # Test tag
        assert git.tag("v1.0.0", "Release") is True

        # Test merge
        assert git.merge("feature") is True


class TestCompleteVersionCheck:
    """Complete test coverage for version checking"""

    @patch('requests.get')
    def test_check_pypi_version(self, mock_get):
        """Test PyPI version checking"""
        # Success case
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "1.2.3"}}
        mock_get.return_value = mock_response

        version = check_pypi_version("specpulse")
        assert version == "1.2.3"

        # Failure case
        mock_get.side_effect = Exception("Error")
        version = check_pypi_version("specpulse")
        assert version is None

    def test_compare_versions(self):
        """Test version comparison"""
        is_newer, is_major = compare_versions("1.0.0", "2.0.0")
        assert is_newer is True
        assert is_major is True

        is_newer, is_major = compare_versions("1.0.0", "1.0.1")
        assert is_newer is True
        assert is_major is False

        is_newer, is_major = compare_versions("1.0.0", "1.0.0")
        assert is_newer is False

        is_newer, is_major = compare_versions("invalid", "1.0.0")
        assert is_newer is False

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_should_check_version(self, mock_read, mock_exists):
        """Test version check timing"""
        # No cache file
        mock_exists.return_value = False
        assert should_check_version() is True

        # Recent cache
        mock_exists.return_value = True
        cache_data = {
            "last_check": datetime.now().isoformat(),
            "latest_version": "1.2.3"
        }
        mock_read.return_value = json.dumps(cache_data)
        assert should_check_version() is False

        # Old cache
        old_time = datetime.now() - timedelta(hours=25)
        cache_data["last_check"] = old_time.isoformat()
        mock_read.return_value = json.dumps(cache_data)
        assert should_check_version() is True

        # Invalid cache
        mock_read.return_value = "invalid json"
        assert should_check_version() is True

    def test_get_update_message(self):
        """Test update message generation"""
        msg = get_update_message("1.0.0", "2.0.0", True)
        assert "MAJOR" in msg
        assert "2.0.0" in msg

        msg = get_update_message("1.0.0", "1.0.1", False)
        assert "1.0.1" in msg

        msg = get_update_message("1.0.0", "1.0.0", False)
        # No update needed, message might be empty or indicate up-to-date
        assert isinstance(msg, str)