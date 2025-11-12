"""
Model Tests for Monitor

Unit tests for monitor data models including TaskInfo, ProgressData,
TaskHistory, and related classes.
"""

import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import Mock

from specpulse.monitor.models import (
    TaskState, TaskInfo, ProgressData, TaskHistory, MonitoringConfig
)


class TestTaskState:
    """Test TaskState enum functionality."""

    def test_task_state_values(self):
        """Test all TaskState enum values."""
        assert TaskState.PENDING.value == "pending"
        assert TaskState.IN_PROGRESS.value == "in_progress"
        assert TaskState.COMPLETED.value == "completed"
        assert TaskState.BLOCKED.value == "blocked"
        assert TaskState.FAILED.value == "failed"
        assert TaskState.CANCELLED.value == "cancelled"

    def test_task_state_ordering(self):
        """Test TaskState enum ordering."""
        # States should be in logical progression order
        states = list(TaskState)
        expected_order = [
            TaskState.PENDING,
            TaskState.IN_PROGRESS,
            TaskState.COMPLETED,
            TaskState.BLOCKED,
            TaskState.FAILED,
            TaskState.CANCELLED
        ]
        assert states == expected_order

    def test_task_state_from_string(self):
        """Test creating TaskState from string."""
        assert TaskState("pending") == TaskState.PENDING
        assert TaskState("in_progress") == TaskState.IN_PROGRESS
        assert TaskState("completed") == TaskState.COMPLETED
        assert TaskState("blocked") == TaskState.BLOCKED
        assert TaskState("failed") == TaskState.FAILED
        assert TaskState("cancelled") == TaskState.CANCELLED

    def test_task_state_invalid_string(self):
        """Test creating TaskState from invalid string."""
        with pytest.raises(ValueError):
            TaskState("invalid_state")


