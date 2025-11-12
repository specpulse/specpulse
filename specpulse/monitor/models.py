"""
Task Monitor Data Models

This module contains the core data structures for the SpecPulse task monitoring system.
Provides type-safe data models with validation for task states and progress tracking.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


class TaskState(Enum):
    """Enumeration for possible task states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "TaskState":
        """Create TaskState from string value."""
        for state in cls:
            if state.value == value.lower():
                return state
        raise ValueError(f"Invalid TaskState value: {value}")

    def is_terminal(self) -> bool:
        """Check if this is a terminal state (completed or blocked)."""
        return self in (TaskState.COMPLETED, TaskState.BLOCKED)

    def is_active(self) -> bool:
        """Check if this is an active state (in_progress)."""
        return self == TaskState.IN_PROGRESS


@dataclass
class TaskInfo:
    """Information about a specific task."""
    id: str
    title: str
    state: TaskState
    last_updated: datetime
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    description: Optional[str] = None
    assignee: Optional[str] = None
    priority: Optional[str] = None
    estimated_hours: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "state": self.state.value,
            "last_updated": self.last_updated.isoformat(),
            "execution_time": self.execution_time,
            "error_message": self.error_message,
            "description": self.description,
            "assignee": self.assignee,
            "priority": self.priority,
            "estimated_hours": self.estimated_hours,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskInfo":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            state=TaskState.from_string(data["state"]),
            last_updated=datetime.fromisoformat(data["last_updated"]),
            execution_time=data.get("execution_time"),
            error_message=data.get("error_message"),
            description=data.get("description"),
            assignee=data.get("assignee"),
            priority=data.get("priority"),
            estimated_hours=data.get("estimated_hours"),
        )

    def transition_to(self, new_state: TaskState, error_message: Optional[str] = None) -> None:
        """Transition to a new state with validation."""
        if self.state == new_state:
            return  # No change needed

        # Validate state transitions
        if self.state == TaskState.COMPLETED:
            raise ValueError("Cannot transition from COMPLETED state")

        if self.state == TaskState.BLOCKED and new_state != TaskState.PENDING:
            # Can only unblock to pending state
            raise ValueError("Blocked tasks can only transition to PENDING")

        self.state = new_state
        self.last_updated = datetime.now()

        if new_state == TaskState.BLOCKED and error_message:
            self.error_message = error_message
        elif new_state != TaskState.BLOCKED:
            self.error_message = None

    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.state == TaskState.COMPLETED

    def is_active(self) -> bool:
        """Check if task is currently active (in progress or blocked)."""
        return self.state in (TaskState.IN_PROGRESS, TaskState.BLOCKED)

    @property
    def duration(self) -> Optional[float]:
        """Get task duration in various ways."""
        if self.execution_time is not None:
            return self.execution_time

        # If no execution_time, could calculate based on other factors
        # This is a simplified implementation
        return None

    def __eq__(self, other) -> bool:
        """Compare tasks based on ID."""
        if not isinstance(other, TaskInfo):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on task ID."""
        return hash(self.id)


@dataclass
class ProgressData:
    """Overall progress information for a feature or project."""
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    blocked_tasks: int
    pending_tasks: int
    percentage: float
    last_updated: datetime
    feature_id: Optional[str] = None
    project_path: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate data consistency."""
        calculated_total = self.completed_tasks + self.in_progress_tasks + self.blocked_tasks + self.pending_tasks
        if calculated_total != self.total_tasks:
            raise ValueError(f"Task count mismatch: {calculated_total} != {self.total_tasks}")

        if not 0 <= self.percentage <= 100:
            raise ValueError(f"Percentage must be between 0 and 100, got {self.percentage}")

    @classmethod
    def from_tasks(cls, tasks: List[TaskInfo], feature_id: Optional[str] = None) -> "ProgressData":
        """Create ProgressData from a list of tasks."""
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.state == TaskState.COMPLETED)
        in_progress_tasks = sum(1 for task in tasks if task.state == TaskState.IN_PROGRESS)
        blocked_tasks = sum(1 for task in tasks if task.state == TaskState.BLOCKED)
        pending_tasks = sum(1 for task in tasks if task.state == TaskState.PENDING)

        # Calculate percentage (completed tasks / total tasks)
        percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return cls(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            in_progress_tasks=in_progress_tasks,
            blocked_tasks=blocked_tasks,
            pending_tasks=pending_tasks,
            percentage=round(percentage, 1),
            last_updated=datetime.now(),
            feature_id=feature_id,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "in_progress_tasks": self.in_progress_tasks,
            "blocked_tasks": self.blocked_tasks,
            "pending_tasks": self.pending_tasks,
            "percentage": self.percentage,
            "last_updated": self.last_updated.isoformat(),
            "feature_id": self.feature_id,
            "project_path": self.project_path,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgressData":
        """Create from dictionary."""
        return cls(
            total_tasks=data["total_tasks"],
            completed_tasks=data["completed_tasks"],
            in_progress_tasks=data["in_progress_tasks"],
            blocked_tasks=data["blocked_tasks"],
            pending_tasks=data["pending_tasks"],
            percentage=data["percentage"],
            last_updated=datetime.fromisoformat(data["last_updated"]),
            feature_id=data.get("feature_id"),
            project_path=data.get("project_path"),
        )

    def is_complete(self) -> bool:
        """Check if progress is 100% complete."""
        return self.percentage >= 100.0

    def has_active_tasks(self) -> bool:
        """Check if there are active tasks (in progress or blocked)."""
        return self.in_progress_tasks > 0 or self.blocked_tasks > 0


@dataclass
class TaskHistory:
    """Historical tracking of task state changes."""
    task_id: str
    timestamp: datetime
    old_state: Optional[TaskState]
    new_state: TaskState
    execution_time: Optional[float] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "task_id": self.task_id,
            "timestamp": self.timestamp.isoformat(),
            "old_state": self.old_state.value if self.old_state else None,
            "new_state": self.new_state.value,
            "execution_time": self.execution_time,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskHistory":
        """Create from dictionary."""
        return cls(
            task_id=data["task_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            old_state=TaskState.from_string(data["old_state"]) if data["old_state"] else None,
            new_state=TaskState.from_string(data["new_state"]),
            execution_time=data.get("execution_time"),
            notes=data.get("notes"),
        )

    def is_completion(self) -> bool:
        """Check if this history entry represents a task completion."""
        return self.new_state == TaskState.COMPLETED

    def is_start(self) -> bool:
        """Check if this history entry represents a task start."""
        return (
            self.old_state == TaskState.PENDING and
            self.new_state == TaskState.IN_PROGRESS
        )


@dataclass
class MonitoringConfig:
    """Configuration for task monitoring system."""
    auto_discovery: bool = True
    history_retention_days: int = 30
    max_tasks_per_feature: int = 1000
    progress_calculation_method: str = "simple"  # simple, weighted, trending
    backup_enabled: bool = True
    max_backups: int = 5
    update_interval_seconds: int = 60
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "auto_discovery": self.auto_discovery,
            "history_retention_days": self.history_retention_days,
            "max_tasks_per_feature": self.max_tasks_per_feature,
            "progress_calculation_method": self.progress_calculation_method,
            "backup_enabled": self.backup_enabled,
            "max_backups": self.max_backups,
            "update_interval_seconds": self.update_interval_seconds,
            "cache_enabled": self.cache_enabled,
            "cache_ttl_seconds": self.cache_ttl_seconds,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MonitoringConfig":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class TaskMetrics:
    """Detailed metrics for a single task."""
    task_id: str
    feature_id: str
    created_time: datetime
    started_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    total_duration: Optional[float] = None  # Total time from creation to completion in seconds
    execution_time: Optional[float] = None   # Actual work time in seconds
    wait_time: Optional[float] = None        # Time waiting between work sessions
    state_transitions: int = 0
    blocked_count: int = 0

    @property
    def efficiency_ratio(self) -> float:
        """Calculate efficiency ratio (execution_time / total_duration)."""
        if not self.total_duration or not self.execution_time:
            return 0.0
        return self.execution_time / self.total_duration

    @property
    def average_block_duration(self) -> float:
        """Calculate average duration of blocks."""
        if self.blocked_count == 0:
            return 0.0
        # This would need detailed block history for accurate calculation
        return 0.0


@dataclass
class PerformanceData:
    """Performance analytics data for a feature."""
    feature_id: str
    total_tasks: int
    completed_tasks: int
    average_task_duration: float  # Average time to complete a task in seconds
    total_project_duration: float  # Total project duration in seconds
    tasks_per_day: float  # Average tasks completed per day
    completion_rate: float  # Percentage of tasks completed
    blocked_rate: float   # Percentage of tasks that were blocked
    last_updated: datetime

    def is_on_track(self) -> bool:
        """Check if project performance is on track."""
        # Simple heuristic: on track if completion rate > 50% and blocked rate < 20%
        return self.completion_rate > 0.5 and self.blocked_rate < 0.2


@dataclass
class WorkflowState:
    """Current state of the development workflow."""
    feature_id: str
    current_phase: str
    total_phases: int
    completed_phases: int
    active_tasks: List[str]
    blocked_tasks: List[str]
    next_milestone: Optional[str]
    last_activity: datetime
    is_paused: bool = False

    @property
    def progress_percentage(self) -> float:
        """Calculate workflow progress percentage."""
        if self.total_phases == 0:
            return 0.0
        return (self.completed_phases / self.total_phases) * 100

    def has_blockers(self) -> bool:
        """Check if there are any blocked tasks."""
        return len(self.blocked_tasks) > 0

    def is_active(self) -> bool:
        """Check if workflow is currently active."""
        return not self.is_paused and len(self.active_tasks) > 0