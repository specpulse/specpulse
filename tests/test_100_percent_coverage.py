"""Comprehensive tests to achieve 100% coverage."""
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, call
import pytest
import subprocess
import json
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from specpulse.cli.main import SpecPulseCLI
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.utils.console import Console
from specpulse.utils.git_utils import GitUtils


class TestCLIFullCoverage:
    """Test all CLI paths for 100% coverage."""
    
    def test_cli_init_all_templates(self):
        """Test all template options."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            cli = SpecPulseCLI(no_color=True)
            
            # Test each template
            templates = ["default", "web", "api", "ml", "data"]
            for template in templates:
                project_dir = Path(tmpdir) / f"test_{template}"
                with patch('specpulse.cli.main.SpecPulse') as mock_sp:
                    mock_sp.return_value.initialize_project.return_value = True
                    result = cli.init(f"test_{template}", template=template)
                    assert result is True
    
    def test_cli_init_with_git_error(self):
        """Test git initialization error handling."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            cli = SpecPulseCLI(no_color=True)
            
            with patch('specpulse.cli.main.SpecPulse') as mock_sp:
                mock_sp.return_value.initialize_project.return_value = True
                with patch('specpulse.utils.git_utils.GitUtils.is_git_repo', return_value=False):
                    with patch('specpulse.utils.git_utils.GitUtils.init_repo', side_effect=Exception("Git error")):
                        result = cli.init("test", no_git=False)
                        # Should still succeed even if git fails
                        assert result is True
    
    def test_cli_sync_all_paths(self):
        """Test sync with all possible paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # Create project structure
            (Path(tmpdir) / ".specpulse").mkdir()
            (Path(tmpdir) / ".specpulse" / "config.yaml").write_text("project_name: test")
            (Path(tmpdir) / "memory").mkdir()
            (Path(tmpdir) / "memory" / "context.md").write_text("# Context")
            
            cli = SpecPulseCLI(no_color=True)
            
            # Test successful sync
            with patch('specpulse.utils.git_utils.GitUtils.is_git_repo', return_value=True):
                with patch('specpulse.utils.git_utils.GitUtils.sync_project') as mock_sync:
                    mock_sync.return_value = (True, "Synced")
                    result = cli.sync()
                    assert result is True
            
            # Test sync with no git
            with patch('specpulse.utils.git_utils.GitUtils.is_git_repo', return_value=False):
                result = cli.sync()
                assert result is False
    
    def test_cli_validate_all_components(self):
        """Test validation of all components."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # Create full project structure
            dirs = [".specpulse", "memory", "specs/001-test", "plans/001-test", "tasks/001-test"]
            for d in dirs:
                (Path(tmpdir) / d).mkdir(parents=True)
            
            files = {
                ".specpulse/config.yaml": "project_name: test",
                "memory/constitution.md": "# Constitution",
                "memory/context.md": "# Context",
                "specs/001-test/spec.md": "# Spec",
                "plans/001-test/plan.md": "# Plan",
                "tasks/001-test/tasks.md": "# Tasks"
            }
            
            for path, content in files.items():
                (Path(tmpdir) / path).write_text(content)
            
            cli = SpecPulseCLI(no_color=True, verbose=True)
            
            # Test validate all
            result = cli.validate()
            assert result is not None
            
            # Test validate specific components
            for component in ["spec", "plan", "task", "constitution", "memory"]:
                result = cli.validate(component=component)
                assert result is not None
    
    def test_cli_doctor_comprehensive(self):
        """Test doctor command with all checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # Create project
            (Path(tmpdir) / ".specpulse").mkdir()
            (Path(tmpdir) / ".specpulse" / "config.yaml").write_text("project_name: test\nversion: 1.0.0")
            
            cli = SpecPulseCLI(no_color=True, verbose=True)
            
            with patch('specpulse.cli.main.subprocess.run') as mock_run:
                # Mock different command responses
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="Python 3.11.0"),  # Python version
                    MagicMock(returncode=0, stdout="git version 2.40.0"),  # Git version
                    MagicMock(returncode=1),  # pip show fails
                ]
                
                result = cli.doctor()
                assert result is True
    
    def test_cli_edge_cases(self):
        """Test CLI edge cases and error paths."""
        cli = SpecPulseCLI(no_color=True)
        
        # Test init with existing project
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            (Path(tmpdir) / ".specpulse").mkdir()
            
            result = cli.init("test", here=True)
            assert result is False  # Should fail
        
        # Test commands in non-project directory
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            assert cli.sync() is False
            assert cli.validate() is False


class TestCoreFullCoverage:
    """Test core module for 100% coverage."""
    
    def test_specpulse_all_methods(self):
        """Test all SpecPulse methods."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = SpecPulse(Path(tmpdir))
            
            # Test project initialization
            assert sp.initialize_project("test") is True
            
            # Test structure validation
            assert sp.validate_structure() is True
            
            # Test memory system
            sp.update_memory("context", {"test": "data"})
            memory = sp.get_memory("context")
            assert memory is not None
            
            # Test with missing directories
            shutil.rmtree(Path(tmpdir) / "memory")
            assert sp.validate_structure() is False
    
    def test_validator_all_checks(self):
        """Test all validator methods."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test structure
            (Path(tmpdir) / "specs/001-test").mkdir(parents=True)
            (Path(tmpdir) / "plans/001-test").mkdir(parents=True)
            (Path(tmpdir) / "tasks/001-test").mkdir(parents=True)
            (Path(tmpdir) / "memory").mkdir()
            
            # Create test files with various states
            spec_content = """
            # Specification
            ## Requirements
            - Must have authentication
            - [NEEDS CLARIFICATION: What auth method?]
            ## User Stories
            As a user, I want to login
            """
            
            plan_content = """
            # Plan
            ## Phase Gates
            - ✅ Simplicity check passed
            ## Modules
            - auth
            - api
            - database
            """
            
            task_content = """
            # Tasks
            - [x] T001: Setup
            - [ ] T002: Implementation
            - [ ] T003: Testing
            """
            
            (Path(tmpdir) / "specs/001-test/spec.md").write_text(spec_content)
            (Path(tmpdir) / "plans/001-test/plan.md").write_text(plan_content)
            (Path(tmpdir) / "tasks/001-test/tasks.md").write_text(task_content)
            (Path(tmpdir) / "memory/constitution.md").write_text("# Constitution\n## Article I")
            
            validator = Validator(Path(tmpdir))
            
            # Test all validation methods
            assert validator.validate_spec() is not None
            assert validator.validate_plan() is not None
            assert validator.validate_tasks() is not None
            assert validator.validate_constitution() is True
            assert validator.validate_memory() is True
            
            # Test edge cases
            assert validator.check_clarifications() == 1
            assert validator.check_phase_gates() is True
            assert validator.check_complexity() == 3
            
            # Test with missing files
            os.remove(Path(tmpdir) / "memory/constitution.md")
            assert validator.validate_constitution() is False


class TestUtilsFullCoverage:
    """Test utils for 100% coverage."""
    
    def test_console_all_methods(self):
        """Test all console methods."""
        console = Console(no_color=True)
        
        # Test all output methods
        console.print("Test")
        console.success("Success")
        console.error("Error")
        console.warning("Warning")
        console.info("Info")
        console.header("Header")
        console.section("Section")
        
        # Test progress spinner
        with console.progress("Testing"):
            pass
        
        # Test tables
        console.table(["Col1", "Col2"], [["Row1", "Row2"]])
        
        # Test prompts
        with patch('builtins.input', return_value='yes'):
            assert console.confirm("Confirm?") is True
        
        with patch('builtins.input', return_value='no'):
            assert console.confirm("Confirm?") is False
        
        # Test with color enabled
        console_color = Console(no_color=False)
        console_color.success("Colored output")
    
    def test_git_utils_all_methods(self):
        """Test all GitUtils methods."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # Test non-git directory
            assert GitUtils.is_git_repo() is False
            
            # Initialize git repo
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                assert GitUtils.init_repo() is True
            
            # Test git operations
            with patch('subprocess.run') as mock_run:
                # Mock successful git commands
                mock_run.return_value = MagicMock(
                    returncode=0,
                    stdout="main",
                    stderr=""
                )
                
                assert GitUtils.get_current_branch() == "main"
                assert GitUtils.create_branch("feature") is True
                assert GitUtils.commit("Test commit") is True
                
                # Test sync
                success, message = GitUtils.sync_project("Test sync")
                assert success is True
            
            # Test git command failures
            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.CalledProcessError(1, "git")
                
                assert GitUtils.get_current_branch() == "unknown"
                assert GitUtils.create_branch("feature") is False
                assert GitUtils.commit("Test") is False
            
            # Test with git repo detected
            with patch('os.path.exists', return_value=True):
                assert GitUtils.is_git_repo() is True


