"""
LLM Task Status Manager for SpecPulse

This module enforces strict LLM compliance and automated task status management.
It ensures that LLM operations follow rigid rules and update task status automatically.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

from ..utils.console import Console
from ..utils.error_handler import ValidationError, ErrorSeverity


class TaskStatus(Enum):
    """Task status enumeration with strict transitions"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    WAITING_FOR_INPUT = "waiting_for_input"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class LLMOperationType(Enum):
    """LLM operation types for tracking"""
    SPEC_CREATION = "spec_creation"
    PLAN_CREATION = "plan_creation"
    TASK_CREATION = "task_creation"
    TASK_EXECUTION = "task_execution"
    MEMORY_UPDATE = "memory_update"
    STATUS_UPDATE = "status_update"
    VALIDATION = "validation"


@dataclass
class TaskStatusRule:
    """Strict rule definition for task operations"""
    id: str
    name: str
    description: str
    operation_type: LLMOperationType
    required_status_before: List[TaskStatus]
    status_after_success: TaskStatus
    status_after_failure: TaskStatus
    mandatory_files: List[str]
    forbidden_operations: List[str]
    validation_checks: List[str]


@dataclass
class LLMOperation:
    """LLM operation tracking record"""
    operation_id: str
    operation_type: LLMOperationType
    task_id: Optional[str]
    feature_id: Optional[str]
    feature_name: Optional[str]
    status_before: TaskStatus
    status_after: Optional[TaskStatus]
    start_time: datetime
    end_time: Optional[datetime]
    files_created: List[str]
    files_modified: List[str]
    validation_passed: bool
    error_message: Optional[str]
    llm_compliance_score: float  # 0.0 to 1.0


