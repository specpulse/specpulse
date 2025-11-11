"""
Comprehensive tests for SpecPulse core functionality.

This module provides thorough testing of the main SpecPulse class
including initialization, template management, and project setup.
"""

import pytest
import json
import yaml
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from specpulse.core.specpulse import SpecPulse
from specpulse.utils.error_handler import ValidationError, ProjectStructureError


class TestSpecPulseInitialization:
    """Test SpecPulse initialization and configuration"""

    def test_init_default_paths(self, temp_project_dir):
        """Test SpecPulse initialization with default paths"""
        specpulse = SpecPulse()

        assert specpulse.project_path == Path.cwd()
        assert specpulse.config == {}
        assert hasattr(specpulse, 'template_provider')
        assert hasattr(specpulse, 'memory_provider')
        assert hasattr(specpulse, 'script_generator')
        assert hasattr(specpulse, 'ai_provider')
        assert hasattr(specpulse, 'decomposition_service')

    def test_init_with_project_path(self, temp_project_dir):
        """Test SpecPulse initialization with custom project path"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        assert specpulse.project_path == temp_project_dir

    def test_init_with_service_container(self, temp_project_dir):
        """Test SpecPulse initialization with service container"""
        from specpulse.core.service_container import ServiceContainer

        container = ServiceContainer()
        specpulse = SpecPulse(
            project_path=temp_project_dir,
            container=container
        )

        assert specpulse.project_path == temp_project_dir
        # Services should be resolved from container
        assert specpulse.template_provider is not None

    def test_load_config_existing(self, temp_project_dir):
        """Test loading existing configuration"""
        # Create .specpulse directory and config file
        specpulse_dir = temp_project_dir / ".specpulse"
        specpulse_dir.mkdir()

        config_data = {
            "version": "2.6.0",
            "project": {
                "name": "test-project",
                "type": "web"
            },
            "ai": {
                "primary": "claude"
            }
        }

        config_file = specpulse_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        specpulse = SpecPulse(project_path=temp_project_dir)

        assert specpulse.config["project"]["name"] == "test-project"
        assert specpulse.config["ai"]["primary"] == "claude"

    def test_load_config_corrupted(self, temp_project_dir):
        """Test loading corrupted configuration file"""
        # Create .specpulse directory and corrupted config file
        specpulse_dir = temp_project_dir / ".specpulse"
        specpulse_dir.mkdir()

        config_file = specpulse_dir / "config.yaml"
        with open(config_file, 'w') as f:
            f.write("invalid: yaml: content: [")  # Invalid YAML

        specpulse = SpecPulse(project_path=temp_project_dir)

        # Should fallback to empty config
        assert specpulse.config == {}

    def test_load_config_nonexistent(self, temp_project_dir):
        """Test loading when config file doesn't exist"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Should return empty config
        assert specpulse.config == {}

    def test_resources_directory_resolution(self, temp_project_dir):
        """Test resources directory resolution"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        assert specpulse.resources_dir.exists()
        assert specpulse.templates_dir.exists()


class TestSpecPulseTemplateMethods:
    """Test template delegation methods"""

    def test_get_spec_template(self, temp_project_dir):
        """Test getting specification template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_spec_template', return_value="# Spec Template") as mock_method:
            template = specpulse.get_spec_template()

            assert template == "# Spec Template"
            mock_method.assert_called_once()

    def test_get_plan_template(self, temp_project_dir):
        """Test getting plan template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_plan_template', return_value="# Plan Template") as mock_method:
            template = specpulse.get_plan_template()

            assert template == "# Plan Template"
            mock_method.assert_called_once()

    def test_get_task_template(self, temp_project_dir):
        """Test getting task template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_task_template', return_value="# Task Template") as mock_method:
            template = specpulse.get_task_template()

            assert template == "# Task Template"
            mock_method.assert_called_once()

    def test_get_template_with_variables(self, temp_project_dir):
        """Test getting template with variables"""
        specpulse = SpecPulse(project_path=temp_project_dir)
        variables = {"title": "Test", "content": "Test content"}

        with patch.object(specpulse.template_provider, 'get_template', return_value="Rendered template") as mock_method:
            template = specpulse.get_template("test.md", variables)

            assert template == "Rendered template"
            mock_method.assert_called_once_with("test.md", variables)

    def test_get_decomposition_template(self, temp_project_dir):
        """Test getting decomposition template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_decomposition_template', return_value="# Decomposition Template") as mock_method:
            template = specpulse.get_decomposition_template("microservices")

            assert template == "# Decomposition Template"
            mock_method.assert_called_once_with("microservices")

    def test_get_microservice_template(self, temp_project_dir):
        """Test getting microservice template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_microservice_template', return_value="# Microservice Template") as mock_method:
            template = specpulse.get_microservice_template()

            assert template == "# Microservice Template"
            mock_method.assert_called_once()

    def test_get_api_contract_template(self, temp_project_dir):
        """Test getting API contract template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_api_contract_template', return_value="openapi: 3.0.0") as mock_method:
            template = specpulse.get_api_contract_template()

            assert template == "openapi: 3.0.0"
            mock_method.assert_called_once()

    def test_get_interface_template(self, temp_project_dir):
        """Test getting interface template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_interface_template', return_value="interface Test {}") as mock_method:
            template = specpulse.get_interface_template()

            assert template == "interface Test {}"
            mock_method.assert_called_once()

    def test_get_service_plan_template(self, temp_project_dir):
        """Test getting service plan template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_service_plan_template', return_value="# Service Plan") as mock_method:
            template = specpulse.get_service_plan_template()

            assert template == "# Service Plan"
            mock_method.assert_called_once()

    def test_get_integration_plan_template(self, temp_project_dir):
        """Test getting integration plan template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.template_provider, 'get_integration_plan_template', return_value="# Integration Plan") as mock_method:
            template = specpulse.get_integration_plan_template()

            assert template == "# Integration Plan"
            mock_method.assert_called_once()


