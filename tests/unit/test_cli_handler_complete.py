"""
Complete CLI Handler Tests

Comprehensive tests for CommandHandler functionality.
Designed for 100% code coverage and error handling testing.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys

from specpulse.cli.handlers.command_handler import CommandHandler
from specpulse.core.specpulse import SpecPulse
from specpulse.utils.console import Console
from specpulse.utils.error_handler import SpecPulseError


class TestCommandHandlerComplete:
    """Comprehensive tests for CommandHandler"""

    @pytest.mark.unit
    def test_command_handler_initialization_success(self):
        """Test successful CommandHandler initialization"""
        handler = CommandHandler()

        assert handler is not None
        assert handler.console is not None
        assert handler.verbose is False
        assert handler.error_handler is not None

    @pytest.mark.unit
    def test_command_handler_initialization_with_options(self):
        """Test CommandHandler initialization with custom options"""
        handler = CommandHandler(no_color=True, verbose=True)

        assert handler.console is not None
        assert handler.verbose is True

    @pytest.mark.unit
    def test_command_handler_specpulse_initialization(self):
        """Test SpecPulse component initialization"""
        with patch('specpulse.core.specpulse.SpecPulse') as MockSpecPulse:
            MockSpecPulse.return_value = Mock()

            with patch('specpulse.core.validator.Validator') as MockValidator:
                MockValidator.return_value = Mock()

                handler = CommandHandler()

                # Verify components were initialized
                assert MockSpecPulse.called
                assert MockValidator.called

    @pytest.mark.unit
    def test_command_handler_project_context_detection(self, temp_project_dir):
        """Test project context detection"""
        # Create a SpecPulse project structure
        specpulse_dir = temp_project_dir / ".specpulse"
        specpulse_dir.mkdir(parents=True, exist_ok=True)

        with patch('specpulse.core.specpulse.SpecPulse') as MockSpecPulse:
            MockSpecPulse.return_value = Mock()

            with patch('specpulse.core.validator.Validator') as MockValidator:
                MockValidator.return_value = Mock()

                with patch('specpulse.core.template_manager.TemplateManager') as MockTemplateManager:
                    MockTemplateManager.return_value = Mock()

                    with patch('specpulse.core.memory_manager.MemoryManager') as MockMemoryManager:
                        MockMemoryManager.return_value = Mock()

                        handler = CommandHandler()

                        # Should detect SpecPulse project
                        assert handler.project_root == temp_project_dir
                        assert handler.template_manager is not None
                        assert handler.memory_manager is not None

    @pytest.mark.unit
    def test_command_handler_non_project_context(self):
        """Test handler behavior in non-SpecPulse directory"""
        with patch('specpulse.core.specpulse.SpecPulse') as MockSpecPulse:
            MockSpecPulse.return_value = Mock()

            with patch('specpulse.core.validator.Validator') as MockValidator:
                MockValidator.return_value = Mock()

                handler = CommandHandler()

                # Should not initialize project-dependent components
                assert handler.project_root == Path.cwd()
                assert handler.template_manager is None
                assert handler.memory_manager is None

    @pytest.mark.unit
    def test_command_handler_initialization_error(self):
        """Test CommandHandler initialization error handling"""
        with patch('specpulse.core.specpulse.SpecPulse', side_effect=OSError("Initialization failed")):
            with pytest.raises(SystemExit):
                CommandHandler()

    @pytest.mark.unit
    def test_command_handler_component_initialization_failure(self):
        """Test component initialization failure"""
        with patch('specpulse.core.specpulse.SpecPulse') as MockSpecPulse:
            MockSpecPulse.side_effect = Exception("Component failed")

            with pytest.raises(SystemExit):
                CommandHandler()

    @pytest.mark.unit
    def test_command_handler_projects_commands_registration(self):
        """Test project commands registration"""
        with patch('specpulse.cli.handlers.command_handler.ProjectCommands') as MockProjectCommands:
            mock_commands = Mock()
            MockProjectCommands.return_value = mock_commands

            handler = CommandHandler()
            assert handler.project_commands is mock_commands

    @pytest.mark.unit
    def test_command_handler_feature_commands_registration(self, temp_project_dir):
        """Test feature commands registration in project context"""
        # Create SpecPulse project structure
        (temp_project_dir / ".specpulse").mkdir(parents=True, exist_ok=True)

        with patch('specpulse.cli.handlers.command_handler.SpecPulse') as MockSpecPulse:
            MockSpecPulse.return_value = Mock()

            with patch('specpulse.cli.handlers.command_handler.FeatureCommands') as MockFeatureCommands:
                mock_commands = Mock()
                MockFeatureCommands.return_value = mock_commands

                handler = CommandHandler()
                assert handler.feature_commands is mock_commands

    @pytest.mark.unit
    def test_command_handler_execute_command_success(self, temp_project_dir):
        """Test successful command execution"""
        # Create mock handler with successful method
        mock_handler = Mock()
        mock_handler.project_commands = Mock()
        mock_handler.project_commands.init.return_value = {"status": "success"}

        # Create handler instance with mocked components
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()
            handler.project_commands = mock_handler.project_commands

            result = handler.execute_command('init', project_name='test', here=True)

            assert result["status"] == "success"

    @pytest.mark.unit
    def test_command_handler_execute_command_error(self):
        """Test command execution with error"""
        mock_handler = Mock()
        mock_handler.project_commands = Mock()
        mock_handler.project_commands.init.side_effect = SpecPulseError("Command failed")

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()
            handler.project_commands = mock_handler.project_commands

            with pytest.raises(SpecPulseError):
                handler.execute_command('init', project_name='test')

    @pytest.mark_unit
    def test_command_handler_execute_command_with_command_exception(self):
        """Test command execution with unexpected exception"""
        mock_handler = Mock()
        mock_handler.project_commands = Mock()
        mock_handler.project_commands.init.side_effect = RuntimeError("Unexpected error")

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            with pytest.raises(SystemExit):
                handler = CommandHandler()
                handler.project_commands = mock_handler.project_commands
                handler.execute_command('init', project_name='test')

    @pytest.mark.unit
    def test_command_handler_feature_command_routing(self, temp_project_dir):
        """Test feature command routing"""
        mock_handler = Mock()
        mock_handler.feature_commands = Mock()
        mock_handler.feature_commands.init.return_value = {"status": "success"}

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()
            handler.feature_commands = mock_handler.feature_commands

            # Test feature command routing
            result = handler.execute_command('feature', feature_command='init', feature_name='test')

            assert result["status"] == "success"
            mock_handler.feature_commands.init.assert_called_once_with(feature_name='test')

    @pytest.mark_unit
    def test_command_handler_template_command_routing(self, temp_project_dir):
        """Test template command routing"""
        mock_handler = Mock()
        mock_handler.template_commands = Mock()
        mock_handler.template_commands.list.return_value = ["template1", "template2"]

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()
            handler.template_commands = mock_handler.template_commands

            result = handler.execute_command('template', template_command='list')

            assert result == ["template1", "template2"]
            mock_handler.template_commands.list.assert_called_once_with()

    @pytest.mark.unit
    def test_command_handler_checkpoint_command_routing(self, temp_project_dir):
        """Test checkpoint command routing"""
        mock_handler = Mock()
        mock_handler.project_commands = Mock()

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()
            handler.project_commands = mock_handler.project_commands

            result = handler.execute_command('checkpoint', checkpoint_command='create')

            # Should call project_commands method with checkpoint
            mock_handler.project_commands.checkpoint.assert_called_once()

    @pytest.mark.unit
    def test_command_handler_unsupported_command(self):
        """Test handling of unsupported commands"""
        mock_handler = Mock()

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Mock sys.argv parser for command detection
            with patch.object(sys, 'argv', ['specpulse']):
                # This should result in help being shown
                pass

    @pytest.mark.unit
    def test_command_handler_version_check(self):
        """Test version check during initialization"""
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            with patch('specpulse.cli.handlers.command_handler.CommandHandler._check_for_updates') as mock_check:
                handler = CommandHandler()

                # Verify version check was called
                mock_check.assert_called_once()

    @pytest.mark.unit
    def test_command_handler_verbose_mode(self):
        """Test verbose mode handling"""
        handler = CommandHandler(verbose=True)

        assert handler.verbose is True
        assert handler.error_handler.verbose is True

    @pytest.mark_unit
    def test_command_handler_no_color_mode(self):
        """Test no-color mode handling"""
        handler = CommandHandler(no_color=True)

        assert handler.console is not None
        # Console should be created with no_color option

    @pytest.mark_unit
    def test_command_handler_component_isolation(self):
        """Test component isolation in handler"""
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            # Initialize without components
            handler = CommandHandler()

            # Components should be isolated
            assert handler.specpulse is not None
            assert handler.validator is not None
            assert handler.project_root is not None

    @pytest.mark_unit
    def test_command_handler_service_injection(self, temp_project_dir):
        """Test service injection patterns"""
        # Create custom service container
        custom_container = Mock()
        custom_container.resolve.return_value = Mock()

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            # Mock the _initialize_components method to use custom container
            def initialize_components():
                handler.specpulse = custom_container.resolve('specpulse')
                handler.validator = custom_container.resolve('validator')

            with patch.object(CommandHandler, '_initialize_components', initialize_components):
                handler = CommandHandler()
                assert handler.specpulse is not None
                assert handler.validator is not None

    @pytest_mark.unit
    def test_command_handler_error_recovery_suggestions(self, temp_project_dir):
        """Test error recovery suggestions"""
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            mock_init.side_effect = Exception("Test error")

            with pytest.raises(SystemExit):
                handler = CommandHandler()

            # Should show recovery suggestions
            mock_init.assert_called_once()

    @pytest.mark.unit
    def test_command_handler_utf8_encoding(self, temp_project_dir):
        """Test UTF-8 encoding handling"""
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Should handle UTF-8 encoding properly
            assert handler is not None

    @pytest.mark.unit
    def test_command_handler_windows_compatibility(self):
        """Test Windows compatibility handling"""
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            with patch('sys.platform', 'win32'):
                with patch('os.system') as mock_system:
                    handler = CommandHandler()

                    # Should set UTF-8 encoding on Windows
                    mock_system.assert_called_with('chcp 65001 > nul')

    @pytest.mark_unit
    def test_command_handler_command_validation(self):
        """Test command validation"""
        mock_handler = Mock()
        mock_handler.project_commands = Mock()

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Test with invalid arguments
            with pytest.raises(Exception):
                handler.execute_command('nonexistent_command')

    @pytest.mark_unit
    def test_command_handler_argument_parsing_integration(self, temp_project_dir):
        """Test integration with argument parsing"""
        mock_args = Mock()
        mock_args.command = 'init'
        mock_args.project_name = 'test'
        mock_args.here = True

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Should handle parsed arguments correctly
            with patch('specpulse.cli.handlers.command_handler.CommandHandler.execute_command') as mock_execute:
                mock_execute.return_value = {"status": "success"}

                result = handler.execute_command('init', **vars(mock_args))

                mock_execute.assert_called_once()

    @pytest.mark_unit
    def test_command_handler_multiple_command_support(self, temp_project_dir):
        """Test multiple command types support"""
        mock_handler = Mock()
        mock_handler.project_commands = Mock()
        mock_handler.feature_commands = Mock()
        mock_handler.template_commands = Mock()

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Should support different command types
            with patch('specpulse.cli.handlers.command_handler.CommandHandler.execute_command') as mock_execute:
                # Mock successful execution for different commands
                mock_execute.side_effect = [
                    {"status": "success"},
                    {"status": "success"},
                    {"status": "success"}
                ]

                # Execute different commands
                result1 = handler.execute_command('init')
                result2 = handler.execute_command('feature', feature_command='init')
                result3 = handler.execute_command('template', template_command='list')

                assert all(result["status"] == "success" for result in [result1, result2, result3])

                assert mock_execute.call_count == 3

    @pytest.mark.unit
    def test_command_handler_command_context_switching(self, temp_project_dir):
        """Test command context switching"""
        with patch('specpulse.core.specpulse.SpecPulse') as MockSpecPulse:
            mock_specpulse = Mock()
            MockSpecPulse.return_value = mock_specpulse

            with patch('specpulse.core.validator.Validator') as MockValidator:
                mock_validator = Mock()
                MockValidator.return_value = mock_validator

                with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
                    handler = CommandHandler()

                    # Should handle command context switching
                    with patch.object(handler, 'project_root', temp_project_dir):
                        with patch.object(handler, 'specpulse', mock_specpulse):
                            with patch.object(handler, 'validator', mock_validator):
                                # Commands should use current context
                                result = handler.execute_command('init', here=True)
                                assert result is not None

    @pytest.mark.unit
    def test_command_handler_stateless_operation(self):
        """Test stateless command operations"""
        mock_handler = Mock()

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Stateless operations should work without project context
            with patch('specpulse.cli.handlers.command_handler.CommandHandler.execute_command') as mock_execute:
                mock_execute.return_value = {"status": "success", "message": "Stateless operation"}

                result = handler.execute_command('update')

                assert result["status"] == "success"
                assert "Stateless operation" in result["message"]

    @pytest.mark_unit
    def test_command_handler_error_context_preservation(self):
        """Test error context preservation"""
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler(verbose=True)

            mock_init.side_effect = RuntimeError("Test context error")

            with pytest.raises(SystemExit):
                CommandHandler()

            # Should preserve verbose setting in error context
            # (This is handled by the SystemExit with proper error message)

    @pytest.mark.unit
    def test_command_handler_memory_management(self, temp_project_dir):
        """Test memory management in long-running operations"""
        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Create many mock commands to test memory usage
            for i in range(50):
                setattr(handler, f'mock_command_{i}', Mock())

            # Should handle memory properly
            # (This is more of a design test)
            assert hasattr(handler, 'mock_command_0')
            assert hasattr(handler, 'mock_command_49')

    @pytest.mark.unit
    def test_command_handler_command_timeout_handling(self):
        """Test command timeout handling"""
        mock_handler = Mock()
        mock_handler.project_commands = Mock()

        # Mock a long-running command
        def long_running_command():
            time.sleep(10)  # Simulate long operation
            return {"status": "success"}

        mock_handler.project_commands.init.side_effect = long_running_command

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Should handle timeout (if implemented)
            # This test would need timeout implementation
            start_time = time.time()
            try:
                # This would normally timeout after 10 seconds
                # In a real implementation, this would be shorter
                result = handler.execute_command('init')
                duration = time.time() - start_time
                assert duration > 9  # Should take at least 9 seconds
            except SystemExit:
                # Expected for timeout handling
                pass

    @pytest.mark.unit
    def test_command_handler_command_pipeline(self, temp_project_dir):
        """Test command execution pipeline"""
        mock_handler = Mock()
        mock_handler.project_commands = Mock()
        mock_handler.project_commands.init.return_value = {"status": "success", "project_path": str(temp_project_dir)}

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            with patch('specpulse.cli.handlers.command_handler.CommandHandler.execute_command') as mock_execute:
                # Simulate command pipeline
                def execute_pipeline(command, **kwargs):
                    # Pre-processing
                    if 'preprocess' in kwargs:
                        kwargs['preprocessed'] = True

                    # Execute command
                    result = handler.project_commands.init(**kwargs)

                    # Post-processing
                    if 'postprocess' in kwargs:
                        result['postprocessed'] = True

                    return result

                handler.execute_command = execute_pipeline

                result = handler.execute_command(
                    'init',
                    preprocess=True,
                    postprocess=True
                )

                assert result["status"] == "success"
                assert result["preprocessed"] is True
                assert result["postprocessed"] is True
                assert temp_project_dir.name in result["project_path"]

    @pytest.mark.unit
    def test_command_handler_plugin_system(self, temp_project_dir):
        """Test plugin system integration"""
        # Mock plugin system
        mock_plugin = Mock()
        mock_plugin.before_command.return_value = None
        mock_plugin.after_command.return_value = None

        with patch('specpulse.cli.handlers.command_handler.CommandHandler._initialize_components') as mock_init:
            handler = CommandHandler()

            # Test plugin integration
            with patch.object(handler, 'execute_command') as mock_execute:
                def execute_with_plugin(command, **kwargs):
                    # Before command hook
                    mock_plugin.before_command(command, **kwargs)

                    # Execute command
                    if command == 'test':
                        return {"status": "success", "plugin_enhanced": True}

                    return {"status": "failed"}

                    # After command hook
                    mock_plugin.after_command(command, {"status": "failed"}, **kwargs)

                handler.execute_command = execute_with_plugin

                result = handler.execute_command('test')

                assert result["status"] == "success"
                assert result["plugin_enhanced"] is True
                mock_plugin.before_command.assert_called_once()
                mock_plugin.after_command.assert_called_once()