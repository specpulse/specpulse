"""
Universal ID Generator System

This module provides centralized, atomic ID generation for ALL numbering
systems in SpecPulse, ensuring consistency across all entities:

- Features: 001, 002, 003...
- Specifications: spec-001.md, spec-002.md...
- Plans: plan-001.md, plan-002.md...
- Tasks: T001.md, T002.md...
- Decisions: DEC-001, DEC-002...
- Patterns: PATTERN-001, PATTERN-002...
- Constraints: CONST-001, CONST-002...
- Checkpoints: CHK-001, CHK-002...

CRITICAL: ALL ID generation MUST use this system to prevent conflicts
and ensure consistency across the entire project.
"""

import re
import os
import time
import json
from pathlib import Path
from typing import Dict, Optional, Set, Tuple, List
from enum import Enum
from threading import Lock

class IDType(Enum):
    """Supported ID types with their prefixes and formats."""
    FEATURE = ("feature", "001", 3)
    SPECIFICATION = ("spec", "spec-", 3)
    PLAN = ("plan", "plan-", 3)
    TASK = ("task", "T", 3)
    DECISION = ("decision", "DEC-", 3)
    PATTERN = ("pattern", "PATTERN-", 3)
    CONSTRAINT = ("constraint", "CONST-", 3)
    CHECKPOINT = ("checkpoint", "CHK-", 3)
    SERVICE_TASK = ("service_task", None, 3)  # Service-specific: AUTH-T001

