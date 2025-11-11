"""
Comprehensive tests for utility functions.

This module provides thorough testing of all utility functions
including file operations, validation, and other helper functions.
"""

import pytest
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

from specpulse.utils.file_utils import (
    read_file_safe, write_file_safe, backup_file,
    ensure_directory, get_file_hash, validate_filename
)
from specpulse.utils.validation import (
    validate_feature_id, validate_feature_name,
    validate_spec_number, validate_content,
    validate_json_content, sanitize_input
)
from specpulse.utils.template_utils import (
    render_template, extract_template_variables,
    validate_template_syntax, create_template_context
)
from specpulse.utils.formatting import (
    format_header, format_section, format_list,
    format_table, format_code_block
)


class TestFileUtils:
    """Test file operation utilities"""

    def test_read_file_safe_success(self, temp_dir):
        """Test successful file reading"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content", encoding='utf-8')

        content = read_file_safe(test_file)
        assert content == "Test content"

    def test_read_file_safe_not_found(self, temp_dir):
        """Test reading non-existent file"""
        test_file = temp_dir / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            read_file_safe(test_file)

    def test_read_file_safe_encoding_error(self, temp_dir):
        """Test reading file with encoding issues"""
        test_file = temp_dir / "bad_encoding.txt"
        # Write binary data that can't be read as UTF-8
        test_file.write_bytes(b'\xff\xfe\x00\x00')

        with pytest.raises(UnicodeDecodeError):
            read_file_safe(test_file, encoding='utf-8')

    def test_read_file_safe_with_encoding(self, temp_dir):
        """Test reading file with specific encoding"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content", encoding='utf-8')

        content = read_file_safe(test_file, encoding='utf-8')
        assert content == "Test content"

    def test_write_file_safe_success(self, temp_dir):
        """Test successful file writing"""
        test_file = temp_dir / "output.txt"
        content = "Test content to write"

        write_file_safe(test_file, content)

        assert test_file.exists()
        assert test_file.read_text(encoding='utf-8') == content

    def test_write_file_safe_create_directory(self, temp_dir):
        """Test writing file when directory doesn't exist"""
        test_file = temp_dir / "subdir" / "output.txt"
        content = "Test content"

        write_file_safe(test_file, content, create_dirs=True)

        assert test_file.exists()
        assert test_file.read_text(encoding='utf-8') == content

    def test_write_file_safe_directory_not_created(self, temp_dir):
        """Test writing file when directory doesn't exist and create_dirs=False"""
        test_file = temp_dir / "subdir" / "output.txt"
        content = "Test content"

        with pytest.raises(FileNotFoundError):
            write_file_safe(test_file, content, create_dirs=False)

    def test_backup_file_success(self, temp_dir):
        """Test successful file backup"""
        test_file = temp_dir / "original.txt"
        test_file.write_text("Original content")

        backup_path = backup_file(test_file)

        assert backup_path.exists()
        assert backup_path.name.startswith("original_backup_")
        assert backup_path.read_text() == "Original content"

    def test_backup_file_nonexistent(self, temp_dir):
        """Test backing up non-existent file"""
        test_file = temp_dir / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            backup_file(test_file)

    def test_backup_file_with_timestamp(self, temp_dir):
        """Test backup file with custom timestamp"""
        test_file = temp_dir / "original.txt"
        test_file.write_text("Original content")

        backup_path = backup_file(test_file, timestamp="20231201_120000")

        assert backup_path == temp_dir / "original_backup_20231201_120000.txt"

    def test_ensure_directory_success(self, temp_dir):
        """Test successful directory creation"""
        new_dir = temp_dir / "new_subdir"

        result = ensure_directory(new_dir)

        assert result is True
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_ensure_directory_already_exists(self, temp_dir):
        """Test ensuring directory that already exists"""
        existing_dir = temp_dir / "existing"
        existing_dir.mkdir()

        result = ensure_directory(existing_dir)

        assert result is True
        assert existing_dir.exists()

    def test_ensure_directory_with_parents(self, temp_dir):
        """Test creating directory with parent directories"""
        nested_dir = temp_dir / "parent" / "child" / "grandchild"

        result = ensure_directory(nested_dir)

        assert result is True
        assert nested_dir.exists()
        assert nested_dir.is_dir()

    def test_ensure_directory_permission_error(self):
        """Test directory creation with permission error"""
        restricted_path = Path("/root/restricted_dir")

        # This should fail on most systems
        with pytest.raises((PermissionError, OSError)):
            ensure_directory(restricted_path)

    def test_get_file_hash_success(self, temp_dir):
        """Test successful file hash calculation"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")

        file_hash = get_file_hash(test_file)

        assert isinstance(file_hash, str)
        assert len(file_hash) == 64  # SHA256 hex length

        # Test that same content produces same hash
        file_hash2 = get_file_hash(test_file)
        assert file_hash == file_hash2

    def test_get_file_hash_nonexistent(self, temp_dir):
        """Test hash calculation for non-existent file"""
        test_file = temp_dir / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            get_file_hash(test_file)

    def test_get_file_hash_different_algorithms(self, temp_dir):
        """Test hash calculation with different algorithms"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")

        md5_hash = get_file_hash(test_file, algorithm='md5')
        sha1_hash = get_file_hash(test_file, algorithm='sha1')
        sha256_hash = get_file_hash(test_file, algorithm='sha256')

        assert len(md5_hash) == 32  # MD5 hex length
        assert len(sha1_hash) == 40  # SHA1 hex length
        assert len(sha256_hash) == 64  # SHA256 hex length
        assert md5_hash != sha1_hash != sha256_hash

    def test_validate_filename_valid(self):
        """Test valid filename validation"""
        valid_names = [
            "test.txt",
            "file_name-123.txt",
            "document.pdf",
            "data.json",
            "README",
            "my file.txt"
        ]

        for name in valid_names:
            assert validate_filename(name) is True

    def test_validate_filename_invalid(self):
        """Test invalid filename validation"""
        invalid_names = [
            "",  # Empty
            "file<>name.txt",  # Invalid characters
            "file|name.txt",   # Invalid characters
            "file?.txt",       # Invalid characters
            "file*.txt",       # Invalid characters
            "file\".txt",      # Invalid characters
            "CON",             # Reserved name (Windows)
            "PRN",             # Reserved name (Windows)
            "AUX",             # Reserved name (Windows)
            "file" * 100 + ".txt",  # Too long
        ]

        for name in invalid_names:
            assert validate_filename(name) is False


