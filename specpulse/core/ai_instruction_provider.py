"""
AI Instruction Provider Service

Extracted from SpecPulse God Object - handles AI-specific instructions.

Implements IAIInstructionProvider interface.
"""

from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class AIInstructionProvider:
    """AI instruction provider implementing IAIInstructionProvider"""

    def __init__(self, resources_dir: Path):
        self.resources_dir = resources_dir
        self.claude_commands_dir = resources_dir / "commands" / "claude"
        self.gemini_commands_dir = resources_dir / "commands" / "gemini"
        self.windsurf_commands_dir = resources_dir / "commands" / "windsurf"
        self.cursor_commands_dir = resources_dir / "commands" / "cursor"
        self.github_commands_dir = resources_dir / "commands" / "github"

    # Claude methods
    def get_claude_instructions(self) -> str:
        """Get Claude AI instructions"""
        return """# SpecPulse Commands for Claude
Use /sp-pulse, /sp-spec, /sp-plan, /sp-task for SDD workflow."""

    def get_claude_pulse_command(self) -> str:
        """Get Claude pulse command"""
        return self._load_command_file(self.claude_commands_dir / "sp-pulse.md")

    def get_claude_spec_command(self) -> str:
        """Get Claude spec command"""
        return self._load_command_file(self.claude_commands_dir / "sp-spec.md")

    def get_claude_plan_command(self) -> str:
        """Get Claude plan command"""
        return self._load_command_file(self.claude_commands_dir / "sp-plan.md")

    def get_claude_task_command(self) -> str:
        """Get Claude task command"""
        return self._load_command_file(self.claude_commands_dir / "sp-task.md")

    def get_claude_execute_command(self) -> str:
        """Get Claude execute command"""
        return self._load_command_file(self.claude_commands_dir / "sp-execute.md")

    def get_claude_validate_command(self) -> str:
        """Get Claude validate command"""
        return self._load_command_file(self.claude_commands_dir / "sp-validate.md")

    def get_claude_decompose_command(self) -> str:
        """Get Claude decompose command"""
        return self._load_command_file(self.claude_commands_dir / "sp-decompose.md")

    # Gemini methods
    def get_gemini_instructions(self) -> str:
        """Get Gemini CLI instructions"""
        return """# SpecPulse Commands for Gemini CLI
Use /sp-pulse, /sp-spec, /sp-plan, /sp-task for SDD workflow."""

    def get_gemini_pulse_command(self) -> str:
        """Get Gemini pulse command"""
        return self._load_command_file(self.gemini_commands_dir / "sp-pulse.toml")

    def get_gemini_spec_command(self) -> str:
        """Get Gemini spec command"""
        return self._load_command_file(self.gemini_commands_dir / "sp-spec.toml")

    def get_gemini_plan_command(self) -> str:
        """Get Gemini plan command"""
        return self._load_command_file(self.gemini_commands_dir / "sp-plan.toml")

    def get_gemini_task_command(self) -> str:
        """Get Gemini task command"""
        return self._load_command_file(self.gemini_commands_dir / "sp-task.toml")

    def get_gemini_execute_command(self) -> str:
        """Get Gemini execute command"""
        return self._load_command_file(self.gemini_commands_dir / "sp-execute.toml")

    def get_gemini_validate_command(self) -> str:
        """Get Gemini validate command"""
        return self._load_command_file(self.gemini_commands_dir / "sp-validate.toml")

    def get_gemini_decompose_command(self) -> str:
        """Get Gemini decompose command"""
        return self._load_command_file(self.gemini_commands_dir / "sp-decompose.toml")

    # Windsurf methods
    def get_windsurf_instructions(self) -> str:
        """Get Windsurf AI instructions"""
        return """# SpecPulse Commands for Windsurf
Use /sp-pulse, /sp-spec, /sp-plan, /sp-task for SDD workflow."""

    def get_windsurf_pulse_command(self) -> str:
        """Get Windsurf pulse command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-pulse.md")

    def get_windsurf_spec_command(self) -> str:
        """Get Windsurf spec command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-spec.md")

    def get_windsurf_plan_command(self) -> str:
        """Get Windsurf plan command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-plan.md")

    def get_windsurf_task_command(self) -> str:
        """Get Windsurf task command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-task.md")

    def get_windsurf_execute_command(self) -> str:
        """Get Windsurf execute command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-execute.md")

    def get_windsurf_status_command(self) -> str:
        """Get Windsurf status command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-status.md")

    def get_windsurf_continue_command(self) -> str:
        """Get Windsurf continue command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-continue.md")

    def get_windsurf_decompose_command(self) -> str:
        """Get Windsurf decompose command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-decompose.md")

    def get_windsurf_validate_command(self) -> str:
        """Get Windsurf validate command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-validate.md")

    def get_windsurf_clarify_command(self) -> str:
        """Get Windsurf clarify command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-clarify.md")

    def get_windsurf_feature_command(self) -> str:
        """Get Windsurf feature command"""
        return self._load_command_file(self.windsurf_commands_dir / "sp-feature.md")

    # Cursor methods
    def get_cursor_instructions(self) -> str:
        """Get Cursor AI instructions"""
        return """# SpecPulse Commands for Cursor
Use /sp-pulse, /sp-spec, /sp-plan, /sp-task for SDD workflow."""

    def get_cursor_pulse_command(self) -> str:
        """Get Cursor pulse command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-pulse.md")

    def get_cursor_spec_command(self) -> str:
        """Get Cursor spec command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-spec.md")

    def get_cursor_plan_command(self) -> str:
        """Get Cursor plan command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-plan.md")

    def get_cursor_task_command(self) -> str:
        """Get Cursor task command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-task.md")

    def get_cursor_execute_command(self) -> str:
        """Get Cursor execute command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-execute.md")

    def get_cursor_status_command(self) -> str:
        """Get Cursor status command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-status.md")

    def get_cursor_validate_command(self) -> str:
        """Get Cursor validate command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-validate.md")

    def get_cursor_feature_command(self) -> str:
        """Get Cursor feature command"""
        return self._load_command_file(self.cursor_commands_dir / "sp-feature.md")

    # GitHub Copilot methods
    def get_github_instructions(self) -> str:
        """Get GitHub Copilot instructions"""
        return """# SpecPulse Commands for GitHub Copilot