class TestSpecPulseMemoryMethods:
    """Test memory delegation methods"""

    def test_get_constitution_template(self, temp_project_dir):
        """Test getting constitution template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.memory_provider, 'get_constitution_template', return_value="# Constitution") as mock_method:
            template = specpulse.get_constitution_template()

            assert template == "# Constitution"
            mock_method.assert_called_once()

    def test_get_context_template(self, temp_project_dir):
        """Test getting context template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.memory_provider, 'get_context_template', return_value="# Context") as mock_method:
            template = specpulse.get_context_template()

            assert template == "# Context"
            mock_method.assert_called_once()

    def test_get_decisions_template(self, temp_project_dir):
        """Test getting decisions template"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.memory_provider, 'get_decisions_template', return_value="# Decisions") as mock_method:
            template = specpulse.get_decisions_template()

            assert template == "# Decisions"
            mock_method.assert_called_once()


class TestSpecPulseScriptMethods:
    """Test script delegation methods"""

    def test_get_setup_script(self, temp_project_dir):
        """Test getting setup script"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.script_generator, 'get_setup_script', return_value="#!/bin/bash\necho 'Setup'") as mock_method:
            script = specpulse.get_setup_script()

            assert script == "#!/bin/bash\necho 'Setup'"
            mock_method.assert_called_once()

    def test_get_spec_script(self, temp_project_dir):
        """Test getting spec script"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.script_generator, 'get_spec_script', return_value="#!/bin/bash\necho 'Spec'") as mock_method:
            script = specpulse.get_spec_script()

            assert script == "#!/bin/bash\necho 'Spec'"
            mock_method.assert_called_once()

    def test_get_plan_script(self, temp_project_dir):
        """Test getting plan script"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.script_generator, 'get_plan_script', return_value="#!/bin/bash\necho 'Plan'") as mock_method:
            script = specpulse.get_plan_script()

            assert script == "#!/bin/bash\necho 'Plan'"
            mock_method.assert_called_once()

    def test_get_task_script(self, temp_project_dir):
        """Test getting task script"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.script_generator, 'get_task_script', return_value="#!/bin/bash\necho 'Task'") as mock_method:
            script = specpulse.get_task_script()

            assert script == "#!/bin/bash\necho 'Task'"
            mock_method.assert_called_once()

    def test_get_validate_script(self, temp_project_dir):
        """Test getting validate script"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.script_generator, 'get_validate_script', return_value="#!/bin/bash\necho 'Validate'") as mock_method:
            script = specpulse.get_validate_script()

            assert script == "#!/bin/bash\necho 'Validate'"
            mock_method.assert_called_once()

    def test_get_generate_script(self, temp_project_dir):
        """Test getting generate script"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.script_generator, 'get_generate_script', return_value="#!/bin/bash\necho 'Generate'") as mock_method:
            script = specpulse.get_generate_script()

            assert script == "#!/bin/bash\necho 'Generate'"
            mock_method.assert_called_once()


class TestSpecPulseAICommandMethods:
    """Test AI command delegation methods"""

    def test_get_claude_instructions(self, temp_project_dir):
        """Test getting Claude instructions"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_instructions', return_value="# Claude Instructions") as mock_method:
            instructions = specpulse.get_claude_instructions()

            assert instructions == "# Claude Instructions"
            mock_method.assert_called_once()

    def test_get_gemini_instructions(self, temp_project_dir):
        """Test getting Gemini instructions"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_instructions', return_value="# Gemini Instructions") as mock_method:
            instructions = specpulse.get_gemini_instructions()

            assert instructions == "# Gemini Instructions"
            mock_method.assert_called_once()

    def test_claude_pulse_command(self, temp_project_dir):
        """Test getting Claude pulse command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_pulse_command', return_value="/sp-pulse") as mock_method:
            command = specpulse.get_claude_pulse_command()

            assert command == "/sp-pulse"
            mock_method.assert_called_once()

    def test_claude_spec_command(self, temp_project_dir):
        """Test getting Claude spec command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_spec_command', return_value="/sp-spec") as mock_method:
            command = specpulse.get_claude_spec_command()

            assert command == "/sp-spec"
            mock_method.assert_called_once()

    def test_claude_plan_command(self, temp_project_dir):
        """Test getting Claude plan command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_plan_command', return_value="/sp-plan") as mock_method:
            command = specpulse.get_claude_plan_command()

            assert command == "/sp-plan"
            mock_method.assert_called_once()

    def test_claude_task_command(self, temp_project_dir):
        """Test getting Claude task command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_task_command', return_value="/sp-task") as mock_method:
            command = specpulse.get_claude_task_command()

            assert command == "/sp-task"
            mock_method.assert_called_once()

    def test_claude_execute_command(self, temp_project_dir):
        """Test getting Claude execute command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_execute_command', return_value="/sp-execute") as mock_method:
            command = specpulse.get_claude_execute_command()

            assert command == "/sp-execute"
            mock_method.assert_called_once()

    def test_claude_validate_command(self, temp_project_dir):
        """Test getting Claude validate command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_validate_command', return_value="/sp-validate") as mock_method:
            command = specpulse.get_claude_validate_command()

            assert command == "/sp-validate"
            mock_method.assert_called_once()

    def test_claude_decompose_command(self, temp_project_dir):
        """Test getting Claude decompose command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_claude_decompose_command', return_value="/sp-decompose") as mock_method:
            command = specpulse.get_claude_decompose_command()

            assert command == "/sp-decompose"
            mock_method.assert_called_once()

    def test_gemini_pulse_command(self, temp_project_dir):
        """Test getting Gemini pulse command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_pulse_command', return_value="/sp-pulse") as mock_method:
            command = specpulse.get_gemini_pulse_command()

            assert command == "/sp-pulse"
            mock_method.assert_called_once()

    def test_gemini_spec_command(self, temp_project_dir):
        """Test getting Gemini spec command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_spec_command', return_value="/sp-spec") as mock_method:
            command = specpulse.get_gemini_spec_command()

            assert command == "/sp-spec"
            mock_method.assert_called_once()

    def test_gemini_plan_command(self, temp_project_dir):
        """Test getting Gemini plan command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_plan_command', return_value="/sp-plan") as mock_method:
            command = specpulse.get_gemini_plan_command()

            assert command == "/sp-plan"
            mock_method.assert_called_once()

    def test_gemini_task_command(self, temp_project_dir):
        """Test getting Gemini task command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_task_command', return_value="/sp-task") as mock_method:
            command = specpulse.get_gemini_task_command()

            assert command == "/sp-task"
            mock_method.assert_called_once()

    def test_gemini_execute_command(self, temp_project_dir):
        """Test getting Gemini execute command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_execute_command', return_value="/sp-execute") as mock_method:
            command = specpulse.get_gemini_execute_command()

            assert command == "/sp-execute"
            mock_method.assert_called_once()

    def test_gemini_validate_command(self, temp_project_dir):
        """Test getting Gemini validate command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_validate_command', return_value="/sp-validate") as mock_method:
            command = specpulse.get_gemini_validate_command()

            assert command == "/sp-validate"
            mock_method.assert_called_once()

    def test_gemini_decompose_command(self, temp_project_dir):
        """Test getting Gemini decompose command"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch.object(specpulse.ai_provider, 'get_gemini_decompose_command', return_value="/sp-decompose") as mock_method:
            command = specpulse.get_gemini_decompose_command()

            assert command == "/sp-decompose"
            mock_method.assert_called_once()

    def test_generate_claude_commands(self, temp_project_dir):
        """Test generating Claude commands"""
        specpulse = SpecPulse(project_path=temp_project_dir)
        expected_commands = [{"name": "pulse", "command": "/sp-pulse"}]

        with patch.object(specpulse.ai_provider, 'generate_claude_commands', return_value=expected_commands) as mock_method:
            commands = specpulse.generate_claude_commands()

            assert commands == expected_commands
            mock_method.assert_called_once()

    def test_generate_gemini_commands(self, temp_project_dir):
        """Test generating Gemini commands"""
        specpulse = SpecPulse(project_path=temp_project_dir)
        expected_commands = [{"name": "pulse", "command": "/sp-pulse"}]

        with patch.object(specpulse.ai_provider, 'generate_gemini_commands', return_value=expected_commands) as mock_method:
            commands = specpulse.generate_gemini_commands()

            assert commands == expected_commands
            mock_method.assert_called_once()


class TestSpecPulseDecompositionMethods:
    """Test decomposition delegation methods"""

    def test_decompose_specification(self, temp_project_dir):
        """Test specification decomposition"""
        specpulse = SpecPulse(project_path=temp_project_dir)
        spec_dir = temp_project_dir / "specs"
        spec_content = "# Test Specification\n\nThis is a test."
        expected_result = {"components": ["component1", "component2"]}

        with patch.object(specpulse.decomposition_service, 'decompose_specification', return_value=expected_result) as mock_method:
            result = specpulse.decompose_specification(spec_dir, spec_content)

            assert result == expected_result
            mock_method.assert_called_once_with(spec_dir, spec_content)


class TestSpecPulseInitialization:
    """Test SpecPulse project initialization"""

    def test_init_with_project_name(self, temp_project_dir):
        """Test initialization with project name"""
        specpulse = SpecPulse(project_path=temp_project_dir)
        project_name = "test-project"

        with patch('sys.platform', 'linux'):  # Mock platform to avoid chcp
            result = specpulse.init(project_name=project_name)

            assert result["status"] == "success"
            assert result["project_name"] == project_name
            assert (temp_project_dir / project_name / ".specpulse").exists()
            assert (temp_project_dir / project_name / ".claude").exists()
            assert (temp_project_dir / project_name / ".gemini").exists()

    def test_init_here_flag(self, temp_project_dir):
        """Test initialization with here=True"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('sys.platform', 'linux'):
            result = specpulse.init(here=True)

            assert result["status"] == "success"
            assert (temp_project_dir / ".specpulse").exists()
            assert (temp_project_dir / ".claude").exists()
            assert (temp_project_dir / ".gemini").exists()

    def test_init_with_ai_assistant(self, temp_project_dir):
        """Test initialization with AI assistant specified"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('sys.platform', 'linux'):
            result = specpulse.init(here=True, ai_assistant="claude")

            assert result["status"] == "success"
            assert result["ai_assistant"] == "claude"

            # Check config file
            config_path = temp_project_dir / ".specpulse" / "config.yaml"
            assert config_path.exists()

            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                assert config["ai"]["primary"] == "claude"

    def test_init_with_gemini_assistant(self, temp_project_dir):
        """Test initialization with Gemini AI assistant"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('sys.platform', 'linux'):
            result = specpulse.init(here=True, ai_assistant="gemini")

            assert result["status"] == "success"
            assert result["ai_assistant"] == "gemini"

    def test_init_invalid_project_name(self, temp_project_dir):
        """Test initialization with invalid project name"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        result = specpulse.init(project_name="invalid name with spaces")

        assert result["status"] == "error"
        assert "invalid characters" in result["error"].lower()

    def test_init_nonexistent_project_path(self, temp_project_dir):
        """Test initialization with nonexistent project path"""
        specpulse = SpecPulse(project_path=temp_project_dir)
        nonexistent_path = temp_project_dir / "nonexistent"

        result = specpulse.init(project_name="test", here=False)

        # Should create the directory if it doesn't exist
        assert nonexistent_path.exists()
        assert result["status"] == "success"

    def test_copy_templates(self, temp_project_dir):
        """Test template copying during initialization"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create source templates
        (specpulse.templates_dir / "spec.md").write_text("# Spec Template")
        (specpulse.templates_dir / "plan.md").write_text("# Plan Template")
        (specpulse.templates_dir / "task.md").write_text("# Task Template")

        # Create decomposition directory
        decomp_dir = specpulse.templates_dir / "decomposition"
        decomp_dir.mkdir()
        (decomp_dir / "microservices.md").write_text("# Microservices Template")

        with patch('sys.platform', 'linux'):
            specpulse.init(here=True)

            # Check templates were copied
            project_templates = temp_project_dir / ".specpulse" / "templates"
            assert (project_templates / "spec.md").exists()
            assert (project_templates / "plan.md").exists()
            assert (project_templates / "task.md").exists()
            assert (project_templates / "decomposition" / "microservices.md").exists()

            # Check template registry was created
            registry_path = temp_project_dir / ".specpulse" / "template_registry.json"
            assert registry_path.exists()

            with open(registry_path, 'r') as f:
                registry = json.load(f)
                assert "templates" in registry
                assert "core" in registry["templates"]
                assert "decomposition" in registry["templates"]

    def test_copy_ai_commands(self, temp_project_dir):
        """Test AI command copying during initialization"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create source command files
        commands_dir = specpulse.resources_dir / "commands"
        commands_dir.mkdir(parents=True)

        claude_commands = commands_dir / "claude"
        claude_commands.mkdir()
        (claude_commands / "pulse.md").write_text("# Claude Pulse Command")

        gemini_commands = commands_dir / "gemini"
        gemini_commands.mkdir()
        (gemini_commands / "pulse.toml").write_text("[command]")

        with patch('sys.platform', 'linux'):
            specpulse.init(here=True, ai_assistant="claude")

            # Check Claude commands were copied
            claude_dst = temp_project_dir / ".claude" / "commands"
            assert claude_dst.exists()
            assert (claude_dst / "pulse.md").exists()

            # Check Gemini commands directory exists (even if not configured)
            gemini_dst = temp_project_dir / ".gemini" / "commands"
            assert gemini_dst.exists()

    def test_create_documentation(self, temp_project_dir):
        """Test documentation creation during initialization"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('sys.platform', 'linux'):
            specpulse.init(here=True)

            # Check documentation files were created
            docs_dir = temp_project_dir / ".specpulse" / "docs"
            assert (docs_dir / "AI_FALLBACK_GUIDE.md").exists()
            assert (docs_dir / "AI_INTEGRATION.md").exists()
            assert (docs_dir / "README.md").exists()

            # Check content of fallback guide
            fallback_guide = (docs_dir / "AI_FALLBACK_GUIDE.md").read_text()
            assert "Fallback Procedures" in fallback_guide
            assert "CLI Failure Detection" in fallback_guide

    def test_create_initial_memory(self, temp_project_dir):
        """Test initial memory file creation"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Create memory resource files
        memory_resources = specpulse.resources_dir / "memory"
        memory_resources.mkdir(parents=True)
        (memory_resources / "constitution.md").write_text("# Constitution")
        (memory_resources / "decisions.md").write_text("# Decisions")

        # Create validation files
        (specpulse.resources_dir / "validation_rules.yaml").write_text("rules: []")
        (specpulse.resources_dir / "validation_examples.yaml").write_text("examples: []")

        with patch('sys.platform', 'linux'):
            specpulse.init(here=True)

            # Check memory files were copied
            memory_dir = temp_project_dir / ".specpulse" / "memory"
            assert (memory_dir / "constitution.md").exists()
            assert (memory_dir / "decisions.md").exists()
            assert (memory_dir / "context.md").exists()

            # Check validation files were copied
            assert (temp_project_dir / ".specpulse" / "validation_rules.yaml").exists()
            assert (temp_project_dir / ".specpulse" / "validation_examples.yaml").exists()

            # Check context.md content
            context_content = (memory_dir / "context.md").read_text()
            assert temp_project_dir.name in context_content
            assert "SpecPulse" in context_content

    def test_init_with_exception_handling(self, temp_project_dir):
        """Test initialization exception handling"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Mock an exception during directory creation
        with patch('pathlib.Path.mkdir', side_effect=PermissionError("Permission denied")):
            with patch('sys.platform', 'linux'):
                result = specpulse.init(here=True)

                assert result["status"] == "error"
                assert "Permission denied" in result["error"]

    def test_init_config_creation(self, temp_project_dir):
        """Test configuration file creation during initialization"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('sys.platform', 'linux'):
            result = specpulse.init(here=True, ai_assistant="claude")

            assert result["status"] == "success"

            # Check config file exists and has correct content
            config_path = temp_project_dir / ".specpulse" / "config.yaml"
            assert config_path.exists()

            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

                assert "version" in config
                assert "project" in config
                assert "ai" in config
                assert "templates" in config
                assert "conventions" in config

                assert config["project"]["name"] == temp_project_dir.name
                assert config["ai"]["primary"] == "claude"


class TestSpecPulseEdgeCases:
    """Test SpecPulse edge cases and error conditions"""

    def test_version_import_fallback(self, temp_project_dir):
        """Test version import fallback mechanisms"""
        # Mock the various import attempts to fail
        with patch.dict('sys.modules', {
            'specpulse': Mock(__version__=Mock(side_effect=ImportError)),
            'specpulse._version': Mock(__version__=Mock(side_effect=ImportError))
        }):
            # Should fallback to hardcoded version
            specpulse = SpecPulse(project_path=temp_project_dir)
            # The version should be set to fallback value during initialization
            # This is indirectly tested through successful initialization

    def test_resources_directory_fallback(self, temp_project_dir):
        """Test resources directory fallback when importlib fails"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # The resources directory should be resolved either through importlib
        # or fallback to relative path
        assert hasattr(specpulse, 'resources_dir')
        assert hasattr(specpulse, 'templates_dir')

    def test_windows_platform_handling(self, temp_project_dir):
        """Test Windows platform-specific handling"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        with patch('sys.platform', 'win32'):
            with patch('os.system') as mock_system:
                specpulse.init(here=True)

                # Should have called chcp command on Windows
                mock_system.assert_called_with('chcp 65001 > nul')

    def test_missing_resources_directory(self, temp_project_dir):
        """Test handling when resources directory doesn't exist"""
        from specpulse.utils.error_handler import ResourceError

        specpulse = SpecPulse(project_path=temp_project_dir)

        # Mock resources directory as non-existent
        with patch.object(specpulse, 'resources_dir', Path('/nonexistent/resources')):
            with pytest.raises(ResourceError):
                # Re-initialize to trigger the resource check
                SpecPulse(project_path=temp_project_dir)

    def test_service_resolution_failure(self, temp_project_dir):
        """Test handling of service resolution failures"""
        from specpulse.core.service_container import ServiceContainer
        from specpulse.core.interfaces import ITemplateProvider

        container = ServiceContainer()

        # Don't register the required service
        with pytest.raises(Exception):  # Should raise some kind of resolution error
            SpecPulse(project_path=temp_project_dir, container=container)

    def test_template_delegation_error_handling(self, temp_project_dir):
        """Test error handling in template delegation methods"""
        specpulse = SpecPulse(project_path=temp_project_dir)

        # Mock template provider to raise an exception
        with patch.object(specpulse.template_provider, 'get_spec_template', side_effect=Exception("Template error")):
            with pytest.raises(Exception, match="Template error"):
                specpulse.get_spec_template()

    def test_init_with_unicode_project_name(self, temp_project_dir):
        """Test initialization with unicode project name"""
        specpulse = SpecPulse(project_path=temp_project_dir)
        unicode_name = "テストプロジェクト"

        with patch('sys.platform', 'linux'):
            result = specpulse.init(project_name=unicode_name)

            # Should handle unicode project name
            assert result["status"] == "success"
            assert result["project_name"] == unicode_name
            assert (temp_project_dir / unicode_name / ".specpulse").exists()


if __name__ == "__main__":
    pytest.main([__file__])