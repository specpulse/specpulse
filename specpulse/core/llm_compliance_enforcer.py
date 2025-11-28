"""
LLM Compliance Enforcer for SpecPulse

This module provides rigid enforcement mechanisms to ensure LLM operations
follow strict rules without interpretation or deviation.
"""

import re
import json
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from functools import wraps

from .llm_task_status_manager import LLMTaskStatusManager, TaskStatus, LLMOperationType
from ..utils.error_handler import ValidationError, ErrorSeverity
from ..utils.console import Console


@dataclass
class ComplianceRule:
    """Strict compliance rule that cannot be overridden"""
    name: str
    description: str
    validator: Callable
    is_mandatory: bool = True
    violation_message: str = ""


class LLMComplianceError(Exception):
    """Exception raised when LLM violates compliance rules"""
    pass


class LLMComplianceEnforcer:
    """
    Enforces rigid LLM compliance with no interpretation allowed.
    LLM operations must follow exact rules or fail immediately.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.status_manager = LLMTaskStatusManager(project_root)
        self.console = Console()

        # Define compliance rules
        self.compliance_rules = self._define_compliance_rules()

        # Track current operation context
        self.current_context = {}
        self.enforcement_active = False

    def _define_compliance_rules(self) -> List[ComplianceRule]:
        """Define rigid compliance rules"""
        rules = []

        # Rule 1: Session Management
        rules.append(ComplianceRule(
            name="session_management",
            description="LLM must start and end sessions properly",
            validator=self._validate_session_management,
            is_mandatory=True,
            violation_message="LLM operation started without proper session management"
        ))

        # Rule 2: Directory Enforcement
        rules.append(ComplianceRule(
            name="directory_enforcement",
            description="All file operations must stay within .specpulse",
            validator=self._validate_directory_compliance,
            is_mandatory=True,
            violation_message="File operation detected outside .specpulse directory"
        ))

        # Rule 3: Status Updates
        rules.append(ComplianceRule(
            name="status_updates",
            description="Task status must be updated before and after operations",
            validator=self._validate_status_updates,
            is_mandatory=True,
            violation_message="Task status not properly updated during operation"
        ))

        # Rule 4: File Tracking
        rules.append(ComplianceRule(
            name="file_tracking",
            description="All file operations must be tracked",
            validator=self._validate_file_tracking,
            is_mandatory=True,
            violation_message="File operation not properly tracked"
        ))

        # Rule 5: Operation Rules
        rules.append(ComplianceRule(
            name="operation_rules",
            description="Operation-specific rules must be followed",
            validator=self._validate_operation_rules,
            is_mandatory=True,
            violation_message="Operation rules violated"
        ))

        # Rule 6: Memory Updates
        rules.append(ComplianceRule(
            name="memory_updates",
            description="Memory files must be updated after each operation",
            validator=self._validate_memory_updates,
            is_mandatory=True,
            violation_message="Memory files not updated as required"
        ))

        return rules

    def enforce_compliance(self, operation_type: LLMOperationType,
                          task_id: Optional[str] = None,
                          feature_id: Optional[str] = None,
                          feature_name: Optional[str] = None) -> str:
        """
        Start enforced compliance for an LLM operation.
        Returns session ID that must be used for all subsequent operations.

        Args:
            operation_type: Type of operation being performed
            task_id: Task identifier (if applicable)
            feature_id: Feature identifier (if applicable)
            feature_name: Feature name (if applicable)

        Returns:
            Session ID for tracking this operation

        Raises:
            LLMComplianceError: If compliance cannot be enforced
        """
        try:
            # Generate session ID
            session_id = f"llm_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{operation_type.value}"

            # Start LLM session with tracking
            if not self.status_manager.start_llm_session(
                session_id, operation_type, task_id, feature_id, feature_name
            ):
                raise LLMComplianceError("Failed to start LLM session")

            # Initialize context
            self.current_context = {
                "session_id": session_id,
                "operation_type": operation_type,
                "task_id": task_id,
                "feature_id": feature_id,
                "feature_name": feature_name,
                "start_time": datetime.now(),
                "files_created": [],
                "files_modified": [],
                "status_updates": []
            }

            self.enforcement_active = True

            # Initial status update
            if task_id:
                current_status = self.status_manager.get_task_status(task_id)
                self.current_context["initial_status"] = current_status

                # Set to in_progress if starting execution
                if operation_type == LLMOperationType.TASK_EXECUTION and current_status == TaskStatus.NOT_STARTED:
                    self.status_manager.update_task_status(task_id, TaskStatus.IN_PROGRESS, "LLM session started")

            return session_id

        except Exception as e:
            raise LLMComplianceError(f"Failed to enforce compliance: {e}")

    def track_file_creation(self, file_path: Path) -> bool:
        """
        Track file creation with strict validation.

        Args:
            file_path: Path to file being created

        Returns:
            True if file creation is compliant

        Raises:
            LLMComplianceError: If file creation violates rules
        """
        if not self.enforcement_active:
            raise LLMComplianceError("File operation outside of enforced session")

        try:
            # Validate directory compliance
            if not self.status_manager.path_manager.validate_specpulse_path(file_path):
                raise LLMComplianceError(f"File creation outside .specpulse: {file_path}")

            # Track the operation
            if not self.status_manager.track_file_operation(file_path, "created"):
                raise LLMComplianceError(f"Failed to track file creation: {file_path}")

            # Update context
            self.current_context["files_created"].append(str(file_path))

            return True

        except Exception as e:
            raise LLMComplianceError(f"File creation violation: {e}")

    def track_file_modification(self, file_path: Path) -> bool:
        """
        Track file modification with strict validation.

        Args:
            file_path: Path to file being modified

        Returns:
            True if file modification is compliant

        Raises:
            LLMComplianceError: If file modification violates rules
        """
        if not self.enforcement_active:
            raise LLMComplianceError("File operation outside of enforced session")

        try:
            # Validate directory compliance
            if not self.status_manager.path_manager.validate_specpulse_path(file_path):
                raise LLMComplianceError(f"File modification outside .specpulse: {file_path}")

            # Track the operation
            if not self.status_manager.track_file_operation(file_path, "modified"):
                raise LLMComplianceError(f"Failed to track file modification: {file_path}")

            # Update context
            self.current_context["files_modified"].append(str(file_path))

            return True

        except Exception as e:
            raise LLMComplianceError(f"File modification violation: {e}")

    def force_status_update(self, task_id: str, new_status: TaskStatus, justification: str) -> bool:
        """
        Force task status update with validation.

        Args:
            task_id: Task identifier
            new_status: New task status
            justification: Reason for status change

        Returns:
            True if status update is compliant

        Raises:
            LLMComplianceError: If status update violates rules
        """
        if not self.enforcement_active:
            raise LLMComplianceError("Status update outside of enforced session")

        try:
            # Update status through status manager
            if not self.status_manager.update_task_status(task_id, new_status, justification):
                raise LLMComplianceError(f"Invalid status transition: {new_status.value}")

            # Update context
            self.current_context["status_updates"].append({
                "task_id": task_id,
                "new_status": new_status.value,
                "justification": justification,
                "timestamp": datetime.now().isoformat()
            })

            return True

        except Exception as e:
            raise LLMComplianceError(f"Status update violation: {e}")

    def enforce_memory_update(self, memory_content: str) -> bool:
        """
        Enforce memory file update with validation.

        Args:
            memory_content: Content to write to memory file

        Returns:
            True if memory update is compliant

        Raises:
            LLMComplianceError: If memory update violates rules
        """
        if not self.enforcement_active:
            raise LLMComplianceError("Memory update outside of enforced session")

        try:
            # Update context.md file
            context_file = self.status_manager.path_manager.memory_dir / "context.md"

            # Track file modification
            self.track_file_modification(context_file)

            # Append to context file with proper formatting
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_info = self.current_context

            content_to_add = f"""

