"""
LLM Task Lifecycle Manager for SpecPulse

This module provides automated task lifecycle management for LLM operations
with strict enforcement and no interpretation allowed.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from .llm_task_status_manager import LLMTaskStatusManager, TaskStatus, LLMOperationType
from .llm_compliance_enforcer import LLMComplianceEnforcer
from .path_manager import PathManager
from ..utils.error_handler import ValidationError, ErrorSeverity
from ..utils.console import Console


class LifecycleEvent(Enum):
    """Task lifecycle events"""
    CREATED = "created"
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class LifecycleTrigger(Enum):
    """Lifecycle event triggers"""
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    LLM_OPERATION = "llm_operation"
    TIMEOUT = "timeout"
    ERROR = "error"
    DEPENDENCY = "dependency"


@dataclass
class LifecycleEventRecord:
    """Record of a lifecycle event"""
    task_id: str
    event: LifecycleEvent
    trigger: LifecycleTrigger
    timestamp: datetime
    description: str
    context: Dict[str, Any]
    session_id: Optional[str] = None


@dataclass
class TaskDependency:
    """Task dependency definition"""
    task_id: str
    depends_on: str  # task_id this task depends on
    dependency_type: str  # "completion", "success", "start"
    description: str


@dataclass
class LifecycleRule:
    """Rule for automated lifecycle management"""
    id: str
    name: str
    description: str
    trigger_event: LifecycleEvent
    target_status: TaskStatus
    condition: Callable[[Dict[str, Any]], bool]
    action: Callable[[str, Dict[str, Any]], bool]
    is_enabled: bool = True


class LLMTaskLifecycleManager:
    """
    Automated task lifecycle management for LLM operations.
    Enforces strict lifecycle rules with no interpretation.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.path_manager = PathManager(project_root)
        self.status_manager = LLMTaskStatusManager(project_root)
        self.enforcer = LLMComplianceEnforcer(project_root)
        self.console = Console()

        # Lifecycle tracking
        self.lifecycle_dir = self.path_manager.memory_dir / "lifecycle"
        self.lifecycle_dir.mkdir(parents=True, exist_ok=True)

        self.events_file = self.lifecycle_dir / "events.json"
        self.rules_file = self.lifecycle_dir / "rules.json"
        self.dependencies_file = self.lifecycle_dir / "dependencies.json"

        # Initialize tracking
        self._initialize_lifecycle_tracking()

        # Define lifecycle rules
        self.lifecycle_rules = self._define_lifecycle_rules()

        # Current operation tracking
        self.current_operations = {}

    def _initialize_lifecycle_tracking(self) -> None:
        """Initialize lifecycle tracking files"""
        # Events tracking
        if not self.events_file.exists():
            initial_events = {
                "version": "1.0",
                "total_events": 0,
                "events": []
            }
            self.events_file.write_text(json.dumps(initial_events, indent=2), encoding='utf-8')

        # Rules tracking
        if not self.rules_file.exists():
            initial_rules = {
                "version": "1.0",
                "active_rules": [],
                "rule_history": []
            }
            self.rules_file.write_text(json.dumps(initial_rules, indent=2), encoding='utf-8')

        # Dependencies tracking
        if not self.dependencies_file.exists():
            initial_dependencies = {
                "version": "1.0",
                "dependencies": [],
                "dependency_graph": {}
            }
            self.dependencies_file.write_text(json.dumps(initial_dependencies, indent=2), encoding='utf-8')

    def _define_lifecycle_rules(self) -> Dict[str, LifecycleRule]:
        """Define automated lifecycle management rules"""
        rules = {}

        # Rule 1: Auto-start tasks when dependencies are met
        rules["auto_start"] = LifecycleRule(
            id="auto_start",
            name="Auto-Start Tasks",
            description="Automatically start tasks when dependencies are satisfied",
            trigger_event=LifecycleEvent.CREATED,
            target_status=TaskStatus.IN_PROGRESS,
            condition=self._check_dependencies_satisfied,
            action=self._auto_start_task,
            is_enabled=True
        )

        # Rule 2: Auto-block tasks when dependencies fail
        rules["auto_block"] = LifecycleRule(
            id="auto_block",
            name="Auto-Block Tasks",
            description="Automatically block tasks when dependencies fail",
            trigger_event=LifecycleEvent.FAILED,
            target_status=TaskStatus.BLOCKED,
            condition=self._check_dependent_tasks,
            action=self._auto_block_dependent_tasks,
            is_enabled=True
        )

        # Rule 3: Auto-timeout long-running tasks
        rules["auto_timeout"] = LifecycleRule(
            id="auto_timeout",
            name="Auto-Timeout Tasks",
            description="Automatically timeout tasks running too long",
            trigger_event=LifecycleEvent.IN_PROGRESS,
            target_status=TaskStatus.BLOCKED,
            condition=self._check_task_timeout,
            action=self._auto_timeout_task,
            is_enabled=True
        )

        # Rule 4: Auto-cleanup completed tasks
        rules["auto_cleanup"] = LifecycleRule(
            id="auto_cleanup",
            name="Auto-Cleanup Tasks",
            description="Automatically cleanup old completed tasks",
            trigger_event=LifecycleEvent.COMPLETED,
            target_status=TaskStatus.COMPLETED,
            condition=self._check_cleanup_eligibility,
            action=self._auto_cleanup_task,
            is_enabled=False  # Disabled by default
        )

        return rules

    def record_lifecycle_event(self, task_id: str, event: LifecycleEvent,
                             trigger: LifecycleTrigger = LifecycleTrigger.MANUAL,
                             description: str = "", context: Optional[Dict[str, Any]] = None,
                             session_id: Optional[str] = None) -> bool:
        """
        Record a lifecycle event and trigger automated responses.

        Args:
            task_id: Task identifier
            event: Lifecycle event
            trigger: What triggered this event
            description: Event description
            context: Additional context information
            session_id: LLM session ID (if applicable)

        Returns:
            True if event recorded and processed successfully
        """
        try:
            # Create event record
            event_record = LifecycleEventRecord(
                task_id=task_id,
                event=event,
                trigger=trigger,
                timestamp=datetime.now(),
                description=description,
                context=context or {},
                session_id=session_id
            )

            # Save event
            self._save_lifecycle_event(event_record)

            # Get current task status
            current_status = self.status_manager.get_task_status(task_id)

            # Trigger automated responses
            self._process_lifecycle_event(event_record, current_status)

            return True

        except Exception as e:
            self.console.error(f"Failed to record lifecycle event: {e}")
            return False

    def add_task_dependency(self, task_id: str, depends_on: str,
                           dependency_type: str = "completion",
                           description: str = "") -> bool:
        """
        Add a task dependency.

        Args:
            task_id: Task that has the dependency
            depends_on: Task this task depends on
            dependency_type: Type of dependency
            description: Dependency description

        Returns:
            True if dependency added successfully
        """
        try:
            dependencies = self._load_dependencies()

            new_dependency = TaskDependency(
                task_id=task_id,
                depends_on=depends_on,
                dependency_type=dependency_type,
                description=description or f"{task_id} depends on {depends_on}"
            )

            dependencies["dependencies"].append(asdict(new_dependency))

            # Update dependency graph
            if task_id not in dependencies["dependency_graph"]:
                dependencies["dependency_graph"][task_id] = []
            dependencies["dependency_graph"][task_id].append(depends_on)

            self._save_dependencies(dependencies)

            # Record lifecycle event
            self.record_lifecycle_event(
                task_id,
                LifecycleEvent.CREATED,
                LifecycleTrigger.MANUAL,
                f"Added dependency on {depends_on}",
                {"dependency_type": dependency_type}
            )

            return True

        except Exception as e:
            self.console.error(f"Failed to add task dependency: {e}")
            return False

    def start_task_lifecycle(self, task_id: str, feature_id: Optional[str] = None,
                           feature_name: Optional[str] = None,
                           auto_dependencies: bool = True) -> str:
        """
        Start task lifecycle with automatic management.

        Args:
            task_id: Task identifier
            feature_id: Feature identifier
            feature_name: Feature name
            auto_dependencies: Whether to auto-detect dependencies

        Returns:
            Session ID for tracking
        """
        try:
            # Record task creation
            self.record_lifecycle_event(
                task_id,
                LifecycleEvent.CREATED,
                LifecycleTrigger.AUTOMATIC,
                f"Task lifecycle started",
                {
                    "feature_id": feature_id,
                    "feature_name": feature_name,
                    "auto_dependencies": auto_dependencies
                }
            )

            # Auto-detect dependencies if enabled
            if auto_dependencies:
                self._auto_detect_dependencies(task_id)

            # Check if task can start immediately
            current_status = self.status_manager.get_task_status(task_id)
            if self._check_dependencies_satisfied({"task_id": task_id}):
                self.record_lifecycle_event(
                    task_id,
                    LifecycleEvent.STARTED,
                    LifecycleTrigger.AUTOMATIC,
                    "Dependencies satisfied, task started"
                )
                self.status_manager.update_task_status(task_id, TaskStatus.IN_PROGRESS, "Auto-started")

            return f"lifecycle_{task_id}_{int(time.time())}"

        except Exception as e:
            self.record_lifecycle_event(
                task_id,
                LifecycleEvent.FAILED,
                LifecycleTrigger.ERROR,
                f"Failed to start lifecycle: {e}"
            )
            raise

    def process_llm_operation(self, operation_type: LLMOperationType,
                            task_id: str, success: bool,
                            context: Optional[Dict[str, Any]] = None,
                            session_id: Optional[str] = None) -> bool:
        """
        Process LLM operation and update task lifecycle accordingly.

        Args:
            operation_type: Type of LLM operation
            task_id: Task identifier
            success: Whether operation was successful
            context: Operation context
            session_id: LLM session ID

        Returns:
            True if processed successfully
        """
        try:
            if success:
                # Determine lifecycle event based on operation type
                if operation_type == LLMOperationType.TASK_EXECUTION:
                    event = LifecycleEvent.IN_PROGRESS
                    description = "LLM task execution in progress"
                elif operation_type in [LLMOperationType.SPEC_CREATION, LLMOperationType.PLAN_CREATION]:
                    event = LifecycleEvent.STARTED
                    description = f"LLM {operation_type.value} completed"
                else:
                    event = LifecycleEvent.IN_PROGRESS
                    description = f"LLM {operation_type.value} successful"

                trigger = LifecycleTrigger.LLM_OPERATION

            else:
                event = LifecycleEvent.FAILED
                description = f"LLM {operation_type.value} failed"
                trigger = LifecycleTrigger.ERROR

            # Record lifecycle event
            self.record_lifecycle_event(
                task_id,
                event,
                trigger,
                description,
                context,
                session_id
            )

            # Check for automated responses
            self._check_automated_responses(task_id, event)

            return True

        except Exception as e:
            self.console.error(f"Failed to process LLM operation: {e}")
            return False

    def get_task_lifecycle_status(self, task_id: str) -> Dict[str, Any]:
        """Get comprehensive lifecycle status for a task"""
        try:
            events = self._load_events()
            task_events = [e for e in events["events"] if e["task_id"] == task_id]

            current_status = self.status_manager.get_task_status(task_id)
            dependencies = self._load_dependencies()
            task_dependencies = [d for d in dependencies["dependencies"] if d["task_id"] == task_id]

            # Calculate lifecycle metrics
            total_events = len(task_events)
            last_event = task_events[-1] if task_events else None
            created_time = None
            started_time = None
            duration = None

            for event in task_events:
                if event["event"] == LifecycleEvent.CREATED.value:
                    created_time = datetime.fromisoformat(event["timestamp"])
                elif event["event"] == LifecycleEvent.STARTED.value:
                    started_time = datetime.fromisoformat(event["timestamp"])

            if created_time and started_time:
                duration = (started_time - created_time).total_seconds()

            return {
                "task_id": task_id,
                "current_status": current_status.value,
                "total_events": total_events,
                "last_event": last_event,
                "created_time": created_time.isoformat() if created_time else None,
                "started_time": started_time.isoformat() if started_time else None,
                "start_duration_seconds": duration,
                "dependencies": task_dependencies,
                "lifecycle_active": last_event is not None
            }

        except Exception as e:
            return {"error": str(e)}

    def get_lifecycle_summary(self) -> Dict[str, Any]:
        """Get comprehensive lifecycle summary"""
        try:
            events = self._load_events()
            dependencies = self._load_dependencies()

            # Calculate metrics
            total_events = events["total_events"]
            active_tasks = set()
            completed_tasks = set()
            failed_tasks = set()

            for event in events["events"]:
                task_id = event["task_id"]
                if event["event"] in [LifecycleEvent.STARTED.value, LifecycleEvent.IN_PROGRESS.value]:
                    active_tasks.add(task_id)
                elif event["event"] == LifecycleEvent.COMPLETED.value:
                    completed_tasks.add(task_id)
                    active_tasks.discard(task_id)
                elif event["event"] == LifecycleEvent.FAILED.value:
                    failed_tasks.add(task_id)
                    active_tasks.discard(task_id)

            # Rule status
            active_rules = [rule_id for rule_id, rule in self.lifecycle_rules.items() if rule.is_enabled]

            return {
                "total_events": total_events,
                "active_tasks": len(active_tasks),
                "completed_tasks": len(completed_tasks),
                "failed_tasks": len(failed_tasks),
                "total_dependencies": len(dependencies["dependencies"]),
                "active_rules": len(active_rules),
                "rule_ids": list(active_rules),
                "lifecycle_health": len(completed_tasks) / max(1, len(completed_tasks) + len(failed_tasks))
            }

        except Exception as e:
            return {"error": str(e)}

    # Private methods for lifecycle automation
    def _save_lifecycle_event(self, event_record: LifecycleEventRecord) -> None:
        """Save lifecycle event to file"""
        events = self._load_events()

        event_dict = asdict(event_record)
        event_dict["timestamp"] = event_record.timestamp.isoformat()
        event_dict["event"] = event_record.event.value
        event_dict["trigger"] = event_record.trigger.value

        events["events"].append(event_dict)
        events["total_events"] += 1

        self.events_file.write_text(json.dumps(events, indent=2), encoding='utf-8')

    def _load_events(self) -> Dict[str, Any]:
        """Load lifecycle events"""
        return json.loads(self.events_file.read_text(encoding='utf-8'))

    def _load_dependencies(self) -> Dict[str, Any]:
        """Load task dependencies"""
        return json.loads(self.dependencies_file.read_text(encoding='utf-8'))

    def _save_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Save task dependencies"""
        self.dependencies_file.write_text(json.dumps(dependencies, indent=2), encoding='utf-8')

    def _process_lifecycle_event(self, event_record: LifecycleEventRecord,
                               current_status: TaskStatus) -> None:
        """Process lifecycle event and trigger rules"""
        for rule_id, rule in self.lifecycle_rules.items():
            if not rule.is_enabled:
                continue

            if rule.trigger_event == event_record.event:
                context = {
                    "task_id": event_record.task_id,
                    "current_status": current_status,
                    "event": event_record,
                    **event_record.context
                }

                try:
                    if rule.condition(context):
                        rule.action(event_record.task_id, context)
                except Exception as e:
                    self.console.error(f"Lifecycle rule {rule_id} failed: {e}")

    def _check_automated_responses(self, task_id: str, event: LifecycleEvent) -> None:
        """Check for automated responses to lifecycle events"""
        # This can be expanded with more complex automation logic
        pass

    # Rule condition and action implementations
    def _check_dependencies_satisfied(self, context: Dict[str, Any]) -> bool:
        """Check if task dependencies are satisfied"""
        task_id = context["task_id"]
        dependencies = self._load_dependencies()

        task_dependencies = [d for d in dependencies["dependencies"] if d["task_id"] == task_id]

        for dep in task_dependencies:
            dep_status = self.status_manager.get_task_status(dep["depends_on"])

            if dep["dependency_type"] == "completion":
                if dep_status != TaskStatus.COMPLETED:
                    return False
            elif dep["dependency_type"] == "success":
                if dep_status not in [TaskStatus.COMPLETED]:
                    return False
            elif dep["dependency_type"] == "start":
                if dep_status == TaskStatus.NOT_STARTED:
                    return False

        return True

    def _auto_start_task(self, task_id: str, context: Dict[str, Any]) -> bool:
        """Auto-start a task when dependencies are satisfied"""
        try:
            self.status_manager.update_task_status(task_id, TaskStatus.IN_PROGRESS, "Auto-started (dependencies satisfied)")
            self.record_lifecycle_event(
                task_id,
                LifecycleEvent.STARTED,
                LifecycleTrigger.AUTOMATIC,
                "Auto-started due to satisfied dependencies"
            )
            return True
        except Exception as e:
            self.console.error(f"Failed to auto-start task {task_id}: {e}")
            return False

    def _check_dependent_tasks(self, context: Dict[str, Any]) -> bool:
        """Check if there are dependent tasks that need to be blocked"""
        failed_task_id = context["event"].task_id
        dependencies = self._load_dependencies()

        dependent_tasks = [d for d in dependencies["dependencies"] if d["depends_on"] == failed_task_id]
        return len(dependent_tasks) > 0

    def _auto_block_dependent_tasks(self, failed_task_id: str, context: Dict[str, Any]) -> bool:
        """Block dependent tasks when a task fails"""
        try:
            dependencies = self._load_dependencies()
            dependent_tasks = [d for d in dependencies["dependencies"] if d["depends_on"] == failed_task_id]

            for dep in dependent_tasks:
                current_status = self.status_manager.get_task_status(dep["task_id"])
                if current_status in [TaskStatus.NOT_STARTED, TaskStatus.IN_PROGRESS]:
                    self.status_manager.update_task_status(
                        dep["task_id"],
                        TaskStatus.BLOCKED,
                        f"Blocked due to dependency failure: {failed_task_id}"
                    )
                    self.record_lifecycle_event(
                        dep["task_id"],
                        LifecycleEvent.BLOCKED,
                        LifecycleTrigger.DEPENDENCY,
                        f"Blocked by failed dependency: {failed_task_id}"
                    )

            return True

        except Exception as e:
            self.console.error(f"Failed to block dependent tasks: {e}")
            return False

    def _check_task_timeout(self, context: Dict[str, Any]) -> bool:
        """Check if task has timed out"""
        task_id = context["task_id"]
        events = self._load_events()

        # Find the last IN_PROGRESS event
        task_events = [e for e in events["events"] if e["task_id"] == task_id]
        in_progress_events = [e for e in task_events if e["event"] == LifecycleEvent.IN_PROGRESS.value]

        if not in_progress_events:
            return False

        last_progress = max(in_progress_events, key=lambda x: x["timestamp"])
        last_time = datetime.fromisoformat(last_progress["timestamp"])

        # Timeout after 24 hours (configurable)
        timeout_hours = 24
        timeout_threshold = datetime.now() - timedelta(hours=timeout_hours)

        return last_time < timeout_threshold

    def _auto_timeout_task(self, task_id: str, context: Dict[str, Any]) -> bool:
        """Auto-timeout a task that has been running too long"""
        try:
            self.status_manager.update_task_status(
                task_id,
                TaskStatus.BLOCKED,
                "Auto-timeout: Task exceeded maximum duration"
            )
            self.record_lifecycle_event(
                task_id,
                LifecycleEvent.TIMEOUT,
                LifecycleTrigger.TIMEOUT,
                "Task automatically timed out"
            )
            return True
        except Exception as e:
            self.console.error(f"Failed to timeout task {task_id}: {e}")
            return False

    def _check_cleanup_eligibility(self, context: Dict[str, Any]) -> bool:
        """Check if task is eligible for cleanup"""
        task_id = context["task_id"]
        events = self._load_events()

        task_events = [e for e in events["events"] if e["task_id"] == task_id]
        completed_events = [e for e in task_events if e["event"] == LifecycleEvent.COMPLETED.value]

        if not completed_events:
            return False

        # Cleanup tasks completed more than 30 days ago
        last_completion = max(completed_events, key=lambda x: x["timestamp"])
        completion_time = datetime.fromisoformat(last_completion["timestamp"])
        cleanup_threshold = datetime.now() - timedelta(days=30)

        return completion_time < cleanup_threshold

    def _auto_cleanup_task(self, task_id: str, context: Dict[str, Any]) -> bool:
        """Auto-cleanup an old completed task"""
        try:
            # This could archive old task files, etc.
            self.record_lifecycle_event(
                task_id,
                LifecycleEvent.COMPLETED,  # Still completed, but cleaned up
                LifecycleTrigger.AUTOMATIC,
                "Task auto-cleanup performed"
            )
            return True
        except Exception as e:
            self.console.error(f"Failed to cleanup task {task_id}: {e}")
            return False

    def _auto_detect_dependencies(self, task_id: str) -> None:
        """Auto-detect task dependencies based on naming patterns"""
        # This can be enhanced with more sophisticated dependency detection
        pass


__all__ = [
    'LLMTaskLifecycleManager',
    'LifecycleEvent',
    'LifecycleTrigger',
    'LifecycleEventRecord',
    'TaskDependency',
    'LifecycleRule'
]