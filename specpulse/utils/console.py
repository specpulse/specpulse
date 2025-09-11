"""
Console utilities for SpecPulse with beautiful visual elements
"""

import sys
import time
import random
from typing import Optional, List, Dict, Any
from .. import __version__
from rich.console import Console as RichConsole
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich import box
from rich.style import Style


class Console:
    """Enhanced console output with Rich library for beautiful visuals"""
    
    # ASCII Art Banner
    BANNER = r"""
+=====================================================================+
|                                                                     |
|    _____ ____  _____ _____ ____  _   _ _     _____ _____           |
|   / ____|  _ \|  ___/ ____|  _ \| | | | |   / ____|  ___|          |
|   | (___ | |_) | |__ | |    | |_) | | | | |   | (___ | |__          |
|   \___ \|  __/|  __|| |    |  __/| | | | |    \___ \|  __|         |
|   ____) | |   | |___| |____| |   | |_| | |________) | |___         |
|   |_____/|_|   |______\_____|_|    \___/|______|_____/|_____|       |
|                                                                     |
|          Specification-Driven Development Framework                |
|                    Beyond Traditional Development                   |
|                                                                     |
+=====================================================================+
"""

    MINI_BANNER_TEMPLATE = """
+---------------------------------------+
|  SPECPULSE v{version:<23} |
|  Specification-Driven Development     |
|  Framework Ready                      |
+---------------------------------------+
"""

    # Animated frames for loading
    LOADING_FRAMES = ["|", "/", "-", "\\"]
    PULSE_FRAMES = ["o", "O", "0", "O"]
    ROCKET_FRAMES = [">>", ">>>", ">>>>", ">>>>>", "  >>>>>", "    >>>>>"]
    
    def __init__(self, no_color: bool = False, verbose: bool = False):
        self.console = RichConsole(force_terminal=not no_color)
        self.no_color = no_color
        self.verbose = verbose
    
    def show_banner(self, mini: bool = False):
        """Display ASCII art banner"""
        if mini:
            banner = self.MINI_BANNER_TEMPLATE.format(version=__version__)
        else:
            banner = self.BANNER
        gradient_colors = ["bright_blue", "bright_cyan", "bright_white"]
        
        lines = banner.strip().split('\n')
        for i, line in enumerate(lines):
            color = gradient_colors[i % len(gradient_colors)]
            self.console.print(line, style=color, justify="center")
        
        if not mini:
            self.console.print()
    
    def info(self, message: str, icon: str = "[i]"):
        """Print info message with icon"""
        self.console.print(f"{icon}  [bright_blue]{message}[/bright_blue]")
    
    def success(self, message: str, icon: str = "[OK]"):
        """Print success message with checkmark"""
        self.console.print(f"{icon}  [bright_green]{message}[/bright_green]")
    
    def warning(self, message: str, icon: str = "[!]"):
        """Print warning message"""
        self.console.print(f"{icon}  [yellow]{message}[/yellow]")
    
    def error(self, message: str, icon: str = "[X]"):
        """Print error message"""
        self.console.print(f"{icon}  [bright_red]{message}[/bright_red]")
    
    def header(self, message: str, style: str = "bright_cyan"):
        """Print a beautiful header"""
        panel = Panel(
            Text(message, justify="center", style="bold"),
            box=box.DOUBLE_EDGE,
            style=style,
            padding=(1, 2)
        )
        self.console.print()
        self.console.print(panel)
        self.console.print()
    
    def section(self, title: str, content: str = None):
        """Print a section with title"""
        self.console.print()
        self.console.rule(f"[bold bright_cyan]{title}[/bold bright_cyan]")
        if content:
            self.console.print(content)
        self.console.print()
    
    def progress_bar(self, description: str, total: int):
        """Create a beautiful progress bar"""
        # Simplified for Windows compatibility
        self.console.print(f"[bold blue]{description}[/bold blue]")
        # Return a dummy object that can be used as context manager
        class DummyProgress:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def add_task(self, *args, **kwargs):
                return 0
            def update(self, *args, **kwargs):
                pass
        return DummyProgress()
    
    def spinner(self, message: str):
        """Show a loading spinner"""
        # Simplified version for Windows compatibility
        self.console.print(f"[bold cyan]{message}...[/bold cyan]")
        return None
    
    def animated_text(self, text: str, delay: float = 0.03):
        """Print text with typewriter effect"""
        for char in text:
            self.console.print(char, end="")
            time.sleep(delay)
        self.console.print()
    
    def prompt(self, message: str, default: Optional[str] = None) -> str:
        """Beautiful prompt for user input"""
        return Prompt.ask(
            f"[bold bright_cyan]{message}[/bold bright_cyan]",
            default=default,
            console=self.console
        )
    
    def confirm(self, message: str, default: bool = False) -> bool:
        """Beautiful confirmation prompt"""
        return Confirm.ask(
            f"[bold yellow]{message}[/bold yellow]",
            default=default,
            console=self.console
        )
    
    def table(self, title: str, headers: List[str], rows: List[List[Any]], 
              box_style=box.ROUNDED, show_footer: bool = False):
        """Create a beautiful table"""
        table = Table(
            title=title,
            box=box_style,
            show_header=True,
            header_style="bold magenta",
            show_footer=show_footer
        )
        
        # Add columns
        for header in headers:
            table.add_column(header, style="cyan", no_wrap=True)
        
        # Add rows with alternating colors
        for i, row in enumerate(rows):
            style = "white" if i % 2 == 0 else "bright_white"
            table.add_row(*[str(cell) for cell in row], style=style)
        
        self.console.print(table)
    
    def tree(self, title: str, items: Dict[str, Any]):
        """Create a beautiful tree structure"""
        tree = Tree(f"[bold bright_green]{title}[/bold bright_green]")
        self._build_tree(tree, items)
        self.console.print(tree)
    
    def _build_tree(self, tree: Tree, items: Dict[str, Any]):
        """Recursively build tree structure"""
        for key, value in items.items():
            if isinstance(value, dict):
                branch = tree.add(f"[bright_yellow]{key}[/bright_yellow]")
                self._build_tree(branch, value)
            elif isinstance(value, list):
                branch = tree.add(f"[bright_cyan]{key}[/bright_cyan]")
                for item in value:
                    branch.add(f"[white]{item}[/white]")
            else:
                tree.add(f"[bright_blue]{key}[/bright_blue]: [white]{value}[/white]")
    
    def code_block(self, code: str, language: str = "python", theme: str = "monokai"):
        """Display syntax-highlighted code"""
        syntax = Syntax(code, language, theme=theme, line_numbers=True)
        panel = Panel(syntax, title=f"[bold]{language.upper()} Code[/bold]", 
                     border_style="bright_green", box=box.ROUNDED)
        self.console.print(panel)
    
    def status_panel(self, title: str, items: List[tuple]):
        """Create a status panel with items"""
        content = "\n".join([f"[bold]{k}:[/bold] {v}" for k, v in items])
        panel = Panel(
            content,
            title=f"[bold bright_white]{title}[/bold bright_white]",
            border_style="bright_blue",
            box=box.DOUBLE
        )
        self.console.print(panel)
    
    def validation_results(self, results: Dict[str, bool]):
        """Display validation results with visual indicators"""
        self.console.print()
        self.console.rule("[bold]Validation Results[/bold]", style="bright_cyan")
        self.console.print()
        
        all_passed = all(results.values())
        
        for component, passed in results.items():
            if passed:
                self.console.print(f"  [OK] {component}: [bright_green]PASSED[/bright_green]")
            else:
                self.console.print(f"  [X] {component}: [bright_red]FAILED[/bright_red]")
        
        self.console.print()
        if all_passed:
            self.console.print(
                Panel(
                    "[bold bright_green]All validations passed! Ready for implementation.[/bold bright_green]",
                    border_style="bright_green",
                    box=box.DOUBLE
                )
            )
        else:
            self.console.print(
                Panel(
                    "[bold bright_red]Some validations failed. Please fix issues before proceeding.[/bold bright_red]",
                    border_style="bright_red",
                    box=box.DOUBLE
                )
            )
    
    def feature_showcase(self, features: List[Dict[str, str]]):
        """Display features in a beautiful grid"""
        panels = []
        colors = ["bright_blue", "bright_green", "bright_yellow", "bright_magenta", "bright_cyan"]
        
        for i, feature in enumerate(features):
            color = colors[i % len(colors)]
            panel = Panel(
                f"[{color}]{feature['description']}[/{color}]",
                title=f"[bold]{feature['name']}[/bold]",
                border_style=color,
                box=box.ROUNDED,
                padding=(1, 2)
            )
            panels.append(panel)
        
        # Display in columns
        self.console.print(Columns(panels, padding=(1, 2), expand=False))
    
    def animated_success(self, message: str):
        """Show animated success message"""
        frames = ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[====]", "[DONE]"]
        
        with Live(console=self.console, refresh_per_second=4) as live:
            for frame in frames:
                live.update(f"[bright_green]{frame}[/bright_green] {message}")
                time.sleep(0.2)
        
        self.success(f"{message} - Complete!")
    
    def pulse_animation(self, message: str, duration: float = 2.0):
        """Show pulsing animation"""
        start_time = time.time()
        
        with Live(console=self.console, refresh_per_second=10) as live:
            while time.time() - start_time < duration:
                for frame in self.PULSE_FRAMES:
                    live.update(f"[bright_cyan]{frame}[/bright_cyan]  {message}")
                    time.sleep(0.1)
    
    def rocket_launch(self, message: str = "Launching SpecPulse"):
        """Show rocket launch animation"""
        for frame in self.ROCKET_FRAMES:
            self.console.print(f"\r{frame} {message}", end="")
            time.sleep(0.1)
        self.console.print("\r" + " " * 50 + "\r", end="")
        self.success(f"{message} - Launched!")
    
    def divider(self, char: str = "─", style: str = "bright_blue"):
        """Print a divider line"""
        width = self.console.width
        self.console.print(char * width, style=style)
    
    def gradient_text(self, text: str, colors: List[str] = None):
        """Print text with gradient colors"""
        if not colors:
            colors = ["bright_red", "bright_yellow", "bright_green", 
                     "bright_cyan", "bright_blue", "bright_magenta"]
        
        words = text.split()
        colored_words = []
        
        for i, word in enumerate(words):
            color = colors[i % len(colors)]
            colored_words.append(f"[{color}]{word}[/{color}]")
        
        self.console.print(" ".join(colored_words))
    
    def celebration(self):
        """Show celebration animation"""
        symbols = ["*", "+", "o", "O", "@", "#", "!", "~"]
        
        for _ in range(3):
            line = " ".join(random.choices(symbols, k=20))
            self.console.print(line, justify="center", style="bright_yellow")
            time.sleep(0.2)
        
        self.console.print()
        self.gradient_text("Congratulations! Project successfully initialized!", 
                          ["bright_yellow", "bright_green"])
        self.console.print()