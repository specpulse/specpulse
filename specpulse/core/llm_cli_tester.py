"""
LLM CLI Tester for SpecPulse

This module provides comprehensive testing for CLI-LLM integration
to ensure everything works smoothly without interpretation issues.
"""

import tempfile
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from .llm_cli_interface import LLMCLIInterface, CLICommand, CLICommandResult
from .llm_compliance_enforcer import LLMComplianceEnforcer
from .llm_task_status_manager import LLMTaskStatusManager, TaskStatus, LLMOperationType
from ..utils.error_handler import ValidationError, ErrorSeverity
from ..utils.console import Console


class TestResult(Enum):
    """Test result enumeration"""
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


@dataclass
class TestCase:
    """Test case definition"""
    name: str
    description: str
    command: CLICommand
    args: List[str]
    expected_success: bool
    expected_files: List[str]
    validation_function: Optional[callable] = None
    timeout: int = 30


@dataclass
class TestExecution:
    """Test execution result"""
    test_case: TestCase
    result: TestResult
    cli_result: Optional[CLICommandResult]
    execution_time: float
    error_message: Optional[str]
    compliance_score: float


class LLMCLITester:
    """
    Comprehensive tester for CLI-LLM integration.
    Ensures all operations work smoothly and follow strict rules.
    """

    def __init__(self, project_root: Optional[Path] = None):
        if project_root is None:
            # Create temporary project for testing
            self.temp_project = self._create_test_project()
            self.project_root = self.temp_project
        else:
            self.project_root = project_root
            self.temp_project = None

        self.cli_interface = LLMCLIInterface(self.project_root)
        self.enforcer = LLMComplianceEnforcer(self.project_root)
        self.status_manager = LLMTaskStatusManager(self.project_root)
        self.console = Console()

        # Test results
        self.test_results: List[TestExecution] = []

    def _create_test_project(self) -> Path:
        """Create a temporary SpecPulse project for testing"""
        import tempfile
        import shutil

        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix="specpulse_test_"))

        try:
            # Initialize SpecPulse project
            from .specpulse import SpecPulse
            specpulse = SpecPulse(project_path=temp_dir)

            init_result = specpulse.init(
                project_name="Test Project",
                here=True,
                ai_assistant="claude",
                force=True
            )

            if init_result["status"] != "success":
                raise ValidationError("Failed to initialize test project", "test_setup", ErrorSeverity.HIGH)

            return temp_dir

        except Exception as e:
            # Cleanup on failure
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise ValidationError(f"Failed to create test project: {e}", "test_setup", ErrorSeverity.HIGH)

    def define_test_cases(self) -> List[TestCase]:
        """Define comprehensive test cases for CLI-LLM integration"""
        test_cases = []

        # Test 1: Status command
        test_cases.append(TestCase(
            name="status_basic",
            description="Basic status command should succeed",
            command=CLICommand.STATUS,
            args=[],
            expected_success=True,
            expected_files=[],
            timeout=10
        ))

        # Test 2: Detailed status
        test_cases.append(TestCase(
            name="status_detailed",
            description="Detailed status command should succeed",
            command=CLICommand.STATUS,
            args=["--detailed"],
            expected_success=True,
            expected_files=[],
            timeout=15
        ))

        # Test 3: Doctor command
        test_cases.append(TestCase(
            name="doctor_basic",
            description="Doctor command should succeed",
            command=CLICommand.DOCTOR,
            args=[],
            expected_success=True,
            expected_files=[],
            timeout=20
        ))

        # Test 4: Validation command
        test_cases.append(TestCase(
            name="validate_basic",
            description="Basic validation should succeed",
            command=CLICommand.VALIDATE,
            args=[],
            expected_success=True,
            expected_files=[],
            timeout=15
        ))

        # Test 5: Create specification
        test_cases.append(TestCase(
            name="create_spec",
            description="Create specification should succeed",
            command=CLICommand.SPEC,
            args=["create", "--id", "001", "--name", "test-feature", "--template", "tech"],
            expected_success=True,
            expected_files=[".specpulse/specs/001-test-feature/spec-001.md"],
            timeout=30,
            validation_function=self._validate_spec_creation
        ))

        # Test 6: Create plan
        test_cases.append(TestCase(
            name="create_plan",
            description="Create plan should succeed",
            command=CLICommand.PLAN,
            args=["create", "--feature-id", "001", "--feature-name", "test-feature"],
            expected_success=True,
            expected_files=[".specpulse/plans/001-test-feature/plan-1.md"],
            timeout=30,
            validation_function=self._validate_plan_creation
        ))

        # Test 7: Create task
        test_cases.append(TestCase(
            name="create_task",
            description="Create task should succeed",
            command=CLICommand.TASK,
            args=["create", "--feature-id", "001", "--feature-name", "test-feature", "--type", "implementation"],
            expected_success=True,
            expected_files=[".specpulse/tasks/001-test-feature/task-001.md"],
            timeout=30,
            validation_function=self._validate_task_creation
        ))

        # Test 8: Invalid specification (should fail)
        test_cases.append(TestCase(
            name="invalid_spec",
            description="Invalid specification creation should fail",
            command=CLICommand.SPEC,
            args=["create", "--id", "invalid", "--name", "", "--template", "tech"],
            expected_success=False,
            expected_files=[],
            timeout=15
        ))

        # Test 9: Clarify command
        test_cases.append(TestCase(
            name="clarify_basic",
            description="Clarify command should succeed",
            command=CLICommand.CLARIFY,
            args=[],
            expected_success=True,
            expected_files=[],
            timeout=20
        ))

        # Test 10: Compliance validation
        test_cases.append(TestCase(
            name="compliance_check",
            description="Compliance should be maintained",
            command=CLICommand.DOCTOR,
            args=[],
            expected_success=True,
            expected_files=[],
            timeout=15,
            validation_function=self._validate_compliance
        ))

        return test_cases

    def run_test_case(self, test_case: TestCase) -> TestExecution:
        """Run a single test case"""
        start_time = time.time()

        try:
            # Execute the command
            cli_result = self.cli_interface.execute_command(
                test_case.command,
                test_case.args,
                timeout=test_case.timeout
            )

            execution_time = time.time() - start_time

            # Check if success matches expectation
            success_match = (cli_result.success == test_case.expected_success)

            # Check if expected files exist
            files_exist = True
            for expected_file in test_case.expected_files:
                file_path = self.project_root / expected_file
                if not file_path.exists():
                    files_exist = False
                    break

            # Run validation function if provided
            validation_passed = True
            if test_case.validation_function:
                validation_passed = test_case.validation_function(cli_result)

            # Get compliance score
            compliance_report = self.cli_interface.get_compliance_status()
            compliance_score = compliance_report.get("compliance_score", 0.0)

            # Determine test result
            if cli_result.success == test_case.expected_success and files_exist and validation_passed:
                result = TestResult.PASS
            else:
                result = TestResult.FAIL

            error_message = None
            if result == TestResult.FAIL:
                error_parts = []
                if not success_match:
                    error_parts.append(f"Success mismatch: expected {test_case.expected_success}, got {cli_result.success}")
                if not files_exist:
                    error_parts.append("Missing expected files")
                if not validation_passed:
                    error_parts.append("Validation function failed")
                error_message = "; ".join(error_parts)

            return TestExecution(
                test_case=test_case,
                result=result,
                cli_result=cli_result,
                execution_time=execution_time,
                error_message=error_message,
                compliance_score=compliance_score
            )

        except Exception as e:
            execution_time = time.time() - start_time

            return TestExecution(
                test_case=test_case,
                result=TestResult.ERROR,
                cli_result=None,
                execution_time=execution_time,
                error_message=str(e),
                compliance_score=0.0
            )

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test cases and return results"""
        test_cases = self.define_test_cases()
        self.test_results = []

        total_start_time = time.time()

        for i, test_case in enumerate(test_cases, 1):
            self.console.info(f"Running test {i}/{len(test_cases)}: {test_case.name}")

            test_execution = self.run_test_case(test_case)
            self.test_results.append(test_execution)

            # Print immediate result
            status_symbol = {
                TestResult.PASS: "✓",
                TestResult.FAIL: "✗",
                TestResult.ERROR: "⚠",
                TestResult.SKIP: "⊘"
            }.get(test_execution.result, "?")

            self.console.print(f"  {status_symbol} {test_case.name}: {test_execution.result.value.upper()}")

        total_execution_time = time.time() - total_start_time

        # Generate summary
        summary = self._generate_test_summary(total_execution_time)

        return summary

    def _generate_test_summary(self, total_time: float) -> Dict[str, Any]:
        """Generate comprehensive test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.result == TestResult.PASS)
        failed_tests = sum(1 for result in self.test_results if result.result == TestResult.FAIL)
        error_tests = sum(1 for result in self.test_results if result.result == TestResult.ERROR)
        skipped_tests = sum(1 for result in self.test_results if result.result == TestResult.SKIP)

        # Calculate average compliance score
        compliance_scores = [result.compliance_score for result in self.test_results if result.compliance_score > 0]
        avg_compliance = sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0.0

        # Collect failed tests
        failed_test_details = []
        for result in self.test_results:
            if result.result in [TestResult.FAIL, TestResult.ERROR]:
                failed_test_details.append({
                    "name": result.test_case.name,
                    "result": result.result.value,
                    "error": result.error_message,
                    "compliance_score": result.compliance_score
                })

        summary = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "skipped": skipped_tests,
            "success_rate": (passed_tests / total_tests) if total_tests > 0 else 0.0,
            "total_execution_time": total_time,
            "average_compliance_score": avg_compliance,
            "failed_tests": failed_test_details,
            "recommendations": self._generate_recommendations()
        }

        return summary

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        failed_tests = [result for result in self.test_results if result.result == TestResult.FAIL]
        error_tests = [result for result in self.test_results if result.result == TestResult.ERROR]

        if error_tests:
            recommendations.append("Fix critical errors in CLI commands before proceeding")

        if failed_tests:
            recommendations.append("Review failed test cases and update validation logic")

        low_compliance_tests = [result for result in self.test_results if result.compliance_score < 0.9]
        if low_compliance_tests:
            recommendations.append("Improve LLM compliance scoring for better enforcement")

        if not any(result.test_case.name.startswith("create_") and result.result == TestResult.PASS
                  for result in self.test_results):
            recommendations.append("Ensure core functionality (spec/plan/task creation) works properly")

        return recommendations

    # Validation functions
    def _validate_spec_creation(self, cli_result: CLICommandResult) -> bool:
        """Validate specification creation"""
        if not cli_result.success:
            return False

        # Check if spec file was created with proper content
        spec_file = self.project_root / ".specpulse" / "specs" / "001-test-feature" / "spec-001.md"
        if not spec_file.exists():
            return False

        content = spec_file.read_text(encoding='utf-8')
        required_sections = ["# Specification", "## Overview", "## Requirements", "## Acceptance Criteria"]

        return all(section in content for section in required_sections)

    def _validate_plan_creation(self, cli_result: CLICommandResult) -> bool:
        """Validate plan creation"""
        if not cli_result.success:
            return False

        # Check if plan file was created
        plan_file = self.project_root / ".specpulse" / "plans" / "001-test-feature" / "plan-1.md"
        if not plan_file.exists():
            return False

        content = plan_file.read_text(encoding='utf-8')
        required_sections = ["# Implementation Plan", "## Tasks", "## Dependencies"]

        return all(section in content for section in required_sections)

    def _validate_task_creation(self, cli_result: CLICommandResult) -> bool:
        """Validate task creation"""
        if not cli_result.success:
            return False

        # Check if task file was created
        task_file = self.project_root / ".specpulse" / "tasks" / "001-test-feature" / "task-001.md"
        if not task_file.exists():
            return False

        content = task_file.read_text(encoding='utf-8')
        required_sections = ["# Task", "## Description", "## Implementation", "## Testing"]

        return all(section in content for section in required_sections)

    def _validate_compliance(self, cli_result: CLICommandResult) -> bool:
        """Validate compliance maintenance"""
        compliance_report = self.cli_interface.get_compliance_status()
        return compliance_report.get("compliance_score", 0.0) >= 0.9

    def print_test_report(self, summary: Dict[str, Any]) -> None:
        """Print detailed test report"""
        print("\n" + "="*60)
        print("SPECPLUS CLI-LLM INTEGRATION TEST REPORT")
        print("="*60)

        print(f"\n📊 SUMMARY:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✓")
        print(f"   Failed: {summary['failed']} ✗")
        print(f"   Errors: {summary['errors']} ⚠")
        print(f"   Success Rate: {summary['success_rate']:.1%}")
        print(f"   Execution Time: {summary['total_execution_time']:.2f}s")
        print(f"   Avg Compliance Score: {summary['average_compliance_score']:.3f}")

        if summary['failed_tests']:
            print(f"\n❌ FAILED TESTS:")
            for failed in summary['failed_tests']:
                print(f"   - {failed['name']}: {failed['result'].upper()}")
                if failed['error']:
                    print(f"     Error: {failed['error']}")
                print(f"     Compliance: {failed['compliance_score']:.3f}")

        if summary['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(summary['recommendations'], 1):
                print(f"   {i}. {rec}")

        # Overall status
        if summary['success_rate'] >= 0.9:
            status = "🎉 EXCELLENT"
            color = "green"
        elif summary['success_rate'] >= 0.7:
            status = "✅ GOOD"
            color = "yellow"
        else:
            status = "❌ NEEDS IMPROVEMENT"
            color = "red"

        print(f"\n🏆 OVERALL STATUS: {status}")
        print("="*60)

    def cleanup(self) -> None:
        """Cleanup temporary test project"""
        if self.temp_project and self.temp_project.exists():
            import shutil
            try:
                shutil.rmtree(self.temp_project)
            except Exception as e:
                self.console.warning(f"Failed to cleanup temp project: {e}")


# Convenience function for quick testing
def quick_cli_test(project_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Run a quick CLI-LLM integration test.

    Args:
        project_root: Optional project root path

    Returns:
        Test summary dictionary
    """
    tester = LLMCLITester(project_root)
    try:
        summary = tester.run_all_tests()
        tester.print_test_report(summary)
        return summary
    finally:
        tester.cleanup()


__all__ = [
    'LLMCLITester',
    'TestCase',
    'TestExecution',
    'TestResult',
    'quick_cli_test'
]