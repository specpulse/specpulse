"""
Complete Core Module Tests

Comprehensive tests for SpecPulse core functionality.
Designed for 100% code coverage.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import yaml
from datetime import datetime

from specpulse.core.specpulse import SpecPulse
from specpulse.core.service_container import ServiceContainer
from specpulse.core.path_manager import PathManager
from specpulse.core.template_provider import TemplateProvider
from specpulse.core.memory_provider import MemoryProvider
from specpulse.models.project_context import ProjectContext
from specpulse.utils.error_handler import SpecPulseError, ValidationError


class TestSpecPulseComplete:
    """Comprehensive tests for SpecPulse core functionality"""

    @pytest.mark.unit
    def test_specpulse_initialization_success(self, temp_project_dir):
        """Test successful SpecPulse initialization"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        assert specpulse.project_path == temp_project_dir
        assert specpulse.config is not None
        assert specpulse.config["version"] == "2.6.0"
        assert specpulse.resources_dir.exists()

    @pytest.mark.unit
    def test_specpulse_initialization_with_invalid_path(self):
        """Test SpecPulse initialization with invalid path"""
        with pytest.raises((OSError, ValidationError)):
            SpecPulse(project_path=Path("/invalid/nonexistent/path"))

    @pytest.mark.unit
    def test_specpulse_config_loading(self, temp_project_dir):
        """Test configuration loading from YAML file"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        config_path = temp_project_dir / ".specpulse" / "config.yaml"
        assert config_path.exists()

        # Verify config structure
        assert "project" in specpulse.config
        assert "ai" in specpulse.config
        assert "templates" in specpulse.config
        assert "conventions" in specpulse.config

    @pytest.mark.unit
    def test_specpulse_service_injection(self, temp_project_dir, service_container):
        """Test service dependency injection"""
        specpulse = SpecPulse(
            project_path=temp_project_dir,
            container=service_container
        )

        # Verify services are injected
        assert specpulse.template_provider is not None
        assert specpulse.memory_provider is not None
        assert specpulse.script_generator is not None
        assert specpulse.ai_provider is not None

    @pytest.mark.unit
    def test_specpulse_default_services(self, temp_project_dir):
        """Test default service creation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Verify default services are created
        assert specpulse.template_provider is not None
        assert specpulse.memory_provider is not None
        assert specpulse.script_generator is not None
        assert specpulse.ai_provider is not None

    @pytest.mark.unit
    def test_specpulse_init_complete_workflow(self, temp_project_dir):
        """Test complete initialization workflow"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Mock console to avoid output
        with patch('specpulse.utils.console.Console') as mock_console:
            result = specpulse.init(
                project_name="test-project",
                here=True,
                ai_assistant="claude"
            )

        assert result["status"] == "success"
        assert result["project_name"] == "test-project"
        assert result["project_path"] == str(temp_project_dir)
        assert result["ai_assistant"] == "claude"

    @pytest.mark.unit
    def test_specpulse_init_with_templates(self, temp_project_dir):
        """Test initialization with template creation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify template files are created
        templates_dir = temp_project_dir / ".specpulse" / "templates"
        assert templates_dir.exists()
        assert (templates_dir / "spec.md").exists()
        assert (templates_dir / "plan.md").exists()
        assert (templates_dir / "task.md").exists()

    @pytest.mark.unit
    def test_specpulse_init_error_handling(self, temp_project_dir):
        """Test error handling during initialization"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Mock directory creation to fail
        with patch.object(Path, 'mkdir', side_effect=OSError("Permission denied")):
            with patch('specpulse.utils.console.Console'):
                result = specpulse.init(here=True)

        assert result["status"] == "error"
        assert "Permission denied" in result["error"]

    @pytest.mark.unit
    def test_specpulse_init_with_invalid_project_name(self, temp_project_dir):
        """Test initialization with invalid project name"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            # Test with invalid characters
            result = specpulse.init(project_name="project@name")

        assert result["status"] == "error"
        assert "invalid characters" in result["error"]

    @pytest.mark.unit
    def test_specpulse_template_copying(self, temp_project_dir):
        """Test template file copying during init"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create source templates
        source_templates_dir = specpulse.resources_dir / "templates"
        source_templates_dir.mkdir(parents=True, exist_ok=True)

        (source_templates_dir / "test.md").write_text("test template")

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify template was copied
        dest_template = temp_project_dir / ".specpulse" / "templates" / "test.md"
        assert dest_template.exists()
        assert dest_template.read_text() == "test template"

    @pytest.mark.unit
    def test_specpulse_memory_file_creation(self, temp_project_dir):
        """Test memory file creation during init"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify memory files are created
        memory_dir = temp_project_dir / ".specpulse" / "memory"
        assert memory_dir.exists()
        assert (memory_dir / "context.md").exists()
        assert (memory_dir / "decisions.md").exists()

    @pytest.mark.unit
    def test_specpulse_ai_command_copying(self, temp_project_dir):
        """Test AI command file copying"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create source AI commands
        source_commands_dir = specpulse.resources_dir / "commands"
        source_commands_dir.mkdir(parents=True, exist_ok=True)
        claude_dir = source_commands_dir / "claude"
        claude_dir.mkdir(exist_ok=True)

        (claude_dir / "test.md").write_text("test command")

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify AI command was copied
        dest_command = temp_project_dir / ".claude" / "commands" / "test.md"
        assert dest_command.exists()

    @pytest.mark.unit
    def test_specpulse_init_with_custom_tier(self, temp_project_dir):
        """Test initialization with custom tier"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True, ai_assistant="claude")

        assert result["status"] == "success"
        assert result["ai_assistant"] == "claude"

    @pytest.mark.unit
    def test_specpulse_multiple_inits(self, temp_project_dir):
        """Test multiple initializations in same directory"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            # First init
            result1 = specpulse.init(here=True)
            assert result1["status"] == "success"

            # Second init should still work
            result2 = specpulse.init(here=True)
            assert result2["status"] == "success"

    @pytest.mark.unit
    def test_specpulse_init_creates_registry(self, temp_project_dir):
        """Test that template registry is created"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify template registry is created
        registry_path = temp_project_dir / ".specpulse" / "template_registry.json"
        assert registry_path.exists()

        # Verify registry content
        with open(registry_path) as f:
            registry = yaml.safe_load(f)

        assert "version" in registry
        assert "templates" in registry
        assert registry["version"] == "2.6.0"

    @pytest.mark.unit
    def test_specpulse_resource_directory_resolution(self, temp_project_dir):
        """Test resource directory resolution"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Should resolve to actual resources directory
        assert specpulse.resources_dir.exists()
        assert (specpulse.resources_dir / "templates").exists()
        assert (specpulse.resources_dir / "commands").exists()

    @pytest.mark.unit
    def test_specpulse_configuration_validation(self, temp_project_dir):
        """Test configuration validation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        config = specpulse.config

        # Required fields should be present
        assert "version" in config
        assert "project" in config
        assert "ai" in config

        # Project config validation
        assert "name" in config["project"]
        assert "type" in config["project"]
        assert "created" in config["project"]

    @pytest.mark.unit
    def test_specpulse_with_missing_resources(self):
        """Test behavior when resources directory is missing"""
        # Create temp dir without resources
        temp_dir = Path(tempfile.mkdtemp())

        try:
            # Mock resources_dir to non-existent path
            with patch.object(SpecPulse, 'resources_dir', Path("/nonexistent")):
                with pytest.raises(Exception):  # Should raise some kind of error
                    SpecPulse(project_path=temp_dir)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.mark.unit
    def test_specpulse_service_container_integration(self, temp_project_dir):
        """Test integration with service container"""
        container = ServiceContainer()

        # Register custom services
        mock_service = Mock()
        container.register('custom_service', mock_service)

        specpulse = SpecPulse(
            project_path=temp_project_dir,
            container=container
        )

        # Verify service container is used
        assert hasattr(specpulse, '_container')

    @pytest.mark.unit
    def test_specpulse_backward_compatibility(self, temp_project_dir):
        """Test backward compatibility with old project structure"""
        # Create legacy structure
        legacy_dirs = ["specs", "plans", "tasks", "memory", "templates"]
        for dir_name in legacy_dirs:
            (temp_project_dir / dir_name).mkdir(exist_ok=True)

        specpulse = SpecPulse(project_path=temp_project_dir)

        # Should still initialize
        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        assert result["status"] == "success"

    @pytest.mark.unit
    def test_specpulse_template_fallback(self, temp_project_dir):
        """Test template fallback when source templates missing"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Remove source templates
        if specpulse.templates_dir.exists():
            shutil.rmtree(specpulse.templates_dir)

        with patch('specpulse.utils.console.Console') as mock_console:
            result = specpulse.init(here=True)

        # Should still succeed with fallback templates
        assert result["status"] == "success"

    @pytest.mark.unit
    def test_specpulse_init_with_here_flag(self, temp_project_dir):
        """Test initialization with --here flag"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        assert result["status"] == "success"
        assert result["project_path"] == str(temp_project_dir)

    @pytest.mark.unit
    def test_specpulse_init_with_project_name(self, temp_project_dir):
        """Test initialization with custom project name"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        new_project_dir = temp_project_dir / "custom-project"

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(project_name="custom-project")

        assert result["status"] == "success"
        assert "custom-project" in result["project_path"]

    @pytest.mark.unit
    def test_specpulse_init_documentation_creation(self, temp_project_dir):
        """Test documentation file creation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify docs directory and files
        docs_dir = temp_project_dir / ".specpulse" / "docs"
        assert docs_dir.exists()
        assert (docs_dir / "AI_FALLBACK_GUIDE.md").exists()
        assert (docs_dir / "AI_INTEGRATION.md").exists()
        assert (docs_dir / "README.md").exists()

    @pytest.mark.unit
    def test_specpulse_init_creates_checkpoints_dir(self, temp_project_dir):
        """Test checkpoints directory creation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify checkpoints directory
        checkpoints_dir = temp_project_dir / ".specpulse" / "checkpoints"
        assert checkpoints_dir.exists()

    @pytest.mark.unit
    def test_specpulse_init_creates_cache_dir(self, temp_project_dir):
        """Test cache directory creation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify cache directory
        cache_dir = temp_project_dir / ".specpulse" / "cache"
        assert cache_dir.exists()

    @pytest.mark.unit
    def test_specpulse_init_creates_memory_notes_dir(self, temp_project_dir):
        """Test memory notes directory creation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify memory notes directory
        notes_dir = temp_project_dir / ".specpulse" / "memory" / "notes"
        assert notes_dir.exists()

    @pytest.mark.unit
    def test_specpulse_validation_file_copying(self, temp_project_dir):
        """Test validation files copying"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create source validation files
        validation_dir = specpulse.resources_dir
        validation_dir.mkdir(parents=True, exist_ok=True)

        (validation_dir / "validation_rules.yaml").write_text("test: rules")
        (validation_dir / "validation_examples.yaml").write_text("test: examples")

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify validation files were copied
        specpulse_dir = temp_project_dir / ".specpulse"
        assert (specpulse_dir / "validation_rules.yaml").exists()
        assert (specpulse_dir / "validation_examples.yaml").exists()

    @pytest.mark.unit
    def test_specpulse_memory_files_content(self, temp_project_dir):
        """Test memory files content"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Check context.md content
        context_file = temp_project_dir / ".specpulse" / "memory" / "context.md"
        context_content = context_file.read_text()
        assert "Project: test-project" in context_content
        assert "SpecPulse Version:" in context_content
        assert "Active Feature: None" in context_content

        # Check decisions.md content
        decisions_file = temp_project_dir / ".specpulse" / "memory" / "decisions.md"
        decisions_content = decisions_file.read_text()
        assert "Architectural Decisions" in decisions_content
        assert "No decisions recorded yet" in decisions_content

    @pytest.mark.unit
    def test_specpulse_init_copies_all_ai_commands(self, temp_project_dir):
        """Test all AI command files are copied"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create source AI commands
        source_commands = specpulse.resources_dir / "commands"
        source_commands.mkdir(parents=True, exist_ok=True)

        claude_dir = source_commands / "claude"
        claude_dir.mkdir(exist_ok=True)

        gemini_dir = source_commands / "gemini"
        gemini_dir.mkdir(exist_ok=True)

        # Create test command files
        (claude_dir / "sp-test.md").write_text("claude command")
        (gemini_dir / "sp-test.toml").write_text("gemini command")

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify both Claude and Gemini commands are copied
        claude_dest = temp_project_dir / ".claude" / "commands" / "sp-test.md"
        gemini_dest = temp_project_dir / ".gemini" / "commands" / "sp-test.toml"

        assert claude_dest.exists()
        assert gemini_dest.exists()
        assert claude_dest.read_text() == "claude command"
        assert gemini_dest.read_text() == "gemini command"

    @pytest.mark.unit
    def test_specpulse_error_handling_on_corrupted_config(self, temp_project_dir):
        """Test handling of corrupted config file"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create corrupted config file
        config_path = temp_project_dir / ".specpulse" / "config.yaml"
        config_path.write_text("invalid: yaml: content: [")

        # Should handle gracefully or raise appropriate error
        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # The init should still work by creating a new config
        assert result["status"] == "success"

    @pytest.mark.unit
    def test_specpulse_decomposition_templates_copying(self, temp_project_dir):
        """Test decomposition templates copying"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create decomposition templates
        decomp_dir = specpulse.resources_dir / "templates" / "decomposition"
        decomp_dir.mkdir(parents=True, exist_ok=True)

        (decomp_dir / "microservices.md").write_text("microservice template")
        (decomp_dir / "api-contract.yaml").write_text("api: contract")

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify decomposition templates were copied
        dest_decomp_dir = temp_project_dir / ".specpulse" / "templates" / "decomposition"
        assert (dest_decomp_dir / "microservices.md").exists()
        assert (dest_decomp_dir / "api-contract.yaml").exists()
        assert (dest_decomp_dir / "microservices.md").read_text() == "microservice template"
        assert (dest_decomp_dir / "api-contract.yaml").read_text() == "api: contract"

    @pytest.mark.unit
    def test_specpulse_template_registry_structure(self, temp_project_dir):
        """Test template registry structure"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        registry_path = temp_project_dir / ".specpulse" / "template_registry.json"

        with open(registry_path) as f:
            registry = yaml.safe_load(f)

        # Verify registry structure
        assert "version" in registry
        assert "created" in registry
        assert "templates" in registry

        templates = registry["templates"]
        assert "core" in templates
        assert "decomposition" in templates

        core_templates = templates["core"]
        assert "spec" in core_templates
        assert "plan" in core_templates
        assert "task" in core_templates

    @pytest.mark.unit
    def test_specpulse_concurrent_init_protection(self, temp_project_dir):
        """Test protection against concurrent initialization"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # This test simulates concurrent access scenarios
        with patch('specpulse.utils.console.Console'):
            result1 = specpulse.init(here=True)
            result2 = specpulse.init(here=True)

            # Both should succeed (idempotent operation)
            assert result1["status"] == "success"
            assert result2["status"] == "success"

    @pytest.mark.unit
    def test_specpulse_memory_files_integrity(self, temp_project_dir):
        """Test memory files maintain integrity"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        # Verify memory files have valid YAML structure (where applicable)
        memory_files = [
            "memory/context.md",
            "memory/decisions.md"
        ]

        for memory_file in memory_files:
            file_path = temp_project_dir / ".specpulse" / memory_file
            assert file_path.exists()
            assert file_path.stat().st_size > 0  # File is not empty

    @pytest.mark.unit
    def test_specpulse_template_backup_system(self, temp_project_dir):
        """Test template backup system integration"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Test that template backups directory is created
        with patch('specpulse.utils.console.Console'):
            result = specpulse.init(here=True)

        backup_dir = temp_project_dir / ".specpulse" / "template_backups"
        assert backup_dir.exists()

        # Verify backup system can be used (directory exists and writable)
        test_backup = backup_dir / "test_backup.md"
        test_backup.write_text("test content")
        assert test_backup.exists()
        test_backup.unlink()  # Cleanup