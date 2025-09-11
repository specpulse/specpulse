"""
Comprehensive test suite for SpecPulse Console module.
Tests all console functionality with proper Rich library mocking.
"""

import pytest
import unittest
from unittest.mock import patch, MagicMock, call
import time
from typing import List, Dict, Any

from specpulse.utils.console import Console


class TestConsole(unittest.TestCase):
    """Comprehensive tests for Console class"""

    def setUp(self):
        """Set up test environment"""
        # Create console with no_color=True for testing
        self.console = Console(no_color=True, verbose=False)
        
    def test_init_with_defaults(self):
        """Test Console initialization with default parameters"""
        console = Console()
        self.assertFalse(console.no_color)
        self.assertFalse(console.verbose)

    def test_init_with_custom_params(self):
        """Test Console initialization with custom parameters"""
        console = Console(no_color=True, verbose=True)
        self.assertTrue(console.no_color)
        self.assertTrue(console.verbose)

    @patch('specpulse.utils.console.RichConsole')
    def test_init_force_terminal_setting(self, mock_rich_console):
        """Test that force_terminal is set based on no_color parameter"""
        # Test with no_color=False
        Console(no_color=False)
        mock_rich_console.assert_called_with(force_terminal=True)
        
        mock_rich_console.reset_mock()
        
        # Test with no_color=True
        Console(no_color=True)
        mock_rich_console.assert_called_with(force_terminal=False)

    def test_banner_constants(self):
        """Test banner constants are properly defined"""
        self.assertIsInstance(Console.BANNER, str)
        self.assertIsInstance(Console.MINI_BANNER_TEMPLATE, str)
        self.assertIn("SPECPULSE", Console.BANNER)
        self.assertIn("version", Console.MINI_BANNER_TEMPLATE)

    def test_animation_frame_constants(self):
        """Test animation frame constants"""
        self.assertIsInstance(Console.LOADING_FRAMES, list)
        self.assertIsInstance(Console.PULSE_FRAMES, list)
        self.assertIsInstance(Console.ROCKET_FRAMES, list)
        self.assertTrue(len(Console.LOADING_FRAMES) > 0)
        self.assertTrue(len(Console.PULSE_FRAMES) > 0)
        self.assertTrue(len(Console.ROCKET_FRAMES) > 0)

    @patch('specpulse.utils.console.__version__', '1.0.0')
    def test_show_banner_full(self):
        """Test showing full banner"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.show_banner(mini=False)
            
            # Should print multiple lines of the banner
            self.assertTrue(mock_print.call_count > 5)

    @patch('specpulse.utils.console.__version__', '1.0.0')
    def test_show_banner_mini(self):
        """Test showing mini banner"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.show_banner(mini=True)
            
            # Should print the mini banner
            mock_print.assert_called()
            # Check that version is included
            banner_call = mock_print.call_args_list[0]
            self.assertIn("1.0.0", str(banner_call))

    def test_info_message(self):
        """Test info message printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.info("Test info message")
            
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Test info message", call_args)
            self.assertIn("[i]", call_args)

    def test_info_message_custom_icon(self):
        """Test info message with custom icon"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.info("Test message", icon="[INFO]")
            
            call_args = mock_print.call_args[0][0]
            self.assertIn("Test message", call_args)
            self.assertIn("[INFO]", call_args)

    def test_success_message(self):
        """Test success message printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.success("Test success message")
            
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Test success message", call_args)
            self.assertIn("[OK]", call_args)

    def test_warning_message(self):
        """Test warning message printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.warning("Test warning message")
            
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Test warning message", call_args)
            self.assertIn("[!]", call_args)

    def test_error_message(self):
        """Test error message printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.error("Test error message")
            
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Test error message", call_args)
            self.assertIn("[X]", call_args)

    @patch('specpulse.utils.console.Panel')
    def test_header(self, mock_panel):
        """Test header printing"""
        mock_panel_instance = MagicMock()
        mock_panel.return_value = mock_panel_instance
        
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.header("Test Header", style="bright_cyan")
            
            # Should create panel and print it
            mock_panel.assert_called_once()
            self.assertEqual(mock_print.call_count, 3)  # Two empty prints + panel

    @patch('specpulse.utils.console.Panel')
    def test_header_default_style(self, mock_panel):
        """Test header with default style"""
        with patch.object(self.console.console, 'print'):
            self.console.header("Test Header")
            
            # Check that default style is used
            panel_kwargs = mock_panel.call_args[1]
            self.assertEqual(panel_kwargs['style'], 'bright_cyan')

    def test_section(self):
        """Test section printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            with patch.object(self.console.console, 'rule') as mock_rule:
                self.console.section("Test Section", "Test content")
                
                mock_rule.assert_called_once()
                # Should print empty lines and content
                self.assertTrue(mock_print.call_count >= 3)

    def test_section_no_content(self):
        """Test section printing without content"""
        with patch.object(self.console.console, 'print') as mock_print:
            with patch.object(self.console.console, 'rule') as mock_rule:
                self.console.section("Test Section")
                
                mock_rule.assert_called_once_with("[bold bright_cyan]Test Section[/bold bright_cyan]")
                # Should print empty lines only
                self.assertTrue(mock_print.call_count >= 2)

    def test_progress_bar(self):
        """Test progress bar creation"""
        with patch.object(self.console.console, 'print') as mock_print:
            progress = self.console.progress_bar("Processing", 10)
            
            # Should print description
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Processing", call_args)
            
            # Should return context manager
            self.assertIsNotNone(progress)
            
            # Test context manager usage
            with progress as p:
                task = p.add_task("test", total=10)
                self.assertEqual(task, 0)
                p.update(task, advance=1)  # Should not raise exception

    def test_spinner(self):
        """Test spinner display"""
        with patch.object(self.console.console, 'print') as mock_print:
            result = self.console.spinner("Loading")
            
            # Should print loading message
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Loading", call_args)
            
            # Should return None for simplified version
            self.assertIsNone(result)

    @patch('specpulse.utils.console.time.sleep')
    def test_animated_text(self, mock_sleep):
        """Test animated text printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.animated_text("Hello", delay=0.01)
            
            # Should print each character
            self.assertEqual(mock_print.call_count, 6)  # 5 chars + final newline
            
            # Should call sleep for each character
            self.assertEqual(mock_sleep.call_count, 5)

    @patch('specpulse.utils.console.Prompt.ask')
    def test_prompt(self, mock_ask):
        """Test user input prompt"""
        mock_ask.return_value = "user input"
        
        result = self.console.prompt("Enter something", default="default")
        
        self.assertEqual(result, "user input")
        mock_ask.assert_called_once_with(
            "[bold bright_cyan]Enter something[/bold bright_cyan]",
            default="default",
            console=self.console.console
        )

    @patch('specpulse.utils.console.Confirm.ask')
    def test_confirm(self, mock_ask):
        """Test confirmation prompt"""
        mock_ask.return_value = True
        
        result = self.console.confirm("Are you sure?", default=False)
        
        self.assertTrue(result)
        mock_ask.assert_called_once_with(
            "[bold yellow]Are you sure?[/bold yellow]",
            default=False,
            console=self.console.console
        )

    @patch('specpulse.utils.console.Table')
    def test_table(self, mock_table_class):
        """Test table creation and display"""
        mock_table = MagicMock()
        mock_table_class.return_value = mock_table
        
        headers = ["Col1", "Col2", "Col3"]
        rows = [
            ["Row1Col1", "Row1Col2", "Row1Col3"],
            ["Row2Col1", "Row2Col2", "Row2Col3"]
        ]
        
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.table("Test Table", headers, rows)
            
            # Should create table with proper parameters
            mock_table_class.assert_called_once()
            table_kwargs = mock_table_class.call_args[1]
            self.assertEqual(table_kwargs['title'], "Test Table")
            
            # Should add columns
            self.assertEqual(mock_table.add_column.call_count, 3)
            
            # Should add rows
            self.assertEqual(mock_table.add_row.call_count, 2)
            
            # Should print table
            mock_print.assert_called_once_with(mock_table)

    @patch('specpulse.utils.console.Table')
    def test_table_with_custom_options(self, mock_table_class):
        """Test table with custom styling options"""
        mock_table = MagicMock()
        mock_table_class.return_value = mock_table
        
        from rich import box
        
        with patch.object(self.console.console, 'print'):
            self.console.table("Test", ["Col1"], [["Data"]], box_style=box.DOUBLE, show_footer=True)
            
            table_kwargs = mock_table_class.call_args[1]
            self.assertEqual(table_kwargs['box'], box.DOUBLE)
            self.assertTrue(table_kwargs['show_footer'])

    @patch('specpulse.utils.console.Tree')
    def test_tree(self, mock_tree_class):
        """Test tree structure creation"""
        mock_tree = MagicMock()
        mock_tree_class.return_value = mock_tree
        
        tree_items = {
            "root": {
                "child1": "value1",
                "child2": ["item1", "item2"],
                "child3": {
                    "grandchild": "nested_value"
                }
            }
        }
        
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.tree("Test Tree", tree_items)
            
            mock_tree_class.assert_called_once_with("[bold bright_green]Test Tree[/bold bright_green]")
            mock_print.assert_called_once_with(mock_tree)

    def test_build_tree_recursive(self):
        """Test _build_tree method with nested structures"""
        from rich.tree import Tree
        tree = Tree("Root")
        
        items = {
            "string_value": "test",
            "list_value": ["item1", "item2"],
            "dict_value": {
                "nested_string": "nested_test",
                "nested_list": ["nested1", "nested2"]
            }
        }
        
        self.console._build_tree(tree, items)
        
        # Should add items to tree (testing that no exceptions are raised)
        # The actual tree structure testing would require more complex mocking

    @patch('specpulse.utils.console.Syntax')
    @patch('specpulse.utils.console.Panel')
    def test_code_block(self, mock_panel, mock_syntax):
        """Test code block display"""
        mock_syntax_instance = MagicMock()
        mock_syntax.return_value = mock_syntax_instance
        mock_panel_instance = MagicMock()
        mock_panel.return_value = mock_panel_instance
        
        code = "print('Hello, World!')"
        
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.code_block(code, language="python", theme="monokai")
            
            mock_syntax.assert_called_once_with(code, "python", theme="monokai", line_numbers=True)
            mock_panel.assert_called_once()
            mock_print.assert_called_once_with(mock_panel_instance)

    @patch('specpulse.utils.console.Panel')
    def test_status_panel(self, mock_panel):
        """Test status panel creation"""
        mock_panel_instance = MagicMock()
        mock_panel.return_value = mock_panel_instance
        
        items = [("Status", "OK"), ("Count", "5"), ("Error", "None")]
        
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.status_panel("Test Status", items)
            
            mock_panel.assert_called_once()
            mock_print.assert_called_once_with(mock_panel_instance)

    def test_validation_results_all_passed(self):
        """Test validation results display when all pass"""
        results = {
            "Component 1": True,
            "Component 2": True,
            "Component 3": True
        }
        
        with patch.object(self.console.console, 'print') as mock_print:
            with patch.object(self.console.console, 'rule') as mock_rule:
                self.console.validation_results(results)
                
                # Should print rule, results, and success panel
                mock_rule.assert_called_once()
                # Check that all components show PASSED
                print_calls = [str(call) for call in mock_print.call_args_list]
                passed_calls = [call for call in print_calls if "PASSED" in call]
                self.assertEqual(len(passed_calls), 3)

    def test_validation_results_some_failed(self):
        """Test validation results display when some fail"""
        results = {
            "Component 1": True,
            "Component 2": False,
            "Component 3": True
        }
        
        with patch.object(self.console.console, 'print') as mock_print:
            with patch.object(self.console.console, 'rule') as mock_rule:
                self.console.validation_results(results)
                
                # Should show mixed results
                print_calls = [str(call) for call in mock_print.call_args_list]
                passed_calls = [call for call in print_calls if "PASSED" in call]
                failed_calls = [call for call in print_calls if "FAILED" in call]
                
                self.assertEqual(len(passed_calls), 2)
                self.assertEqual(len(failed_calls), 1)

    @patch('specpulse.utils.console.Panel')
    @patch('specpulse.utils.console.Columns')
    def test_feature_showcase(self, mock_columns, mock_panel):
        """Test feature showcase display"""
        mock_panels = [MagicMock() for _ in range(3)]
        mock_panel.side_effect = mock_panels
        mock_columns_instance = MagicMock()
        mock_columns.return_value = mock_columns_instance
        
        features = [
            {"name": "Feature 1", "description": "Description 1"},
            {"name": "Feature 2", "description": "Description 2"},
            {"name": "Feature 3", "description": "Description 3"}
        ]
        
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.feature_showcase(features)
            
            # Should create panels for each feature
            self.assertEqual(mock_panel.call_count, 3)
            
            # Should create columns
            mock_columns.assert_called_once_with(mock_panels, padding=(1, 2), expand=False)
            
            # Should print columns
            mock_print.assert_called_once_with(mock_columns_instance)

    @patch('specpulse.utils.console.Live')
    @patch('specpulse.utils.console.time.sleep')
    def test_animated_success(self, mock_sleep, mock_live):
        """Test animated success message"""
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        with patch.object(self.console, 'success') as mock_success:
            self.console.animated_success("Test completed")
            
            # Should use Live context manager
            mock_live.assert_called_once()
            
            # Should call update multiple times for animation
            self.assertTrue(mock_live_instance.update.call_count >= 6)
            
            # Should call success at the end
            mock_success.assert_called_once_with("Test completed - Complete!")

    @patch('specpulse.utils.console.Live')
    @patch('specpulse.utils.console.time.time')
    @patch('specpulse.utils.console.time.sleep')
    def test_pulse_animation(self, mock_sleep, mock_time, mock_live):
        """Test pulse animation"""
        # Mock time to control duration
        mock_time.side_effect = [0, 0.5, 1.0, 1.5, 2.1]  # Exceeds duration after 4th call
        
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        self.console.pulse_animation("Processing", duration=2.0)
        
        mock_live.assert_called_once()
        # Should update with pulse frames
        self.assertTrue(mock_live_instance.update.call_count > 0)

    @patch('specpulse.utils.console.time.sleep')
    def test_rocket_launch(self, mock_sleep):
        """Test rocket launch animation"""
        with patch.object(self.console.console, 'print') as mock_print:
            with patch.object(self.console, 'success') as mock_success:
                self.console.rocket_launch("Test launch")
                
                # Should print rocket frames
                self.assertTrue(mock_print.call_count >= len(Console.ROCKET_FRAMES))
                
                # Should call success at the end
                mock_success.assert_called_once_with("Test launch - Launched!")
                
                # Should sleep between frames
                self.assertTrue(mock_sleep.call_count >= len(Console.ROCKET_FRAMES))

    def test_divider(self):
        """Test divider line printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            # Mock console width
            self.console.console.width = 80
            
            self.console.divider()
            
            mock_print.assert_called_once()
            call_args = mock_print.call_args
            self.assertIn("─" * 80, call_args[0])

    def test_divider_custom_char(self):
        """Test divider with custom character and style"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.console.width = 50
            
            self.console.divider(char="*", style="red")
            
            call_args = mock_print.call_args
            self.assertIn("*" * 50, call_args[0])
            self.assertEqual(call_args[1]['style'], "red")

    def test_gradient_text(self):
        """Test gradient text printing"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.gradient_text("Hello world test")
            
            mock_print.assert_called_once()
            # Should color each word differently
            call_args = mock_print.call_args[0][0]
            self.assertIn("[", call_args)  # Should contain color tags
            self.assertIn("]", call_args)

    def test_gradient_text_custom_colors(self):
        """Test gradient text with custom colors"""
        with patch.object(self.console.console, 'print') as mock_print:
            custom_colors = ["red", "green", "blue"]
            self.console.gradient_text("one two three four", colors=custom_colors)
            
            call_args = mock_print.call_args[0][0]
            self.assertIn("[red]", call_args)
            self.assertIn("[green]", call_args)
            self.assertIn("[blue]", call_args)

    @patch('specpulse.utils.console.random.choices')
    @patch('specpulse.utils.console.time.sleep')
    def test_celebration(self, mock_sleep, mock_choices):
        """Test celebration animation"""
        mock_choices.return_value = ["*"] * 20
        
        with patch.object(self.console.console, 'print') as mock_print:
            with patch.object(self.console, 'gradient_text') as mock_gradient:
                self.console.celebration()
                
                # Should print celebration lines
                self.assertTrue(mock_print.call_count >= 3)
                
                # Should call gradient_text for congratulations
                mock_gradient.assert_called_once()
                
                # Should sleep between lines
                self.assertTrue(mock_sleep.call_count >= 3)

    def test_console_width_property(self):
        """Test console width property access"""
        # Mock width property
        self.console.console.width = 120
        
        with patch.object(self.console.console, 'print'):
            self.console.divider()
            
        # Should access width property without error
        self.assertEqual(self.console.console.width, 120)


if __name__ == '__main__':
    unittest.main()