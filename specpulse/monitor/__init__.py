"""
SpecPulse Task Monitor Module

This module provides task monitoring and progress tracking capabilities
for SpecPulse projects. It includes state management, progress calculation,
and CLI integration for monitoring development progress.
"""

from .models import TaskState, TaskInfo, ProgressData, TaskHistory, MonitoringConfig
from .storage import StateStorage
from .state_manager import TaskStateManager
from .calculator import ProgressCalculator
from .display import StatusDisplay
from .task_updater import TaskFileUpdater, TaskFileSyncManager
from .errors import MonitorError, StorageError, CorruptedDataError, ErrorHandler
from .integration import WorkflowIntegration

__version__ = "1.0.0"
__all__ = [
    "TaskState",
    "TaskInfo",
    "ProgressData",
    "TaskHistory",
    "MonitoringConfig",
    "StateStorage",
    "TaskStateManager",
    "ProgressCalculator",
    "StatusDisplay",
    "TaskFileUpdater",
    "TaskFileSyncManager",
    "MonitorError",
    "StorageError",
    "CorruptedDataError",
    "ErrorHandler",
    "WorkflowIntegration",
]