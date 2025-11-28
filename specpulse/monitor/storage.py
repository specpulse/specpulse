"""
State Storage Module for Task Monitor

This module provides atomic file operations for persisting task state data.
Ensures data integrity with atomic writes, backup procedures, and JSON schema validation.
"""

import json
import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import threading
from contextlib import contextmanager

# Import platform-specific file locking
if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

from .models import TaskInfo, ProgressData, TaskHistory, MonitoringConfig


class StateStorage:
    """Handles atomic file operations for task state persistence."""

    def __init__(self, project_path: Path, config: Optional[MonitoringConfig] = None):
        """Initialize storage with project path and configuration."""
        self.project_path = Path(project_path)
        self.memory_path = self.project_path / ".specpulse" / "memory"
        self.config = config or MonitoringConfig()

        # Ensure memory directory exists
        self.memory_path.mkdir(parents=True, exist_ok=True)

        # File paths
        self.state_file = self.memory_path / "task-states.json"
        self.progress_file = self.memory_path / "task-progress.json"
        self.history_file = self.memory_path / "task-history.json"
        self.config_file = self.memory_path / "monitor-config.json"

        # Backup directory
        self.backup_dir = self.memory_path / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        # Progress and history directories for individual features
        self.progress_dir = self.memory_path / "progress"
        self.history_dir = self.memory_path / "history"
        self.progress_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)

        # Thread safety
        self._locks = {
            'state': threading.RLock(),
            'progress': threading.RLock(),
            'history': threading.RLock(),
            'config': threading.RLock(),
        }

        # Initialize files if they don't exist
        self._initialize_files()

    def _initialize_files(self) -> None:
        """Create default files if they don't exist."""
        default_files = {
            self.state_file: {"tasks": {}, "metadata": {"last_updated": datetime.now().isoformat()}},
            self.progress_file: {"features": {}, "metadata": {"last_updated": datetime.now().isoformat()}},
            self.history_file: {"history": [], "metadata": {"last_updated": datetime.now().isoformat()}},
            self.config_file: self.config.to_dict(),
        }

        for file_path, default_content in default_files.items():
            if not file_path.exists():
                self._atomic_write(file_path, default_content)

    @contextmanager
    def _file_lock(self, file_type: str):
        """Context manager for thread-safe and process-safe file operations."""
        # Thread-level lock
        lock = self._locks[file_type]
        lock.acquire()

        # Process-level lock using lock file
        lock_file_map = {
            'state': self.memory_path / '.state.lock',
            'progress': self.memory_path / '.progress.lock',
            'history': self.memory_path / '.history.lock',
            'config': self.memory_path / '.config.lock',
        }

        lock_file_path = lock_file_map.get(file_type)
        lock_file = None

        try:
            if lock_file_path:
                # Create lock file if it doesn't exist
                lock_file_path.touch(exist_ok=True)
                lock_file = open(lock_file_path, 'w')

                # Acquire file-level lock (process-safe)
                if sys.platform == "win32":
                    # Windows file locking
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
                else:
                    # Unix file locking
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)

            yield

        finally:
            # Release file-level lock
            if lock_file:
                try:
                    if sys.platform == "win32":
                        msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                    lock_file.close()
                except Exception:
                    pass  # Best effort to release

            # Release thread-level lock
            lock.release()

    def _atomic_write(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Write data to file atomically using temporary file and rename."""
        # Create temporary file in same directory to ensure atomic rename
        temp_fd, temp_path = tempfile.mkstemp(
            dir=file_path.parent,
            prefix=f".{file_path.stem}_tmp_",
            suffix=file_path.suffix
        )

        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)

            # Use os.replace() for truly atomic replacement on all platforms
            # os.replace() handles Windows' requirement to remove existing files atomically
            os.replace(temp_path, file_path)

        except Exception:
            # Clean up temp file if something went wrong
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except OSError:
                pass
            raise

    def _backup_file(self, file_path: Path) -> None:
        """Create backup of file before modification if backup is enabled."""
        if not self.config.backup_enabled or not file_path.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = self.backup_dir / backup_name

        try:
            shutil.copy2(file_path, backup_path)
            self._cleanup_old_backups()
        except Exception:
            # Don't fail if backup fails, but log warning in real implementation
            pass

    def _cleanup_old_backups(self) -> None:
        """Remove old backup files keeping only the most recent ones."""
        if not self.backup_dir.exists():
            return

        backup_files = list(self.backup_dir.glob("task-states_*.json"))
        backup_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Keep only the most recent backups
        for backup_file in backup_files[self.config.max_backups:]:
            try:
                backup_file.unlink()
            except OSError:
                pass

    def _read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Read and parse JSON file with error handling."""
        if not file_path.exists():
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # In case of corrupted file, try to restore from backup
            return self._restore_from_backup(file_path) or {}

    def _restore_from_backup(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Attempt to restore file from latest backup."""
        if not self.backup_dir.exists():
            return None

        # Find most recent backup for this file
        backup_pattern = f"{file_path.stem}_*{file_path.suffix}"
        backup_files = list(self.backup_dir.glob(backup_pattern))

        if not backup_files:
            return None

        # Get the most recent backup
        latest_backup = max(backup_files, key=lambda p: p.stat().st_mtime)

        try:
            with open(latest_backup, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    # Task State Operations
    def save_tasks(self, tasks: List[TaskInfo], feature_id: str) -> None:
        """Save tasks for a specific feature."""
        with self._file_lock('state'):
            self._backup_file(self.state_file)

            # Read existing data
            data = self._read_json_file(self.state_file)

            # Update tasks for this feature
            data["tasks"][feature_id] = {
                task.id: task.to_dict() for task in tasks
            }
            data["metadata"]["last_updated"] = datetime.now().isoformat()

            self._atomic_write(self.state_file, data)

    def load_tasks(self, feature_id: str) -> List[TaskInfo]:
        """Load tasks for a specific feature."""
        with self._file_lock('state'):
            data = self._read_json_file(self.state_file)

            feature_tasks = data.get("tasks", {}).get(feature_id, {})
            return [
                TaskInfo.from_dict(task_data)
                for task_data in feature_tasks.values()
            ]

    def save_task_state(self, task: TaskInfo, feature_id: str) -> None:
        """Save a single task state change."""
        with self._file_lock('state'):
            self._backup_file(self.state_file)

            data = self._read_json_file(self.state_file)

            if feature_id not in data["tasks"]:
                data["tasks"][feature_id] = {}

            data["tasks"][feature_id][task.id] = task.to_dict()
            data["metadata"]["last_updated"] = datetime.now().isoformat()

            self._atomic_write(self.state_file, data)

    # Progress Data Operations
    def save_progress(self, progress: ProgressData) -> None:
        """Save progress data for a feature."""
        with self._file_lock('progress'):
            self._backup_file(self.progress_file)

            data = self._read_json_file(self.progress_file)

            if progress.feature_id:
                data["features"][progress.feature_id] = progress.to_dict()
            data["metadata"]["last_updated"] = datetime.now().isoformat()

            self._atomic_write(self.progress_file, data)

    def load_progress(self, feature_id: str) -> Optional[ProgressData]:
        """Load progress data for a feature."""
        with self._file_lock('progress'):
            data = self._read_json_file(self.progress_file)

            feature_data = data.get("features", {}).get(feature_id)
            if feature_data:
                return ProgressData.from_dict(feature_data)

        return None

    # History Operations
    def save_history_entry(self, history: TaskHistory) -> None:
        """Save a single history entry."""
        with self._file_lock('history'):
            self._backup_file(self.history_file)

            data = self._read_json_file(self.history_file)

            data["history"].append(history.to_dict())
            data["metadata"]["last_updated"] = datetime.now().isoformat()

            # Cleanup old history entries
            cutoff_date = datetime.now() - timedelta(days=self.config.history_retention_days)
            data["history"] = [
                entry for entry in data["history"]
                if datetime.fromisoformat(entry["timestamp"]) > cutoff_date
            ]

            self._atomic_write(self.history_file, data)

    def load_history(self, feature_id: str, limit: Optional[int] = None) -> List[TaskHistory]:
        """Load history entries for a feature."""
        # BUG-006 FIX: Validate feature_id is not empty to prevent returning all entries
        if not feature_id or not feature_id.strip():
            return []

        with self._file_lock('history'):
            data = self._read_json_file(self.history_file)

            # Extract feature prefix safely
            feature_prefix = feature_id.split("-")[0] if "-" in feature_id else feature_id

            history_entries = [
                TaskHistory.from_dict(entry)
                for entry in data.get("history", [])
                if feature_prefix and entry.get("task_id", "").startswith(feature_prefix)
            ]

            # Sort by timestamp (newest first)
            history_entries.sort(key=lambda h: h.timestamp, reverse=True)

            if limit:
                history_entries = history_entries[:limit]

            return history_entries

    # Configuration Operations
    def save_config(self, config: MonitoringConfig) -> None:
        """Save monitoring configuration."""
        with self._file_lock('config'):
            self._atomic_write(self.config_file, config.to_dict())
            self.config = config

    def load_config(self) -> MonitoringConfig:
        """Load monitoring configuration."""
        with self._file_lock('config'):
            if self.config_file.exists():
                data = self._read_json_file(self.config_file)
                self.config = MonitoringConfig.from_dict(data)

            return self.config

    # Utility Methods
    def get_all_features(self) -> List[str]:
        """Get list of all feature IDs with stored data."""
        with self._file_lock('state'):
            data = self._read_json_file(self.state_file)
            return list(data.get("tasks", {}).keys())

    def reset_feature_data(self, feature_id: str) -> None:
        """Remove all data for a specific feature."""
        with self._file_lock('state'), self._file_lock('progress'):
            # Reset tasks
            self._backup_file(self.state_file)
            state_data = self._read_json_file(self.state_file)
            state_data["tasks"].pop(feature_id, None)
            state_data["metadata"]["last_updated"] = datetime.now().isoformat()
            self._atomic_write(self.state_file, state_data)

            # Reset progress
            self._backup_file(self.progress_file)
            progress_data = self._read_json_file(self.progress_file)
            progress_data["features"].pop(feature_id, None)
            progress_data["metadata"]["last_updated"] = datetime.now().isoformat()
            self._atomic_write(self.progress_file, progress_data)

    def validate_data_integrity(self) -> Dict[str, Any]:
        """Validate integrity of stored data and return report."""
        report = {
            "valid": True,
            "issues": [],
            "files_checked": []
        }

        files_to_check = [
            ("task-states.json", self.state_file),
            ("task-progress.json", self.progress_file),
            ("task-history.json", self.history_file),
            ("monitor-config.json", self.config_file),
        ]

        for filename, filepath in files_to_check:
            try:
                if filepath.exists():
                    data = self._read_json_file(filepath)
                    if not isinstance(data, dict):
                        report["issues"].append(f"{filename}: Invalid data format")
                        report["valid"] = False
                    report["files_checked"].append(f"{filename}: OK")
                else:
                    report["files_checked"].append(f"{filename}: Not found")
            except Exception as e:
                report["issues"].append(f"{filename}: {str(e)}")
                report["valid"] = False

        return report