class TestTaskInfo:
    """Test TaskInfo model functionality."""

    def test_task_info_creation(self):
        """Test TaskInfo object creation."""
        now = datetime.now()
        task = TaskInfo(
            id="T001",
            title="Test task",
            state=TaskState.PENDING,
            last_updated=now,
            description="Test description",
            estimated_hours=2.0,
            execution_time=1.5,
            error_message=None
        )

        assert task.id == "T001"
        assert task.title == "Test task"
        assert task.state == TaskState.PENDING
        assert task.last_updated == now
        assert task.description == "Test description"
        assert task.estimated_hours == 2.0
        assert task.execution_time == 1.5
        assert task.error_message is None

    def test_task_info_creation_minimal(self):
        """Test TaskInfo creation with minimal parameters."""
        task = TaskInfo(
            id="T001",
            title="Test task",
            state=TaskState.PENDING,
            last_updated=datetime.now()
        )

        assert task.id == "T001"
        assert task.title == "Test task"
        assert task.state == TaskState.PENDING
        assert task.description is None
        assert task.estimated_hours is None
        assert task.execution_time is None
        assert task.error_message is None

    def test_task_info_to_dict(self):
        """Test TaskInfo serialization to dictionary."""
        now = datetime.now()
        task = TaskInfo(
            id="T001",
            title="Test task",
            state=TaskState.PENDING,
            last_updated=now,
            description="Test description",
            estimated_hours=2.0
        )

        task_dict = task.to_dict()

        assert task_dict["id"] == "T001"
        assert task_dict["title"] == "Test task"
        assert task_dict["state"] == "pending"
        assert task_dict["last_updated"] == now.isoformat()
        assert task_dict["description"] == "Test description"
        assert task_dict["estimated_hours"] == 2.0

    def test_task_info_from_dict(self):
        """Test TaskInfo deserialization from dictionary."""
        now = datetime.now()
        task_dict = {
            "id": "T001",
            "title": "Test task",
            "state": "pending",
            "last_updated": now.isoformat(),
            "description": "Test description",
            "estimated_hours": 2.0,
            "execution_time": None,
            "error_message": None
        }

        task = TaskInfo.from_dict(task_dict)

        assert task.id == "T001"
        assert task.title == "Test task"
        assert task.state == TaskState.PENDING
        assert task.last_updated == now
        assert task.description == "Test description"
        assert task.estimated_hours == 2.0

    def test_task_info_json_serialization(self):
        """Test TaskInfo JSON serialization and deserialization."""
        now = datetime.now()
        original_task = TaskInfo(
            id="T001",
            title="Test task",
            state=TaskState.COMPLETED,
            last_updated=now,
            execution_time=1.25
        )

        # Serialize to JSON
        task_json = json.dumps(original_task.to_dict())

        # Deserialize from JSON
        task_dict = json.loads(task_json)
        restored_task = TaskInfo.from_dict(task_dict)

        assert restored_task.id == original_task.id
        assert restored_task.title == original_task.title
        assert restored_task.state == original_task.state
        assert restored_task.execution_time == original_task.execution_time

    def test_task_info_is_completed(self):
        """Test TaskInfo is_completed method."""
        completed_task = TaskInfo(
            id="T001", title="Task", state=TaskState.COMPLETED, last_updated=datetime.now()
        )
        pending_task = TaskInfo(
            id="T002", title="Task", state=TaskState.PENDING, last_updated=datetime.now()
        )
        failed_task = TaskInfo(
            id="T003", title="Task", state=TaskState.FAILED, last_updated=datetime.now()
        )

        assert completed_task.is_completed() is True
        assert pending_task.is_completed() is False
        assert failed_task.is_completed() is False

    def test_task_info_is_active(self):
        """Test TaskInfo is_active method."""
        active_task = TaskInfo(
            id="T001", title="Task", state=TaskState.IN_PROGRESS, last_updated=datetime.now()
        )
        blocked_task = TaskInfo(
            id="T002", title="Task", state=TaskState.BLOCKED, last_updated=datetime.now()
        )
        completed_task = TaskInfo(
            id="T003", title="Task", state=TaskState.COMPLETED, last_updated=datetime.now()
        )

        assert active_task.is_active() is True
        assert blocked_task.is_active() is True
        assert completed_task.is_active() is False

    def test_task_info_duration(self):
        """Test TaskInfo duration calculation."""
        start_time = datetime.now() - timedelta(hours=2)
        end_time = datetime.now()

        # Task with execution time
        task_with_execution = TaskInfo(
            id="T001", title="Task", state=TaskState.COMPLETED,
            last_updated=end_time, execution_time=1.5
        )
        assert task_with_execution.duration == 1.5

        # Task without execution time (should estimate based on timestamps)
        task_without_execution = TaskInfo(
            id="T002", title="Task", state=TaskState.COMPLETED,
            last_updated=end_time
        )
        # This might return None or an estimate based on other logic
        assert task_without_execution.duration is None or isinstance(task_without_execution.duration, (int, float))

    def test_task_info_equality(self):
        """Test TaskInfo equality comparison."""
        now = datetime.now()
        task1 = TaskInfo(
            id="T001", title="Task", state=TaskState.PENDING, last_updated=now
        )
        task2 = TaskInfo(
            id="T001", title="Different Title", state=TaskState.COMPLETED, last_updated=now
        )
        task3 = TaskInfo(
            id="T002", title="Task", state=TaskState.PENDING, last_updated=now
        )

        assert task1 == task2  # Same ID
        assert task1 != task3  # Different ID
        assert hash(task1) == hash(task2)
        assert hash(task1) != hash(task3)


