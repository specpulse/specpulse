"""
CLI Commands Tests for Monitor

Comprehensive tests for monitor CLI commands including all command options,
error handling, and output validation.
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from specpulse.cli.monitor import MonitorCommands
from specpulse.monitor import (
    TaskState, TaskInfo, ProgressData, TaskHistory, MonitoringConfig,
    StateStorage, TaskStateManager
)


class TestMonitorCommands:
    """Test suite for MonitorCommands CLI interface."""

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory with SpecPulse structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create SpecPulse directory structure
            (project_path / ".specpulse" / "memory").mkdir(parents=True)
            (project_path / ".specpulse" / "tasks" / "001-test-feature").mkdir(parents=True)

            # Create sample task files
            tasks_dir = project_path / ".specpulse" / "tasks" / "001-test-feature"

            # Task 1 - Completed
            (tasks_dir / "task-001.md").write_text("""
### T001: Setup project structure
- [x] Create directory structure
- [x] Initialize configuration

**Status**: [x] completed
""")

            # Task 2 - In Progress
            (tasks_dir / "task-002.md").write_text("""
### T002: Implement core functionality
- [>] Database setup
- [ ] API implementation
- [ ] User interface

**Status**: [>] in_progress
""")

            # Task 3 - Pending
            (tasks_dir / "task-003.md").write_text("""
### T003: Write documentation
- [ ] API documentation
- [ ] User guide
- [ ] Developer guide

**Status**: [ ] pending
""")

            yield project_path

    @pytest.fixture
    def monitor_commands(self, temp_project_dir):
        """Create MonitorCommands instance for testing."""
        return MonitorCommands(temp_project_dir, verbose=False, no_color=True)

    @pytest.fixture
    def monitor_commands_verbose(self, temp_project_dir):
        """Create MonitorCommands instance with verbose mode."""
        return MonitorCommands(temp_project_dir, verbose=True, no_color=True)

    def test_status_command_basic(self, temp_project_dir, monitor_commands):
        """Test basic status command functionality."""

        # Create monitor data first
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        # Discover and save tasks
        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test status command
        status_output = monitor_commands.status("001-test-feature")

        assert "Task Monitor Status" in status_output
        assert "T001" in status_output
        assert "T002" in status_output
        assert "T003" in status_output
        assert "completed" in status_output.lower()
        assert "in_progress" in status_output.lower()
        assert "pending" in status_output.lower()

    def test_status_command_auto_discover(self, temp_project_dir, monitor_commands):
        """Test status command with automatic feature discovery."""

        # Create monitor data first
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        # Discover and save tasks
        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test status without specifying feature_id
        status_output = monitor_commands.status()

        assert "Task Monitor Status" in status_output
        assert "T001" in status_output

    def test_status_command_no_features(self, temp_project_dir, monitor_commands):
        """Test status command when no features exist."""

        status_output = monitor_commands.status()

        assert "No active features found" in status_output
        assert "Initialize a feature first" in status_output

    def test_status_command_no_tasks(self, temp_project_dir, monitor_commands):
        """Test status command when feature exists but has no tasks."""

        # Create feature without tasks
        (temp_project_dir / ".specpulse" / "memory" / "context.md").write_text("""