Use /sp-pulse, /sp-spec, /sp-plan, /sp-task for SDD workflow."""

    def get_github_pulse_command(self) -> str:
        """Get GitHub Copilot pulse command"""
        return self._load_command_file(self.github_commands_dir / "sp-pulse.prompt.md")

    def get_github_spec_command(self) -> str:
        """Get GitHub Copilot spec command"""
        return self._load_command_file(self.github_commands_dir / "sp-spec.prompt.md")

    def get_github_plan_command(self) -> str:
        """Get GitHub Copilot plan command"""
        return self._load_command_file(self.github_commands_dir / "sp-plan.prompt.md")

    def get_github_task_command(self) -> str:
        """Get GitHub Copilot task command"""
        return self._load_command_file(self.github_commands_dir / "sp-task.prompt.md")

    def get_github_execute_command(self) -> str:
        """Get GitHub Copilot execute command"""
        return self._load_command_file(self.github_commands_dir / "sp-execute.prompt.md")

    def get_github_status_command(self) -> str:
        """Get GitHub Copilot status command"""
        return self._load_command_file(self.github_commands_dir / "sp-status.prompt.md")

    def get_github_validate_command(self) -> str:
        """Get GitHub Copilot validate command"""
        return self._load_command_file(self.github_commands_dir / "sp-validate.prompt.md")

    def get_github_feature_command(self) -> str:
        """Get GitHub Copilot feature command"""
        return self._load_command_file(self.github_commands_dir / "sp-feature.prompt.md")

    # Command generation
    def generate_claude_commands(self) -> List[Dict]:
        """Generate all Claude AI commands"""
        commands = []
        if self.claude_commands_dir.exists():
            for cmd_file in self.claude_commands_dir.glob("*.md"):
                content = cmd_file.read_text(encoding='utf-8')
                commands.append({
                    "name": cmd_file.stem,
                    "description": "Claude AI command",
                    "content": content
                })
        return commands

    def generate_gemini_commands(self) -> List[Dict]:
        """Generate all Gemini AI commands"""
        commands = []
        if self.gemini_commands_dir.exists():
            for cmd_file in self.gemini_commands_dir.glob("*.toml"):
                content = cmd_file.read_text(encoding='utf-8')
                commands.append({
                    "name": cmd_file.stem,
                    "description": "Gemini AI command",
                    "content": content
                })
        return commands

    def generate_windsurf_commands(self) -> List[Dict]:
        """Generate all Windsurf AI commands"""
        commands = []
        if self.windsurf_commands_dir.exists():
            for cmd_file in self.windsurf_commands_dir.glob("*.md"):
                content = cmd_file.read_text(encoding='utf-8')
                commands.append({
                    "name": cmd_file.stem,
                    "description": "Windsurf AI command",
                    "content": content
                })
        return commands

    def generate_cursor_commands(self) -> List[Dict]:
        """Generate all Cursor AI commands"""
        commands = []
        if self.cursor_commands_dir.exists():
            for cmd_file in self.cursor_commands_dir.glob("*.md"):
                content = cmd_file.read_text(encoding='utf-8')
                commands.append({
                    "name": cmd_file.stem,
                    "description": "Cursor AI command",
                    "content": content
                })
        return commands

    def generate_github_commands(self) -> List[Dict]:
        """Generate all GitHub Copilot AI commands"""
        commands = []
        if self.github_commands_dir.exists():
            for cmd_file in self.github_commands_dir.glob("*.prompt.md"):
                content = cmd_file.read_text(encoding='utf-8')
                commands.append({
                    "name": cmd_file.stem,
                    "description": "GitHub Copilot AI command",
                    "content": content
                })
        return commands

    def generate_all_commands(self) -> Dict[str, List[Dict]]:
        """Generate commands for all supported AI tools"""
        all_commands = {}

        # Tools configuration
        tools = [
            ("claude", "*.md", "Claude AI command"),
            ("gemini", "*.toml", "Gemini AI command"),
            ("windsurf", "*.md", "Windsurf AI command"),
            ("cursor", "*.md", "Cursor AI command"),
            ("github", "*.prompt.md", "GitHub Copilot AI command")
        ]

        for tool_name, pattern, description in tools:
            tool_dir = self.resources_dir / "commands" / tool_name
            if tool_dir.exists():
                commands = []
                for cmd_file in tool_dir.glob(pattern):
                    content = cmd_file.read_text(encoding='utf-8')
                    commands.append({
                        "name": cmd_file.stem,
                        "description": description,
                        "content": content
                    })
                all_commands[tool_name] = commands

        return all_commands

    def _load_command_file(self, command_path: Path) -> str:
        """Load command file or return not found message"""
        if command_path.exists():
            try:
                return command_path.read_text(encoding='utf-8')
            except Exception as e:
                logger.error(f"Failed to read command file: {e}")
        return f"# {command_path.stem} command not found"


__all__ = ['AIInstructionProvider']