class TestProgressData:
    """Test ProgressData model functionality."""

    def test_progress_data_creation(self):
        """Test ProgressData object creation."""
        now = datetime.now()
        progress = ProgressData(
            feature_id="001-test",
            percentage=75.0,
            total_tasks=10,
            completed_tasks=7,
            in_progress_tasks=1,
            pending_tasks=1,
            blocked_tasks=1,
            last_updated=now
        )

        assert progress.feature_id == "001-test"
        assert progress.percentage == 75.0
        assert progress.total_tasks == 10
        assert progress.completed_tasks == 7
        assert progress.in_progress_tasks == 1
        assert progress.pending_tasks == 1
        assert progress.blocked_tasks == 1
        assert progress.last_updated == now

    def test_progress_data_from_tasks(self):
        """Test ProgressData creation from task list."""
        now = datetime.now()
        tasks = [
            TaskInfo(id="T001", title="Task 1", state=TaskState.COMPLETED, last_updated=now),
            TaskInfo(id="T002", title="Task 2", state=TaskState.COMPLETED, last_updated=now),
            TaskInfo(id="T003", title="Task 3", state=TaskState.IN_PROGRESS, last_updated=now),
            TaskInfo(id="T004", title="Task 4", state=TaskState.PENDING, last_updated=now),
            TaskInfo(id="T005", title="Task 5", state=TaskState.BLOCKED, last_updated=now),
        ]

        progress = ProgressData.from_tasks(tasks, "001-test")

        assert progress.feature_id == "001-test"
        assert progress.total_tasks == 5
        assert progress.completed_tasks == 2
        assert progress.in_progress_tasks == 1
        assert progress.pending_tasks == 1
        assert progress.blocked_tasks == 1
        assert progress.percentage == 40.0  # 2/5 * 100

    def test_progress_data_from_empty_tasks(self):
        """Test ProgressData creation from empty task list."""
        progress = ProgressData.from_tasks([], "001-empty")

        assert progress.feature_id == "001-empty"
        assert progress.total_tasks == 0
        assert progress.completed_tasks == 0
        assert progress.in_progress_tasks == 0
        assert progress.pending_tasks == 0
        assert progress.blocked_tasks == 0
        assert progress.percentage == 0.0

    def test_progress_data_to_dict(self):
        """Test ProgressData serialization to dictionary."""
        now = datetime.now()
        progress = ProgressData(
            feature_id="001-test",
            percentage=75.0,
            total_tasks=10,
            completed_tasks=7,
            in_progress_tasks=1,
            pending_tasks=1,
            blocked_tasks=1,
            last_updated=now
        )

        progress_dict = progress.to_dict()

        assert progress_dict["feature_id"] == "001-test"
        assert progress_dict["percentage"] == 75.0
        assert progress_dict["total_tasks"] == 10
        assert progress_dict["completed_tasks"] == 7
        assert progress_dict["last_updated"] == now.isoformat()

    def test_progress_data_from_dict(self):
        """Test ProgressData deserialization from dictionary."""
        now = datetime.now()
        progress_dict = {
            "feature_id": "001-test",
            "percentage": 75.0,
            "total_tasks": 10,
            "completed_tasks": 7,
            "in_progress_tasks": 1,
            "pending_tasks": 1,
            "blocked_tasks": 1,
            "last_updated": now.isoformat()
        }

        progress = ProgressData.from_dict(progress_dict)

        assert progress.feature_id == "001-test"
        assert progress.percentage == 75.0
        assert progress.total_tasks == 10
        assert progress.completed_tasks == 7

    def test_progress_data_is_complete(self):
        """Test ProgressData is_complete method."""
        complete_progress = ProgressData(
            feature_id="001-test", percentage=100.0, total_tasks=5,
            completed_tasks=5, in_progress_tasks=0, blocked_tasks=0,
            pending_tasks=0, last_updated=datetime.now()
        )
        incomplete_progress = ProgressData(
            feature_id="001-test", percentage=75.0, total_tasks=5,
            completed_tasks=3, in_progress_tasks=1, blocked_tasks=0,
            pending_tasks=1, last_updated=datetime.now()
        )

        assert complete_progress.is_complete() is True
        assert incomplete_progress.is_complete() is False

    def test_progress_data_has_active_tasks(self):
        """Test ProgressData has_active_tasks method."""
        active_progress = ProgressData(
            feature_id="001-test", percentage=50.0, total_tasks=5,
            completed_tasks=2, in_progress_tasks=1, blocked_tasks=0,
            pending_tasks=2, last_updated=datetime.now()
        )
        inactive_progress = ProgressData(
            feature_id="001-test", percentage=100.0, total_tasks=5,
            completed_tasks=5, in_progress_tasks=0, blocked_tasks=0,
            pending_tasks=0, last_updated=datetime.now()
        )

        assert active_progress.has_active_tasks() is True
        assert inactive_progress.has_active_tasks() is False