class TestValidationUtils:
    """Test validation utilities"""

    def test_validate_feature_id_valid(self):
        """Test valid feature ID validation"""
        valid_ids = [
            "001",
            "123",
            "999",
            "000"
        ]

        for feature_id in valid_ids:
            assert validate_feature_id(feature_id) is True

    def test_validate_feature_id_invalid(self):
        """Test invalid feature ID validation"""
        invalid_ids = [
            "",      # Empty
            "1",     # Too short
            "1234",  # Too long
            "abc",   # Non-numeric
            "12a",   # Mixed
            "01",    # Only 2 digits
            "12",    # Only 2 digits
            " 123",  # Leading space
            "123 ",  # Trailing space
            "12.3",  # Decimal
        ]

        for feature_id in invalid_ids:
            assert validate_feature_id(feature_id) is False

    def test_validate_feature_name_valid(self):
        """Test valid feature name validation"""
        valid_names = [
            "user-auth",
            "data-processing",
            "api-integration",
            "simple",
            "feature_name",
            "feature-123",
            "a",  # Minimum length
        ]

        for name in valid_names:
            assert validate_feature_name(name) is True

    def test_validate_feature_name_invalid(self):
        """Test invalid feature name validation"""
        invalid_names = [
            "",                      # Empty
            "Feature Name",          # Spaces
            "feature_name",          # Underscores not allowed
            "123feature",            # Starts with number
            "feature$",              # Invalid character
            "feature@domain",        # Invalid character
            "a" * 51,                # Too long
            "-feature",              # Starts with hyphen
            "feature-",              # Ends with hyphen
            "feature--name",         # Double hyphen
            "FEATURE",               # All uppercase
        ]

        for name in invalid_names:
            assert validate_feature_name(name) is False

    def test_validate_spec_number_valid(self):
        """Test valid spec number validation"""
        valid_numbers = [1, 5, 10, 100, 999]

        for number in valid_numbers:
            assert validate_spec_number(number) is True

    def test_validate_spec_number_invalid(self):
        """Test invalid spec number validation"""
        invalid_numbers = [
            0,      # Too low
            -1,     # Negative
            1000,   # Too high
            1.5,    # Float
            "1",    # String
            None,   # None
        ]

        for number in invalid_numbers:
            assert validate_spec_number(number) is False

    def test_validate_content_valid(self):
        """Test valid content validation"""
        valid_contents = [
            "This is valid content",
            "# Header\n\nSome content here",
            "Content with **bold** and *italic*",
            "1. List item\n2. Another item",
            "```python\ncode block\n```",
            "x" * 10,  # Minimum length
        ]

        for content in valid_contents:
            assert validate_content(content) is True

    def test_validate_content_invalid(self):
        """Test invalid content validation"""
        invalid_contents = [
            "",              # Empty
            "   ",           # Only whitespace
            "x" * 5,         # Too short
            None,            # None
            123,             # Not string
        ]

        for content in invalid_contents:
            assert validate_content(content) is False

    def test_validate_json_content_valid(self):
        """Test valid JSON content validation"""
        valid_jsons = [
            '{"key": "value"}',
            '{"array": [1, 2, 3]}',
            '{"nested": {"inner": "value"}}',
            '{"empty": {}}',
            '[]',
            'null',
            'true',
            '123',
            '"string"',
        ]

        for json_content in valid_jsons:
            assert validate_json_content(json_content) is True

    def test_validate_json_content_invalid(self):
        """Test invalid JSON content validation"""
        invalid_jsons = [
            "",                    # Empty
            "{key: value}",        # Missing quotes
            '{"key": value}',      # Missing quotes around value
            '{"key": "value",}',   # Trailing comma
            '{"key": "value"',     # Missing closing brace
            'not json at all',     # Not JSON
            None,                  # None
        ]

        for json_content in invalid_jsons:
            assert validate_json_content(json_content) is False

    def test_sanitize_input_text(self):
        """Test input sanitization for text"""
        test_cases = [
            ("normal text", "normal text"),
            ("text with spaces", "text with spaces"),
            ("Text_WITH_CAPS", "text_with_caps"),
            ("text-with-dashes", "text-with-dashes"),
            ("text123numbers", "text123numbers"),
            ("Text$With%Special^Chars", "textwithspecialchars"),
            ("  leading and trailing  ", "leading and trailing"),
            ("multiple   spaces", "multiple spaces"),
            ("NEW\nLINE\r\nCARRIAGE", "new line carriage"),
        ]

        for input_text, expected in test_cases:
            assert sanitize_input(input_text) == expected

    def test_sanitize_input_empty(self):
        """Test sanitizing empty input"""
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""
        assert sanitize_input("   ") == ""

    def test_sanitize_input_with_custom_allowed(self):
        """Test sanitization with custom allowed characters"""
        result = sanitize_input("text-with_underscores", allowed="-_")
        assert result == "text-with_underscores"