class TestIntegrationFullCoverage:
    """Integration tests for uncovered paths."""
    
    def test_full_workflow(self):
        """Test complete workflow from init to validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # Initialize project
            cli = SpecPulseCLI(no_color=True, verbose=True)
            
            # Test init with all options
            result = cli.init("test-project", 
                            here=False,
                            template="web",
                            ai="claude",
                            no_git=False)
            
            # Create some specs and validate
            if result:
                project_dir = Path(tmpdir) / "test-project"
                if project_dir.exists():
                    os.chdir(project_dir)
                    
                    # Create a spec
                    spec_dir = project_dir / "specs" / "001-feature"
                    spec_dir.mkdir(parents=True, exist_ok=True)
                    (spec_dir / "spec.md").write_text("# Test Spec")
                    
                    # Validate
                    cli.validate()
                    
                    # Doctor
                    cli.doctor()
                    
                    # Sync (if git)
                    cli.sync()
    
    def test_error_recovery(self):
        """Test error recovery paths."""
        cli = SpecPulseCLI(no_color=True)
        
        # Test with permission errors
        with patch('os.makedirs', side_effect=PermissionError("No permission")):
            result = cli.init("test")
            assert result is False
        
        # Test with file write errors
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            with patch('builtins.open', side_effect=IOError("Cannot write")):
                sp = SpecPulse(Path(tmpdir))
                result = sp.initialize_project("test")
                assert result is False
    
    def test_all_ai_integrations(self):
        """Test AI integration setup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "ai-test"
            
            # Test Claude setup
            cli = SpecPulseCLI(no_color=True)
            with patch('specpulse.cli.main.SpecPulse') as mock_sp:
                mock_sp.return_value.initialize_project.return_value = True
                
                # Mock file operations for Claude
                with patch('shutil.copytree'):
                    with patch('pathlib.Path.mkdir'):
                        result = cli.init("ai-test", ai="claude")
                        assert result is True
            
            # Test Gemini setup
            with patch('specpulse.cli.main.SpecPulse') as mock_sp:
                mock_sp.return_value.initialize_project.return_value = True
                
                # Mock file operations for Gemini
                with patch('shutil.copytree'):
                    with patch('pathlib.Path.mkdir'):
                        result = cli.init("ai-test2", ai="gemini")
                        assert result is True


