"""
Task File Updater Module

This module provides functionality to automatically update task markdown files
when task states change, ensuring bidirectional synchronization between
monitoring system and task files.
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from .models import TaskInfo, TaskState
from .errors import MonitorError, safe_execute


class TaskFileUpdater:
    """Handles automatic updates to task markdown files."""

    def __init__(self, project_path: Path):
        """Initialize task file updater."""
        self.project_path = Path(project_path)
        self.tasks_base_path = self.project_path / ".specpulse" / "tasks"

    def update_task_file(self, task: TaskInfo, feature_id: str) -> bool:
        """Update task markdown file with new state information."""
        try:
            task_file = self._find_task_file(task.id, feature_id)
            if not task_file:
                return False

            return self._update_file_content(task_file, task)
        except Exception as e:
            raise MonitorError(f"Failed to update task file: {e}",
                             suggestion="Check file permissions and task file format")

    def _find_task_file(self, task_id: str, feature_id: str) -> Optional[Path]:
        """Find the markdown file for a given task."""
        feature_dir = self.tasks_base_path / feature_id
        if not feature_dir.exists():
            return None

        # Try different naming patterns
        patterns = [
            f"task-{task_id.replace('T', '')}.md",
            f"{task_id.lower()}.md",
            f"{task_id}.md"
        ]

        # Direct pattern matching
        for pattern in patterns:
            task_file = feature_dir / pattern
            if task_file.exists():
                return task_file

        # Search in all markdown files
        for md_file in feature_dir.glob("*.md"):
            if self._file_contains_task_id(md_file, task_id):
                return md_file

        return None

    def _file_contains_task_id(self, file_path: Path, task_id: str) -> bool:
        """Check if file contains the specified task ID."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for task ID patterns
            patterns = [
                rf"###\s*{re.escape(task_id)}:",
                rf"##\s*{re.escape(task_id)}:",
                rf"#{1,4}\s*.*{re.escape(task_id)}",
                rf"ID:\s*{re.escape(task_id)}",
                rf"Task ID:\s*{re.escape(task_id)}"
            ]

            return any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)
        except Exception:
            return False

    def _update_file_content(self, file_path: Path, task: TaskInfo) -> bool:
        """Update the content of a task markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            updated_content = self._apply_state_updates(content, task)

            # Only write if content actually changed
            if updated_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

            return True
        except Exception:
            return False

    def _apply_state_updates(self, content: str, task: TaskInfo) -> str:
        """Apply state updates to task content."""
        updated_content = content

        # Update task state checkboxes
        updated_content = self._update_task_checkboxes(updated_content, task.state)

        # Update status section
        updated_content = self._update_status_section(updated_content, task)

        # Add/update metadata section
        updated_content = self._update_metadata_section(updated_content, task)

        # Update timestamp
        updated_content = self._update_timestamp(updated_content)

        return updated_content

    def _update_task_checkboxes(self, content: str, state: TaskState) -> str:
        """Update task checkboxes based on state."""
        lines = content.split('\n')
        updated_lines = []

        # State to checkbox mapping
        checkbox_map = {
            TaskState.COMPLETED: "[x]",
            TaskState.IN_PROGRESS: "[>]",
            TaskState.BLOCKED: "[!]",
            TaskState.PENDING: "[ ]"
        }

        target_checkbox = checkbox_map[state]

        for line in lines:
            # Look for checkbox patterns
            if re.match(r'^\s*-\s*\[[x\s>!]\]', line):
                # Update the first checkbox found (assuming main task checkbox)
                line = re.sub(r'^(\s*-\s*)\[[x\s>!]\]', r'\1' + target_checkbox, line, count=1)
            updated_lines.append(line)

        return '\n'.join(updated_lines)

    def _update_status_section(self, content: str, task: TaskInfo) -> str:
        """Update or add status section."""
        # Look for existing status section
        status_pattern = r'\*\*Status:\*\*\s*(.+?)(?=\n\n|\n[A-Z#*]|\Z)'
        status_match = re.search(status_pattern, content, re.DOTALL | re.IGNORECASE)

        state_text = {
            TaskState.COMPLETED: "✅ completed",
            TaskState.IN_PROGRESS: "🔄 in_progress",
            TaskState.BLOCKED: "❌ blocked",
            TaskState.PENDING: "⏳ pending"
        }.get(task.state, str(task.state))

        if status_match:
            # Update existing status
            content = re.sub(
                status_pattern,
                f"**Status:** {state_text}",
                content,
                flags=re.DOTALL | re.IGNORECASE
            )
        else:
            # Add status section before the end
            content = content.rstrip() + f"\n\n**Status:** {state_text}\n"

        return content

    def _update_metadata_section(self, content: str, task: TaskInfo) -> str:
        """Update or add metadata section."""
        metadata_section = f"""