class TestTemplateUtils:
    """Test template utility functions"""

    def test_render_template_simple(self):
        """Test simple template rendering"""
        template = "Hello {{name}}!"
        context = {"name": "World"}

        result = render_template(template, context)
        assert result == "Hello World!"

    def test_render_template_multiple_vars(self):
        """Test template with multiple variables"""
        template = "{{greeting}}, {{name}}! Today is {{day}}."
        context = {
            "greeting": "Hello",
            "name": "Alice",
            "day": "Monday"
        }

        result = render_template(template, context)
        assert result == "Hello, Alice! Today is Monday."

    def test_render_template_missing_var(self):
        """Test template with missing variable"""
        template = "Hello {{name}}!"
        context = {}  # Missing 'name'

        result = render_template(template, context)
        assert result == "Hello !"  # Variable left empty

    def test_render_template_nested_context(self):
        """Test template with nested context"""
        template = "User: {{user.name}}, Email: {{user.email}}"
        context = {
            "user": {
                "name": "John",
                "email": "john@example.com"
            }
        }

        result = render_template(template, context)
        assert result == "User: John, Email: john@example.com"

    def test_extract_template_variables(self):
        """Test extracting variables from template"""
        template = """
        # {{title}}

        Author: {{author}}
        Date: {{date}}

        Content:
        {{content}}
        """

        variables = extract_template_variables(template)

        expected_vars = {"title", "author", "date", "content"}
        assert set(variables) == expected_vars

    def test_extract_template_variables_duplicates(self):
        """Test extracting variables with duplicates"""
        template = "{{name}} says hello to {{name}}"

        variables = extract_template_variables(template)

        assert variables == ["name"]  # Should deduplicate

    def test_extract_template_variables_none(self):
        """Test extracting variables from template with no variables"""
        template = "This is just plain text with no variables."

        variables = extract_template_variables(template)

        assert variables == []

    def test_validate_template_syntax_valid(self):
        """Test validation of valid template syntax"""
        valid_templates = [
            "Hello {{name}}",
            "{{var1}} and {{var2}}",
            "No variables here",
            "{{nested.value}}",
            "{{array[0]}}",
        ]

        for template in valid_templates:
            assert validate_template_syntax(template) is True

    def test_validate_template_syntax_invalid(self):
        """Test validation of invalid template syntax"""
        invalid_templates = [
            "{{name",           # Missing closing brace
            "{{name}}}",        # Extra closing brace
            "{{{name}}",        # Extra opening brace
            "{{name",           # Unclosed variable
            "name}}",           # Unopened closing
        ]

        for template in invalid_templates:
            assert validate_template_syntax(template) is False

    def test_create_template_context(self):
        """Test creating template context"""
        base_context = {"name": "Alice", "role": "developer"}
        additional = {"project": "SpecPulse", "status": "active"}

        context = create_template_context(base_context, **additional)

        expected = {
            "name": "Alice",
            "role": "developer",
            "project": "SpecPulse",
            "status": "active"
        }
        assert context == expected

    def test_create_template_context_override(self):
        """Test template context with overrides"""
        base_context = {"name": "Alice", "status": "pending"}
        overrides = {"name": "Bob", "project": "New Project"}

        context = create_template_context(base_context, **overrides)

        expected = {
            "name": "Bob",  # Overridden
            "status": "pending",
            "project": "New Project"
        }
        assert context == expected


