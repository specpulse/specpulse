"""
Task State Manager Module

This module provides the TaskStateManager class for handling task state transitions,
automatic task discovery, and historical state tracking.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime

from .models import TaskInfo, TaskState, TaskHistory, MonitoringConfig
from .storage import StateStorage


class TaskStateManager:
    """Manages task states with automatic discovery and historical tracking."""

    def __init__(self, storage: StateStorage, config: MonitoringConfig):
        """Initialize state manager with storage and configuration."""
        self.storage = storage
        self.config = config
        self._task_cache: Dict[str, List[TaskInfo]] = {}
        self._last_discovery: Dict[str, datetime] = {}

    def discover_tasks(self, feature_id: str) -> List[TaskInfo]:
        """Automatically discover tasks from .specpulse/tasks/ directories."""
        # Check cache first
        if self._should_use_cache(feature_id):
            return self._task_cache.get(feature_id, [])

        tasks_path = self.storage.project_path / ".specpulse" / "tasks" / feature_id
        discovered_tasks = []

        if tasks_path.exists():
            # Discover tasks from markdown files
            for task_file in tasks_path.glob("*.md"):
                task_info = self._parse_task_file(task_file, feature_id)
                if task_info:
                    discovered_tasks.append(task_info)

        # Load existing states from storage
        existing_tasks = self.storage.load_tasks(feature_id)
        existing_task_map = {task.id: task for task in existing_tasks}

        # Merge discovered tasks with existing states
        merged_tasks = []
        for discovered_task in discovered_tasks:
            if discovered_task.id in existing_task_map:
                # Use existing state but update title if changed
                existing_task = existing_task_map[discovered_task.id]
                existing_task.title = discovered_task.title
                merged_tasks.append(existing_task)
            else:
                # New task discovered
                merged_tasks.append(discovered_task)

        # Add tasks that exist in storage but weren't discovered (might be archived)
        for existing_task in existing_tasks:
            if existing_task.id not in {task.id for task in discovered_tasks}:
                merged_tasks.append(existing_task)

        # Update cache
        self._task_cache[feature_id] = merged_tasks
        self._last_discovery[feature_id] = datetime.now()

        # Save merged tasks
        self.storage.save_tasks(merged_tasks, feature_id)

        return merged_tasks

    def _should_use_cache(self, feature_id: str) -> bool:
        """Check if cached data is still valid."""
        if feature_id not in self._task_cache:
            return False

        if feature_id not in self._last_discovery:
            return False

        time_since_discovery = datetime.now() - self._last_discovery[feature_id]
        return time_since_discovery.total_seconds() < self.config.update_interval_seconds

    def _parse_task_file(self, file_path: Path, feature_id: str) -> Optional[TaskInfo]:
        """Parse a task markdown file and extract task information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract task ID from filename or content
            task_id = self._extract_task_id(file_path, content)
            if not task_id:
                return None

            # Extract task title from content
            title = self._extract_task_title(content)
            if not title:
                title = f"Task {task_id}"

            # Check if task is completed based on checkbox status
            state = self._determine_task_state(content)

            return TaskInfo(
                id=task_id,
                title=title,
                state=state,
                last_updated=datetime.now(),
                description=self._extract_task_description(content)
            )

        except Exception:
            # Skip files that can't be parsed
            return None

    def _extract_task_id(self, file_path: Path, content: str) -> Optional[str]:
        """Extract task ID from filename or content."""
        # Try to extract from filename first
        filename_match = re.match(r'task-(\d+)', file_path.stem, re.IGNORECASE)
        if filename_match:
            return f"T{filename_match.group(1).zfill(3)}"

        # Try to extract from content
        id_patterns = [
            r'###\s*T(\d+):',
            r'###\s*([A-Z]+-\d+):',
            r'Task\s+ID:\s*(\w+)',
            r'ID:\s*(\w+)',
        ]

        for pattern in id_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                task_id = match.group(1)
                # Normalize format
                if task_id.isdigit():
                    return f"T{task_id.zfill(3)}"
                return task_id.upper()

        return None

    def _extract_task_title(self, content: str) -> Optional[str]:
        """Extract task title from content."""
        patterns = [
            r'###\s*[A-Z0-9-]+:\s*(.+)$',
            r'#{1,3}\s*(.+)$',
            r'Title:\s*(.+)$',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Remove common prefixes
                title = re.sub(r'^(Task|T\d+)\s*[-:]?\s*', '', title, flags=re.IGNORECASE)
                return title if title else None

        return None

    def _extract_task_description(self, content: str) -> Optional[str]:
        """Extract task description from content."""
        # Look for description section
        desc_match = re.search(r'Description:\s*(.+?)(?=\n\n|\n[A-Z]|\Z)', content, re.DOTALL | re.IGNORECASE)
        if desc_match:
            return desc_match.group(1).strip()

        # Look for first paragraph after title
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#') and i + 1 < len(lines):
                # Found a title, get next non-empty line
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        return lines[j].strip()

        return None

    def _determine_task_state(self, content: str) -> TaskState:
        """Determine task state based on checkbox patterns."""
        # Look for completed checkbox pattern
        if re.search(r'-\s*\[x\]', content, re.IGNORECASE):
            return TaskState.COMPLETED

        # Look for in-progress checkbox pattern
        if re.search(r'-\s*\[>\]', content, re.IGNORECASE):
            return TaskState.IN_PROGRESS

        # Look for blocked checkbox pattern
        if re.search(r'-\s*\[!\]', content, re.IGNORECASE):
            return TaskState.BLOCKED

        # Look for error indicators
        if re.search(r'error|failed|exception', content, re.IGNORECASE):
            return TaskState.BLOCKED

        # Default to pending
        return TaskState.PENDING

    def get_tasks(self, feature_id: str) -> List[TaskInfo]:
        """Get all tasks for a feature, with automatic discovery."""
        if self.config.auto_discovery:
            return self.discover_tasks(feature_id)
        else:
            return self.storage.load_tasks(feature_id)

    def get_task(self, feature_id: str, task_id: str) -> Optional[TaskInfo]:
        """Get a specific task by ID."""
        tasks = self.get_tasks(feature_id)
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def update_task_state(self, feature_id: str, task_id: str, new_state: TaskState,
                         error_message: Optional[str] = None, notes: Optional[str] = None) -> bool:
        """Update task state with validation and history tracking."""
        task = self.get_task(feature_id, task_id)
        if not task:
            return False

        old_state = task.state

        # Validate state transition
        try:
            task.transition_to(new_state, error_message)
        except ValueError:
            return False

        # Save history entry
        history = TaskHistory(
            task_id=task_id,
            timestamp=datetime.now(),
            old_state=old_state,
            new_state=new_state,
            notes=notes
        )
        self.storage.save_history_entry(history)

        # Save updated task
        self.storage.save_task_state(task, feature_id)

        # Update task file automatically
        from .task_updater import TaskFileUpdater
        try:
            updater = TaskFileUpdater(self.storage.project_path)
            updater.update_task_file(task, feature_id)
        except Exception:
            # Don't let file update failures break task state management
            pass

        # Update cache
        if feature_id in self._task_cache:
            for i, cached_task in enumerate(self._task_cache[feature_id]):
                if cached_task.id == task_id:
                    self._task_cache[feature_id][i] = task
                    break

        return True

    def start_task(self, feature_id: str, task_id: str) -> bool:
        """Mark a task as in-progress."""
        return self.update_task_state(feature_id, task_id, TaskState.IN_PROGRESS)

    def complete_task(self, feature_id: str, task_id: str, execution_time: Optional[float] = None) -> bool:
        """Mark a task as completed."""
        task = self.get_task(feature_id, task_id)
        if not task:
            return False

        if execution_time:
            task.execution_time = execution_time

        return self.update_task_state(feature_id, task_id, TaskState.COMPLETED)

    def block_task(self, feature_id: str, task_id: str, error_message: str) -> bool:
        """Mark a task as blocked with an error message."""
        return self.update_task_state(
            feature_id, task_id, TaskState.BLOCKED,
            error_message=error_message
        )

    def reset_task(self, feature_id: str, task_id: str) -> bool:
        """Reset a task to pending state."""
        return self.update_task_state(feature_id, task_id, TaskState.PENDING)

    def get_task_statistics(self, feature_id: str) -> Dict[str, int]:
        """Get task count statistics by state."""
        tasks = self.get_tasks(feature_id)
        stats = {
            "total": len(tasks),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "blocked": 0
        }

        for task in tasks:
            stats[task.state.value] += 1

        return stats

    def get_tasks_by_state(self, feature_id: str, state: TaskState) -> List[TaskInfo]:
        """Get all tasks in a specific state."""
        tasks = self.get_tasks(feature_id)
        return [task for task in tasks if task.state == state]

    def clear_cache(self, feature_id: Optional[str] = None) -> None:
        """Clear task discovery cache."""
        if feature_id:
            self._task_cache.pop(feature_id, None)
            self._last_discovery.pop(feature_id, None)
        else:
            self._task_cache.clear()
            self._last_discovery.clear()

    def refresh_tasks(self, feature_id: str) -> List[TaskInfo]:
        """Force refresh of task discovery."""
        self.clear_cache(feature_id)
        return self.discover_tasks(feature_id)