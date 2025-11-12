"""
Status Display Module

This module provides the StatusDisplay class for formatting and displaying
task status and progress information using the Rich library.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime

try:
    from rich.console import Console
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .models import TaskInfo, ProgressData, TaskHistory, TaskState


class StatusDisplay:
    """Handles terminal display formatting for task monitoring."""

    def __init__(self, no_color: bool = False):
        """Initialize display with color preference."""
        self.no_color = no_color
        if RICH_AVAILABLE:
            self.console = Console(no_color=no_color, width=None if no_color else 100)
        else:
            self.console = None

    def show_status(self, progress: ProgressData, tasks: List[TaskInfo], verbose_mode: bool = False) -> str:
        """Display current task status with progress indicators."""
        if RICH_AVAILABLE:
            return self._rich_status_display(progress, tasks, verbose_mode)
        else:
            return self._plain_status_display(progress, tasks, verbose_mode)

    def _rich_status_display(self, progress: ProgressData, tasks: List[TaskInfo], verbose_mode: bool = False) -> str:
        """Create Rich-based status display."""
        output_lines = []

        # Header
        if progress.feature_id:
            title = f"Task Monitor Status - Feature {progress.feature_id}"
        else:
            title = "Task Monitor Status"

        header = Panel(
            Text(title, style="bold blue"),
            border_style="blue"
        )
        output_lines.append(str(header))

        # Progress Section
        progress_table = Table(title="Progress Overview", show_header=True, box=box.ROUNDED)
        progress_table.add_column("Metric", style="cyan")
        progress_table.add_column("Value", style="green")

        progress_table.add_row("Total Tasks", str(progress.total_tasks))
        progress_table.add_row("Completed", f"[green]{progress.completed_tasks}[/green]")
        progress_table.add_row("In Progress", f"[yellow]{progress.in_progress_tasks}[/yellow]")
        progress_table.add_row("Blocked", f"[red]{progress.blocked_tasks}[/red]")
        progress_table.add_row("Pending", f"[blue]{progress.pending_tasks}[/blue]")

        # Progress bar
        progress_bar = self._create_progress_bar(progress.percentage)
        progress_table.add_row("Progress", progress_bar)

        output_lines.append(str(progress_table))

        # Task details (if verbose or if there are issues)
        if verbose_mode or progress.blocked_tasks > 0 or progress.in_progress_tasks > 0:
            task_table = Table(title="Task Details", show_header=True, box=box.ROUNDED)
            task_table.add_column("ID", style="cyan")
            task_table.add_column("Title", style="white")
            task_table.add_column("State", style="yellow")
            task_table.add_column("Last Updated", style="dim")

            # Sort tasks by state priority (blocked, in_progress, pending, completed)
            state_priority = {
                TaskState.BLOCKED: 0,
                TaskState.IN_PROGRESS: 1,
                TaskState.PENDING: 2,
                TaskState.COMPLETED: 3,
            }

            sorted_tasks = sorted(tasks, key=lambda t: state_priority.get(t.state, 4))

            for task in sorted_tasks[:20]:  # Limit to 20 tasks for readability
                state_style = {
                    TaskState.COMPLETED: "green",
                    TaskState.IN_PROGRESS: "yellow",
                    TaskState.BLOCKED: "red",
                    TaskState.PENDING: "blue",
                }.get(task.state, "white")

                state_icon = {
                    TaskState.COMPLETED: "✓",
                    TaskState.IN_PROGRESS: "⟳",
                    TaskState.BLOCKED: "✗",
                    TaskState.PENDING: "○",
                }.get(task.state, "?")

                task_table.add_row(
                    task.id,
                    task.title[:50] + "..." if len(task.title) > 50 else task.title,
                    f"[{state_style}]{state_icon} {task.state.value}[/{state_style}]",
                    task.last_updated.strftime("%Y-%m-%d %H:%M") if task.last_updated else "Never"
                )

            output_lines.append(str(task_table))

        # Issues and warnings
        issues = self._identify_issues(progress, tasks)
        if issues:
            issues_table = Table(title="Issues & Warnings", show_header=False, box=box.ROUNDED)
            issues_table.add_column("Issue", style="yellow")

            for issue in issues:
                issues_table.add_row(f"⚠ {issue}")

            output_lines.append(str(issues_table))

        # Footer
        footer = Text(f"Last updated: {progress.last_updated.strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
        output_lines.append(str(footer))

        return "\n\n".join(output_lines)

    def _plain_status_display(self, progress: ProgressData, tasks: List[TaskInfo], verbose_mode: bool = False) -> str:
        """Create plain text status display (fallback)."""
        lines = []

        # Header
        if progress.feature_id:
            lines.append(f"=== Task Monitor Status - Feature {progress.feature_id} ===")
        else:
            lines.append("=== Task Monitor Status ===")

        lines.append("")

        # Progress Overview
        lines.append("Progress Overview:")
        lines.append(f"  Total Tasks: {progress.total_tasks}")
        lines.append(f"  Completed: {progress.completed_tasks}")
        lines.append(f"  In Progress: {progress.in_progress_tasks}")
        lines.append(f"  Blocked: {progress.blocked_tasks}")
        lines.append(f"  Pending: {progress.pending_tasks}")

        # Simple progress bar
        bar_length = 30
        filled_length = int(bar_length * progress.percentage / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        lines.append(f"  Progress: [{bar}] {progress.percentage}%")

        lines.append("")

        # Task details (if verbose or issues)
        if verbose_mode or progress.blocked_tasks > 0:
            lines.append("Task Details:")
            lines.append("  ID    Title                                   State       Last Updated")
            lines.append("  ----  --------------------------------------  ---------  ----------------")

            # Sort tasks by state priority
            state_priority = {
                TaskState.BLOCKED: 0,
                TaskState.IN_PROGRESS: 1,
                TaskState.PENDING: 2,
                TaskState.COMPLETED: 3,
            }

            sorted_tasks = sorted(tasks, key=lambda t: state_priority.get(t.state, 4))

            for task in sorted_tasks[:20]:
                state_icon = {
                    TaskState.COMPLETED: "✓",
                    TaskState.IN_PROGRESS: "⟳",
                    TaskState.BLOCKED: "✗",
                    TaskState.PENDING: "○",
                }.get(task.state, "?")

                title = task.title[:40] + "..." if len(task.title) > 40 else task.title
                last_updated = task.last_updated.strftime("%Y-%m-%d %H:%M") if task.last_updated else "Never"

                lines.append(f"  {task.id:<5} {title:<40} {state_icon} {task.state.value:<10} {last_updated}")

            lines.append("")

        # Issues
        issues = self._identify_issues(progress, tasks)
        if issues:
            lines.append("Issues & Warnings:")
            for issue in issues:
                lines.append(f"  ⚠ {issue}")
            lines.append("")

        # Footer
        lines.append(f"Last updated: {progress.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(lines)

    def _create_progress_bar(self, percentage: float) -> str:
        """Create a Rich-formatted progress bar."""
        if RICH_AVAILABLE:
            # Use Rich progress bar
            progress = Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console,
                transient=True,
            )

            # Create progress bar
            bar_color = "green" if percentage >= 80 else "yellow" if percentage >= 50 else "red"
            progress.add_task("Progress", completed=percentage, total=100)

            # Capture progress bar output
            with self.console.capture() as capture:
                progress.refresh()

            return capture.get().strip()
        else:
            # Fallback to simple text bar
            bar_length = 20
            filled_length = int(bar_length * percentage / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            return f"[{bar}] {percentage}%"

    def _identify_issues(self, progress: ProgressData, tasks: List[TaskInfo]) -> List[str]:
        """Identify issues and warnings from current state."""
        issues = []

        # Check for blocked tasks
        if progress.blocked_tasks > 0:
            blocked_tasks = [task for task in tasks if task.state == TaskState.BLOCKED]
            issues.append(f"{progress.blocked_tasks} task(s) blocked")

            for task in blocked_tasks[:3]:  # Show first 3 blocked tasks
                if task.error_message:
                    issues.append(f"  {task.id}: {task.error_message}")

        # Check for long-running in-progress tasks
        now = datetime.now()
        for task in tasks:
            if task.state == TaskState.IN_PROGRESS and task.last_updated:
                age_hours = (now - task.last_updated).total_seconds() / 3600
                if age_hours > 24:  # More than 24 hours
                    issues.append(f"Task {task.id} in progress for {int(age_hours)} hours")

        # Check for stalled progress
        if progress.total_tasks > 0:
            if progress.percentage == 0 and progress.in_progress_tasks == 0:
                issues.append("No progress - all tasks are pending")
            elif progress.in_progress_tasks > 5:
                issues.append(f"High number of in-progress tasks ({progress.in_progress_tasks})")

        return issues

    def show_progress(self, progress: Optional[ProgressData], history: List[TaskHistory], detailed: bool = False) -> str:
        """Display detailed progress analytics."""
        if RICH_AVAILABLE:
            return self._rich_progress_display(progress, history, detailed)
        else:
            return self._plain_progress_display(progress, history, detailed)

    def _rich_progress_display(self, progress: Optional[ProgressData], history: List[TaskHistory], detailed: bool = False) -> str:
        """Create Rich-based progress analytics display."""
        output_lines = []

        # Header
        title = "Progress Analytics"
        header = Panel(
            Text(title, style="bold blue"),
            border_style="blue"
        )
        output_lines.append(str(header))

        if progress:
            # Current progress
            progress_table = Table(title="Current Progress", show_header=True, box=box.ROUNDED)
            progress_table.add_column("Metric", style="cyan")
            progress_table.add_column("Value", style="green")

            progress_table.add_row("Completion", f"{progress.percentage}%")
            progress_table.add_row("Completed Tasks", f"{progress.completed_tasks}/{progress.total_tasks}")

            if progress.total_tasks > 0:
                remaining = progress.total_tasks - progress.completed_tasks
                progress_table.add_row("Remaining Tasks", str(remaining))

                # Estimated completion
                if progress.percentage > 0:
                    total_phases = 100 / progress.percentage if progress.percentage > 0 else 1
                    completion_phases = 1
                    remaining_phases = total_phases - completion_phases
                    progress_table.add_row("Work Remaining", f"{remaining_phases:.1f}x current progress")

            output_lines.append(str(progress_table))

        # Historical trends
        if history:
            history_table = Table(title="Recent Activity", show_header=True, box=box.ROUNDED)
            history_table.add_column("Time", style="dim")
            history_table.add_column("Task ID", style="cyan")
            history_table.add_column("Change", style="yellow")
            history_table.add_column("Details", style="white")

            # Show recent history
            recent_history = history[:10]  # Last 10 entries
            for entry in recent_history:
                time_str = entry.timestamp.strftime("%m-%d %H:%M")
                change_str = f"{entry.old_state.value if entry.old_state else 'NEW'} → {entry.new_state.value}"

                # Color code the change
                if entry.new_state == TaskState.COMPLETED:
                    change_style = "green"
                elif entry.new_state == TaskState.BLOCKED:
                    change_style = "red"
                elif entry.new_state == TaskState.IN_PROGRESS:
                    change_style = "yellow"
                else:
                    change_style = "blue"

                history_table.add_row(
                    time_str,
                    entry.task_id,
                    f"[{change_style}]{change_str}[/{change_style}]",
                    entry.notes or ""
                )

            output_lines.append(str(history_table))

        if not progress and not history:
            no_data_panel = Panel(
                Text("No progress data available", style="yellow"),
                border_style="yellow"
            )
            output_lines.append(str(no_data_panel))

        return "\n\n".join(output_lines)

    def _plain_progress_display(self, progress: Optional[ProgressData], history: List[TaskHistory], detailed: bool = False) -> str:
        """Create plain text progress analytics display."""
        lines = []

        # Header
        lines.append("=== Progress Analytics ===")
        lines.append("")

        if progress:
            # Current progress
            lines.append("Current Progress:")
            lines.append(f"  Completion: {progress.percentage}%")
            lines.append(f"  Completed Tasks: {progress.completed_tasks}/{progress.total_tasks}")

            if progress.total_tasks > 0:
                remaining = progress.total_tasks - progress.completed_tasks
                lines.append(f"  Remaining Tasks: {remaining}")

            lines.append("")

        # Historical trends
        if history:
            lines.append("Recent Activity:")
            lines.append("  Time      Task ID  Change                    Details")
            lines.append("  ----      -------  ------                    -------")

            recent_history = history[:10]  # Last 10 entries
            for entry in recent_history:
                time_str = entry.timestamp.strftime("%m-%d %H:%M")
                change_str = f"{entry.old_state.value if entry.old_state else 'NEW'} → {entry.new_state.value}"
                details = entry.notes or ""

                lines.append(f"  {time_str:<9} {entry.task_id:<8} {change_str:<25} {details}")

            lines.append("")

        if not progress and not history:
            lines.append("No progress data available")
            lines.append("")

        return "\n".join(lines)

    def show_history(self, history: List[TaskHistory], limit: int = 20) -> str:
        """Display task state change history."""
        if not history:
            return "No history available."

        if RICH_AVAILABLE:
            return self._rich_history_display(history, limit)
        else:
            return self._plain_history_display(history, limit)

    def _rich_history_display(self, history: List[TaskHistory], limit: int = 20) -> str:
        """Create Rich-based history display."""
        output_lines = []

        # Header
        title = f"Task History (Last {min(limit, len(history))} entries)"
        header = Panel(
            Text(title, style="bold blue"),
            border_style="blue"
        )
        output_lines.append(str(header))

        # History table
        history_table = Table(show_header=True, box=box.ROUNDED)
        history_table.add_column("Time", style="dim")
        history_table.add_column("Task ID", style="cyan")
        history_table.add_column("State Change", style="yellow")
        history_table.add_column("Details", style="white")

        for entry in history[:limit]:
            time_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")

            old_state = entry.old_state.value if entry.old_state else "NEW"
            change_str = f"{old_state} → {entry.new_state.value}"

            # Color code based on new state
            if entry.new_state == TaskState.COMPLETED:
                change_style = "green"
            elif entry.new_state == TaskState.BLOCKED:
                change_style = "red"
            elif entry.new_state == TaskState.IN_PROGRESS:
                change_style = "yellow"
            else:
                change_style = "blue"

            history_table.add_row(
                time_str,
                entry.task_id,
                f"[{change_style}]{change_str}[/{change_style}]",
                entry.notes or ""
            )

        output_lines.append(str(history_table))

        return "\n\n".join(output_lines)

    def _plain_history_display(self, history: List[TaskHistory], limit: int = 20) -> str:
        """Create plain text history display."""
        lines = []

        # Header
        lines.append(f"=== Task History (Last {min(limit, len(history))} entries) ===")
        lines.append("")

        # History entries
        lines.append("Time                     Task ID  State Change              Details")
        lines.append("----                     -------  -----------              -------")

        for entry in history[:limit]:
            time_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            old_state = entry.old_state.value if entry.old_state else "NEW"
            change_str = f"{old_state} → {entry.new_state.value}"
            details = entry.notes or ""

            lines.append(f"{time_str:<24} {entry.task_id:<8} {change_str:<25} {details}")

        return "\n".join(lines)