class TestFormattingUtils:
    """Test formatting utility functions"""

    def test_format_header(self):
        """Test header formatting"""
        result = format_header("Test Header", level=1)
        assert result == "# Test Header"

        result = format_header("Test Header", level=2)
        assert result == "## Test Header"

        result = format_header("Test Header", level=3)
        assert result == "### Test Header"

    def test_format_header_invalid_level(self):
        """Test header formatting with invalid level"""
        with pytest.raises(ValueError):
            format_header("Test", level=0)

        with pytest.raises(ValueError):
            format_header("Test", level=7)

    def test_format_section(self):
        """Test section formatting"""
        title = "Introduction"
        content = "This is the introduction content."

        result = format_section(title, content)

        expected = "## Introduction\n\nThis is the introduction content."
        assert result == expected

    def test_format_section_multiline(self):
        """Test section formatting with multiline content"""
        title = "Steps"
        content = "Step 1\nStep 2\nStep 3"

        result = format_section(title, content)

        expected = "## Steps\n\nStep 1\nStep 2\nStep 3"
        assert result == expected

    def test_format_list_string_items(self):
        """Test formatting list with string items"""
        items = ["Item 1", "Item 2", "Item 3"]

        result = format_list(items)

        expected = "- Item 1\n- Item 2\n- Item 3"
        assert result == expected

    def test_format_list_numbered(self):
        """Test formatting numbered list"""
        items = ["First", "Second", "Third"]

        result = format_list(items, numbered=True)

        expected = "1. First\n2. Second\n3. Third"
        assert result == expected

    def test_format_list_empty(self):
        """Test formatting empty list"""
        result = format_list([])
        assert result == ""

    def test_format_table_simple(self):
        """Test simple table formatting"""
        headers = ["Name", "Age", "City"]
        rows = [
            ["Alice", "25", "New York"],
            ["Bob", "30", "San Francisco"],
        ]

        result = format_table(headers, rows)

        lines = result.split('\n')
        assert "| Name | Age | City |" in lines[0] or "| Name  | Age | City |" in lines[0]
        assert "| ---- | --- | ---- |" in result
        assert "| Alice | 25 | New York |" in result
        assert "| Bob | 30 | San Francisco |" in result

    def test_format_table_empty(self):
        """Test formatting empty table"""
        result = format_table([], [])
        assert result == ""

    def test_format_table_mismatched_columns(self):
        """Test table with mismatched column counts"""
        headers = ["Name", "Age"]
        rows = [
            ["Alice", "25", "Extra"],  # Too many columns
            ["Bob"],  # Too few columns
        ]

        # Should handle gracefully or raise appropriate error
        try:
            result = format_table(headers, rows)
            # If it doesn't raise an error, it should still produce valid markdown
            assert isinstance(result, str)
        except ValueError:
            # Raising an error is also acceptable
            pass

    def test_format_code_block(self):
        """Test code block formatting"""
        code = "print('Hello, World!')"

        result = format_code_block(code, language="python")

        expected = "```python\nprint('Hello, World!')\n```"
        assert result == expected

    def test_format_code_block_no_language(self):
        """Test code block formatting without language"""
        code = "some code here"

        result = format_code_block(code)

        expected = "```\nsome code here\n```"
        assert result == expected

    def test_format_code_block_multiline(self):
        """Test code block formatting with multiline code"""
        code = "def hello():\n    print('Hello, World!')\n    return True"

        result = format_code_block(code, language="python")

        expected = "```python\ndef hello():\n    print('Hello, World!')\n    return True\n```"
        assert result == expected


