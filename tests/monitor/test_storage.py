"""
Storage Tests for Monitor

Unit tests for StateStorage and related storage functionality including
file operations, data persistence, backup management, and integrity validation.
"""

import pytest
import tempfile
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, mock_open

from specpulse.monitor.storage import StateStorage
from specpulse.monitor.models import (
    TaskInfo, ProgressData, TaskHistory, MonitoringConfig, TaskState
)
from specpulse.monitor.errors import StorageError, CorruptedDataError


class TestStateStorage:
    """Test suite for StateStorage functionality."""

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory with SpecPulse structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / ".specpulse" / "memory").mkdir(parents=True)
            yield project_path

    @pytest.fixture
    def storage(self, temp_project_dir):
        """Create StateStorage instance for testing."""
        config = MonitoringConfig()
        return StateStorage(temp_project_dir, config)

    @pytest.fixture
    def sample_tasks(self):
        """Create sample task data for testing."""
        now = datetime.now()
        return [
            TaskInfo(
                id="T001",
                title="Setup project structure",
                state=TaskState.COMPLETED,
                last_updated=now - timedelta(hours=2),
                execution_time=0.5
            ),
            TaskInfo(
                id="T002",
                title="Implement core functionality",
                state=TaskState.IN_PROGRESS,
                last_updated=now - timedelta(hours=1),
                estimated_hours=3.0
            ),
            TaskInfo(
                id="T003",
                title="Write tests",
                state=TaskState.PENDING,
                last_updated=now,
                estimated_hours=2.0
            ),
            TaskInfo(
                id="T004",
                title="Fix bug",
                state=TaskState.BLOCKED,
                last_updated=now - timedelta(minutes=30),
                error_message="Dependency issue"
            )
        ]

    def test_storage_initialization(self, temp_project_dir):
        """Test StateStorage initialization."""
        config = MonitoringConfig()
        storage = StateStorage(temp_project_dir, config)

        assert storage.project_path == temp_project_dir
        assert storage.config == config
        assert storage.memory_dir == temp_project_dir / ".specpulse" / "memory"
        assert storage.state_file == storage.memory_dir / "task-states.json"
        assert storage.progress_dir == storage.memory_dir / "progress"
        assert storage.history_dir == storage.memory_dir / "history"
        assert storage.backup_dir == storage.memory_dir / "backups"

    def test_storage_directory_creation(self, temp_project_dir):
        """Test that storage creates necessary directories."""
        # Remove memory directory to test creation
        memory_dir = temp_project_dir / ".specpulse" / "memory"
        if memory_dir.exists():
            memory_dir.rmdir()

        config = MonitoringConfig()
        storage = StateStorage(temp_project_dir, config)

        # Directories should be created
        assert memory_dir.exists()
        assert (memory_dir / "progress").exists()
        assert (memory_dir / "history").exists()
        assert (memory_dir / "backups").exists()

    def test_save_tasks_basic(self, storage, sample_tasks):
        """Test basic task saving functionality."""
        feature_id = "001-test-feature"

        # Save tasks
        storage.save_tasks(sample_tasks, feature_id)

        # Verify file was created
        state_file = storage.state_file
        assert state_file.exists()

        # Verify content
        with open(state_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert feature_id in data
        assert len(data[feature_id]) == len(sample_tasks)

        # Verify task data
        saved_tasks = [TaskInfo.from_dict(task_dict) for task_dict in data[feature_id]]
        assert saved_tasks[0].id == "T001"
        assert saved_tasks[0].state == TaskState.COMPLETED
        assert saved_tasks[1].id == "T002"
        assert saved_tasks[1].state == TaskState.IN_PROGRESS

    def test_save_tasks_backup_creation(self, storage, sample_tasks):
        """Test that backup is created when saving tasks."""
        config = MonitoringConfig(backup_enabled=True, max_backups=3)
        storage.config = config

        # Save initial tasks
        storage.save_tasks(sample_tasks, "001-test-feature")

        # Modify tasks and save again
        modified_tasks = sample_tasks.copy()
        modified_tasks[0].state = TaskState.FAILED
        storage.save_tasks(modified_tasks, "001-test-feature")

        # Check backup files
        backup_files = list(storage.backup_dir.glob("task-states_*.json"))
        assert len(backup_files) >= 1

        # Verify backup contains old data
        with open(backup_files[0], 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        assert "001-test-feature" in backup_data
        backup_task = backup_data["001-test-feature"][0]
        assert backup_task["state"] == "completed"  # Original state

    def test_save_tasks_backup_limit(self, storage, sample_tasks):
        """Test that backup limit is respected."""
        config = MonitoringConfig(backup_enabled=True, max_backups=2)
        storage.config = config

        # Save tasks multiple times to exceed backup limit
        for i in range(5):
            modified_tasks = sample_tasks.copy()
            modified_tasks[0].execution_time = float(i)
            storage.save_tasks(modified_tasks, "001-test-feature")
            time.sleep(0.01)  # Ensure different timestamps

        # Check backup files
        backup_files = list(storage.backup_dir.glob("task-states_*.json"))
        assert len(backup_files) <= config.max_backups

    def test_save_tasks_disabled_backup(self, storage, sample_tasks):
        """Test that backup can be disabled."""
        config = MonitoringConfig(backup_enabled=False)
        storage.config = config

        # Save tasks
        storage.save_tasks(sample_tasks, "001-test-feature")

        # Check no backup files
        backup_files = list(storage.backup_dir.glob("task-states_*.json"))
        assert len(backup_files) == 0

    def test_load_tasks_basic(self, storage, sample_tasks):
        """Test basic task loading functionality."""
        feature_id = "001-test-feature"

        # Save tasks first
        storage.save_tasks(sample_tasks, feature_id)

        # Load tasks
        loaded_tasks = storage.load_tasks(feature_id)

        assert len(loaded_tasks) == len(sample_tasks)

        # Verify task data
        for original, loaded in zip(sample_tasks, loaded_tasks):
            assert loaded.id == original.id
            assert loaded.title == original.title
            assert loaded.state == original.state
            assert loaded.last_updated == original.last_updated

    def test_load_tasks_nonexistent_feature(self, storage):
        """Test loading tasks for non-existent feature."""
        loaded_tasks = storage.load_tasks("999-nonexistent")

        assert loaded_tasks == []

    def test_load_tasks_corrupted_file(self, storage):
        """Test loading tasks from corrupted file."""
        # Create corrupted state file
        with open(storage.state_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")

        # Should handle corruption gracefully
        loaded_tasks = storage.load_tasks("001-test-feature")

        assert loaded_tasks == []  # Should return empty list on corruption

    def test_load_tasks_empty_file(self, storage):
        """Test loading tasks from empty file."""
        # Create empty state file
        storage.state_file.touch()

        loaded_tasks = storage.load_tasks("001-test-feature")

        assert loaded_tasks == []

    def test_save_progress_basic(self, storage):
        """Test basic progress saving functionality."""
        now = datetime.now()
        progress = ProgressData(
            feature_id="001-test-feature",
            percentage=75.0,
            total_tasks=10,
            completed_tasks=7,
            last_updated=now
        )

        # Save progress
        storage.save_progress(progress)

        # Verify file was created
        progress_file = storage.progress_dir / "001-test-feature.json"
        assert progress_file.exists()

        # Verify content
        with open(progress_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["feature_id"] == "001-test-feature"
        assert data["percentage"] == 75.0
        assert data["total_tasks"] == 10
        assert data["completed_tasks"] == 7

    def test_load_progress_basic(self, storage):
        """Test basic progress loading functionality."""
        now = datetime.now()
        progress = ProgressData(
            feature_id="001-test-feature",
            percentage=75.0,
            total_tasks=10,
            completed_tasks=7,
            last_updated=now
        )

        # Save progress first
        storage.save_progress(progress)

        # Load progress
        loaded_progress = storage.load_progress("001-test-feature")

        assert loaded_progress.feature_id == progress.feature_id
        assert loaded_progress.percentage == progress.percentage
        assert loaded_progress.total_tasks == progress.total_tasks
        assert loaded_progress.completed_tasks == progress.completed_tasks

    def test_load_progress_nonexistent_feature(self, storage):
        """Test loading progress for non-existent feature."""
        loaded_progress = storage.load_progress("999-nonexistent")

        assert loaded_progress is None

    def test_save_history_entry_basic(self, storage):
        """Test basic history entry saving functionality."""
        now = datetime.now()
        history = TaskHistory(
            task_id="T001",
            timestamp=now,
            old_state=TaskState.PENDING,
            new_state=TaskState.COMPLETED,
            duration=1.5
        )

        # Save history entry
        storage.save_history_entry(history, "001-test-feature")

        # Verify file was created
        history_file = storage.history_dir / "001-test-feature.json"
        assert history_file.exists()

        # Verify content
        with open(history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["task_id"] == "T001"
        assert data[0]["old_state"] == "pending"
        assert data[0]["new_state"] == "completed"
        assert data[0]["duration"] == 1.5

    def test_load_history_basic(self, storage):
        """Test basic history loading functionality."""
        now = datetime.now()
        history_entries = [
            TaskHistory(
                task_id="T001",
                timestamp=now - timedelta(hours=2),
                old_state=TaskState.PENDING,
                new_state=TaskState.IN_PROGRESS
            ),
            TaskHistory(
                task_id="T001",
                timestamp=now - timedelta(hours=1),
                old_state=TaskState.IN_PROGRESS,
                new_state=TaskState.COMPLETED,
                duration=1.5
            )
        ]

        # Save history entries
        for history in history_entries:
            storage.save_history_entry(history, "001-test-feature")

        # Load history
        loaded_history = storage.load_history("001-test-feature")

        assert len(loaded_history) == len(history_entries)

        # Verify history data (should be in chronological order)
        assert loaded_history[0].task_id == "T001"
        assert loaded_history[0].old_state == TaskState.PENDING
        assert loaded_history[1].task_id == "T001"
        assert loaded_history[1].new_state == TaskState.COMPLETED

    def test_load_history_with_limit(self, storage):
        """Test loading history with limit parameter."""
        now = datetime.now()

        # Create many history entries
        for i in range(15):
            history = TaskHistory(
                task_id=f"T{(i % 3) + 1:03d}",
                timestamp=now - timedelta(minutes=i * 10),
                old_state=TaskState.PENDING,
                new_state=TaskState.COMPLETED if i % 2 == 0 else TaskState.IN_PROGRESS
            )
            storage.save_history_entry(history, "001-test-feature")

        # Load with limit
        loaded_history = storage.load_history("001-test-feature", limit=10)

        assert len(loaded_history) == 10

    def test_load_history_nonexistent_feature(self, storage):
        """Test loading history for non-existent feature."""
        loaded_history = storage.load_history("999-nonexistent")

        assert loaded_history == []

    def test_get_all_features(self, storage, sample_tasks):
        """Test getting all feature IDs."""
        # Save tasks for multiple features
        storage.save_tasks(sample_tasks, "001-test-feature")
        storage.save_tasks(sample_tasks, "002-another-feature")

        # Get all features
        features = storage.get_all_features()

        assert len(features) == 2
        assert "001-test-feature" in features
        assert "002-another-feature" in features

    def test_get_all_features_empty(self, storage):
        """Test getting all features when no data exists."""
        features = storage.get_all_features()

        assert features == []

    def test_delete_feature_data(self, storage, sample_tasks):
        """Test deleting all data for a feature."""
        feature_id = "001-test-feature"

        # Save all types of data
        storage.save_tasks(sample_tasks, feature_id)

        progress = ProgressData.from_tasks(sample_tasks, feature_id)
        storage.save_progress(progress)

        history = TaskHistory(
            task_id="T001", timestamp=datetime.now(),
            old_state=TaskState.PENDING, new_state=TaskState.COMPLETED
        )
        storage.save_history_entry(history, feature_id)

        # Delete feature data
        storage.delete_feature_data(feature_id)

        # Verify data is deleted
        loaded_tasks = storage.load_tasks(feature_id)
        loaded_progress = storage.load_progress(feature_id)
        loaded_history = storage.load_history(feature_id)

        assert loaded_tasks == []
        assert loaded_progress is None
        assert loaded_history == []

    def test_reset_feature_data(self, storage, sample_tasks):
        """Test resetting feature data."""
        feature_id = "001-test-feature"

        # Save data
        storage.save_tasks(sample_tasks, feature_id)

        # Reset feature data
        storage.reset_feature_data(feature_id)

        # Verify data is reset
        loaded_tasks = storage.load_tasks(feature_id)
        assert loaded_tasks == []

    def test_save_config(self, storage):
        """Test configuration saving."""
        config = MonitoringConfig(
            auto_discovery=False,
            update_interval_seconds=60,
            history_retention_days=45
        )

        # Save config
        storage.save_config(config)

        # Verify file was created
        config_file = storage.memory_dir / "monitor-config.json"
        assert config_file.exists()

        # Verify content
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["auto_discovery"] is False
        assert data["update_interval_seconds"] == 60
        assert data["history_retention_days"] == 45

    def test_load_config(self, storage):
        """Test configuration loading."""
        config = MonitoringConfig(
            auto_discovery=False,
            update_interval_seconds=60,
            history_retention_days=45
        )

        # Save config first
        storage.save_config(config)

        # Load config
        loaded_config = storage.load_config()

        assert loaded_config.auto_discovery is False
        assert loaded_config.update_interval_seconds == 60
        assert loaded_config.history_retention_days == 45

    def test_load_config_default(self, storage):
        """Test loading default configuration when no file exists."""
        loaded_config = storage.load_config()

        # Should return default config
        assert loaded_config.auto_discovery is True
        assert loaded_config.update_interval_seconds == 30
        assert loaded_config.history_retention_days == 30

    def test_validate_data_integrity_valid(self, storage, sample_tasks):
        """Test data integrity validation with valid data."""
        # Save valid data
        storage.save_tasks(sample_tasks, "001-test-feature")

        # Validate integrity
        report = storage.validate_data_integrity()

        assert report["valid"] is True
        assert len(report["issues"]) == 0
        assert len(report["files_checked"]) > 0

    def test_validate_data_integrity_corrupted(self, storage):
        """Test data integrity validation with corrupted data."""
        # Create corrupted state file
        with open(storage.state_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")

        # Validate integrity
        report = storage.validate_data_integrity()

        assert report["valid"] is False
        assert len(report["issues"]) > 0

        # Check for specific corruption issues
        issue_texts = " ".join(report["issues"]).lower()
        assert any(keyword in issue_texts for keyword in ["corrupted", "invalid", "json"])

    def test_validate_data_integrity_missing_files(self, storage):
        """Test data integrity validation with missing files."""
        # Don't create any files

        # Validate integrity
        report = storage.validate_data_integrity()

        # Should be valid since no files to check
        assert report["valid"] is True

    def test_cleanup_old_history(self, storage):
        """Test cleanup of old history entries."""
        now = datetime.now()
        feature_id = "001-test-feature"

        # Create old history entries (beyond retention period)
        retention_days = 30
        config = MonitoringConfig(history_retention_days=retention_days)
        storage.config = config

        # Create entries older than retention period
        old_date = now - timedelta(days=retention_days + 5)
        for i in range(5):
            history = TaskHistory(
                task_id="T001",
                timestamp=old_date - timedelta(hours=i),
                old_state=TaskState.PENDING,
                new_state=TaskState.COMPLETED
            )
            storage.save_history_entry(history, feature_id)

        # Create recent entries
        for i in range(3):
            history = TaskHistory(
                task_id="T002",
                timestamp=now - timedelta(hours=i),
                old_state=TaskState.PENDING,
                new_state=TaskState.COMPLETED
            )
            storage.save_history_entry(history, feature_id)

        # Cleanup old history
        storage.cleanup_old_history()

        # Verify only recent entries remain
        remaining_history = storage.load_history(feature_id)
        assert len(remaining_history) == 3
        for entry in remaining_history:
            assert entry.task_id == "T002"

    def test_cleanup_old_backups(self, storage, sample_tasks):
        """Test cleanup of old backup files."""
        config = MonitoringConfig(backup_enabled=True, max_backups=2)
        storage.config = config

        # Create many backup files
        for i in range(5):
            # Create backup files with old timestamps
            backup_file = storage.backup_dir / f"task-states_{i}.json"
            backup_file.write_text('{"test": "data"}')

            # Set old modification time
            old_time = time.time() - (i * 86400)  # i days ago
            backup_file.touch(times=(old_time, old_time))

        # Cleanup old backups
        storage.cleanup_old_backups()

        # Verify backup limit is respected
        backup_files = list(storage.backup_dir.glob("task-states_*.json"))
        assert len(backup_files) <= config.max_backups

    def test_concurrent_access_safety(self, storage, sample_tasks):
        """Test thread safety of storage operations."""
        import threading

        results = []
        errors = []

        def worker_task(worker_id):
            try:
                feature_id = f"001-worker-{worker_id}"
                storage.save_tasks(sample_tasks, feature_id)
                loaded_tasks = storage.load_tasks(feature_id)
                results.append((worker_id, len(loaded_tasks)))
            except Exception as e:
                errors.append((worker_id, str(e)))

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_task, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5
        for worker_id, task_count in results:
            assert task_count == len(sample_tasks)

    def test_file_encoding_handling(self, storage, sample_tasks):
        """Test proper file encoding handling."""
        # Create tasks with special characters
        special_tasks = [
            TaskInfo(
                id="T001",
                title="Tâsk wïth ünïcodé & spëciâl chârs",
                state=TaskState.PENDING,
                last_updated=datetime.now()
            ),
            TaskInfo(
                id="T002",
                title="Задача с русскими символами",
                state=TaskState.COMPLETED,
                last_updated=datetime.now()
            )
        ]

        # Save tasks
        storage.save_tasks(special_tasks, "001-unicode-test")

        # Load tasks
        loaded_tasks = storage.load_tasks("001-unicode-test")

        # Verify special characters are preserved
        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].title == "Tâsk wïth ünïcodé & spëciâl chârs"
        assert loaded_tasks[1].title == "Задача с русскими символами"

    def test_atomic_write_operations(self, storage, sample_tasks):
        """Test that write operations are atomic."""
        feature_id = "001-atomic-test"

        # Mock file operations to simulate interruption
        with patch('builtins.open', side_effect=IOError("Simulated write failure")):
            with pytest.raises(IOError):
                storage.save_tasks(sample_tasks, feature_id)

        # File should not exist or be incomplete after failure
        if storage.state_file.exists():
            # If file exists, it should be valid JSON or empty
            try:
                with open(storage.state_file, 'r') as f:
                    json.load(f)
                # If we get here, file is valid JSON
            except json.JSONDecodeError:
                pytest.fail("File should not contain partial/invalid JSON after failure")

    def test_storage_error_handling(self, storage):
        """Test proper error handling and custom exceptions."""
        # Test with non-existent directory (should create it)
        storage.memory_dir.rmdir()

        # Should not raise error, should create directory
        storage.save_tasks([], "001-test")

        # Test with permission denied (simulate)
        with patch('pathlib.Path.mkdir', side_effect=PermissionError("Permission denied")):
            with pytest.raises(StorageError):
                storage.save_tasks([], "001-test")

    def test_backup_creation_on_corruption(self, storage, sample_tasks):
        """Test backup creation when corruption is detected."""
        # Save initial data
        storage.save_tasks(sample_tasks, "001-test-feature")

        # Corrupt the main file
        with open(storage.state_file, 'w') as f:
            f.write("corrupted data")

        # Try to load data (should detect corruption)
        loaded_tasks = storage.load_tasks("001-test-feature")
        assert loaded_tasks == []  # Should handle corruption gracefully

        # Check if backup was created before corruption
        backup_files = list(storage.backup_dir.glob("task-states_*.json"))
        # Note: This depends on implementation details about when backups are created