## LLM Operation Update - {timestamp}
- **Session ID**: {session_info.get('session_id', 'unknown')}
- **Operation**: {session_info.get('operation_type', 'unknown').value if hasattr(session_info.get('operation_type', ''), 'value') else str(session_info.get('operation_type', 'unknown'))}
- **Task ID**: {session_info.get('task_id', 'N/A')}
- **Feature**: {session_info.get('feature_name', 'N/A')} ({session_info.get('feature_id', 'N/A')})
- **Files Created**: {len(session_info.get('files_created', []))}
- **Files Modified**: {len(session_info.get('files_modified', []))}
- **Status Updates**: {len(session_info.get('status_updates', []))}

{memory_content}

---

"""

            # Write to context file
            if context_file.exists():
                existing_content = context_file.read_text(encoding='utf-8')
                updated_content = existing_content + content_to_add
            else:
                updated_content = f"# SpecPulse Context\n\n{content_to_add}"

            context_file.write_text(updated_content, encoding='utf-8')

            return True

        except Exception as e:
            raise LLMComplianceError(f"Memory update violation: {e}")

    def validate_and_end_session(self, success: bool = True, error_message: Optional[str] = None) -> bool:
        """
        Validate all compliance rules and end the current session.

        Args:
            success: Whether the operation was successful
            error_message: Error message if operation failed

        Returns:
            True if session ends successfully

        Raises:
            LLMComplianceError: If compliance validation fails
        """
        if not self.enforcement_active:
            raise LLMComplianceError("No active enforcement session")

        try:
            # Update context with end time
            self.current_context["end_time"] = datetime.now()
            self.current_context["success"] = success

            # Enforce memory update if successful
            if success:
                memory_content = f"LLM operation completed successfully.\n\n**Summary:**\n"
                if self.current_context.get("files_created"):
                    memory_content += f"- Files created: {', '.join(self.current_context['files_created'])}\n"
                if self.current_context.get("files_modified"):
                    memory_content += f"- Files modified: {', '.join(self.current_context['files_modified'])}\n"
                if self.current_context.get("status_updates"):
                    memory_content += f"- Status updates: {len(self.current_context['status_updates'])} updates made\n"

                self.enforce_memory_update(memory_content)

            # Validate all compliance rules
            compliance_result = self.status_manager.enforce_llm_compliance(self.current_context)

            if not compliance_result["compliant"]:
                violation_summary = ", ".join(compliance_result["violations"] + compliance_result["forbidden_actions_detected"])
                raise LLMComplianceError(f"Compliance validation failed: {violation_summary}")

            # End the session through status manager
            if not self.status_manager.end_llm_session(success, error_message):
                raise LLMComplianceError("Failed to end LLM session properly")

            # Clear enforcement state
            self.enforcement_active = False
            session_id = self.current_context.get("session_id")
            self.current_context = {}

            return True

        except Exception as e:
            # Try to end session with error
            try:
                self.status_manager.end_llm_session(False, str(e))
            except:
                pass

            self.enforcement_active = False
            session_id = self.current_context.get("session_id")
            self.current_context = {}

            raise LLMComplianceError(f"Session validation failed: {e}")

    def get_compliance_report(self) -> Dict[str, Any]:
        """Get comprehensive compliance report"""
        try:
            return {
                "compliance_score": self.status_manager.get_compliance_score(),
                "active_sessions": self.status_manager.get_active_sessions(),
                "current_session": self.current_context.get("session_id") if self.enforcement_active else None,
                "rules_enforced": len(self.compliance_rules),
                "mandatory_rules": sum(1 for rule in self.compliance_rules if rule.is_mandatory)
            }
        except Exception as e:
            return {"error": str(e)}

    # Validation method implementations
    def _validate_session_management(self, context: Dict[str, Any]) -> bool:
        """Validate session management compliance"""
        return "session_id" in context and self.enforcement_active

    def _validate_directory_compliance(self, context: Dict[str, Any]) -> bool:
        """Validate directory compliance"""
        files = context.get("files_created", []) + context.get("files_modified", [])
        for file_path in files:
            if not self.status_manager.path_manager.validate_specpulse_path(Path(file_path)):
                return False
        return True

    def _validate_status_updates(self, context: Dict[str, Any]) -> bool:
        """Validate status update compliance"""
        if context.get("task_id"):
            return len(context.get("status_updates", [])) > 0
        return True  # Status updates optional for operations without task_id

    def _validate_file_tracking(self, context: Dict[str, Any]) -> bool:
        """Validate file tracking compliance"""
        files_created = context.get("files_created", [])
        files_modified = context.get("files_modified", [])
        return len(files_created) + len(files_modified) > 0 or context.get("operation_type") in [LLMOperationType.STATUS_UPDATE]

    def _validate_operation_rules(self, context: Dict[str, Any]) -> bool:
        """Validate operation-specific rules"""
        operation_type = context.get("operation_type")
        if not operation_type:
            return False

        # Validate based on operation type
        if operation_type == LLMOperationType.SPEC_CREATION:
            return any("spec-" in f for f in context.get("files_created", []))
        elif operation_type == LLMOperationType.PLAN_CREATION:
            return any("plan-" in f for f in context.get("files_created", []))
        elif operation_type == LLMOperationType.TASK_EXECUTION:
            return len(context.get("status_updates", [])) >= 1

        return True

    def _validate_memory_updates(self, context: Dict[str, Any]) -> bool:
        """Validate memory update compliance"""
        # Check if context.md was modified
        files_modified = context.get("files_modified", [])
        return any("memory/context.md" in f or "context.md" in f for f in files_modified)


def enforce_llm_compliance(operation_type: LLMOperationType,
                          task_id: Optional[str] = None,
                          feature_id: Optional[str] = None,
                          feature_name: Optional[str] = None):
    """
    Decorator to enforce LLM compliance for a function.

    Usage:
    @enforce_llm_compliance(LLMOperationType.TASK_EXECUTION, task_id="001")
    def my_llm_function():
        # Function code here
        pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get project root from first argument if it's a SpecPulse instance
            project_root = None
            if args and hasattr(args[0], 'project_root'):
                project_root = Path(args[0].project_root)
            elif 'project_root' in kwargs:
                project_root = Path(kwargs['project_root'])
            else:
                # Default to current directory
                project_root = Path.cwd()

            enforcer = LLMComplianceEnforcer(project_root)

            try:
                # Start enforcement
                session_id = enforcer.enforce_compliance(
                    operation_type, task_id, feature_id, feature_name
                )

                # Execute the function
                result = func(*args, **kwargs)

                # End session successfully
                enforcer.validate_and_end_session(True)

                return result

            except Exception as e:
                # End session with error
                try:
                    enforcer.validate_and_end_session(False, str(e))
                except:
                    pass

                raise

        return wrapper
    return decorator


# Import datetime for session ID generation
from datetime import datetime

__all__ = [
    'LLMComplianceEnforcer',
    'LLMComplianceError',
    'ComplianceRule',
    'enforce_llm_compliance'
]