class TestTaskHistory:
    """Test TaskHistory model functionality."""

    def test_task_history_creation(self):
        """Test TaskHistory object creation."""
        now = datetime.now()
        history = TaskHistory(
            task_id="T001",
            timestamp=now,
            old_state=TaskState.PENDING,
            new_state=TaskState.IN_PROGRESS,
            execution_time=0.5,
            notes="Started working on task"
        )

        assert history.task_id == "T001"
        assert history.timestamp == now
        assert history.old_state == TaskState.PENDING
        assert history.new_state == TaskState.IN_PROGRESS
        assert history.execution_time == 0.5
        assert history.notes == "Started working on task"

    def test_task_history_creation_minimal(self):
        """Test TaskHistory creation with minimal parameters."""
        now = datetime.now()
        history = TaskHistory(
            task_id="T001",
            timestamp=now,
            old_state=TaskState.PENDING,
            new_state=TaskState.COMPLETED
        )

        assert history.task_id == "T001"
        assert history.timestamp == now
        assert history.old_state == TaskState.PENDING
        assert history.new_state == TaskState.COMPLETED
        assert history.execution_time is None
        assert history.notes is None

    def test_task_history_to_dict(self):
        """Test TaskHistory serialization to dictionary."""
        now = datetime.now()
        history = TaskHistory(
            task_id="T001",
            timestamp=now,
            old_state=TaskState.PENDING,
            new_state=TaskState.COMPLETED,
            execution_time=1.5,
            notes="Task completed successfully"
        )

        history_dict = history.to_dict()

        assert history_dict["task_id"] == "T001"
        assert history_dict["timestamp"] == now.isoformat()
        assert history_dict["old_state"] == "pending"
        assert history_dict["new_state"] == "completed"
        assert history_dict["execution_time"] == 1.5
        assert history_dict["notes"] == "Task completed successfully"

    def test_task_history_from_dict(self):
        """Test TaskHistory deserialization from dictionary."""
        now = datetime.now()
        history_dict = {
            "task_id": "T001",
            "timestamp": now.isoformat(),
            "old_state": "pending",
            "new_state": "completed",
            "execution_time": 1.5,
            "notes": "Task completed successfully"
        }

        history = TaskHistory.from_dict(history_dict)

        assert history.task_id == "T001"
        assert history.timestamp == now
        assert history.old_state == TaskState.PENDING
        assert history.new_state == TaskState.COMPLETED
        assert history.execution_time == 1.5
        assert history.notes == "Task completed successfully"

    def test_task_history_is_completion(self):
        """Test TaskHistory is_completion method."""
        completion_history = TaskHistory(
            task_id="T001", timestamp=datetime.now(),
            old_state=TaskState.IN_PROGRESS, new_state=TaskState.COMPLETED
        )
        non_completion_history = TaskHistory(
            task_id="T002", timestamp=datetime.now(),
            old_state=TaskState.PENDING, new_state=TaskState.IN_PROGRESS
        )

        assert completion_history.is_completion() is True
        assert non_completion_history.is_completion() is False

    def test_task_history_is_start(self):
        """Test TaskHistory is_start method."""
        start_history = TaskHistory(
            task_id="T001", timestamp=datetime.now(),
            old_state=TaskState.PENDING, new_state=TaskState.IN_PROGRESS
        )
        non_start_history = TaskHistory(
            task_id="T002", timestamp=datetime.now(),
            old_state=TaskState.IN_PROGRESS, new_state=TaskState.COMPLETED
        )

        assert start_history.is_start() is True
        assert non_start_history.is_start() is False


class TestMonitoringConfig:
    """Test MonitoringConfig model functionality."""

    def test_monitoring_config_defaults(self):
        """Test MonitoringConfig default values."""
        config = MonitoringConfig()

        assert config.auto_discovery is True
        assert config.update_interval_seconds == 60
        assert config.history_retention_days == 30
        assert config.max_tasks_per_feature == 1000
        assert config.backup_enabled is True
        assert config.max_backups == 5
        assert config.cache_enabled is True
        assert config.cache_ttl_seconds == 300

    def test_monitoring_config_custom_values(self):
        """Test MonitoringConfig with custom values."""
        config = MonitoringConfig(
            auto_discovery=False,
            update_interval_seconds=60,
            history_retention_days=60,
            max_tasks_per_feature=500,
            backup_enabled=False,
            max_backups=10,
            cache_enabled=False,
            cache_ttl_seconds=600
        )

        assert config.auto_discovery is False
        assert config.update_interval_seconds == 60
        assert config.history_retention_days == 60
        assert config.max_tasks_per_feature == 500
        assert config.backup_enabled is False
        assert config.max_backups == 10
        assert config.cache_enabled is False
        assert config.cache_ttl_seconds == 600

    def test_monitoring_config_to_dict(self):
        """Test MonitoringConfig serialization to dictionary."""
        config = MonitoringConfig(
            auto_discovery=False,
            update_interval_seconds=45
        )

        config_dict = config.to_dict()

        assert config_dict["auto_discovery"] is False
        assert config_dict["update_interval_seconds"] == 45
        assert "history_retention_days" in config_dict

    def test_monitoring_config_from_dict(self):
        """Test MonitoringConfig deserialization from dictionary."""
        config_dict = {
            "auto_discovery": False,
            "update_interval_seconds": 45,
            "history_retention_days": 45
        }

        config = MonitoringConfig.from_dict(config_dict)

        assert config.auto_discovery is False
        assert config.update_interval_seconds == 45
        assert config.history_retention_days == 45

    def test_monitoring_config_validation(self):
        """Test MonitoringConfig value validation."""
        # Test valid values
        config = MonitoringConfig(update_interval_seconds=30)
        assert config.update_interval_seconds == 30

        # Test invalid values (should not raise errors but handle gracefully)
        config = MonitoringConfig(update_interval_seconds=-1)
        # Implementation should handle negative values appropriately


