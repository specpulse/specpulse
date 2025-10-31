"""
Tests for CommandHandler

These tests verify the refactored CLI command handler functionality.
"""

import pytest
from pathlib import Path
import tempfile
from unittest.mock import Mock, patch, MagicMock

from specpulse.cli.handlers.command_handler import CommandHandler
from specpulse.utils.error_handler import SpecPulseError


class TestCommandHandler:
    """Test CommandHandler functionality"""

    def test_command_handler_initialization(self):
        """Test that CommandHandler initializes correctly"""
        handler = CommandHandler(no_color=True, verbose=False)

        assert handler is not None
        assert handler.console is not None
        assert handler.error_handler is not None
        assert handler.specpulse is not None
        assert handler.validator is not None

    def test_command_handler_verbose_mode(self):
        """Test verbose mode initialization"""
        handler = CommandHandler(verbose=True)

        assert handler.verbose is True
        assert handler.error_handler.verbose is True

    def test_command_handler_no_color_mode(self):
        """Test no-color mode initialization"""
        handler = CommandHandler(no_color=True)

        assert handler.console is not None

    @patch('specpulse.cli.handlers.command_handler.SpecPulse')
    def test_command_execution_routing(self, mock_specpulse):
        """Test that commands are routed correctly"""
        handler = CommandHandler()

        # Test that command routing works
        assert hasattr(handler, 'execute_command')
        assert callable(handler.execute_command)

    def test_is_specpulse_project_detection(self):
        """Test project detection"""
        handler = CommandHandler()

        # Test with non-project directory
        assert handler._is_specpulse_project(Path("/tmp")) is False

    def test_project_commands_available(self):
        """Test that project commands are available"""
        handler = CommandHandler()

        assert hasattr(handler, 'project_commands')
        assert handler.project_commands is not None

    def test_error_handling_in_command_execution(self):
        """Test error handling during command execution"""
        handler = CommandHandler()

        # Test unknown command
        with pytest.raises(SpecPulseError, match="Unknown command"):
            handler.execute_command('nonexistent_command')


class TestProjectCommands:
    """Test project-level commands"""

    def test_doctor_command_structure(self):
        """Test doctor command is callable"""
        from specpulse.cli.commands.project_commands import ProjectCommands
        from specpulse.utils.console import Console

        console = Console()
        project_root = Path.cwd()
        commands = ProjectCommands(console, project_root)

        assert hasattr(commands, 'doctor')
        assert callable(commands.doctor)

    def test_update_command_structure(self):
        """Test update command is callable"""
        from specpulse.cli.commands.project_commands import ProjectCommands
        from specpulse.utils.console import Console

        console = Console()
        project_root = Path.cwd()
        commands = ProjectCommands(console, project_root)

        assert hasattr(commands, 'update')
        assert callable(commands.update)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
