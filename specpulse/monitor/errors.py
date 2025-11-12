"""
Error Handling and Logging Module

This module provides comprehensive error handling and logging capabilities
for the task monitoring system with graceful degradation and user-friendly messages.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import traceback

from .models import MonitoringConfig


class MonitorError(Exception):
    """Base exception for task monitoring errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None, details: Optional[str] = None):
        """Initialize monitor error with optional suggestion and details."""
        super().__init__(message)
        self.suggestion = suggestion
        self.details = details
        self.timestamp = datetime.now()


class TaskDiscoveryError(MonitorError):
    """Raised when task discovery fails."""
    pass


class StateTransitionError(MonitorError):
    """Raised when invalid state transitions are attempted."""
    pass


class DataCorruptionError(MonitorError):
    """Raised when data corruption is detected."""
    pass


class ConfigurationError(MonitorError):
    """Raised when configuration is invalid."""
    pass


class PerformanceError(MonitorError):
    """Raised when performance thresholds are exceeded."""
    pass


class IntegrationError(MonitorError):
    """Raised when integration with SpecPulse workflow fails."""
    pass


class StorageError(MonitorError):
    """Raised when storage operations fail."""
    pass


class CorruptedDataError(MonitorError):
    """Raised when corrupted data is detected."""
    pass


class ErrorHandler:
    """Handles error processing and user-friendly message generation."""

    def __init__(self, verbose: bool = False, log_file: Optional[Path] = None):
        """Initialize error handler with verbosity and optional log file."""
        self.verbose = verbose
        self.log_file = log_file
        self.error_count = 0
        self.recent_errors: List[Dict[str, Any]] = []

        # Setup logging
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        # Create logger
        self.logger = logging.getLogger('specpulse.monitor')
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)

        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.INFO if not self.verbose else logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler if specified
        if self.log_file:
            try:
                self.log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(self.log_file)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                # Don't let logging setup failures break the application
                print(f"Warning: Could not setup log file: {e}", file=sys.stderr)

    def handle_error(self, error: Exception, context: Optional[str] = None) -> str:
        """Handle an error and return user-friendly message."""
        self.error_count += 1

        # Log the error
        self.logger.error(f"Error in {context or 'unknown context'}: {str(error)}")
        if self.verbose:
            self.logger.debug(traceback.format_exc())

        # Record error for analysis
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
            "count": self.error_count
        }
        self.recent_errors.append(error_record)

        # Keep only last 100 errors
        if len(self.recent_errors) > 100:
            self.recent_errors = self.recent_errors[-100:]

        # Generate user-friendly message
        if isinstance(error, MonitorError):
            return self._format_monitor_error(error)
        else:
            return self._format_generic_error(error, context)

    def _format_monitor_error(self, error: MonitorError) -> str:
        """Format monitor-specific errors."""
        message = f"❌ {str(error)}"

        if error.suggestion:
            message += f"\n💡 Suggestion: {error.suggestion}"

        if self.verbose and error.details:
            message += f"\n📋 Details: {error.details}"

        return message

    def _format_generic_error(self, error: Exception, context: Optional[str] = None) -> str:
        """Format generic exceptions."""
        message = f"❌ An unexpected error occurred"

        if context:
            message += f" while {context}"

        message += f": {str(error)}"

        if self.verbose:
            message += f"\n📋 Details: {traceback.format_exc()}"
        else:
            message += "\n💡 Use --verbose for more details"

        return message

    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of recent errors."""
        if not self.recent_errors:
            return {"total_errors": 0, "recent_errors": []}

        # Analyze error types
        error_types = {}
        for error in self.recent_errors:
            error_type = error["type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1

        return {
            "total_errors": self.error_count,
            "recent_errors": len(self.recent_errors),
            "error_types": error_types,
            "last_error": self.recent_errors[-1] if self.recent_errors else None
        }

    def clear_errors(self) -> None:
        """Clear error history."""
        self.recent_errors.clear()
        self.error_count = 0


class SafeExecutor:
    """Provides safe execution with graceful error handling."""

    def __init__(self, error_handler: ErrorHandler):
        """Initialize safe executor with error handler."""
        self.error_handler = error_handler

    def safe_execute(self, func, *args, default_return=None, context: Optional[str] = None, **kwargs):
        """Execute function safely with error handling."""
        try:
            return func(*args, **kwargs)
        except Exception as error:
            error_message = self.error_handler.handle_error(error, context)
            if default_return is not None:
                return default_return
            raise error

    def safe_execute_with_fallback(self, func, fallback_func, *args, context: Optional[str] = None, **kwargs):
        """Execute function with fallback on failure."""
        try:
            return func(*args, **kwargs)
        except Exception as error:
            error_message = self.error_handler.handle_error(error, context)
            self.error_handler.logger.warning(f"Using fallback for {context or 'operation'}")
            return fallback_func(*args, **kwargs)


class ValidationLogger:
    """Logs validation results and data integrity issues."""

    def __init__(self, log_file: Optional[Path] = None):
        """Initialize validation logger."""
        self.log_file = log_file
        self.validation_history: List[Dict[str, Any]] = []

        # Setup validation logger
        self.logger = logging.getLogger('specpulse.monitor.validation')
        self.logger.setLevel(logging.INFO)

        if log_file:
            try:
                log_file.parent.mkdir(parents=True, exist_ok=True)
                handler = logging.FileHandler(log_file)
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            except Exception:
                pass  # Don't let logging failures break validation

    def log_validation_result(self, result: Dict[str, Any], feature_id: Optional[str] = None) -> None:
        """Log validation result."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "feature_id": feature_id,
            "result": result
        }
        self.validation_history.append(record)

        # Log to file
        if result.get("valid", True):
            self.logger.info(f"Validation passed for feature {feature_id or 'unknown'}")
        else:
            self.logger.warning(f"Validation failed for feature {feature_id or 'unknown'}")
            for issue in result.get("issues", []):
                self.logger.warning(f"  Issue: {issue}")

        # Keep only last 1000 validation records
        if len(self.validation_history) > 1000:
            self.validation_history = self.validation_history[-1000:]

    def get_validation_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get validation summary for recent days."""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 3600)

        recent_validations = [
            record for record in self.validation_history
            if datetime.fromisoformat(record["timestamp"]).timestamp() > cutoff_date
        ]

        if not recent_validations:
            return {"total_validations": 0, "pass_rate": 0.0, "issues": []}

        total = len(recent_validations)
        passed = sum(1 for record in recent_validations if record["result"].get("valid", True))
        pass_rate = (passed / total) * 100 if total > 0 else 0

        # Collect common issues
        issues = {}
        for record in recent_validations:
            for issue in record["result"].get("issues", []):
                issues[issue] = issues.get(issue, 0) + 1

        return {
            "total_validations": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round(pass_rate, 1),
            "common_issues": sorted(issues.items(), key=lambda x: x[1], reverse=True)[:10]
        }


class PerformanceMonitor:
    """Monitors performance and warns about potential issues."""

    def __init__(self, config: MonitoringConfig):
        """Initialize performance monitor with configuration."""
        self.config = config
        self.performance_log: List[Dict[str, Any]] = []
        self.thresholds = {
            "max_task_count": config.max_tasks_per_feature,
            "max_response_time": 3.0,  # seconds
            "max_memory_usage": 50 * 1024 * 1024,  # 50MB
        }

    def log_performance(self, operation: str, duration: float, task_count: int = 0,
                        memory_usage: Optional[int] = None) -> None:
        """Log performance metrics."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration": duration,
            "task_count": task_count,
            "memory_usage": memory_usage
        }
        self.performance_log.append(record)

        # Check thresholds
        warnings = self._check_thresholds(record)
        for warning in warnings:
            print(f"⚠️  Performance Warning: {warning}", file=sys.stderr)

        # Keep only last 1000 records
        if len(self.performance_log) > 1000:
            self.performance_log = self.performance_log[-1000]

    def _check_thresholds(self, record: Dict[str, Any]) -> List[str]:
        """Check performance thresholds and return warnings."""
        warnings = []

        if record["duration"] > self.thresholds["max_response_time"]:
            warnings.append(
                f"{record['operation']} took {record['duration']:.2f}s "
                f"(threshold: {self.thresholds['max_response_time']}s)"
            )

        if record["task_count"] > self.thresholds["max_task_count"]:
            warnings.append(
                f"Task count {record['task_count']} exceeds threshold "
                f"({self.thresholds['max_task_count']})"
            )

        if (record["memory_usage"] and
            record["memory_usage"] > self.thresholds["max_memory_usage"]):
            memory_mb = record["memory_usage"] / (1024 * 1024)
            threshold_mb = self.thresholds["max_memory_usage"] / (1024 * 1024)
            warnings.append(
                f"Memory usage {memory_mb:.1f}MB exceeds threshold "
                f"({threshold_mb:.1f}MB)"
            )

        return warnings

    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for recent hours."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)

        recent_records = [
            record for record in self.performance_log
            if datetime.fromisoformat(record["timestamp"]).timestamp() > cutoff_time
        ]

        if not recent_records:
            return {"total_operations": 0, "average_duration": 0.0}

        total_operations = len(recent_records)
        durations = [record["duration"] for record in recent_records]
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)

        # Group by operation type
        operations = {}
        for record in recent_records:
            op = record["operation"]
            if op not in operations:
                operations[op] = []
            operations[op].append(record["duration"])

        operation_stats = {}
        for op, op_durations in operations.items():
            operation_stats[op] = {
                "count": len(op_durations),
                "average": sum(op_durations) / len(op_durations),
                "max": max(op_durations),
                "min": min(op_durations)
            }

        return {
            "total_operations": total_operations,
            "average_duration": round(avg_duration, 3),
            "max_duration": round(max_duration, 3),
            "min_duration": round(min_duration, 3),
            "operation_breakdown": operation_stats
        }


