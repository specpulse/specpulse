"""
SpecPulse Workflow Integration

This module provides integration hooks with the existing SpecPulse workflow
to enable automatic task state updates during command execution.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import functools

from .models import TaskInfo, TaskState, TaskHistory
from .storage import StateStorage
from .state_manager import TaskStateManager
from .calculator import ProgressCalculator
from ..utils.error_handler import ErrorHandler


class WorkflowIntegration:
    """Integrates task monitoring with SpecPulse workflow."""

    def __init__(self, project_path: Path):
        """Initialize workflow integration."""
        self.project_path = Path(project_path)
        self.storage = StateStorage(project_path)
        self.state_manager = TaskStateManager(self.storage, self.storage.config)
        self.calculator = ProgressCalculator()
        self.error_handler = ErrorHandler()
        self._current_feature: Optional[str] = None
        self._current_task: Optional[str] = None

    def get_active_feature(self) -> Optional[str]:
        """Get the currently active feature from context."""
        try:
            context_file = self.project_path / ".specpulse" / "memory" / "context.md"
            if context_file.exists():
                with open(context_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract active feature
                for line in content.split('\n'):
                    if line.startswith("## Active Feature:"):
                        feature_line = line.replace("## Active Feature:", "").strip()
                        # Extract feature ID
                        parts = feature_line.split()
                        if parts:
                            return parts[0].replace(":", "").strip()
        except Exception as e:
            self.error_handler.log_warning(f"Failed to read active feature from context: {e}")

        return None

    def start_task_monitoring(self, feature_id: str, task_id: str) -> bool:
        """Start monitoring a task execution."""
        try:
            self._current_feature = feature_id
            self._current_task = task_id

            # Mark task as in-progress
            success = self.state_manager.start_task(feature_id, task_id)

            if success:
                # Log the start
                self._log_workflow_event("task_started", {
                    "feature_id": feature_id,
                    "task_id": task_id,
                    "timestamp": datetime.now().isoformat()
                })

            return success
        except Exception as e:
            self.error_handler.log_error(f"Failed to start task monitoring for {feature_id}/{task_id}: {e}")
            return False

    def complete_task_monitoring(self, feature_id: str, task_id: str,
                               execution_time: Optional[float] = None) -> bool:
        """Mark task as completed and calculate metrics."""
        try:
            # Mark task as completed
            success = self.state_manager.complete_task(feature_id, task_id, execution_time)

            if success:
                # Update project progress
                self._update_project_progress(feature_id)

                # Log the completion
                self._log_workflow_event("task_completed", {
                    "feature_id": feature_id,
                    "task_id": task_id,
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat()
                })

            # Clear current tracking
            if self._current_task == task_id:
                self._current_task = None

            return success
        except Exception as e:
            self.error_handler.log_error(f"Failed to complete task monitoring for {feature_id}/{task_id}: {e}")
            return False

    def block_task_monitoring(self, feature_id: str, task_id: str, error_message: str) -> bool:
        """Mark task as blocked with error information."""
        try:
            # Mark task as blocked
            success = self.state_manager.block_task(feature_id, task_id, error_message)

            if success:
                # Log the blockage
                self._log_workflow_event("task_blocked", {
                    "feature_id": feature_id,
                    "task_id": task_id,
                    "error_message": error_message,
                    "timestamp": datetime.now().isoformat()
                })

            # Clear current tracking
            if self._current_task == task_id:
                self._current_task = None

            return success
        except Exception as e:
            self.error_handler.log_error(f"Failed to block task for {feature_id}/{task_id}: {e}")
            return False

    def _update_project_progress(self, feature_id: str) -> None:
        """Update overall project progress."""
        try:
            tasks = self.state_manager.get_tasks(feature_id)
            progress = self.calculator.calculate_progress(tasks, feature_id)
            self.storage.save_progress(progress)
        except Exception as e:
            # Don't let progress updates fail task execution, but log the error
            self.error_handler.log_warning(f"Failed to update project progress for {feature_id}: {e}")

    def _log_workflow_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log workflow events for debugging and auditing."""
        try:
            log_file = self.project_path / ".specpulse" / "memory" / "workflow-log.json"

            # Read existing log
            if log_file.exists():
                import json
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
            else:
                log_data = {"events": []}

            # Add new event
            log_data["events"].append({
                "type": event_type,
                "data": data,
                "timestamp": datetime.now().isoformat()
            })

            # Keep only last 100 events
            if len(log_data["events"]) > 100:
                log_data["events"] = log_data["events"][-100:]

            # Write back
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # Don't let logging fail task execution, but log the error
            self.error_handler.log_warning(f"Failed to log workflow event {event_type}: {e}")

    def cleanup_old_logs(self, days: int = 30) -> None:
        """Clean up old workflow logs."""
        try:
            log_file = self.project_path / ".specpulse" / "memory" / "workflow-log.json"
            if log_file.exists():
                import json
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)

                cutoff_date = datetime.now().timestamp() - (days * 24 * 3600)

                # Filter old events
                log_data["events"] = [
                    event for event in log_data["events"]
                    if datetime.fromisoformat(event["timestamp"]).timestamp() > cutoff_date
                ]

                with open(log_file, 'w', encoding='utf-8') as f:
                    json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.error_handler.log_warning(f"Failed to cleanup old logs: {e}")


