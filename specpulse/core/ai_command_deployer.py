"""
AI Command Deployer - Deploys AI platform command files for SpecPulse

This module handles copying and deploying AI command files for various
platforms (Claude, Gemini, Windsurf, etc.) with enforced directory isolation.
Extracted from specpulse.py to reduce complexity.
"""

import logging
import shutil
from pathlib import Path
from typing import List, Optional

from .path_manager import PathManager

logger = logging.getLogger(__name__)

# Supported AI platforms
VALID_AI_TOOLS = ['claude', 'gemini', 'windsurf', 'cursor', 'github', 'opencode', 'crush', 'qwen']

# Platform-specific configuration
PLATFORM_CONFIG = {
    'github': {
        'subdir': 'prompts',
        'pattern': '*.prompt.md',
        'dir_attr': 'github_dir'
    },
    'gemini': {
        'subdir': 'commands',
        'pattern': '*.toml',
        'dir_attr': 'gemini_dir'
    },
    'windsurf': {
        'subdir': 'workflows',
        'pattern': '*.md',
        'dir_attr': 'windsurf_dir'
    },
    'opencode': {
        'subdir': 'command',
        'pattern': '*.md',
        'dir_attr': 'opencode_dir'
    },
    'crush': {
        'subdir': 'commands/sp',
        'pattern': '*.md',
        'dir_attr': 'crush_dir'
    },
    'qwen': {
        'subdir': 'commands',
        'pattern': '*.toml',
        'dir_attr': 'qwen_dir'
    },
    'claude': {
        'subdir': 'commands',
        'pattern': '*.md',
        'dir_attr': 'claude_dir'
    },
    'cursor': {
        'subdir': 'commands',
        'pattern': '*.md',
        'dir_attr': 'cursor_dir'
    }
}


def parse_ai_assistant(ai_assistant: Optional[str]) -> List[str]:
    """
    Parse AI assistant selection into list of tools.

    Args:
        ai_assistant: Comma-separated list of AI tools, 'all', or single tool name.
                     If None or empty, defaults to ['claude'].

    Returns:
        List of validated AI tool names
    """
    if not ai_assistant:
        return ['claude']

    # Handle comma-separated selections
    tools = [tool.strip().lower() for tool in ai_assistant.split(',') if tool.strip()]

    # Handle 'all' keyword
    if 'all' in tools:
        return VALID_AI_TOOLS.copy()

    # Validate and return only valid tool names
    return [tool for tool in tools if tool in VALID_AI_TOOLS]


def deploy_ai_commands(
    project_path: Path,
    resources_dir: Path,
    ai_assistant: Optional[str],
    console=None
) -> bool:
    """
    Deploy AI command files based on chosen assistant(s) with enforced directory isolation.

    Args:
        project_path: Path to the project root
        resources_dir: Path to SpecPulse resources directory
        ai_assistant: AI assistant selection (e.g., 'claude', 'gemini,cursor', 'all')
        console: Optional console for output messages

    Returns:
        True if deployment was successful, False otherwise
    """
    path_manager = PathManager(project_path)
    commands_dir = resources_dir / "commands"
    selected_tools = parse_ai_assistant(ai_assistant)

    # Lock custom commands to their directories
    if not path_manager.lock_custom_commands_to_directories(selected_tools):
        if console:
            console.error("Failed to lock custom commands to their directories")
        return False

    # Deploy commands for each selected tool
    for tool in selected_tools:
        _deploy_tool_commands(tool, commands_dir, path_manager, console)

    # Validate AI command isolation after copying
    violations = path_manager.validate_ai_command_isolation()
    if violations and console:
        console.warning(f"AI command isolation violations found: {violations}")

    # Show summary
    if console and selected_tools:
        tool_names = ", ".join(selected_tools).upper()
        console.info(f"Configured for: {tool_names} (ENFORCED directory structure)")

    # Log enforcement status
    enforcement_results = path_manager.enforce_specpulse_rules()
    if not enforcement_results['valid']:
        if console:
            console.error(f"Directory structure enforcement failed: {enforcement_results['errors']}")
        return False

    return True


def _deploy_tool_commands(
    tool: str,
    commands_dir: Path,
    path_manager: PathManager,
    console=None
) -> int:
    """
    Deploy commands for a specific AI tool.

    Args:
        tool: Name of the AI tool (e.g., 'claude', 'gemini')
        commands_dir: Directory containing command templates
        path_manager: PathManager instance for directory management
        console: Optional console for output messages

    Returns:
        Number of files copied
    """
    tool_dir = commands_dir / tool
    if not tool_dir.exists():
        logger.warning(f"Command directory not found for {tool}: {tool_dir}")
        return 0

    # Get platform configuration
    config = PLATFORM_CONFIG.get(tool, PLATFORM_CONFIG['claude'])

    # Build destination directory path
    base_dir = getattr(path_manager, config['dir_attr'])

    # Handle nested subdirectories (e.g., 'commands/sp' for crush)
    subdir_parts = config['subdir'].split('/')
    dst_dir = base_dir
    for part in subdir_parts:
        dst_dir = dst_dir / part

    dst_dir.mkdir(parents=True, exist_ok=True)

    # Copy matching files
    pattern = config['pattern']
    found_files = list(tool_dir.glob(pattern))

    for cmd_file in found_files:
        shutil.copy2(cmd_file, dst_dir / cmd_file.name)

    if console and found_files:
        console.success(f"Copied {len(found_files)} {tool.title()} AI commands")

    return len(found_files)


def get_supported_platforms() -> List[str]:
    """
    Get list of supported AI platforms.

    Returns:
        List of platform names
    """
    return VALID_AI_TOOLS.copy()


def get_platform_config(platform: str) -> dict:
    """
    Get configuration for a specific AI platform.

    Args:
        platform: Platform name (e.g., 'claude', 'gemini')

    Returns:
        Platform configuration dictionary or default config if not found
    """
    return PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG['claude']).copy()


__all__ = [
    'deploy_ai_commands',
    'parse_ai_assistant',
    'get_supported_platforms',
    'get_platform_config',
    'VALID_AI_TOOLS',
    'PLATFORM_CONFIG'
]