# Global error handler instance (initialized when needed)
_global_error_handler: Optional[ErrorHandler] = None
_global_performance_monitor: Optional[PerformanceMonitor] = None
_global_validation_logger: Optional[ValidationLogger] = None


def get_error_handler(verbose: bool = False, log_file: Optional[Path] = None) -> ErrorHandler:
    """Get or create global error handler."""
    global _global_error_handler

    if _global_error_handler is None:
        _global_error_handler = ErrorHandler(verbose, log_file)

    return _global_error_handler


def get_performance_monitor(config: MonitoringConfig) -> PerformanceMonitor:
    """Get or create global performance monitor."""
    global _global_performance_monitor

    if _global_performance_monitor is None:
        _global_performance_monitor = PerformanceMonitor(config)

    return _global_performance_monitor


def get_validation_logger(log_file: Optional[Path] = None) -> ValidationLogger:
    """Get or create global validation logger."""
    global _global_validation_logger

    if _global_validation_logger is None:
        _global_validation_logger = ValidationLogger(log_file)

    return _global_validation_logger


def handle_monitor_error(error: Exception, context: Optional[str] = None) -> str:
    """Convenient function to handle monitor errors."""
    handler = get_error_handler()
    return handler.handle_error(error, context)


def safe_execute(func, *args, default_return=None, context: Optional[str] = None, **kwargs):
    """Convenient function for safe execution."""
    handler = get_error_handler()
    executor = SafeExecutor(handler)
    return executor.safe_execute(func, *args, default_return=default_return, context=context, **kwargs)