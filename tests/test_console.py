"""
Tests for Console utility
"""

import pytest
from unittest.mock import patch, MagicMock
from rich.table import Table
from rich.tree import Tree

from specpulse.utils.console import Console


class TestConsole:
    """Test Console functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.console = Console(no_color=True, verbose=False)

    def test_initialization(self):
        """Test Console initialization"""
        console = Console(no_color=False, verbose=True)
        assert console.console is not None
        assert console.verbose is True

    def test_show_banner(self):
        """Test banner display"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.show_banner()
            mock_print.assert_called()

    def test_show_banner_mini(self):
        """Test mini banner display"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.show_banner(mini=True)
            mock_print.assert_called()

    @patch('rich.console.Console.print')
    def test_info(self, mock_print):
        """Test info message"""
        self.console.info("Test info")
        mock_print.assert_called_once()

    @patch('rich.console.Console.print')
    def test_success(self, mock_print):
        """Test success message"""
        self.console.success("Test success")
        mock_print.assert_called_once()

    @patch('rich.console.Console.print')
    def test_warning(self, mock_print):
        """Test warning message"""
        self.console.warning("Test warning")
        mock_print.assert_called_once()

    @patch('rich.console.Console.print')
    def test_error(self, mock_print):
        """Test error message"""
        self.console.error("Test error")
        mock_print.assert_called_once()

    @patch('rich.console.Console.print')
    def test_header(self, mock_print):
        """Test header display"""
        self.console.header("Test Header")
        mock_print.assert_called_once()

    @patch('rich.console.Console.print')
    def test_section(self, mock_print):
        """Test section display"""
        self.console.section("Section Title", "Section content")
        assert mock_print.called

    @patch('rich.console.Console.print')
    def test_section_without_content(self, mock_print):
        """Test section without content"""
        self.console.section("Section Title")
        assert mock_print.called

    def test_progress_bar(self):
        """Test progress bar creation"""
        progress = self.console.progress_bar("Test", 100)
        assert progress is not None
        assert hasattr(progress, '__enter__')
        assert hasattr(progress, '__exit__')

    @patch('rich.console.Console.status')
    def test_spinner(self, mock_status):
        """Test spinner creation"""
        mock_context = MagicMock()
        mock_status.return_value = mock_context

        spinner = self.console.spinner("Loading")
        assert spinner is not None

    @patch('rich.console.Console.print')
    def test_animated_text(self, mock_print):
        """Test animated text"""
        self.console.animated_text("Test", delay=0.001)
        assert mock_print.called

    @patch('rich.prompt.Prompt.ask')
    def test_prompt(self, mock_ask):
        """Test prompt"""
        mock_ask.return_value = "answer"

        result = self.console.prompt("Question")
        assert result == "answer"
        mock_ask.assert_called_once()

    @patch('rich.prompt.Confirm.ask')
    def test_confirm(self, mock_ask):
        """Test confirm"""
        mock_ask.return_value = True

        result = self.console.confirm("Confirm?")
        assert result is True
        mock_ask.assert_called_once()

    @patch('rich.console.Console.print')
    def test_table(self, mock_print):
        """Test table display"""
        headers = ["Col1", "Col2"]
        rows = [["A", "B"], ["C", "D"]]

        self.console.table("Test Table", headers, rows)
        mock_print.assert_called_once()

        # Verify a Table object was created
        call_args = mock_print.call_args[0]
        assert isinstance(call_args[0], Table)

    @patch('rich.console.Console.print')
    def test_tree(self, mock_print):
        """Test tree display"""
        items = {"root": {"child1": None, "child2": {"grandchild": None}}}

        self.console.tree("Test Tree", items)
        mock_print.assert_called_once()

        # Verify a Tree object was created
        call_args = mock_print.call_args[0]
        assert isinstance(call_args[0], Tree)

    @patch('rich.console.Console.print')
    def test_code_block(self, mock_print):
        """Test code block display"""
        code = "print('Hello World')"

        self.console.code_block(code, language="python")
        mock_print.assert_called_once()

    @patch('rich.console.Console.print')
    def test_divider(self, mock_print):
        """Test divider display"""
        self.console.divider()
        mock_print.assert_called_once()

    @patch('rich.console.Console.print')
    def test_divider_custom(self, mock_print):
        """Test custom divider"""
        self.console.divider(char="=", style="red")
        mock_print.assert_called_once()

    def test_pulse_animation(self):
        """Test pulse animation"""
        # Just ensure it doesn't raise an exception
        self.console.pulse_animation(duration=0.01, message="Test")

    def test_type_effect(self):
        """Test type effect"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.type_effect("Test", delay=0.001)
            assert mock_print.called

    def test_verbose_mode(self):
        """Test verbose mode output"""
        console = Console(no_color=True, verbose=True)

        with patch.object(console.console, 'print') as mock_print:
            console.info("Verbose info")
            mock_print.assert_called()

    def test_no_color_mode(self):
        """Test no color mode"""
        console = Console(no_color=True, verbose=False)
        assert console.console is not None

    def test_gradient_text(self):
        """Test gradient text display"""
        with patch.object(self.console.console, 'print') as mock_print:
            self.console.gradient_text("Gradient")
            mock_print.assert_called()