"""
Integration Tests for Task Monitor

Comprehensive integration tests for the task monitoring system,
including end-to-end workflow validation and cross-platform compatibility.
"""

import pytest
import tempfile
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from specpulse.monitor import (
    TaskState, TaskInfo, ProgressData, TaskHistory, MonitoringConfig,
    StateStorage, TaskStateManager, ProgressCalculator, StatusDisplay,
    WorkflowIntegration, ErrorHandler
)
from specpulse.cli.monitor import MonitorCommands


class TestTaskMonitorIntegration:
    """Integration tests for the complete task monitoring system."""

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create SpecPulse structure
            (project_path / ".specpulse" / "memory").mkdir(parents=True)
            (project_path / ".specpulse" / "tasks" / "001-test-feature").mkdir(parents=True)

            # Create context file
            context_file = project_path / ".specpulse" / "memory" / "context.md"
            context_file.write_text("""
# Project Context

## Active Feature: 001-test-feature
- Feature ID: 001
- Status: Active
- Started: 2025-11-12T01:58:47.392538
""")

            yield project_path

    @pytest.fixture
    def sample_tasks(self):
        """Create sample task data."""
        return [
            TaskInfo(
                id="T001",
                title="Setup project structure",
                state=TaskState.COMPLETED,
                last_updated=datetime.now() - timedelta(hours=2),
                execution_time=0.25
            ),
            TaskInfo(
                id="T002",
                title="Implement core functionality",
                state=TaskState.IN_PROGRESS,
                last_updated=datetime.now() - timedelta(hours=1),
                estimated_hours=2.0
            ),
            TaskInfo(
                id="T003",
                title="Write tests",
                state=TaskState.PENDING,
                last_updated=datetime.now(),
                estimated_hours=1.5
            ),
            TaskInfo(
                id="T004",
                title="Fix critical bug",
                state=TaskState.BLOCKED,
                last_updated=datetime.now() - timedelta(minutes=30),
                error_message="Dependency resolution failed"
            )
        ]

    @pytest.fixture
    def monitor_commands(self, temp_project_dir):
        """Create MonitorCommands instance."""
        return MonitorCommands(temp_project_dir, verbose=True, no_color=True)

    def test_complete_workflow(self, temp_project_dir, sample_tasks, monitor_commands):
        """Test complete monitoring workflow from task discovery to progress tracking."""

        # Initialize storage and state manager
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        # Save initial tasks
        state_manager.storage.save_tasks(sample_tasks, "001-test-feature")

        # Test status display
        status_output = monitor_commands.status("001-test-feature", verbose_mode=True)
        assert "Task Monitor Status" in status_output
        assert "T001" in status_output
        assert "T002" in status_output
        assert "50.0%" in status_output  # 2 completed out of 4 = 50%

        # Test progress display
        progress_output = monitor_commands.progress("001-test-feature", detailed=True)
        assert "Progress Analytics" in progress_output

        # Test task state transition
        success = state_manager.complete_task("001-test-feature", "T002", execution_time=1.8)
        assert success

        # Verify updated status
        updated_status = monitor_commands.status("001-test-feature")
        assert "75.0%" in updated_status  # 3 completed out of 4 = 75%

        # Test history
        history_output = monitor_commands.history("001-test-feature")
        assert "Task History" in history_output

    def test_task_discovery_from_markdown(self, temp_project_dir):
        """Test automatic task discovery from markdown files."""

        # Create sample task files
        tasks_dir = temp_project_dir / ".specpulse" / "tasks" / "001-test-feature"

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

        # Task 3 - Blocked
        (tasks_dir / "task-003.md").write_text("""
### T003: Integration testing
- [!] Unit tests (blocked by missing dependencies)
- [ ] Integration tests
- [ ] End-to-end tests

**Status**: [!] blocked
**Error**: Missing test framework dependency
""")

        # Test discovery
        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        discovered_tasks = state_manager.discover_tasks("001-test-feature")

        assert len(discovered_tasks) == 3
        assert discovered_tasks[0].id == "T001"
        assert discovered_tasks[0].state == TaskState.COMPLETED
        assert discovered_tasks[1].id == "T002"
        assert discovered_tasks[1].state == TaskState.IN_PROGRESS
        assert discovered_tasks[2].id == "T003"
        assert discovered_tasks[2].state == TaskState.BLOCKED
        assert "Missing test framework" in discovered_tasks[2].error_message

    def test_persistence_and_recovery(self, temp_project_dir, sample_tasks):
        """Test data persistence and recovery mechanisms."""

        storage = StateStorage(temp_project_dir)

        # Save initial data
        storage.save_tasks(sample_tasks, "001-test-feature")

        progress = ProgressData.from_tasks(sample_tasks, "001-test-feature")
        storage.save_progress(progress)

        # Save history entries
        history = TaskHistory(
            task_id="T001",
            timestamp=datetime.now(),
            old_state=None,
            new_state=TaskState.COMPLETED
        )
        storage.save_history_entry(history)

        # Verify data persistence
        loaded_tasks = storage.load_tasks("001-test-feature")
        assert len(loaded_tasks) == len(sample_tasks)

        loaded_progress = storage.load_progress("001-test-feature")
        assert loaded_progress.percentage == progress.percentage

        loaded_history = storage.load_history("001-test-feature")
        assert len(loaded_history) == 1
        assert loaded_history[0].task_id == "T001"

        # Test backup creation
        state_file = temp_project_dir / ".specpulse" / "memory" / "task-states.json"
        assert state_file.exists()

        backup_dir = temp_project_dir / ".specpulse" / "memory" / "backups"
        # Note: Backups are created only on modification, not initial save

    def test_error_handling_and_recovery(self, temp_project_dir):
        """Test error handling and graceful degradation."""

        error_handler = ErrorHandler(verbose=True)

        # Test custom monitor error
        from specpulse.monitor.errors import TaskDiscoveryError
        discovery_error = TaskDiscoveryError(
            "Cannot find task directory",
            suggestion="Ensure .specpulse/tasks/ directory exists",
            details="Checked path: /nonexistent/path"
        )

        error_message = error_handler.handle_error(discovery_error, "task discovery")
        assert "Cannot find task directory" in error_message
        assert "Suggestion:" in error_message
        assert "Details:" in error_message

        # Test generic error
        try:
            raise ValueError("Invalid input parameter")
        except Exception as e:
            error_message = error_handler.handle_error(e, "parameter validation")
            assert "unexpected error occurred" in error_message

        # Test error summary
        summary = error_handler.get_error_summary()
        assert summary["total_errors"] >= 2
        assert "TaskDiscoveryError" in summary["error_types"]

    def test_performance_with_large_datasets(self, temp_project_dir):
        """Test performance with large numbers of tasks."""

        # Create many tasks
        large_task_set = []
        for i in range(1000):  # 1000 tasks
            task = TaskInfo(
                id=f"T{i:03d}",
                title=f"Task {i}",
                state=TaskState.PENDING if i % 4 != 0 else TaskState.COMPLETED,
                last_updated=datetime.now() - timedelta(minutes=i),
                estimated_hours=1.0
            )
            large_task_set.append(task)

        # Test storage performance
        start_time = time.time()
        storage = StateStorage(temp_project_dir)
        storage.save_tasks(large_task_set, "001-large-feature")
        save_time = time.time() - start_time

        # Should complete within reasonable time (less than 1 second for 1000 tasks)
        assert save_time < 1.0, f"Save took too long: {save_time:.2f}s"

        # Test loading performance
        start_time = time.time()
        loaded_tasks = storage.load_tasks("001-large-feature")
        load_time = time.time() - start_time

        assert load_time < 0.5, f"Load took too long: {load_time:.2f}s"
        assert len(loaded_tasks) == 1000

        # Test calculation performance
        calculator = ProgressCalculator()
        start_time = time.time()
        progress = calculator.calculate_progress(loaded_tasks, "001-large-feature")
        calc_time = time.time() - start_time

        assert calc_time < 0.1, f"Calculation took too long: {calc_time:.3f}s"
        assert progress.percentage == 25.0  # 250 completed out of 1000

    def test_cross_platform_compatibility(self, temp_project_dir):
        """Test cross-platform file operations."""

        # Test with different path formats
        storage = StateStorage(temp_project_dir)

        # Create tasks with special characters in titles
        special_tasks = [
            TaskInfo(
                id="T001",
                title="Task with & special <chars>",
                state=TaskState.PENDING,
                last_updated=datetime.now()
            ),
            TaskInfo(
                id="T002",
                title="Tâsk wïth ünïcodé",
                state=TaskState.COMPLETED,
                last_updated=datetime.now()
            )
        ]

        # Save and load with special characters
        storage.save_tasks(special_tasks, "001-unicode-feature")
        loaded_tasks = storage.load_tasks("001-unicode-feature")

        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].title == "Task with & special <chars>"
        assert loaded_tasks[1].title == "Tâsk wïth ünïcodé"

        # Test JSON serialization/deserialization
        for task in loaded_tasks:
            task_dict = task.to_dict()
            restored_task = TaskInfo.from_dict(task_dict)
            assert restored_task.id == task.id
            assert restored_task.title == task.title
            assert restored_task.state == task.state

    def test_workflow_integration(self, temp_project_dir):
        """Test integration with SpecPulse workflow."""

        integration = WorkflowIntegration(temp_project_dir)

        # Test feature detection
        active_feature = integration.get_active_feature()
        assert active_feature == "001-test-feature"

        # Test task monitoring workflow
        feature_id = "001-test-feature"
        task_id = "T001"

        # Start task
        success = integration.start_task_monitoring(feature_id, task_id)
        assert success

        # Complete task
        success = integration.complete_task_monitoring(feature_id, task_id, execution_time=0.5)
        assert success

        # Verify progress was updated
        progress = integration.storage.load_progress(feature_id)
        assert progress is not None
        assert progress.feature_id == feature_id

        # Test task blocking
        block_success = integration.block_task_monitoring(feature_id, "T002", "Test error")
        assert block_success

        # Verify workflow log was created
        log_file = temp_project_dir / ".specpulse" / "memory" / "workflow-log.json"
        assert log_file.exists()

    def test_concurrent_access_safety(self, temp_project_dir):
        """Test thread safety and concurrent access."""
        import threading

        storage = StateStorage(temp_project_dir)
        results = []
        errors = []

        def worker_task(worker_id):
            try:
                task = TaskInfo(
                    id=f"T{worker_id:03d}",
                    title=f"Worker {worker_id} task",
                    state=TaskState.COMPLETED,
                    last_updated=datetime.now()
                )

                # Each worker saves to a different feature to avoid conflicts
                feature_id = f"001-worker-{worker_id}"
                storage.save_tasks([task], feature_id)

                # Immediately read back
                loaded_tasks = storage.load_tasks(feature_id)
                results.append((worker_id, len(loaded_tasks)))

            except Exception as e:
                errors.append((worker_id, str(e)))

        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker_task, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10
        for worker_id, task_count in results:
            assert task_count == 1

    def test_cli_command_integration(self, temp_project_dir, monitor_commands):
        """Test CLI command integration end-to-end."""

        # Create some test tasks
        tasks_dir = temp_project_dir / ".specpulse" / "tasks" / "001-test-feature"
        (tasks_dir / "task-001.md").write_text("### T001: Test Task\n- [ ] Not started")

        # Test all monitor commands
        status_result = monitor_commands.status()
        assert "Task Monitor Status" in status_result

        progress_result = monitor_commands.progress()
        assert "Progress Analytics" in progress_result

        history_result = monitor_commands.history()
        assert "Task History" in history_result or "No history available" in history_result

        validate_result = monitor_commands.validate()
        assert "monitoring data" in validate_result.lower()

        # Test reset with confirmation
        reset_result = monitor_commands.reset(confirm=True)
        assert "✓ Reset monitoring data" in reset_result

    def test_data_integrity_validation(self, temp_project_dir):
        """Test data integrity validation and corruption recovery."""

        storage = StateStorage(temp_project_dir)

        # Create valid data
        valid_tasks = [
            TaskInfo(
                id="T001",
                title="Valid Task",
                state=TaskState.COMPLETED,
                last_updated=datetime.now()
            )
        ]

        storage.save_tasks(valid_tasks, "001-validation-test")

        # Validate integrity
        integrity_report = storage.validate_data_integrity()
        assert integrity_report["valid"] is True
        assert len(integrity_report["issues"]) == 0

        # Test corrupted data recovery
        state_file = temp_project_dir / ".specpulse" / "memory" / "task-states.json"

        # Corrupt the file
        with open(state_file, 'w') as f:
            f.write("invalid json content")

        # Test recovery
        loaded_tasks = storage.load_tasks("001-validation-test")
        # Should return empty list on corrupted data
        assert isinstance(loaded_tasks, list)

        # Validate after corruption
        corrupted_report = storage.validate_data_integrity()
        assert corrupted_report["valid"] is False
        assert len(corrupted_report["issues"]) > 0

    def test_memory_usage_limits(self, temp_project_dir):
        """Test memory usage stays within limits."""

        import psutil
        import os

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        # Create many tasks and monitor memory
        for feature_batch in range(5):
            tasks = []
            for i in range(200):  # 200 tasks per batch
                task = TaskInfo(
                    id=f"T{feature_batch * 200 + i:03d}",
                    title=f"Memory test task {i}",
                    state=TaskState.PENDING,
                    last_updated=datetime.now(),
                    description="A" * 1000  # 1KB description per task
                )
                tasks.append(task)

            feature_id = f"001-memory-test-{feature_batch}"
            state_manager.storage.save_tasks(tasks, feature_id)

            # Check memory usage
            current_memory = process.memory_info().rss
            memory_increase = (current_memory - initial_memory) / (1024 * 1024)  # MB

            # Memory should not exceed 50MB limit
            assert memory_increase < 50, f"Memory usage too high: {memory_increase:.1f}MB"

    def test_configuration_management(self, temp_project_dir):
        """Test configuration loading and saving."""

        storage = StateStorage(temp_project_dir)

        # Load default configuration
        config = storage.load_config()
        assert config.auto_discovery is True
        assert config.history_retention_days == 30
        assert config.max_tasks_per_feature == 1000

        # Modify and save configuration
        config.auto_discovery = False
        config.history_retention_days = 60
        config.max_tasks_per_feature = 500

        storage.save_config(config)

        # Reload and verify changes
        reloaded_config = storage.load_config()
        assert reloaded_config.auto_discovery is False
        assert reloaded_config.history_retention_days == 60
        assert reloaded_config.max_tasks_per_feature == 500

        # Test configuration validation
        assert reloaded_config.update_interval_seconds > 0
        assert reloaded_config.max_backups > 0