class UniversalIDGenerator:
    """
    Universal ID Generator with atomic operations and conflict prevention.

    This system ensures:
    1. No ID conflicts across different entity types
    2. Atomic generation (no race conditions)
    3. Persistent state across sessions
    4. Consistent formatting everywhere
    5. Easy debugging and tracking
    """

    def __init__(self, project_root: Path):
        """
        Initialize universal ID generator.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root.resolve()
        self.config_dir = self.project_root / ".specpulse"
        self.state_file = self.config_dir / "id_registry.json"
        self.lock_file = self.config_dir / "id_registry.lock"

        # Thread safety
        self._lock = Lock()

        # Ensure directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Initialize state
        self._load_state()

    def _load_state(self):
        """Load ID generation state from file."""
        if self.state_file.exists():
            try:
                content = self.state_file.read_text(encoding='utf-8')
                self._state = json.loads(content)
                # Convert lists back to sets
                if 'used_ids' in self._state and isinstance(self._state['used_ids'], list):
                    self._state['used_ids'] = set(self._state['used_ids'])
            except (json.JSONDecodeError, IOError):
                self._state = self._get_default_state()
        else:
            self._state = self._get_default_state()
            self._save_state()

    def _save_state(self):
        """Save ID generation state to file atomically."""
        with self._lock:
            # Write to temporary file first
            temp_file = self.state_file.with_suffix('.tmp')
            try:
                # Convert sets to lists for JSON serialization
                state_copy = self._state.copy()
                if 'used_ids' in state_copy and isinstance(state_copy['used_ids'], set):
                    state_copy['used_ids'] = list(state_copy['used_ids'])
                temp_file.write_text(json.dumps(state_copy, indent=2), encoding='utf-8')
                temp_file.replace(self.state_file)  # Atomic move
            except Exception as e:
                if temp_file.exists():
                    temp_file.unlink()
                raise e

    def _get_default_state(self) -> Dict:
        """Get default state structure."""
        return {
            "counters": {
                "feature": 0,
                "spec": 0,
                "plan": 0,
                "task": 0,
                "decision": 0,
                "pattern": 0,
                "constraint": 0,
                "checkpoint": 0
            },
            "service_counters": {},  # service_name -> counter
            "used_ids": set(),  # Track all used IDs for conflict detection
            "last_updated": None,
            "version": "1.0"
        }

    def _acquire_lock(self, timeout: float = 5.0) -> bool:
        """Acquire file lock for atomic operations."""
        start_time = time.time()

        while True:
            try:
                if os.name == 'nt':  # Windows
                    import msvcrt
                    self._lock_handle = os.open(str(self.lock_file), os.O_CREAT | os.O_WRONLY | os.O_EXCL)
                else:  # Unix/Linux/macOS
                    import fcntl
                    self._lock_handle = os.open(str(self.lock_file), os.O_CREAT | os.O_WRONLY | os.O_EXCL)
                    fcntl.flock(self._lock_handle, fcntl.LOCK_EX)
                return True
            except (OSError, IOError):
                if time.time() - start_time > timeout:
                    raise TimeoutError("Could not acquire ID generation lock")
                time.sleep(0.1)  # Wait 100ms and retry

    def _release_lock(self):
        """Release file lock."""
        try:
            if hasattr(self, '_lock_handle'):
                os.close(self._lock_handle)
                if self.lock_file.exists():
                    self.lock_file.unlink()
        except (OSError, IOError):
            pass  # Lock file might have been cleaned up

    def get_next_id(self, id_type: IDType, service_prefix: Optional[str] = None) -> str:
        """
        Get next ID for specified type.

        Args:
            id_type: Type of ID to generate
            service_prefix: Optional service prefix for service-specific IDs

        Returns:
            Generated ID as string

        Raises:
            ValueError: If parameters are invalid
            TimeoutError: If lock cannot be acquired
        """
        with self._lock:
            self._acquire_lock()

            try:
                type_name = id_type.value[0]
                prefix = id_type.value[1]
                padding = id_type.value[2]

                # Handle service-specific IDs
                if service_prefix and id_type == IDType.SERVICE_TASK:
                    if not re.match(r'^[A-Z]+$', service_prefix):
                        raise ValueError(f"Invalid service prefix: {service_prefix}")

                    # Initialize service counter if needed
                    if service_prefix not in self._state["service_counters"]:
                        self._state["service_counters"][service_prefix] = 0

                    counter = self._state["service_counters"][service_prefix] + 1
                    self._state["service_counters"][service_prefix] = counter
                    id_string = f"{service_prefix}-T{counter:0{padding}d}"

                else:
                    # Regular IDs
                    if type_name not in self._state["counters"]:
                        raise ValueError(f"Unknown ID type: {type_name}")

                    counter = self._state["counters"][type_name] + 1
                    self._state["counters"][type_name] = counter

                    # Format ID based on type
                    if prefix is None:  # Feature IDs (just numbers)
                        id_string = f"{counter:0{padding}d}"
                    else:
                        id_string = f"{prefix}{counter:0{padding}d}"

                # Check for conflicts
                if id_string in self._state["used_ids"]:
                    raise ValueError(f"ID conflict detected: {id_string} already used")

                # Mark as used and save state
                self._state["used_ids"].add(id_string)
                self._state["last_updated"] = time.time()
                self._save_state()

                return id_string

            finally:
                self._release_lock()

    def get_current_id(self, id_type: IDType, service_prefix: Optional[str] = None) -> str:
        """
        Get current ID without incrementing.

        Args:
            id_type: Type of ID
            service_prefix: Optional service prefix

        Returns:
            Current ID as string
        """
        with self._lock:
            type_name = id_type.value[0]
            prefix = id_type.value[1]
            padding = id_type.value[2]

            if service_prefix and id_type == IDType.SERVICE_TASK:
                counter = self._state["service_counters"].get(service_prefix, 0)
                id_string = f"{service_prefix}-T{counter:0{padding}d}"
            else:
                counter = self._state["counters"].get(type_name, 0)
                if prefix is None:
                    id_string = f"{counter:0{padding}d}"
                else:
                    id_string = f"{prefix}{counter:0{padding}d}"

            return id_string

    def validate_id_format(self, id_string: str) -> Tuple[bool, Optional[IDType], Optional[str]]:
        """
        Validate ID format and return type and service prefix.

        Args:
            id_string: ID string to validate

        Returns:
            Tuple of (is_valid, id_type, service_prefix)
        """
        patterns = [
            (r'^(\d{3})$', IDType.FEATURE, None),
            (r'^(spec-\d{3})\.md$', IDType.SPECIFICATION, None),
            (r'^(plan-\d{3})\.md$', IDType.PLAN, None),
            (r'^(T\d{3})\.md$', IDType.TASK, None),
            (r'^DEC-\d{3}$', IDType.DECISION, None),
            (r'^PATTERN-\d{3}$', IDType.PATTERN, None),
            (r'^CONST-\d{3}$', IDType.CONSTRAINT, None),
            (r'^CHK-\d{3}$', IDType.CHECKPOINT, None),
            (r'^([A-Z]+-T\d{3})\.md$', IDType.SERVICE_TASK, None),
        ]

        for pattern, id_type, _ in patterns:
            if re.match(pattern, id_string, re.IGNORECASE):
                # Extract service prefix if service task
                if id_type == IDType.SERVICE_TASK:
                    match = re.match(r'^([A-Z]+)-T\d{3}\.md$', id_string, re.IGNORECASE)
                    service_prefix = match.group(1) if match else None
                    return True, id_type, service_prefix
                return True, id_type, None

        return False, None, None

    def get_statistics(self) -> Dict:
        """
        Get current ID generation statistics.

        Returns:
            Dictionary with statistics
        """
        with self._lock:
            stats = {
                "counters": self._state["counters"].copy(),
                "service_counters": self._state["service_counters"].copy(),
                "total_ids_used": len(self._state["used_ids"]),
                "last_updated": self._state["last_updated"],
                "version": self._state["version"]
            }
            return stats

    def reset_counters(self, id_types: Optional[List[IDType]] = None):
        """
        Reset specific counters (DANGEROUS - use only for testing).

        Args:
            id_types: List of ID types to reset (None = reset all)
        """
        with self._lock:
            self._acquire_lock()

            try:
                if id_types is None:
                    # Reset all counters
                    for key in self._state["counters"]:
                        self._state["counters"][key] = 0
                    self._state["service_counters"] = {}
                else:
                    # Reset specific counters
                    for id_type in id_types:
                        type_name = id_type.value[0]
                        if type_name in self._state["counters"]:
                            self._state["counters"][type_name] = 0

                self._save_state()

            finally:
                self._release_lock()


# Global instance for easy access
_universal_generator = None

def get_universal_id_generator(project_root: Path) -> UniversalIDGenerator:
    """Get or create universal ID generator instance."""
    global _universal_generator
    if _universal_generator is None or _universal_generator.project_root != Path(project_root).resolve():
        _universal_generator = UniversalIDGenerator(project_root)
    return _universal_generator


# Convenience functions for common operations
def next_feature_id(project_root: Path) -> str:
    """Get next feature ID (e.g., '001', '002')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.FEATURE)

def next_spec_id(project_root: Path) -> str:
    """Get next specification ID (e.g., 'spec-001.md')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.SPECIFICATION)

def next_plan_id(project_root: Path) -> str:
    """Get next plan ID (e.g., 'plan-001.md')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.PLAN)

def next_task_id(project_root: Path, service_prefix: Optional[str] = None) -> str:
    """Get next task ID (e.g., 'T001.md' or 'AUTH-T001.md')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.SERVICE_TASK if service_prefix else IDType.TASK, service_prefix)

def next_decision_id(project_root: Path) -> str:
    """Get next decision ID (e.g., 'DEC-001')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.DECISION)

def next_pattern_id(project_root: Path) -> str:
    """Get next pattern ID (e.g., 'PATTERN-001')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.PATTERN)

def next_constraint_id(project_root: Path) -> str:
    """Get next constraint ID (e.g., 'CONST-001')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.CONSTRAINT)

def next_checkpoint_id(project_root: Path) -> str:
    """Get next checkpoint ID (e.g., 'CHK-001')."""
    generator = get_universal_id_generator(project_root)
    return generator.get_next_id(IDType.CHECKPOINT)