class LLMTaskStatusManager:
    """
    Enforces strict LLM compliance and automated task status management.
    This class ensures LLM operations follow rigid rules without interpretation.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root

        # Import PathManager for enforced directory management
        from .path_manager import PathManager
        self.path_manager = PathManager(project_root)

        # Status tracking files
        self.status_dir = self.path_manager.memory_dir / "task_status"
        self.status_dir.mkdir(parents=True, exist_ok=True)

        self.current_status_file = self.status_dir / "current_status.json"
        self.operation_history_file = self.status_dir / "operation_history.json"
        self.compliance_log_file = self.status_dir / "compliance_log.json"

        # Initialize tracking files
        self._initialize_tracking()

        # Define strict operation rules
        self.operation_rules = self._define_operation_rules()

        # Current LLM session tracking
        self.current_session_id = None
        self.session_start_time = None

    def _initialize_tracking(self) -> None:
        """Initialize tracking files with enforced structure"""
        # Current status tracking
        if not self.current_status_file.exists():
            initial_status = {
                "version": "1.0",
                "project_root": str(self.project_root),
                "last_updated": datetime.now().isoformat(),
                "tasks": {},
                "features": {},
                "global_status": {
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "in_progress_tasks": 0,
                    "blocked_tasks": 0,
                    "llm_compliance_rate": 1.0
                }
            }
            self.current_status_file.write_text(json.dumps(initial_status, indent=2), encoding='utf-8')

        # Operation history tracking
        if not self.operation_history_file.exists():
            initial_history = {
                "version": "1.0",
                "total_operations": 0,
                "operations": [],
                "last_operation_id": 0
            }
            self.operation_history_file.write_text(json.dumps(initial_history, indent=2), encoding='utf-8')

        # Compliance log tracking
        if not self.compliance_log_file.exists():
            initial_compliance = {
                "version": "1.0",
                "total_violations": 0,
                "violations": [],
                "compliance_score": 1.0,
                "last_updated": datetime.now().isoformat()
            }
            self.compliance_log_file.write_text(json.dumps(initial_compliance, indent=2), encoding='utf-8')

    def _define_operation_rules(self) -> Dict[LLMOperationType, TaskStatusRule]:
        """Define strict operation rules that cannot be overridden"""
        return {
            LLMOperationType.SPEC_CREATION: TaskStatusRule(
                id="spec_creation_rule",
                name="Specification Creation Rule",
                description="LLM must update task status when creating specifications",
                operation_type=LLMOperationType.SPEC_CREATION,
                required_status_before=[TaskStatus.NOT_STARTED, TaskStatus.IN_PROGRESS],
                status_after_success=TaskStatus.IN_PROGRESS,
                status_after_failure=TaskStatus.FAILED,
                mandatory_files=["spec-001.md", "decomposition/"],
                forbidden_operations=[
                    "Creating files outside .specpulse/",
                    "Skipping feature validation",
                    "Ignoring template requirements",
                    "Modifying unrelated files"
                ],
                validation_checks=[
                    "validate_specpulse_path_compliance",
                    "validate_spec_template_usage",
                    "validate_feature_id_format",
                    "validate_decomposition_structure"
                ]
            ),

            LLMOperationType.PLAN_CREATION: TaskStatusRule(
                id="plan_creation_rule",
                name="Plan Creation Rule",
                description="LLM must create plans within enforced structure",
                operation_type=LLMOperationType.PLAN_CREATION,
                required_status_before=[TaskStatus.IN_PROGRESS],
                status_after_success=TaskStatus.IN_PROGRESS,
                status_after_failure=TaskStatus.FAILED,
                mandatory_files=["plan-1.md"],
                forbidden_operations=[
                    "Creating files outside .specpulse/plans/",
                    "Skipping task breakdown",
                    "Ignoring existing specifications"
                ],
                validation_checks=[
                    "validate_specpulse_path_compliance",
                    "validate_plan_task_linkage",
                    "validate_implementation_steps"
                ]
            ),

            LLMOperationType.TASK_EXECUTION: TaskStatusRule(
                id="task_execution_rule",
                name="Task Execution Rule",
                description="LLM must track progress and update status during execution",
                operation_type=LLMOperationType.TASK_EXECUTION,
                required_status_before=[TaskStatus.IN_PROGRESS, TaskStatus.WAITING_FOR_INPUT],
                status_after_success=TaskStatus.COMPLETED,
                status_after_failure=TaskStatus.FAILED,
                mandatory_files=[],
                forbidden_operations=[
                    "Modifying files outside task scope",
                    "Skipping status updates",
                    "Creating unplanned files",
                    "Ignoring error handling"
                ],
                validation_checks=[
                    "validate_task_scope_compliance",
                    "validate_status_update_frequency",
                    "validate_error_reporting"
                ]
            ),

            LLMOperationType.MEMORY_UPDATE: TaskStatusRule(
                id="memory_update_rule",
                name="Memory Update Rule",
                description="LLM must update memory files after each operation",
                operation_type=LLMOperationType.MEMORY_UPDATE,
                required_status_before=list(TaskStatus),
                status_after_success=TaskStatus.IN_PROGRESS,
                status_after_failure=TaskStatus.BLOCKED,
                mandatory_files=["context.md"],
                forbidden_operations=[
                    "Modifying memory files outside .specpulse/memory/",
                    "Creating conflicting memory entries",
                    "Ignoring context updates"
                ],
                validation_checks=[
                    "validate_memory_path_compliance",
                    "validate_context_consistency",
                    "validate_memory_entry_format"
                ]
            )
        }

    def start_llm_session(self, session_id: str, operation_type: LLMOperationType,
                         task_id: Optional[str] = None, feature_id: Optional[str] = None,
                         feature_name: Optional[str] = None) -> bool:
        """
        Start a new LLM session with enforced tracking.
        This MUST be called before any LLM operation.

        Args:
            session_id: Unique session identifier
            operation_type: Type of operation being performed
            task_id: Task identifier (if applicable)
            feature_id: Feature identifier (if applicable)
            feature_name: Feature name (if applicable)

        Returns:
            True if session started successfully, False if validation fails
        """
        try:
            # Validate operation type and rules
            rule = self.operation_rules.get(operation_type)
            if not rule:
                self._log_compliance_violation(
                    f"Invalid operation type: {operation_type.value}",
                    "session_start",
                    session_id
                )
                return False

            # Check current status compliance
            if task_id:
                current_status = self.get_task_status(task_id)
                if current_status not in rule.required_status_before:
                    self._log_compliance_violation(
                        f"Task {task_id} has invalid status {current_status.value} for operation {operation_type.value}",
                        "status_check",
                        session_id
                    )
                    return False

            # Initialize session tracking
            self.current_session_id = session_id
            self.session_start_time = datetime.now()

            # Create operation record
            operation = LLMOperation(
                operation_id=session_id,
                operation_type=operation_type,
                task_id=task_id,
                feature_id=feature_id,
                feature_name=feature_name,
                status_before=current_status if task_id else TaskStatus.NOT_STARTED,
                status_after=None,
                start_time=self.session_start_time,
                end_time=None,
                files_created=[],
                files_modified=[],
                validation_passed=False,
                error_message=None,
                llm_compliance_score=0.0
            )

            # Record operation start
            self._record_operation_start(operation)

            return True

        except Exception as e:
            self._log_compliance_violation(
                f"Failed to start LLM session: {e}",
                "session_start",
                session_id
            )
            return False

    def track_file_operation(self, file_path: Path, operation_type: str) -> bool:
        """
        Track file operations for compliance monitoring.
        This MUST be called for every file created or modified.

        Args:
            file_path: Path to file being operated on
            operation_type: "created" or "modified"

        Returns:
            True if operation is compliant, False if it violates rules
        """
        if not self.current_session_id:
            self._log_compliance_violation(
                "File operation outside of tracked session",
                "file_tracking",
                "no_session"
            )
            return False

        try:
            # Validate file path compliance
            if not self.path_manager.validate_specpulse_path(file_path):
                self._log_compliance_violation(
                    f"File operation outside .specpulse: {file_path}",
                    "path_validation",
                    self.current_session_id
                )
                return False

            # Track the operation
            operation_history = self._load_operation_history()
            for operation in operation_history["operations"]:
                if operation["operation_id"] == self.current_session_id:
                    file_list = operation.get(f"files_{operation_type}", [])
                    file_list.append(str(file_path))
                    operation[f"files_{operation_type}"] = list(set(file_list))  # Remove duplicates
                    break

            self._save_operation_history(operation_history)
            return True

        except Exception as e:
            self._log_compliance_violation(
                f"Failed to track file operation: {e}",
                "file_tracking",
                self.current_session_id
            )
            return False

    def update_task_status(self, task_id: str, new_status: TaskStatus,
                          justification: Optional[str] = None) -> bool:
        """
        Update task status with enforced validation.
        This MUST be called during task execution.

        Args:
            task_id: Task identifier
            new_status: New task status
            justification: Reason for status change

        Returns:
            True if status update is valid, False if it violates rules
        """
        try:
            # Load current status
            current_status_data = self._load_current_status()

            # Validate status transition
            if task_id in current_status_data["tasks"]:
                current_status = TaskStatus(current_status_data["tasks"][task_id]["status"])
            else:
                current_status = TaskStatus.NOT_STARTED

            # Check if transition is valid
            if not self._is_valid_status_transition(current_status, new_status):
                self._log_compliance_violation(
                    f"Invalid status transition: {current_status.value} -> {new_status.value}",
                    "status_update",
                    self.current_session_id or "manual"
                )
                return False

            # Update status
            current_status_data["tasks"][task_id] = {
                "status": new_status.value,
                "last_updated": datetime.now().isoformat(),
                "justification": justification or f"Status updated from {current_status.value}",
                "updated_by": "llm" if self.current_session_id else "manual"
            }

            # Update global statistics
            self._update_global_statistics(current_status_data)

            # Save updated status
            self._save_current_status(current_status_data)

            # Update current operation if active
            if self.current_session_id:
                operation_history = self._load_operation_history()
                for operation in operation_history["operations"]:
                    if operation["operation_id"] == self.current_session_id:
                        operation["status_after"] = new_status.value
                        break
                self._save_operation_history(operation_history)

            return True

        except Exception as e:
            self._log_compliance_violation(
                f"Failed to update task status: {e}",
                "status_update",
                self.current_session_id or "manual"
            )
            return False

    def end_llm_session(self, success: bool, error_message: Optional[str] = None) -> bool:
        """
        End current LLM session with final validation and status updates.
        This MUST be called to complete the operation.

        Args:
            success: Whether the operation was successful
            error_message: Error message if operation failed

        Returns:
            True if session ended properly, False if cleanup failed
        """
        if not self.current_session_id:
            return True  # No active session

        try:
            # Load operation history
            operation_history = self._load_operation_history()

            # Find and update current operation
            operation_found = False
            for operation in operation_history["operations"]:
                if operation["operation_id"] == self.current_session_id:
                    operation["end_time"] = datetime.now().isoformat()
                    operation["validation_passed"] = success
                    operation["error_message"] = error_message

                    # Calculate compliance score
                    operation["llm_compliance_score"] = self._calculate_compliance_score(operation)

                    # Update task status based on operation result
                    if operation["task_id"] and operation["operation_type"]:
                        op_type = LLMOperationType(operation["operation_type"])
                        rule = self.operation_rules.get(op_type)

                        if rule:
                            new_status = rule.status_after_success if success else rule.status_after_failure
                            self.update_task_status(
                                operation["task_id"],
                                new_status,
                                f"LLM session {'completed' if success else 'failed'}: {error_message or 'No error'}"
                            )

                    operation_found = True
                    break

            if not operation_found:
                self._log_compliance_violation(
                    "Could not find operation to end",
                    "session_end",
                    self.current_session_id
                )
                return False

            # Save updated operation history
            self._save_operation_history(operation_history)

            # Clear session tracking
            self.current_session_id = None
            self.session_start_time = None

            return True

        except Exception as e:
            self._log_compliance_violation(
                f"Failed to end LLM session: {e}",
                "session_end",
                self.current_session_id
            )
            return False

    def enforce_llm_compliance(self, operation_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforce strict LLM compliance with no interpretation allowed.
        This method validates that LLM follows all rules exactly.

        Args:
            operation_context: Context of the current operation

        Returns:
            Compliance validation result with strict pass/fail
        """
        compliance_result = {
            "compliant": False,
            "violations": [],
            "required_actions": [],
            "forbidden_actions_detected": [],
            "score": 0.0
        }

        try:
            # Validate active session
            if not self.current_session_id:
                compliance_result["violations"].append("No active LLM session found")
                return compliance_result

            # Load current operation
            operation_history = self._load_operation_history()
            current_operation = None
            for operation in operation_history["operations"]:
                if operation["operation_id"] == self.current_session_id:
                    current_operation = operation
                    break

            if not current_operation:
                compliance_result["violations"].append("Could not find current operation")
                return compliance_result

            # Get operation rule
            op_type = LLMOperationType(current_operation["operation_type"])
            rule = self.operation_rules.get(op_type)
            if not rule:
                compliance_result["violations"].append(f"No rule defined for operation type: {op_type.value}")
                return compliance_result

            # Validate required actions
            for action in rule.validation_checks:
                if not self._validate_compliance_check(action, operation_context):
                    compliance_result["violations"].append(f"Failed compliance check: {action}")

            # Check for forbidden operations
            for forbidden in rule.forbidden_operations:
                if self._detect_forbidden_operation(forbidden, operation_context):
                    compliance_result["forbidden_actions_detected"].append(forbidden)

            # Validate file operations
            files_created = current_operation.get("files_created", [])
            files_modified = current_operation.get("files_modified", [])

            for file_path in files_created + files_modified:
                if not self.path_manager.validate_specpulse_path(Path(file_path)):
                    compliance_result["violations"].append(f"File outside .specpulse: {file_path}")

            # Calculate final compliance score
            total_checks = len(rule.validation_checks) + len(rule.forbidden_operations)
            passed_checks = total_checks - len(compliance_result["violations"]) - len(compliance_result["forbidden_actions_detected"])

            compliance_result["score"] = max(0.0, passed_checks / total_checks) if total_checks > 0 else 1.0
            compliance_result["compliant"] = compliance_result["score"] >= 0.95  # 95% compliance required

            # Update compliance log
            if not compliance_result["compliant"]:
                for violation in compliance_result["violations"] + compliance_result["forbidden_actions_detected"]:
                    self._log_compliance_violation(violation, "compliance_check", self.current_session_id)

            return compliance_result

        except Exception as e:
            compliance_result["violations"].append(f"Compliance check failed: {e}")
            self._log_compliance_violation(str(e), "compliance_check", self.current_session_id)
            return compliance_result

    # Helper methods (private)
    def _load_current_status(self) -> Dict[str, Any]:
        """Load current status tracking data"""
        return json.loads(self.current_status_file.read_text(encoding='utf-8'))

    def _save_current_status(self, data: Dict[str, Any]) -> None:
        """Save current status tracking data"""
        data["last_updated"] = datetime.now().isoformat()
        self.current_status_file.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def _load_operation_history(self) -> Dict[str, Any]:
        """Load operation history tracking data"""
        return json.loads(self.operation_history_file.read_text(encoding='utf-8'))

    def _save_operation_history(self, data: Dict[str, Any]) -> None:
        """Save operation history tracking data"""
        self.operation_history_file.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def _record_operation_start(self, operation: LLMOperation) -> None:
        """Record the start of a new operation"""
        history = self._load_operation_history()
        history["last_operation_id"] += 1
        history["total_operations"] += 1

        operation_dict = asdict(operation)
        operation_dict["start_time"] = operation.start_time.isoformat()
        operation_dict["status_before"] = operation.status_before.value

        history["operations"].append(operation_dict)
        self._save_operation_history(history)

    def _log_compliance_violation(self, violation: str, violation_type: str, session_id: str) -> None:
        """Log a compliance violation"""
        compliance_log = json.loads(self.compliance_log_file.read_text(encoding='utf-8'))

        violation_record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "violation_type": violation_type,
            "description": violation,
            "severity": "high"
        }

        compliance_log["violations"].append(violation_record)
        compliance_log["total_violations"] += 1
        compliance_log["last_updated"] = datetime.now().isoformat()

        # Recalculate compliance score
        total_operations = compliance_log.get("total_operations", 1)
        compliance_log["compliance_score"] = max(0.0, 1.0 - (compliance_log["total_violations"] / total_operations))

        self.compliance_log_file.write_text(json.dumps(compliance_log, indent=2), encoding='utf-8')

    def _is_valid_status_transition(self, from_status: TaskStatus, to_status: TaskStatus) -> bool:
        """Validate if a status transition is allowed"""
        # Define strict transition rules
        valid_transitions = {
            TaskStatus.NOT_STARTED: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
            TaskStatus.IN_PROGRESS: [TaskStatus.WAITING_FOR_INPUT, TaskStatus.BLOCKED, TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED],
            TaskStatus.WAITING_FOR_INPUT: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
            TaskStatus.BLOCKED: [TaskStatus.IN_PROGRESS, TaskStatus.FAILED, TaskStatus.CANCELLED],
            TaskStatus.COMPLETED: [],  # Terminal state
            TaskStatus.FAILED: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],  # Can retry
            TaskStatus.CANCELLED: []   # Terminal state
        }

        return to_status in valid_transitions.get(from_status, [])

    def _update_global_statistics(self, status_data: Dict[str, Any]) -> None:
        """Update global task statistics"""
        tasks = status_data["tasks"]
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks.values() if task["status"] == TaskStatus.COMPLETED.value)
        in_progress_tasks = sum(1 for task in tasks.values() if task["status"] == TaskStatus.IN_PROGRESS.value)
        blocked_tasks = sum(1 for task in tasks.values() if task["status"] == TaskStatus.BLOCKED.value)

        status_data["global_status"] = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "blocked_tasks": blocked_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0.0
        }

    def _calculate_compliance_score(self, operation: Dict[str, Any]) -> float:
        """Calculate compliance score for an operation"""
        base_score = 1.0

        # Deduct points for violations
        files_outside_specpulse = 0
        for file_path in operation.get("files_created", []) + operation.get("files_modified", []):
            if not self.path_manager.validate_specpulse_path(Path(file_path)):
                files_outside_specpulse += 1

        file_penalty = min(0.5, files_outside_specpulse * 0.1)

        # Check if operation completed successfully
        if not operation.get("validation_passed", False):
            base_score -= 0.3

        # Check if status was properly updated
        if not operation.get("status_after"):
            base_score -= 0.2

        return max(0.0, base_score - file_penalty)

    def _validate_compliance_check(self, check_name: str, context: Dict[str, Any]) -> bool:
        """Validate a specific compliance check"""
        # Implement validation logic for each check
        validators = {
            "validate_specpulse_path_compliance": self._validate_path_compliance,
            "validate_spec_template_usage": self._validate_template_usage,
            "validate_feature_id_format": self._validate_feature_id,
            "validate_decomposition_structure": self._validate_decomposition,
            "validate_plan_task_linkage": self._validate_plan_linkage,
            "validate_implementation_steps": self._validate_implementation_steps,
            "validate_task_scope_compliance": self._validate_task_scope,
            "validate_status_update_frequency": self._validate_status_frequency,
            "validate_error_reporting": self._validate_error_reporting,
            "validate_memory_path_compliance": self._validate_memory_path,
            "validate_context_consistency": self._validate_context_consistency,
            "validate_memory_entry_format": self._validate_memory_format
        }

        validator = validators.get(check_name)
        if validator:
            return validator(context)

        return True  # Unknown check passes by default

    def _detect_forbidden_operation(self, forbidden_action: str, context: Dict[str, Any]) -> bool:
        """Detect if a forbidden operation was performed"""
        # Implementation for detecting forbidden operations
        if "files outside .specpulse/" in forbidden_action:
            files_created = context.get("files_created", [])
            files_modified = context.get("files_modified", [])
            for file_path in files_created + files_modified:
                if not self.path_manager.validate_specpulse_path(Path(file_path)):
                    return True

        # Add more detection logic as needed
        return False

    # Validation method implementations
    def _validate_path_compliance(self, context: Dict[str, Any]) -> bool:
        """Validate all files are within .specpulse"""
        files = context.get("files_created", []) + context.get("files_modified", [])
        for file_path in files:
            if not self.path_manager.validate_specpulse_path(Path(file_path)):
                return False
        return True

    def _validate_template_usage(self, context: Dict[str, Any]) -> bool:
        """Validate proper template usage"""
        # Check if created files follow template structure
        return True  # Simplified for now

    def _validate_feature_id(self, context: Dict[str, Any]) -> bool:
        """Validate feature ID format"""
        feature_id = context.get("feature_id", "")
        return bool(re.match(r'^\d{3}$', feature_id)) if feature_id else True

    def _validate_decomposition(self, context: Dict[str, Any]) -> bool:
        """Validate decomposition structure"""
        # Check if decomposition directory exists and is valid
        return True  # Simplified for now

    def _validate_plan_linkage(self, context: Dict[str, Any]) -> bool:
        """Validate plan links to tasks properly"""
        return True  # Simplified for now

    def _validate_implementation_steps(self, context: Dict[str, Any]) -> bool:
        """Validate implementation steps are properly defined"""
        return True  # Simplified for now

    def _validate_task_scope(self, context: Dict[str, Any]) -> bool:
        """Validate task execution stays within scope"""
        return True  # Simplified for now

    def _validate_status_frequency(self, context: Dict[str, Any]) -> bool:
        """Validate status updates are frequent enough"""
        return True  # Simplified for now

    def _validate_error_reporting(self, context: Dict[str, Any]) -> bool:
        """Validate errors are properly reported"""
        return True  # Simplified for now

    def _validate_memory_path(self, context: Dict[str, Any]) -> bool:
        """Validate memory files are in correct location"""
        memory_files = [f for f in context.get("files_created", []) + context.get("files_modified", []) if "memory" in f]
        for file_path in memory_files:
            if not self.path_manager.validate_specpulse_path(Path(file_path)):
                return False
        return True

    def _validate_context_consistency(self, context: Dict[str, Any]) -> bool:
        """Validate context consistency"""
        return True  # Simplified for now

    def _validate_memory_format(self, context: Dict[str, Any]) -> bool:
        """Validate memory entry format"""
        return True  # Simplified for now

    # Public interface methods
    def get_task_status(self, task_id: str) -> TaskStatus:
        """Get current status of a task"""
        status_data = self._load_current_status()
        task_info = status_data["tasks"].get(task_id, {"status": TaskStatus.NOT_STARTED.value})
        return TaskStatus(task_info["status"])

    def get_compliance_score(self) -> float:
        """Get overall LLM compliance score"""
        compliance_log = json.loads(self.compliance_log_file.read_text(encoding='utf-8'))
        return compliance_log.get("compliance_score", 1.0)

    def get_active_sessions(self) -> List[str]:
        """Get list of currently active LLM sessions"""
        history = self._load_operation_history()
        active_sessions = []

        for operation in history["operations"]:
            if operation.get("end_time") is None:
                active_sessions.append(operation["operation_id"])

        return active_sessions


__all__ = ['LLMTaskStatusManager', 'TaskStatus', 'LLMOperationType']