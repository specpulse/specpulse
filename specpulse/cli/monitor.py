"""
Monitor Commands for SpecPulse CLI

This module provides task monitoring and progress tracking commands
for SpecPulse projects. Integrates with the existing CLI framework.
"""

import sys
from pathlib import Path
from typing import Optional

from ..monitor import (
    TaskState, TaskInfo, ProgressData, TaskHistory, MonitoringConfig,
    StateStorage, TaskStateManager, ProgressCalculator, StatusDisplay
)


class MonitorCommands:
    """Handler for monitor-related CLI commands."""

    def __init__(self, project_path: Path, verbose: bool = False, no_color: bool = False):
        """Initialize monitor commands with project path and options."""
        self.project_path = Path(project_path)
        self.verbose = verbose
        self.no_color = no_color

        # Initialize components
        self.config = MonitoringConfig()
        self.storage = StateStorage(self.project_path, self.config)
        self.state_manager = TaskStateManager(self.storage, self.config)
        self.progress_calculator = ProgressCalculator()
        self.display = StatusDisplay(no_color=no_color)

    def status(self, feature_id: Optional[str] = None, verbose_mode: bool = False) -> str:
        """Show current task status and progress."""
        try:
            # Auto-discover feature if not specified
            if not feature_id:
                features = self.storage.get_all_features()
                if not features:
                    return "No active features found. Initialize a feature first."
                feature_id = features[0]  # Use most recent feature

            # Load tasks and calculate progress
            tasks = self.state_manager.get_tasks(feature_id)
            if not tasks:
                return f"No tasks found for feature {feature_id}."

            progress = self.progress_calculator.calculate_progress(tasks, feature_id)

            # Generate status display
            output = self.display.show_status(progress, tasks, verbose_mode)

            return output

        except Exception as e:
            if self.verbose:
                import traceback
                return f"Error getting status: {e}\n{traceback.format_exc()}"
            return f"Error getting status: {e}"

    def progress(self, feature_id: Optional[str] = None, detailed: bool = False) -> str:
        """Show detailed progress analytics."""
        try:
            # Auto-discover feature if not specified
            if not feature_id:
                features = self.storage.get_all_features()
                if not features:
                    return "No active features found. Initialize a feature first."
                feature_id = features[0]

            # Load historical data
            history = self.storage.load_history(feature_id, limit=50)
            current_progress = self.storage.load_progress(feature_id)

            # Generate progress display
            output = self.display.show_progress(current_progress, history, detailed)

            return output

        except Exception as e:
            if self.verbose:
                import traceback
                return f"Error getting progress: {e}\n{traceback.format_exc()}"
            return f"Error getting progress: {e}"

    def reset(self, feature_id: Optional[str] = None, confirm: bool = False) -> str:
        """Reset monitoring data for a feature."""
        try:
            # Auto-discover feature if not specified
            if not feature_id:
                features = self.storage.get_all_features()
                if not features:
                    return "No active features found. Initialize a feature first."
                feature_id = features[0]

            if not confirm:
                return f"Use --confirm to reset all monitoring data for feature {feature_id}."

            # Reset feature data
            self.storage.reset_feature_data(feature_id)

            return f"✓ Reset monitoring data for feature {feature_id}"

        except Exception as e:
            if self.verbose:
                import traceback
                return f"Error resetting data: {e}\n{traceback.format_exc()}"
            return f"Error resetting data: {e}"

    def history(self, feature_id: Optional[str] = None, limit: int = 20) -> str:
        """Show historical task state changes."""
        try:
            # Auto-discover feature if not specified
            if not feature_id:
                features = self.storage.get_all_features()
                if not features:
                    return "No active features found. Initialize a feature first."
                feature_id = features[0]

            # Load history
            history = self.storage.load_history(feature_id, limit=limit)

            if not history:
                return f"No history found for feature {feature_id}."

            # Generate history display
            output = self.display.show_history(history, limit)

            return output

        except Exception as e:
            if self.verbose:
                import traceback
                return f"Error getting history: {e}\n{traceback.format_exc()}"
            return f"Error getting history: {e}"

    def validate(self) -> str:
        """Validate monitoring data integrity."""
        try:
            report = self.storage.validate_data_integrity()

            if report["valid"]:
                output = "✓ All monitoring data is valid\n\n"
            else:
                output = "⚠ Issues found in monitoring data:\n\n"

            output += "Files checked:\n"
            for file_status in report["files_checked"]:
                output += f"  {file_status}\n"

            if report["issues"]:
                output += "\nIssues:\n"
                for issue in report["issues"]:
                    output += f"  ❌ {issue}\n"

            return output

        except Exception as e:
            if self.verbose:
                import traceback
                return f"Error validating data: {e}\n{traceback.format_exc()}"
            return f"Error validating data: {e}"

    def sync(self, feature_id: Optional[str] = None, direction: str = "full") -> str:
        """Synchronize task states between monitor and task files."""
        try:
            from .task_updater import TaskFileSyncManager

            # Auto-discover feature if not specified
            if not feature_id:
                features = self.storage.get_all_features()
                if not features:
                    return "No active features found. Initialize a feature first."
                feature_id = features[0]

            sync_manager = TaskFileSyncManager(self.project_path)

            if direction == "full":
                result = sync_manager.full_sync(feature_id)
                output = f"🔄 Full synchronization completed for feature {feature_id}\n\n"
                output += f"Discrepancies found: {result['total_discrepancies']}\n"
                output += f"Task files updated: {result['files_updated']}\n"

                if result['total_discrepancies'] > 0:
                    output += "\nDiscrepancies resolved:\n"
                    for task_id, details in result['file_to_monitor']['discrepancies'].items():
                        output += f"  {task_id}: {details['file_state']} → {details['monitor_state']}\n"

            elif direction == "to_files":
                results = sync_manager.sync_from_monitor_to_files(feature_id)
                output = f"📝 Synced monitor states to task files for feature {feature_id}\n\n"
                output += f"Tasks updated: {sum(results.values())}/{len(results)}\n"

                failed_tasks = [task_id for task_id, success in results.items() if not success]
                if failed_tasks:
                    output += f"\nFailed to update: {', '.join(failed_tasks)}"

            elif direction == "from_files":
                result = sync_manager.sync_from_files_to_monitor(feature_id)
                output = f"📖 Synced task file states to monitor for feature {feature_id}\n\n"
                output += f"Files scanned: {result['total_files']}\n"
                output += f"Tasks synced: {result['synced_count']}\n"

                if result['discrepancies']:
                    output += "\nDiscrepancies found:\n"
                    for task_id, details in result['discrepancies'].items():
                        output += f"  {task_id}: {details['action']} ({details['file_state']} → {details['monitor_state']})\n"

            else:
                output = f"❌ Invalid sync direction: {direction}. Use 'full', 'to_files', or 'from_files'."

            return output

        except Exception as e:
            if self.verbose:
                import traceback
                return f"Error syncing data: {e}\n{traceback.format_exc()}"
            return f"Error syncing data: {e}"