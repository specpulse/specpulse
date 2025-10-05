"""
Tests for CLI module
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import os

from specpulse.cli.main import SpecPulseCLI


class TestSpecPulseCLI:
    """Test SpecPulseCLI functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_cli_initialization(self):
        """Test CLI initialization"""
        cli = SpecPulseCLI(no_color=True, verbose=False)
        assert cli.console is not None
        assert cli.specpulse is not None

    @patch('specpulse.cli.main.Console')
    def test_cli_initialization_with_console(self, mock_console_class):
        """Test CLI initialization with console parameters"""
        cli = SpecPulseCLI(no_color=False, verbose=True)
        mock_console_class.assert_called_once_with(no_color=False, verbose=True)

    def test_init_new_project(self):
        """Test initializing new project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / "test-project"

            cli = SpecPulseCLI(no_color=True)
            cli._create_memory_files = MagicMock()
            cli._create_templates = MagicMock()
            cli._create_scripts = MagicMock()
            cli._create_ai_commands = MagicMock()
            cli._create_manifest = MagicMock()

            # Change to temp directory for test
            original_cwd = Path.cwd()
            os.chdir(tmpdir)

            try:
                result = cli.init("test-project")
                assert result is True
                assert project_path.exists()
                assert (project_path / ".specpulse").exists()
                cli._create_memory_files.assert_called_once()
                cli._create_templates.assert_called_once()
                cli._create_scripts.assert_called_once()
                cli._create_ai_commands.assert_called_once()
                cli._create_manifest.assert_called_once()
            finally:
                os.chdir(original_cwd)

    @patch('pathlib.Path.exists')
    def test_init_existing_project(self, mock_exists):
        """Test init with existing project"""
        mock_exists.return_value = True

        cli = SpecPulseCLI(no_color=True)
        result = cli.init("existing-project")

        assert result is False

    @patch('pathlib.Path.cwd')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    def test_init_here(self, mock_mkdir, mock_exists, mock_cwd):
        """Test init in current directory"""
        mock_cwd.return_value = self.project_path
        mock_exists.return_value = False

        cli = SpecPulseCLI(no_color=True)
        cli._create_memory_files = MagicMock()
        cli._create_templates = MagicMock()
        cli._create_scripts = MagicMock()
        cli._create_ai_commands = MagicMock()
        cli._create_manifest = MagicMock()

        result = cli.init(here=True)

        assert result is True

    def test_create_manifest(self):
        """Test manifest creation"""
        cli = SpecPulseCLI(no_color=True)

        cli._create_manifest(self.project_path, "test-project")

        manifest_file = self.project_path / ".specpulse.yaml"
        assert manifest_file.exists()

        content = manifest_file.read_text()
        assert "test-project" in content
        assert "version" in content

    @patch('specpulse.cli.main.Validator')
    def test_validate(self, mock_validator_class):
        """Test project validation"""
        mock_validator = MagicMock()
        mock_validator.validate_all.return_value = []
        mock_validator_class.return_value = mock_validator

        cli = SpecPulseCLI(no_color=True)
        result = cli.validate()

        assert result is True
        mock_validator.validate_all.assert_called_once()

    @patch('specpulse.cli.main.Validator')
    def test_validate_with_issues(self, mock_validator_class):
        """Test validation with issues"""
        mock_validator = MagicMock()
        mock_validator.validate_all.return_value = [
            {"status": "error", "message": "Test error"}
        ]
        mock_validator_class.return_value = mock_validator

        cli = SpecPulseCLI(no_color=True)
        result = cli.validate()

        assert result is False

    @patch('pathlib.Path.cwd')
    def test_decompose(self, mock_cwd):
        """Test specification decomposition"""
        mock_cwd.return_value = self.project_path

        # Create spec structure
        spec_dir = self.project_path / "specs" / "001-feature"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Feature Spec")

        cli = SpecPulseCLI(no_color=True)
        cli.specpulse.decompose_specification = MagicMock(return_value={
            "services": ["auth", "user"],
            "api_contracts": [],
            "integration_points": []
        })

        result = cli.decompose("001")

        assert result is True
        cli.specpulse.decompose_specification.assert_called_once()

    @patch('pathlib.Path.cwd')
    def test_decompose_no_spec(self, mock_cwd):
        """Test decompose with missing spec"""
        mock_cwd.return_value = self.project_path

        cli = SpecPulseCLI(no_color=True)
        result = cli.decompose("999")

        assert result is False

    @patch('pathlib.Path.cwd')
    def test_list_specs(self, mock_cwd):
        """Test listing specifications"""
        mock_cwd.return_value = self.project_path

        # Create specs
        specs_dir = self.project_path / "specs"
        specs_dir.mkdir()
        (specs_dir / "001-auth").mkdir()
        (specs_dir / "002-payments").mkdir()

        cli = SpecPulseCLI(no_color=True)
        cli.list_specs()

        # Should not raise exception

    @patch('pathlib.Path.cwd')
    def test_list_specs_empty(self, mock_cwd):
        """Test listing specs with no specs directory"""
        mock_cwd.return_value = self.project_path

        cli = SpecPulseCLI(no_color=True)
        cli.list_specs()

        # Should handle gracefully

    @patch('pathlib.Path.cwd')
    def test_doctor(self, mock_cwd):
        """Test doctor command"""
        mock_cwd.return_value = self.project_path

        # Create project structure
        (self.project_path / "memory").mkdir()
        (self.project_path / "templates").mkdir()
        (self.project_path / "scripts").mkdir()
        (self.project_path / "specs").mkdir()

        cli = SpecPulseCLI(no_color=True)
        result = cli.doctor()

        assert result is True

    @patch('pathlib.Path.cwd')
    def test_doctor_missing_directories(self, mock_cwd):
        """Test doctor with missing directories"""
        mock_cwd.return_value = self.project_path

        cli = SpecPulseCLI(no_color=True)
        result = cli.doctor()

        assert result is False

    @patch('subprocess.run')
    def test_update(self, mock_run):
        """Test update command"""
        mock_run.return_value.returncode = 0

        cli = SpecPulseCLI(no_color=True)
        result = cli.update()

        assert result is True
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_update_failure(self, mock_run):
        """Test update command failure"""
        mock_run.return_value.returncode = 1

        cli = SpecPulseCLI(no_color=True)
        result = cli.update()

        assert result is False

    @patch('pathlib.Path.cwd')
    @patch('specpulse.cli.main.GitUtils')
    def test_sync(self, mock_git_utils_class, mock_cwd):
        """Test project sync"""
        mock_cwd.return_value = self.project_path

        mock_git = MagicMock()
        mock_git.is_repo.return_value = True
        mock_git.get_status.return_value = {"modified": [], "untracked": []}
        mock_git_utils_class.return_value = mock_git

        # Create memory directory
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "context.md").write_text("# Context")

        cli = SpecPulseCLI(no_color=True)
        result = cli.sync()

        assert result is True

    @patch('pathlib.Path.cwd')
    @patch('specpulse.cli.main.GitUtils')
    def test_sync_not_git_repo(self, mock_git_utils_class, mock_cwd):
        """Test sync when not a git repo"""
        mock_cwd.return_value = self.project_path

        mock_git = MagicMock()
        mock_git.is_repo.return_value = False
        mock_git_utils_class.return_value = mock_git

        cli = SpecPulseCLI(no_color=True)
        result = cli.sync()

        assert result is False

    @patch('shutil.copy2')
    def test_create_templates(self, mock_copy):
        """Test template creation"""
        # Create mock resources directory
        resources_dir = self.project_path / "resources"
        templates_dir = resources_dir / "templates"
        templates_dir.mkdir(parents=True)

        # Create mock template files
        (templates_dir / "spec.md").write_text("# Spec")
        (templates_dir / "plan.md").write_text("# Plan")
        (templates_dir / "task.md").write_text("# Task")

        cli = SpecPulseCLI(no_color=True)
        cli.specpulse.resources_dir = resources_dir

        project_templates = self.project_path / "templates"
        project_templates.mkdir()

        cli._create_templates(self.project_path)

        assert mock_copy.call_count >= 3

    @patch('shutil.copy2')
    def test_create_memory_files(self, mock_copy):
        """Test memory files creation"""
        # Create mock resources directory
        resources_dir = self.project_path / "resources"
        memory_dir = resources_dir / "memory"
        memory_dir.mkdir(parents=True)

        # Create mock memory files
        (memory_dir / "constitution.md").write_text("# Constitution")
        (memory_dir / "context.md").write_text("# Context")
        (memory_dir / "decisions.md").write_text("# Decisions")

        cli = SpecPulseCLI(no_color=True)
        cli.specpulse.resources_dir = resources_dir

        project_memory = self.project_path / "memory"
        project_memory.mkdir()

        cli._create_memory_files(self.project_path)

        assert mock_copy.call_count >= 3

    def test_create_ai_commands(self):
        """Test AI command creation"""
        cli = SpecPulseCLI(no_color=True)

        # Mock SpecPulse methods
        cli.specpulse.generate_claude_commands = MagicMock(return_value=[
            {"name": "sp-pulse", "description": "Init", "script": "sp-pulse-init.sh"}
        ])
        cli.specpulse.generate_gemini_commands = MagicMock(return_value=[
            {"name": "sp-pulse", "description": "Init", "script": "sp-pulse-init.sh"}
        ])

        # Create directories
        claude_dir = self.project_path / ".claude" / "commands"
        claude_dir.mkdir(parents=True)
        gemini_dir = self.project_path / ".gemini" / "commands"
        gemini_dir.mkdir(parents=True)

        cli._create_ai_commands(self.project_path)

        # Check files were created
        assert len(list(claude_dir.glob("*.md"))) > 0
        assert len(list(gemini_dir.glob("*.toml"))) > 0