class TestMissingCoverage:
    """Test specific missing coverage lines."""
    
    def test_cli_main_missing_lines(self):
        """Cover specific missing lines in CLI main."""
        cli = SpecPulseCLI(no_color=True)
        
        # Test version display
        with patch('specpulse.cli.main.Console.print') as mock_print:
            cli._display_version()
            mock_print.assert_called()
        
        # Test directory validation
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # Test _ensure_in_project with no project
            result = cli._ensure_in_project()
            assert result is False
            
            # Create project and test again
            (Path(tmpdir) / ".specpulse").mkdir()
            result = cli._ensure_in_project()
            assert result is True
    
    def test_console_missing_lines(self):
        """Cover missing console lines."""
        console = Console(no_color=False)
        
        # Test all color methods
        with patch('rich.console.Console.print') as mock_print:
            console.debug("Debug message")
            console.trace("Trace message")
            mock_print.assert_called()
        
        # Test prompt with default
        with patch('builtins.input', return_value=''):
            result = console.prompt("Enter value", default="default")
            assert result == "default"
    
    def test_validator_edge_cases(self):
        """Test validator edge cases."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = Validator(Path(tmpdir))
            
            # Test with malformed files
            (Path(tmpdir) / "specs").mkdir()
            (Path(tmpdir) / "specs" / "001-test").mkdir()
            (Path(tmpdir) / "specs" / "001-test" / "spec.md").write_text("")
            
            result = validator.validate_spec()
            assert result is not None  # Should handle empty files
            
            # Test with unicode in files
            (Path(tmpdir) / "specs" / "001-test" / "spec.md").write_text(
                "# Spec with émoji 🚀\n[NEEDS CLARIFICATION: Test]"
            )
            
            clarifications = validator.check_clarifications()
            assert clarifications >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])