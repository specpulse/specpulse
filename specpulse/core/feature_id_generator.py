"""
Thread-Safe Feature ID Generator

This module provides atomic feature ID generation with file locking
to prevent race conditions when multiple processes/threads create features.

CRITICAL: Use this instead of scanning directories to avoid duplicate IDs.

Platform Support:
- Unix/Linux/macOS: fcntl file locking
- Windows: msvcrt file locking
"""

from pathlib import Path
from typing import Optional
import platform
import time


class FeatureIDGenerator:
    """
    Thread-safe and process-safe feature ID generation.

    Uses file locking to ensure atomic ID generation across:
    - Multiple threads
    - Multiple processes
    - Multiple users (same project)

    The counter is persisted in .specpulse/feature_counter.txt and
    locked during read-modify-write operations.

    Example:
        >>> gen = FeatureIDGenerator(project_root)
        >>> feature_id = gen.get_next_id()  # "001"
        >>> feature_id = gen.get_next_id()  # "002"
        >>> # Even if called simultaneously, no duplicates!
    """

    LOCK_TIMEOUT = 5.0  # Maximum time to wait for lock (seconds)
    COUNTER_FILE = "feature_counter.txt"
    LOCK_FILE = "feature_id.lock"

    def __init__(self, project_root: Path):
        """
        Initialize feature ID generator.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root
        self.config_dir = project_root / ".specpulse"
        self.counter_file = self.config_dir / self.COUNTER_FILE
        self.lock_file = self.config_dir / self.LOCK_FILE

        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_next_id(self) -> str:
        """
        Get next available feature ID (thread-safe, process-safe).

        This method uses file locking to ensure atomicity:
        1. Acquire lock
        2. Read current counter
        3. Increment counter
        4. Write new counter
        5. Release lock

        Returns:
            Next feature ID as 3-digit string (e.g., "001", "042")

        Raises:
            TimeoutError: If cannot acquire lock within timeout
            IOError: If file operations fail

        Example:
            >>> gen = FeatureIDGenerator(Path("/project"))
            >>> id1 = gen.get_next_id()  # "001"
            >>> id2 = gen.get_next_id()  # "002"
        """
        # Ensure lock file exists
        if not self.lock_file.exists():
            self.lock_file.touch()

        # Acquire lock with timeout
        lock_acquired = False
        start_time = time.time()

        while not lock_acquired and (time.time() - start_time) < self.LOCK_TIMEOUT:
            try:
                # Platform-specific locking
                if platform.system() == 'Windows':
                    lock_acquired = self._acquire_lock_windows()
                else:
                    lock_acquired = self._acquire_lock_unix()

                if not lock_acquired:
                    time.sleep(0.1)  # Wait 100ms before retry

            except Exception as e:
                raise IOError(f"Failed to acquire lock: {e}")

        if not lock_acquired:
            raise TimeoutError(
                f"Could not acquire feature ID lock within {self.LOCK_TIMEOUT} seconds. "
                "Another process may be holding the lock."
            )

        try:
            # Critical section: read-modify-write
            current_id = self._read_counter()
            next_id = current_id + 1
            self._write_counter(next_id)

            return f"{next_id:03d}"

        finally:
            # Always release lock
            self._release_lock()

    def initialize_from_existing(self) -> int:
        """
        Initialize counter from existing feature directories.

        Scans specs/ directory to find highest existing feature ID,
        then initializes counter accordingly.

        Returns:
            Highest feature ID found (0 if none exist)

        Example:
            >>> gen = FeatureIDGenerator(project_root)
            >>> max_id = gen.initialize_from_existing()
            >>> # If specs/001-auth and specs/002-payment exist: returns 2
        """
        specs_dir = self.project_root / "specs"

        if not specs_dir.exists():
            return 0

        max_id = 0

        for item in specs_dir.iterdir():
            if item.is_dir():
                # Extract feature ID from directory name (e.g., "001-feature" -> 1)
                import re
                match = re.match(r'^(\d{3})-', item.name)
                if match:
                    feature_id = int(match.group(1))
                    max_id = max(max_id, feature_id)

        # Write to counter file
        with self.lock_file.open('w') as lock:
            # Acquire lock during initialization
            if platform.system() == 'Windows':
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX)

            try:
                self._write_counter(max_id)
            finally:
                if platform.system() == 'Windows':
                    import msvcrt
                    msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

        return max_id

    def get_current_id(self) -> int:
        """
        Get current counter value (without incrementing).

        Returns:
            Current feature ID counter
        """
        return self._read_counter()

    # Private methods

    def _read_counter(self) -> int:
        """Read current counter value from file"""
        if not self.counter_file.exists():
            # Initialize from existing features
            return self.initialize_from_existing()

        try:
            content = self.counter_file.read_text().strip()
            return int(content) if content else 0
        except (ValueError, IOError):
            # Corrupted counter file - reinitialize
            return self.initialize_from_existing()

    def _write_counter(self, value: int):
        """Write counter value to file"""
        self.counter_file.write_text(str(value))

    def _acquire_lock_unix(self) -> bool:
        """Acquire lock on Unix systems (fcntl)"""
        try:
            import fcntl

            # Open lock file
            self._lock_fd = self.lock_file.open('w')

            # Try to acquire exclusive lock (non-blocking)
            fcntl.flock(self._lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

            return True

        except BlockingIOError:
            # Lock is held by another process
            if hasattr(self, '_lock_fd'):
                self._lock_fd.close()
            return False

        except Exception:
            if hasattr(self, '_lock_fd'):
                self._lock_fd.close()
            return False

    def _acquire_lock_windows(self) -> bool:
        """Acquire lock on Windows systems (msvcrt)"""
        try:
            import msvcrt

            # Open lock file
            self._lock_fd = self.lock_file.open('w')

            # Try to acquire lock (non-blocking)
            try:
                msvcrt.locking(self._lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
                return True
            except (IOError, OSError):
                # Lock is held by another process
                if hasattr(self, '_lock_fd') and self._lock_fd:
                    self._lock_fd.close()
                    delattr(self, '_lock_fd')
                return False

        except Exception as e:
            # Any other error
            if hasattr(self, '_lock_fd') and self._lock_fd:
                try:
                    self._lock_fd.close()
                except:
                    pass
                if hasattr(self, '_lock_fd'):
                    delattr(self, '_lock_fd')
            return False

    def _release_lock(self):
        """Release file lock (platform-independent)"""
        if not hasattr(self, '_lock_fd'):
            return

        try:
            if platform.system() == 'Windows':
                import msvcrt
                msvcrt.locking(self._lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self._lock_fd.fileno(), fcntl.LOCK_UN)

        except Exception:
            pass  # Best effort

        finally:
            self._lock_fd.close()
            delattr(self, '_lock_fd')


# Convenience function
def get_next_feature_id(project_root: Path) -> str:
    """
    Convenience function to get next feature ID.

    Args:
        project_root: Project root directory

    Returns:
        Next feature ID as 3-digit string

    Example:
        >>> from specpulse.core.feature_id_generator import get_next_feature_id
        >>> next_id = get_next_feature_id(Path("/project"))
        >>> print(next_id)  # "001"
    """
    generator = FeatureIDGenerator(project_root)
    return generator.get_next_id()


__all__ = ['FeatureIDGenerator', 'get_next_feature_id']