class TestUtilityEdgeCases:
    """Test edge cases and error handling"""

    def test_unicode_handling(self, temp_dir):
        """Test handling of Unicode content"""
        unicode_content = "测试内容 🚀 العربية"

        # Write and read Unicode content
        test_file = temp_dir / "unicode.txt"
        write_file_safe(test_file, unicode_content)
        read_content = read_file_safe(test_file)

        assert read_content == unicode_content

    def test_large_file_operations(self, temp_dir):
        """Test operations on large files"""
        # Create a large file (1MB)
        large_content = "A" * (1024 * 1024)
        test_file = temp_dir / "large.txt"

        start_time = time.time()
        write_file_safe(test_file, large_content)
        write_time = time.time() - start_time

        start_time = time.time()
        read_content = read_file_safe(test_file)
        read_time = time.time() - start_time

        assert read_content == large_content
        assert write_time < 5.0  # Should complete within 5 seconds
        assert read_time < 5.0   # Should complete within 5 seconds

    def test_concurrent_file_operations(self, temp_dir):
        """Test concurrent file operations"""
        import threading
        import queue

        results = queue.Queue()

        def write_file_worker(filename, content):
            try:
                file_path = temp_dir / filename
                write_file_safe(file_path, content)
                results.put(True)
            except Exception as e:
                results.put(e)

        def read_file_worker(filename):
            try:
                file_path = temp_dir / filename
                content = read_file_safe(file_path)
                results.put(content)
            except Exception as e:
                results.put(e)

        # Create a test file first
        test_file = temp_dir / "concurrent_test.txt"
        test_content = "Test content for concurrent operations"
        write_file_safe(test_file, test_content)

        # Start multiple threads reading the same file
        threads = []
        for i in range(5):
            thread = threading.Thread(
                target=read_file_worker,
                args=("concurrent_test.txt",)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        success_count = 0
        while not results.empty():
            result = results.get()
            if result == test_content:
                success_count += 1

        assert success_count == 5

    def test_memory_error_handling(self, temp_dir):
        """Test handling of memory-related errors"""
        # Try to create a very large filename (should fail gracefully)
        very_long_name = "a" * 1000
        long_path = temp_dir / f"{very_long_name}.txt"

        try:
            write_file_safe(long_path, "content")
            # If it succeeds, that's fine on some filesystems
            assert long_path.exists()
        except (OSError, ValueError) as e:
            # Should fail gracefully with a meaningful error
            assert isinstance(e, (OSError, ValueError))

    def test_permission_handling(self, temp_dir):
        """Test handling of permission-related errors"""
        # Create a file and make it read-only if possible
        test_file = temp_dir / "readonly.txt"
        test_file.write_text("original content")

        try:
            # Try to make file read-only (may not work on all systems)
            test_file.chmod(0o444)

            # Try to write to read-only file (should fail)
            with pytest.raises(PermissionError):
                write_file_safe(test_file, "new content")

        finally:
            # Restore write permissions for cleanup
            try:
                test_file.chmod(0o644)
            except:
                pass  # Ignore cleanup errors


class TestPerformanceBenchmarks:
    """Performance benchmarks for utility functions"""

    def test_performance_file_hash(self, temp_dir):
        """Test performance of file hash calculation"""
        # Create a moderately large file
        content = "Performance test content " * 1000
        test_file = temp_dir / "perf_test.txt"
        test_file.write_text(content)

        start_time = time.time()
        file_hash = get_file_hash(test_file)
        elapsed = time.time() - start_time

        # Should complete within reasonable time
        assert elapsed < 1.0
        assert len(file_hash) == 64

    def test_performance_template_rendering(self):
        """Test performance of template rendering"""
        template = "Hello {{name}}! You have {{count}} new messages in {{category}}."
        context = {
            "name": "Alice",
            "count": 42,
            "category": "inbox"
        }

        iterations = 100
        start_time = time.time()

        for _ in range(iterations):
            result = render_template(template, context)

        elapsed = time.time() - start_time
        avg_time = elapsed / iterations

        # Should be very fast per iteration
        assert avg_time < 0.001  # Less than 1ms per iteration

    def test_performance_validation(self):
        """Test performance of validation functions"""
        test_cases = [
            ("001", "feature_id"),
            ("user-auth", "feature_name"),
            (42, "spec_number"),
            ("Valid content with sufficient length", "content"),
        ]

        iterations = 1000
        start_time = time.time()

        for _ in range(iterations):
            for value, validator_name in test_cases:
                if validator_name == "feature_id":
                    validate_feature_id(value)
                elif validator_name == "feature_name":
                    validate_feature_name(value)
                elif validator_name == "spec_number":
                    validate_spec_number(value)
                elif validator_name == "content":
                    validate_content(value)

        elapsed = time.time() - start_time
        avg_time = elapsed / (iterations * len(test_cases))

        # Should be very fast per validation
        assert avg_time < 0.0001  # Less than 0.1ms per validation


if __name__ == "__main__":
    pytest.main([__file__])