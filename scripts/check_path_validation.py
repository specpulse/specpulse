#!/usr/bin/env python3
"""
Pre-commit hook to ensure path validation on user inputs.

This script checks that user-provided paths are validated using
PathValidator before file system operations.

CRITICAL PATTERNS TO CHECK:
- file_path parameters should be validated
- User input → Path() → file operations should have validation
- CLI arguments that become paths should be validated

Exit codes:
- 0: All checks passed
- 1: Validation issues found
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


# Patterns that indicate user input handling
USER_INPUT_PATTERNS = [
    # CLI argument patterns
    r'argparse.*add_argument.*["\'].*name["\']',
    r'@click\.argument\(',
    r'@click\.option\(',
    # Direct file operations with user input
    r'Path\(.*user.*\)',
    r'Path\(.*input.*\)',
    r'Path\(.*args\.',
    r'open\(.*args\.',
]

# File operation patterns that should have validation
FILE_OPERATION_PATTERNS = [
    r'\.write_text\(',
    r'\.write_bytes\(',
    r'\.mkdir\(',
    r'\.touch\(',
    r'\.unlink\(',
    r'\.rmdir\(',
    r'open\(',
    r'shutil\.copy',
    r'shutil\.move',
    r'shutil\.rmtree',
]

# Safe validation patterns
VALIDATION_PATTERNS = [
    r'PathValidator\.validate',
    r'validate_feature_name',
    r'validate_file_path',
    r'_validate.*path',
]


def check_file(file_path: Path) -> List[Tuple[int, str]]:
    """
    Check a Python file for missing path validation.

    Args:
        file_path: Path to Python file

    Returns:
        List of (line_number, issue_description) tuples
    """
    if not file_path.suffix == '.py':
        return []

    if not file_path.exists():
        return []

    issues = []

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        for line_num, line in enumerate(lines, start=1):
            # Skip comments and docstrings
            if line.strip().startswith('#') or '"""' in line or "'''" in line:
                continue

            # Check for file operations with user input
            for pattern in FILE_OPERATION_PATTERNS:
                if re.search(pattern, line):
                    # Check if this line or nearby lines have validation
                    context_start = max(0, line_num - 10)
                    context_end = min(len(lines), line_num + 5)
                    context = '\n'.join(lines[context_start:context_end])

                    has_validation = any(
                        re.search(val_pattern, context)
                        for val_pattern in VALIDATION_PATTERNS
                    )

                    if not has_validation:
                        # Check if it's dealing with user input
                        has_user_input = any(
                            re.search(input_pattern, context)
                            for input_pattern in USER_INPUT_PATTERNS
                        )

                        if has_user_input:
                            issues.append((
                                line_num,
                                f"Possible file operation on user input without "
                                f"PathValidator: {line.strip()}"
                            ))

    except Exception as e:
        print(f"Error checking {file_path}: {e}", file=sys.stderr)

    return issues


def main() -> int:
    """Main entry point"""
    # Get Python files in specpulse/ directory
    project_root = Path(__file__).parent.parent
    specpulse_dir = project_root / "specpulse"

    if not specpulse_dir.exists():
        print("Error: specpulse/ directory not found", file=sys.stderr)
        return 1

    all_issues = []

    # Check all Python files
    for py_file in specpulse_dir.rglob("*.py"):
        # Skip __pycache__ and test files
        if '__pycache__' in str(py_file) or 'test_' in py_file.name:
            continue

        issues = check_file(py_file)
        if issues:
            all_issues.append((py_file, issues))

    # Report issues
    if all_issues:
        print("⚠️  Path validation warnings detected:\n", file=sys.stderr)
        for file_path, issues in all_issues:
            print(f"File: {file_path.relative_to(project_root)}", file=sys.stderr)
            for line_num, issue in issues:
                print(f"  Line {line_num}: {issue}", file=sys.stderr)
            print("", file=sys.stderr)

        print("\n💡 Recommendation:", file=sys.stderr)
        print("  Ensure all user-provided paths are validated with PathValidator", file=sys.stderr)
        print("  before file system operations.", file=sys.stderr)
        print("\n  Example:", file=sys.stderr)
        print("    from specpulse.utils.path_validator import PathValidator", file=sys.stderr)
        print("    safe_path = PathValidator.validate_file_path(base_dir, user_input)", file=sys.stderr)
        print("", file=sys.stderr)

        # Return warning (0) instead of error (1) to not block commits
        # Change to return 1 if you want to enforce strictly
        return 0  # WARNING mode
        # return 1  # STRICT mode (blocks commit)

    print("✅ Path validation check passed", file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
