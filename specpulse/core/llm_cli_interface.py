"""
LLM CLI Interface for SpecPulse

This module provides a standardized interface for LLM to interact with SpecPulse CLI
with strict enforcement and no interpretation allowed.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

from .llm_compliance_enforcer import LLMComplianceEnforcer, enforce_llm_compliance
from .llm_task_status_manager import LLMTaskStatusManager, TaskStatus, LLMOperationType
from ..utils.error_handler import ValidationError, ErrorSeverity
from ..utils.console import Console


class CLICommand(Enum):
    """SpecPulse CLI commands that LLM can use"""
    PULSE = "pulse"
    SPEC = "spec"
    PLAN = "plan"
    TASK = "task"
    EXECUTE = "execute"
    STATUS = "status"
    VALIDATE = "validate"
    FEATURE = "feature"
    DECOMPOSE = "decompose"
    CLARIFY = "clarify"
    CONTINUE = "continue"
    DOCTOR = "doctor"


@dataclass
class CLICommandResult:
    """Result of a CLI command execution"""
    command: str
    success: bool
    return_code: int
    stdout: str
    stderr: str
    execution_time: float
    files_affected: List[str]


class LLMCLIInterface:
    """
    Provides a strict interface for LLM to interact with SpecPulse CLI.
    No interpretation allowed - only exact command execution.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.enforcer = LLMComplianceEnforcer(project_root)
        self.status_manager = LLMTaskStatusManager(project_root)
        self.console = Console()

        # Validate that we're in a SpecPulse project
        self._validate_specpulse_project()

        # Current operation tracking
        self.current_session_id = None
        self.current_operation = None

    def _validate_specpulse_project(self) -> None:
        """Validate that current directory is a SpecPulse project"""
        specpulse_dir = self.project_root / ".specpulse"
        if not specpulse_dir.exists():
            raise ValidationError(
                f"Not a SpecPulse project: {self.project_root}",
                "project_validation",
                ErrorSeverity.FATAL
            )

    def execute_command(self, command: Union[CLICommand, str],
                       args: Optional[List[str]] = None,
                       task_id: Optional[str] = None,
                       feature_id: Optional[str] = None,
                       feature_name: Optional[str] = None,
                       **kwargs) -> CLICommandResult:
        """
        Execute a SpecPulse CLI command with strict enforcement.

        Args:
            command: CLI command to execute
            args: Additional arguments for the command
            task_id: Task ID for tracking
            feature_id: Feature ID for tracking
            feature_name: Feature name for tracking
            **kwargs: Additional keyword arguments

        Returns:
            CLICommandResult with execution details

        Raises:
            ValidationError: If command execution violates rules
        """
        if isinstance(command, str):
            try:
                command = CLICommand(command.lower())
            except ValueError:
                raise ValidationError(f"Invalid command: {command}", "cli_execution", ErrorSeverity.HIGH)

        # Start enforcement session
        operation_type = self._map_command_to_operation_type(command)
        session_id = self.enforcer.enforce_compliance(
            operation_type, task_id, feature_id, feature_name
        )

        self.current_session_id = session_id
        self.current_operation = command

        try:
            # Build command
            cmd = ["python", "-m", "specpulse.cli.main", command.value]
            if args:
                cmd.extend(args)

            # Add common arguments
            if kwargs.get("verbose"):
                cmd.append("--verbose")
            if kwargs.get("force"):
                cmd.append("--force")

            # Execute command
            import time
            start_time = time.time()

            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=kwargs.get("timeout", 300)  # 5 minute default timeout
            )

            execution_time = time.time() - start_time

            # Parse affected files from output
            files_affected = self._parse_affected_files(result.stdout)

            # Create result object
            cli_result = CLICommandResult(
                command=" ".join(cmd),
                success=result.returncode == 0,
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                files_affected=files_affected
            )

            # Track file operations
            for file_path in files_affected:
                full_path = self.project_root / file_path
                if full_path.exists():
                    # Determine if file was created or modified (simplified)
                    self.enforcer.track_file_modification(full_path)

            # Validate success and end session
            success = cli_result.success and not cli_result.stderr
            error_message = cli_result.stderr if not success else None

            self.enforcer.validate_and_end_session(success, error_message)

            return cli_result

        except subprocess.TimeoutExpired:
            self.enforcer.validate_and_end_session(False, "Command execution timed out")
            raise ValidationError(f"Command timed out: {command.value}", "cli_execution", ErrorSeverity.HIGH)

        except Exception as e:
            self.enforcer.validate_and_end_session(False, str(e))
            raise ValidationError(f"Command execution failed: {e}", "cli_execution", ErrorSeverity.HIGH)

        finally:
            self.current_session_id = None
            self.current_operation = None

    def _map_command_to_operation_type(self, command: CLICommand) -> LLMOperationType:
        """Map CLI commands to operation types"""
        mapping = {
            CLICommand.PULSE: LLMOperationType.STATUS_UPDATE,
            CLICommand.SPEC: LLMOperationType.SPEC_CREATION,
            CLICommand.PLAN: LLMOperationType.PLAN_CREATION,
            CLICommand.TASK: LLMOperationType.TASK_CREATION,
            CLICommand.EXECUTE: LLMOperationType.TASK_EXECUTION,
            CLICommand.STATUS: LLMOperationType.STATUS_UPDATE,
            CLICommand.VALIDATE: LLMOperationType.VALIDATION,
            CLICommand.FEATURE: LLMOperationType.SPEC_CREATION,
            CLICommand.DECOMPOSE: LLMOperationType.SPEC_CREATION,
            CLICommand.CLARIFY: LLMOperationType.STATUS_UPDATE,
            CLICommand.CONTINUE: LLMOperationType.TASK_EXECUTION,
            CLICommand.DOCTOR: LLMOperationType.VALIDATION
        }
        return mapping.get(command, LLMOperationType.STATUS_UPDATE)

    def _parse_affected_files(self, output: str) -> List[str]:
        """Parse affected files from CLI output"""
        files = []

        # Look for file patterns in output
        import re

        # Match file paths in output
        file_patterns = [
            r'Created: (\.specpulse/[^\s]+)',
            r'Updated: (\.specpulse/[^\s]+)',
            r'File: (\.specpulse/[^\s]+)',
            r'(\.specpulse/[^\s]+\.(md|json|yaml|toml))'
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, output)
            for match in matches:
                if isinstance(match, tuple):
                    files.append(match[0])
                else:
                    files.append(match)

        return list(set(files))  # Remove duplicates

    # Strict command execution methods - no interpretation allowed
    def create_specification(self, feature_id: str, feature_name: str,
                           template_type: str = "tech",
                           description: Optional[str] = None) -> CLICommandResult:
        """
        Create a specification with strict parameter validation.
        No interpretation of parameters allowed.

        Args:
            feature_id: 3-digit feature identifier (e.g., "001")
            feature_name: Feature name in kebab-case (e.g., "user-auth")
            template_type: Template type (tech, business, etc.)
            description: Optional description

        Returns:
            CLICommandResult with execution details
        """
        # Validate feature_id format
        if not re.match(r'^\d{3}$', feature_id):
            raise ValidationError("Feature ID must be 3 digits (e.g., '001')", "spec_creation", ErrorSeverity.HIGH)

        # Validate feature_name format
        if not re.match(r'^[a-z][a-z0-9-]*$', feature_name):
            raise ValidationError("Feature name must be lowercase with hyphens (e.g., 'user-auth')", "spec_creation", ErrorSeverity.HIGH)

        args = [
            "create",
            "--id", feature_id,
            "--name", feature_name,
            "--template", template_type
        ]

        if description:
            args.extend(["--description", description])

        return self.execute_command(
            CLICommand.SPEC,
            args,
            feature_id=feature_id,
            feature_name=feature_name
        )

    def create_plan(self, feature_id: str, feature_name: str,
                    spec_number: Optional[int] = None) -> CLICommandResult:
        """
        Create a plan for a feature with strict validation.

        Args:
            feature_id: 3-digit feature identifier
            feature_name: Feature name
            spec_number: Specification number to plan for

        Returns:
            CLICommandResult with execution details
        """
        args = [
            "create",
            "--feature-id", feature_id,
            "--feature-name", feature_name
        ]

        if spec_number:
            args.extend(["--spec", str(spec_number)])

        return self.execute_command(
            CLICommand.PLAN,
            args,
            feature_id=feature_id,
            feature_name=feature_name
        )

    def create_task(self, feature_id: str, feature_name: str,
                   plan_number: Optional[int] = None,
                   task_type: str = "implementation") -> CLICommandResult:
        """
        Create a task with strict validation.

        Args:
            feature_id: 3-digit feature identifier
            feature_name: Feature name
            plan_number: Plan number to create tasks for
            task_type: Type of task (implementation, testing, etc.)

        Returns:
            CLICommandResult with execution details
        """
        args = [
            "create",
            "--feature-id", feature_id,
            "--feature-name", feature_name,
            "--type", task_type
        ]

        if plan_number:
            args.extend(["--plan", str(plan_number)])

        return self.execute_command(
            CLICommand.TASK,
            args,
            feature_id=feature_id,
            feature_name=feature_name
        )

    def execute_task(self, task_id: str, task_file: Optional[str] = None) -> CLICommandResult:
        """
        Execute a task with strict validation.

        Args:
            task_id: Task identifier (format: "001-feature-name-task-001")
            task_file: Optional task file path

        Returns:
            CLICommandResult with execution details
        """
        args = [task_id]

        if task_file:
            args.extend(["--file", task_file])

        return self.execute_command(
            CLICommand.EXECUTE,
            args,
            task_id=task_id
        )

    def get_status(self, detailed: bool = False) -> CLICommandResult:
        """
        Get project status with optional detailed view.

        Args:
            detailed: Whether to show detailed status

        Returns:
            CLICommandResult with status information
        """
        args = []
        if detailed:
            args.append("--detailed")

        return self.execute_command(CLICommand.STATUS, args)

    def validate_project(self, strict: bool = False) -> CLICommandResult:
        """
        Validate project structure and rules.

        Args:
            strict: Whether to perform strict validation

        Returns:
            CLICommandResult with validation results
        """
        args = []
        if strict:
            args.append("--strict")

        return self.execute_command(CLICommand.VALIDATE, args)

    def continue_feature(self, feature_id: str) -> CLICommandResult:
        """
        Continue work on a feature.

        Args:
            feature_id: Feature identifier

        Returns:
            CLICommandResult with continuation results
        """
        args = [feature_id]

        return self.execute_command(
            CLICommand.CONTINUE,
            args,
            feature_id=feature_id
        )

    def clarify_specifications(self, spec_id: Optional[str] = None) -> CLICommandResult:
        """
        Address clarification markers in specifications.

        Args:
            spec_id: Optional specification ID to clarify

        Returns:
            CLICommandResult with clarification results
        """
        args = []
        if spec_id:
            args.append(spec_id)

        return self.execute_command(CLICommand.CLARIFY, args)

    def run_doctor(self, fix_issues: bool = False) -> CLICommandResult:
        """
        Run SpecPulse doctor to check system health.

        Args:
            fix_issues: Whether to automatically fix issues

        Returns:
            CLICommandResult with doctor results
        """
        args = []
        if fix_issues:
            args.append("--fix")

        return self.execute_command(CLICommand.DOCTOR, args)

    def get_compliance_status(self) -> Dict[str, Any]:
        """Get current compliance status"""
        return self.enforcer.get_compliance_report()


# Import re for pattern matching
import re


__all__ = [
    'LLMCLIInterface',
    'CLICommand',
    'CLICommandResult'
]