# Project Context
## Active Feature: 002-empty-feature
- Feature ID: 002
- Status: Active
""")

        status_output = monitor_commands.status("002-empty-feature")

        assert "No tasks found for feature 002-empty-feature" in status_output

    def test_status_command_verbose_mode(self, temp_project_dir, monitor_commands_verbose):
        """Test status command in verbose mode."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test verbose status
        status_output = monitor_commands_verbose.status("001-test-feature", verbose_mode=True)

        assert "Task Monitor Status" in status_output
        assert "T001" in status_output
        # Verbose mode should show more details
        assert len(status_output) > 200  # Should be substantial output

    def test_progress_command_basic(self, temp_project_dir, monitor_commands):
        """Test basic progress command functionality."""

        # Create monitor data with history
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Create some history
        history = TaskHistory(
            task_id="T001",
            timestamp=datetime.now() - timedelta(hours=1),
            old_state=TaskState.PENDING,
            new_state=TaskState.COMPLETED
        )
        storage.save_history_entry(history)

        # Test progress command
        progress_output = monitor_commands.progress("001-test-feature")

        assert "Progress Analytics" in progress_output

    def test_progress_command_detailed(self, temp_project_dir, monitor_commands):
        """Test progress command with detailed output."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test detailed progress
        progress_output = monitor_commands.progress("001-test-feature", detailed=True)

        assert "Progress Analytics" in progress_output
        # Detailed mode should show more information
        assert len(progress_output) > 100

    def test_progress_command_auto_discover(self, temp_project_dir, monitor_commands):
        """Test progress command with automatic feature discovery."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test progress without specifying feature_id
        progress_output = monitor_commands.progress()

        assert "Progress Analytics" in progress_output

    def test_progress_command_no_features(self, temp_project_dir, monitor_commands):
        """Test progress command when no features exist."""

        progress_output = monitor_commands.progress()

        assert "No active features found" in progress_output
        assert "Initialize a feature first" in progress_output

    def test_history_command_basic(self, temp_project_dir, monitor_commands):
        """Test basic history command functionality."""

        # Create monitor data with history
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Create multiple history entries
        now = datetime.now()
        history_entries = [
            TaskHistory(
                task_id="T001",
                timestamp=now - timedelta(hours=3),
                old_state=TaskState.PENDING,
                new_state=TaskState.IN_PROGRESS
            ),
            TaskHistory(
                task_id="T001",
                timestamp=now - timedelta(hours=2),
                old_state=TaskState.IN_PROGRESS,
                new_state=TaskState.COMPLETED
            ),
            TaskHistory(
                task_id="T002",
                timestamp=now - timedelta(hours=1),
                old_state=TaskState.PENDING,
                new_state=TaskState.IN_PROGRESS
            )
        ]

        for history in history_entries:
            storage.save_history_entry(history)

        # Test history command
        history_output = monitor_commands.history("001-test-feature")

        assert "Task History" in history_output
        assert "T001" in history_output
        assert "T002" in history_output

    def test_history_command_with_limit(self, temp_project_dir, monitor_commands):
        """Test history command with limit parameter."""

        # Create monitor data with many history entries
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Create many history entries
        now = datetime.now()
        for i in range(25):  # Create 25 entries
            history = TaskHistory(
                task_id=f"T{(i % 3) + 1:03d}",
                timestamp=now - timedelta(minutes=i * 5),
                old_state=TaskState.PENDING,
                new_state=TaskState.COMPLETED if i % 2 == 0 else TaskState.IN_PROGRESS
            )
            storage.save_history_entry(history)

        # Test history with limit
        history_output = monitor_commands.history("001-test-feature", limit=10)

        assert "Task History" in history_output
        # Should show limited history
        assert len(history_output.split('\n')) < 50  # Reasonable length limit

    def test_history_command_no_history(self, temp_project_dir, monitor_commands):
        """Test history command when no history exists."""

        # Create monitor data without history
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test history command
        history_output = monitor_commands.history("001-test-feature")

        assert "No history found for feature 001-test-feature" in history_output

    def test_reset_command_without_confirmation(self, temp_project_dir, monitor_commands):
        """Test reset command without confirmation flag."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test reset without confirmation
        reset_output = monitor_commands.reset("001-test-feature", confirm=False)

        assert "Use --confirm to reset" in reset_output
        assert "001-test-feature" in reset_output

        # Verify data still exists
        loaded_tasks = storage.load_tasks("001-test-feature")
        assert len(loaded_tasks) > 0

    def test_reset_command_with_confirmation(self, temp_project_dir, monitor_commands):
        """Test reset command with confirmation flag."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test reset with confirmation
        reset_output = monitor_commands.reset("001-test-feature", confirm=True)

        assert "✓ Reset monitoring data" in reset_output
        assert "001-test-feature" in reset_output

        # Verify data was reset
        loaded_tasks = storage.load_tasks("001-test-feature")
        assert len(loaded_tasks) == 0

    def test_reset_command_auto_discover(self, temp_project_dir, monitor_commands):
        """Test reset command with automatic feature discovery."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test reset without specifying feature_id
        reset_output = monitor_commands.reset(confirm=True)

        assert "✓ Reset monitoring data" in reset_output

    def test_validate_command_valid_data(self, temp_project_dir, monitor_commands):
        """Test validate command with valid data."""

        # Create valid monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Test validation
        validate_output = monitor_commands.validate()

        assert "✓ All monitoring data is valid" in validate_output
        assert "Files checked:" in validate_output

    def test_validate_command_corrupted_data(self, temp_project_dir, monitor_commands):
        """Test validate command with corrupted data."""

        # Create corrupted state file
        state_file = temp_project_dir / ".specpulse" / "memory" / "task-states.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)

        with open(state_file, 'w') as f:
            f.write("invalid json content")

        # Test validation
        validate_output = monitor_commands.validate()

        assert "⚠ Issues found" in validate_output
        assert "Files checked:" in validate_output
        assert "Issues:" in validate_output
        assert "❌" in validate_output

    def test_sync_command_full(self, temp_project_dir, monitor_commands):
        """Test sync command with full synchronization."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Mock TaskFileSyncManager
        with patch('specpulse.cli.monitor.TaskFileSyncManager') as mock_sync:
            mock_manager = Mock()
            mock_sync.return_value = mock_manager
            mock_manager.full_sync.return_value = {
                'total_discrepancies': 0,
                'files_updated': 0,
                'file_to_monitor': {'discrepancies': {}}
            }

            # Test full sync
            sync_output = monitor_commands.sync("001-test-feature", direction="full")

            assert "🔄 Full synchronization completed" in sync_output
            assert "001-test-feature" in sync_output
            assert "Discrepancies found: 0" in sync_output
            assert "Task files updated: 0" in sync_output

            mock_manager.full_sync.assert_called_once_with("001-test-feature")

    def test_sync_command_to_files(self, temp_project_dir, monitor_commands):
        """Test sync command with to_files direction."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Mock TaskFileSyncManager
        with patch('specpulse.cli.monitor.TaskFileSyncManager') as mock_sync:
            mock_manager = Mock()
            mock_sync.return_value = mock_manager
            mock_manager.sync_from_monitor_to_files.return_value = {
                'T001': True,
                'T002': True,
                'T003': False
            }

            # Test sync to files
            sync_output = monitor_commands.sync("001-test-feature", direction="to_files")

            assert "📝 Synced monitor states to task files" in sync_output
            assert "001-test-feature" in sync_output
            assert "Tasks updated: 2/3" in sync_output
            assert "Failed to update: T003" in sync_output

            mock_manager.sync_from_monitor_to_files.assert_called_once_with("001-test-feature")

    def test_sync_command_from_files(self, temp_project_dir, monitor_commands):
        """Test sync command with from_files direction."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Mock TaskFileSyncManager
        with patch('specpulse.cli.monitor.TaskFileSyncManager') as mock_sync:
            mock_manager = Mock()
            mock_sync.return_value = mock_manager
            mock_manager.sync_from_files_to_monitor.return_value = {
                'total_files': 3,
                'synced_count': 2,
                'discrepancies': {
                    'T001': {
                        'action': 'updated',
                        'file_state': 'completed',
                        'monitor_state': 'pending'
                    }
                }
            }

            # Test sync from files
            sync_output = monitor_commands.sync("001-test-feature", direction="from_files")

            assert "📖 Synced task file states to monitor" in sync_output
            assert "001-test-feature" in sync_output
            assert "Files scanned: 3" in sync_output
            assert "Tasks synced: 2" in sync_output
            assert "Discrepancies found:" in sync_output
            assert "T001: updated (pending → completed)" in sync_output

            mock_manager.sync_from_files_to_monitor.assert_called_once_with("001-test-feature")

    def test_sync_command_invalid_direction(self, temp_project_dir, monitor_commands):
        """Test sync command with invalid direction."""

        sync_output = monitor_commands.sync("001-test-feature", direction="invalid")

        assert "❌ Invalid sync direction" in sync_output
        assert "invalid" in sync_output
        assert "Use 'full', 'to_files', or 'from_files'" in sync_output

    def test_sync_command_auto_discover(self, temp_project_dir, monitor_commands):
        """Test sync command with automatic feature discovery."""

        # Create monitor data
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        tasks = state_manager.discover_tasks("001-test-feature")
        state_manager.storage.save_tasks(tasks, "001-test-feature")

        # Mock TaskFileSyncManager
        with patch('specpulse.cli.monitor.TaskFileSyncManager') as mock_sync:
            mock_manager = Mock()
            mock_sync.return_value = mock_manager
            mock_manager.full_sync.return_value = {
                'total_discrepancies': 0,
                'files_updated': 0,
                'file_to_monitor': {'discrepancies': {}}
            }

            # Test sync without specifying feature_id
            sync_output = monitor_commands.sync(direction="full")

            assert "🔄 Full synchronization completed" in sync_output

    def test_error_handling_verbose_mode(self, temp_project_dir, monitor_commands_verbose):
        """Test error handling in verbose mode."""

        # Test with invalid feature that doesn't exist
        error_output = monitor_commands_verbose.status("999-nonexistent")

        assert "Error getting status" in error_output
        # Verbose mode should include traceback
        assert "Traceback" in error_output or "traceback" in error_output.lower()

    def test_error_handling_normal_mode(self, temp_project_dir, monitor_commands):
        """Test error handling in normal mode."""

        # Test with invalid feature that doesn't exist
        error_output = monitor_commands.status("999-nonexistent")

        assert "Error getting status" in error_output
        # Normal mode should not include traceback
        assert "Traceback" not in error_output and "traceback" not in error_output.lower()

    def test_command_parameter_validation(self, monitor_commands):
        """Test command parameter validation."""

        # Test with None parameters (should use defaults)
        with patch.object(monitor_commands, 'storage') as mock_storage:
            mock_storage.get_all_features.return_value = []

            # These should not raise errors
            result1 = monitor_commands.status()
            result2 = monitor_commands.progress()
            result3 = monitor_commands.history()
            result4 = monitor_commands.reset()

            assert "No active features found" in result1
            assert "No active features found" in result2
            assert "No active features found" in result3
            assert "Use --confirm to reset" in result4

    def test_initialize_with_different_options(self, temp_project_dir):
        """Test MonitorCommands initialization with different options."""

        # Test default initialization
        cmd1 = MonitorCommands(temp_project_dir)
        assert cmd1.verbose is False
        assert cmd1.no_color is False

        # Test with verbose enabled
        cmd2 = MonitorCommands(temp_project_dir, verbose=True)
        assert cmd2.verbose is True
        assert cmd2.no_color is False

        # Test with no_color enabled
        cmd3 = MonitorCommands(temp_project_dir, no_color=True)
        assert cmd3.verbose is False
        assert cmd3.no_color is True

        # Test with both options enabled
        cmd4 = MonitorCommands(temp_project_dir, verbose=True, no_color=True)
        assert cmd4.verbose is True
        assert cmd4.no_color is True

        # All should have proper components initialized
        for cmd in [cmd1, cmd2, cmd3, cmd4]:
            assert hasattr(cmd, 'config')
            assert hasattr(cmd, 'storage')
            assert hasattr(cmd, 'state_manager')
            assert hasattr(cmd, 'progress_calculator')
            assert hasattr(cmd, 'display')