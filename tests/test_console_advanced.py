"""Advanced tests for Console utilities"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import time

from specpulse.utils.console import Console
from specpulse import __version__


class TestConsoleAdvanced(unittest.TestCase):
    """Advanced tests for Console class"""
    
    def setUp(self):
        """Set up test environment"""
        self.console = Console(no_color=True, verbose=True)
        self.console_color = Console(no_color=False, verbose=False)
    
    def test_show_banner(self):
        """Test banner display"""
        # Should not raise errors
        self.console.show_banner(mini=False)
        self.console.show_banner(mini=True)
        
        # With color
        self.console_color.show_banner(mini=False)
        self.console_color.show_banner(mini=True)
    
    def test_header_styles(self):
        """Test header with different styles"""
        self.console.header("Test", style="bright_green")
        self.console.header("Test", style="bright_blue")
        self.console.header("Test", style="bright_yellow")
        self.console.header("Test", style="bright_red")
    
    def test_section(self):
        """Test section display"""
        self.console.section("Test Section")
        self.console_color.section("Test Section")
    
    def test_subsection(self):
        """Test subsection display"""
        self.console.subsection("Test Subsection")
        self.console_color.subsection("Test Subsection")
    
    def test_code_block(self):
        """Test code block display"""
        code = """
def test():
    print("Hello")
"""
        self.console.code_block(code, language="python")
        self.console.code_block(code)  # No language
    
    def test_table(self):
        """Test table display"""
        headers = ["Name", "Value", "Status"]
        rows = [
            ["Test1", "Value1", "OK"],
            ["Test2", "Value2", "FAIL"],
        ]
        
        self.console.table(headers, rows)
        self.console.table(headers, rows, title="Test Table")
        
        # With style
        self.console.table(headers, rows, style="bright_green")
    
    def test_tree(self):
        """Test tree display"""
        data = {
            "root": {
                "child1": {
                    "subchild1": None,
                    "subchild2": None
                },
                "child2": None
            }
        }
        
        self.console.tree(data)
        self.console.tree(data, title="Test Tree")
    
    def test_progress_bar(self):
        """Test progress bar"""
        items = ["item1", "item2", "item3"]
        
        # Mock the track function
        with patch('specpulse.utils.console.track') as mock_track:
            mock_track.return_value = items
            result = list(self.console.progress_bar(items, description="Processing"))
            self.assertEqual(result, items)
    
    def test_spinner(self):
        """Test spinner animation"""
        with patch('time.sleep'):
            self.console.spinner("Loading", duration=0.1)
    
    def test_pulse_animation(self):
        """Test pulse animation"""
        with patch('time.sleep'):
            self.console.pulse_animation("Testing", duration=0.1)
    
    def test_celebration(self):
        """Test celebration animation"""
        with patch('time.sleep'):
            self.console.celebration()
    
    def test_confirm_variations(self):
        """Test confirm with different inputs"""
        test_cases = [
            ('y', True),
            ('Y', True),
            ('yes', True),
            ('YES', True),
            ('n', False),
            ('N', False),
            ('no', False),
            ('NO', False),
            ('', True),  # Default true
            ('maybe', False),  # Invalid = false
        ]
        
        for input_val, expected in test_cases:
            with patch('builtins.input', return_value=input_val):
                result = self.console.confirm("Test?", default=True)
                self.assertEqual(result, expected, f"Failed for input: {input_val}")
    
    def test_prompt_with_choices(self):
        """Test prompt with choice validation"""
        with patch('builtins.input', side_effect=['invalid', 'a']):
            result = self.console.prompt("Choose", choices=['a', 'b', 'c'])
            self.assertEqual(result, 'a')
    
    def test_format_success(self):
        """Test success message formatting"""
        msg = self.console.format_success("Test")
        self.assertIn("Test", msg)
    
    def test_format_error(self):
        """Test error message formatting"""
        msg = self.console.format_error("Test")
        self.assertIn("Test", msg)
    
    def test_format_warning(self):
        """Test warning message formatting"""
        msg = self.console.format_warning("Test")
        self.assertIn("Test", msg)
    
    def test_format_info(self):
        """Test info message formatting"""
        msg = self.console.format_info("Test")
        self.assertIn("Test", msg)
    
    def test_divider(self):
        """Test divider display"""
        self.console.divider()
        self.console.divider(char="=")
        self.console.divider(width=50)
        self.console.divider(style="bright_blue")
    
    def test_json_display(self):
        """Test JSON display"""
        data = {
            "key1": "value1",
            "key2": {
                "nested": "value"
            },
            "key3": [1, 2, 3]
        }
        
        self.console.json(data)
        self.console.json(data, indent=4)
    
    def test_columns(self):
        """Test columns display"""
        items = ["Item1", "Item2", "Item3", "Item4"]
        self.console.columns(items)
        self.console.columns(items, columns=2)
    
    def test_verbose_mode(self):
        """Test verbose mode output"""
        console_verbose = Console(verbose=True)
        console_verbose.debug("Debug message")
        
        console_normal = Console(verbose=False)
        console_normal.debug("Should not appear")
    
    def test_clear(self):
        """Test screen clear"""
        with patch('os.system') as mock_system:
            self.console.clear()
            mock_system.assert_called()
    
    def test_mini_banner_version(self):
        """Test mini banner shows correct version"""
        with patch('sys.stdout.write'):
            self.console.show_banner(mini=True)
            # Version should be formatted correctly
            # The banner template uses __version__
    
    def test_panel(self):
        """Test panel display"""
        self.console.panel("Test content")
        self.console.panel("Test content", title="Test Panel")
        self.console.panel("Test content", subtitle="Subtitle")
        self.console.panel("Test content", style="bright_green")
    
    def test_rule(self):
        """Test rule display"""
        self.console.rule()
        self.console.rule("Title")
        self.console.rule("Title", style="bright_blue")
    
    def test_status(self):
        """Test status context manager"""
        with self.console.status("Processing..."):
            time.sleep(0.01)  # Simulate work
    
    def test_print_exception(self):
        """Test exception printing"""
        try:
            raise ValueError("Test error")
        except ValueError:
            self.console.print_exception()


if __name__ == '__main__':
    unittest.main()