---
**Task Metadata:**
- **Last Updated**: {task.last_updated.strftime('%Y-%m-%d %H:%M:%S')}
- **State**: {task.state.value}
- **Execution Time**: {task.execution_time or 'N/A'} seconds
- **Error Message**: {task.error_message or 'N/A'}
---
"""

        # Remove existing metadata section if present
        content = re.sub(
            r'\n?---\*\*Task Metadata:\*\*.*?---\n?',
            '',
            content,
            flags=re.DOTALL
        )

        # Add new metadata section at the end
        content = content.rstrip() + metadata_section

        return content

    def _update_timestamp(self, content: str) -> str:
        """Update timestamp in content."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Look for existing timestamp patterns
        timestamp_patterns = [
            (r'Last Updated:\s*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}',
             f'Last Updated: {timestamp}'),
            (r'Updated:\s*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}',
             f'Updated: {timestamp}'),
            (r'Modified:\s*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}',
             f'Modified: {timestamp}')
        ]

        for pattern, replacement in timestamp_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        return content

    def bulk_update_tasks(self, tasks: List[TaskInfo], feature_id: str) -> Dict[str, bool]:
        """Update multiple task files at once."""
        results = {}

        for task in tasks:
            success = self.update_task_file(task, feature_id)
            results[task.id] = success

        return results

    def get_task_file_state(self, task_id: str, feature_id: str) -> Optional[TaskState]:
        """Read task state from file (for verification)."""
        task_file = self._find_task_file(task_id, feature_id)
        if not task_file:
            return None

        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for completed checkbox
            if re.search(r'-\s*\[x\]', content):
                return TaskState.COMPLETED

            # Check for in-progress checkbox
            if re.search(r'-\s*\[>\]', content):
                return TaskState.IN_PROGRESS

            # Check for blocked checkbox
            if re.search(r'-\s*\[!\]', content):
                return TaskState.BLOCKED

            # Check for pending checkbox or no checkbox
            if re.search(r'-\s*\[\s\]', content):
                return TaskState.PENDING

            return TaskState.PENDING  # Default

        except Exception:
            return None

    def sync_task_states(self, feature_id: str) -> Dict[str, str]:
        """Synchronize task states between monitor and files."""
        sync_results = {}

        # Get all task files in feature directory
        feature_dir = self.tasks_base_path / feature_id
        if not feature_dir.exists():
            return sync_results

        for task_file in feature_dir.glob("*.md"):
            try:
                task_id = self._extract_task_id_from_file(task_file)
                if task_id:
                    file_state = self.get_task_file_state(task_id, feature_id)
                    if file_state:
                        sync_results[task_id] = file_state.value
            except Exception:
                continue

        return sync_results

    def _extract_task_id_from_file(self, file_path: Path) -> Optional[str]:
        """Extract task ID from filename or content."""
        # Try filename first
        filename_match = re.match(r'task-(\d+)', file_path.stem, re.IGNORECASE)
        if filename_match:
            return f"T{filename_match.group(1).zfill(3)}"

        # Try content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            patterns = [
                r'###\s*T(\d+):',
                r'###\s*([A-Z]+-\d+):',
                r'Task\s+ID:\s*(\w+)',
                r'ID:\s*(\w+)'
            ]

            for pattern in patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    task_id = match.group(1)
                    if task_id.isdigit():
                        return f"T{task_id.zfill(3)}"
                    return task_id.upper()
        except Exception:
            pass

        return None


class TaskFileSyncManager:
    """Manages bidirectional synchronization between monitor and task files."""

    def __init__(self, project_path: Path):
        """Initialize sync manager."""
        self.project_path = Path(project_path)
        self.updater = TaskFileUpdater(project_path)

    def sync_from_monitor_to_files(self, feature_id: str) -> Dict[str, bool]:
        """Sync task states from monitor system to task files."""
        from .state_manager import TaskStateManager
        from .storage import StateStorage

        storage = StateStorage(self.project_path)
        state_manager = TaskStateManager(storage, storage.config)

        # Get current tasks from monitor
        tasks = state_manager.get_tasks(feature_id)

        # Update all task files
        return self.updater.bulk_update_tasks(tasks, feature_id)

    def sync_from_files_to_monitor(self, feature_id: str) -> Dict[str, Any]:
        """Sync task states from task files to monitor system."""
        from .state_manager import TaskStateManager
        from .storage import StateStorage

        storage = StateStorage(self.project_path)
        state_manager = TaskStateManager(storage, storage.config)

        # Get file states
        file_states = self.updater.sync_task_states(feature_id)

        # Get monitor states
        monitor_tasks = state_manager.get_tasks(feature_id)
        monitor_states = {task.id: task.state for task in monitor_tasks}

        # Find discrepancies
        discrepancies = {}
        sync_results = {}

        for task_id, file_state_name in file_states.items():
            from .models import TaskState
            try:
                file_state = TaskState.from_string(file_state_name)
            except ValueError:
                continue

            if task_id in monitor_states:
                monitor_state = monitor_states[task_id]
                if monitor_state != file_state:
                    discrepancies[task_id] = {
                        'file_state': file_state.value,
                        'monitor_state': monitor_state.value,
                        'action': 'update_monitor'
                    }
                    # Update monitor state to match file
                    success = state_manager.update_task_state(
                        feature_id, task_id, file_state
                    )
                    sync_results[task_id] = success
            else:
                # Task exists in file but not in monitor
                discrepancies[task_id] = {
                    'file_state': file_state.value,
                    'monitor_state': None,
                    'action': 'add_to_monitor'
                }

        return {
            'discrepancies': discrepancies,
            'sync_results': sync_results,
            'total_files': len(file_states),
            'synced_count': len(sync_results)
        }

    def full_sync(self, feature_id: str) -> Dict[str, Any]:
        """Perform full bidirectional synchronization."""
        print(f"Starting full synchronization for feature {feature_id}...")

        # Sync from files to monitor (file is source of truth)
        file_to_monitor = self.sync_from_files_to_monitor(feature_id)

        # Sync from monitor to files (ensure consistency)
        monitor_to_files = self.sync_from_monitor_to_files(feature_id)

        return {
            'feature_id': feature_id,
            'file_to_monitor': file_to_monitor,
            'monitor_to_files': monitor_to_files,
            'total_discrepancies': len(file_to_monitor.get('discrepancies', {})),
            'files_updated': len(monitor_to_files)
        }