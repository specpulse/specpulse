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

    def _load_command_file(self, command_path: Path) -> str:
        """Load command file or return not found message"""
        if command_path.exists():
            try:
                return command_path.read_text(encoding='utf-8')
            except Exception as e:
                logger.error(f"Failed to read command file: {e}")
        return f"# {command_path.stem} command not found"


__all__ = ['AIInstructionProvider']