class MonitoringHooks:
    """Provides decorator hooks for automatic task monitoring."""

    def __init__(self, integration: WorkflowIntegration):
        """Initialize hooks with workflow integration."""
        self.integration = integration

    def monitor_task_execution(self, feature_id: Optional[str] = None, task_id: Optional[str] = None):
        """Decorator to automatically monitor task execution."""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Auto-detect feature and task if not provided
                current_feature = feature_id or self.integration.get_active_feature()
                current_task = task_id or self._extract_task_id_from_context()

                if not current_feature or not current_task:
                    # No monitoring info, just execute function
                    return func(*args, **kwargs)

                # Start monitoring
                start_time = datetime.now()
                self.integration.start_task_monitoring(current_feature, current_task)

                try:
                    # Execute the function
                    result = func(*args, **kwargs)

                    # Calculate execution time
                    execution_time = (datetime.now() - start_time).total_seconds()

                    # Mark as completed
                    self.integration.complete_task_monitoring(
                        current_feature, current_task, execution_time
                    )

                    return result

                except Exception as e:
                    # Mark as blocked
                    self.integration.block_task_monitoring(
                        current_feature, current_task, str(e)
                    )
                    raise

            return wrapper
        return decorator

    def _extract_task_id_from_context(self) -> Optional[str]:
        """Extract current task ID from execution context."""
        # Try to get from environment variables
        task_id = os.environ.get('SPECPULSE_CURRENT_TASK')
        if task_id:
            return task_id

        # Try to get from command line arguments
        if len(sys.argv) > 1:
            for arg in sys.argv:
                if arg.startswith(('T', 'AUTH-', 'USER-', 'INT-')):
                    return arg

        # Try to get from working directory
        cwd = Path.cwd()
        if '.specpulse' in cwd.parts:
            # Look for task files in current directory
            for task_file in cwd.glob('task-*.md'):
                match = task_file.stem.replace('task-', '')
                return f"T{match.zfill(3)}"

        return None


# Global integration instance (initialized when needed)
_integration_instance: Optional[WorkflowIntegration] = None
_hooks_instance: Optional[MonitoringHooks] = None


def get_integration(project_path: Optional[Path] = None) -> WorkflowIntegration:
    """Get or create the workflow integration instance."""
    global _integration_instance

    if _integration_instance is None:
        if project_path is None:
            project_path = Path.cwd()
        _integration_instance = WorkflowIntegration(project_path)

    return _integration_instance


def get_hooks(project_path: Optional[Path] = None) -> MonitoringHooks:
    """Get or create the monitoring hooks instance."""
    global _hooks_instance

    if _hooks_instance is None:
        integration = get_integration(project_path)
        _hooks_instance = MonitoringHooks(integration)

    return _hooks_instance


def monitor_command_execution(feature_id: Optional[str] = None, task_id: Optional[str] = None):
    """Convenient decorator for monitoring SpecPulse command execution."""
    hooks = get_hooks()
    return hooks.monitor_task_execution(feature_id, task_id)


# Auto-integration for common SpecPulse operations
def auto_integrate_sp_execute():
    """Automatically integrate with /sp-execute commands."""
    try:
        integration = get_integration()

        # Hook into command execution if possible
        # This would typically be called during SpecPulse initialization
        pass  # Implementation depends on SpecPulse architecture
    except Exception as e:
        # Don't let integration failures break SpecPulse, but log the error
        error_handler = ErrorHandler()
        error_handler.log_warning(f"Failed to auto-integrate sp-execute: {e}")


def initialize_monitoring_integration(project_path: Path) -> bool:
    """Initialize monitoring integration for a SpecPulse project."""
    try:
        integration = get_integration(project_path)

        # Create necessary directories and files
        memory_dir = project_path / ".specpulse" / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)

        # Initialize monitoring configuration
        config = integration.storage.load_config()
        integration.storage.save_config(config)

        # Log initialization
        integration._log_workflow_event("monitoring_initialized", {
            "project_path": str(project_path),
            "timestamp": datetime.now().isoformat()
        })

        return True
    except Exception as e:
        error_handler = ErrorHandler()
        error_handler.log_error(f"Failed to initialize monitoring integration: {e}")
        return False