"""
SpecPulse Configuration Validator
Validates .specpulse/config.yaml structure and content
"""

from pathlib import Path
from typing import List, Dict, Any
import yaml


class ConfigValidator:
    """Validates SpecPulse project configuration"""

    # Required top-level keys
    REQUIRED_KEYS = ['version', 'project', 'ai', 'templates']

    # Required nested keys
    REQUIRED_PROJECT_KEYS = ['name', 'type', 'created']
    REQUIRED_AI_KEYS = ['primary']
    REQUIRED_TEMPLATE_KEYS = ['spec', 'plan', 'task']

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, config_path: Path) -> List[str]:
        """
        Validate configuration file structure

        Args:
            config_path: Path to config.yaml file

        Returns:
            List of error messages (empty if valid)
        """
        self.errors.clear()
        self.warnings.clear()

        # Check file exists
        if not config_path.exists():
            self.errors.append(f"Config file not found: {config_path}")
            return self.errors

        # Load and parse YAML
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML syntax: {e}")
            return self.errors
        except Exception as e:
            self.errors.append(f"Failed to read config file: {e}")
            return self.errors

        if not isinstance(config, dict):
            self.errors.append("Config file must contain a YAML dictionary")
            return self.errors

        # Validate required top-level keys
        for key in self.REQUIRED_KEYS:
            if key not in config:
                self.errors.append(f"Missing required key: {key}")

        # Validate project section
        if 'project' in config:
            project = config['project']
            if not isinstance(project, dict):
                self.errors.append("'project' must be a dictionary")
            else:
                for key in self.REQUIRED_PROJECT_KEYS:
                    if key not in project:
                        self.errors.append(f"Missing required project key: project.{key}")

        # Validate AI section
        if 'ai' in config:
            ai = config['ai']
            if not isinstance(ai, dict):
                self.errors.append("'ai' must be a dictionary")
            else:
                for key in self.REQUIRED_AI_KEYS:
                    if key not in ai:
                        self.errors.append(f"Missing required AI key: ai.{key}")

                # Check valid AI provider
                if 'primary' in ai:
                    valid_providers = ['claude', 'gemini', 'both']
                    if ai['primary'] not in valid_providers:
                        self.warnings.append(
                            f"Unknown AI provider: {ai['primary']} "
                            f"(expected: {', '.join(valid_providers)})"
                        )

        # Validate templates section
        if 'templates' in config:
            templates = config['templates']
            if not isinstance(templates, dict):
                self.errors.append("'templates' must be a dictionary")
            else:
                for key in self.REQUIRED_TEMPLATE_KEYS:
                    if key not in templates:
                        self.errors.append(f"Missing required template key: templates.{key}")

        # Validate version format
        if 'version' in config:
            version = config['version']
            if not isinstance(version, str):
                self.errors.append(f"Version must be a string, got: {type(version).__name__}")
            else:
                # Basic semver check
                parts = version.split('.')
                if len(parts) < 2:
                    self.warnings.append(f"Version format unusual: {version} (expected X.Y.Z)")

        return self.errors

    def auto_fix(self, config_path: Path) -> Dict[str, Any]:
        """
        Auto-fix common configuration issues

        Args:
            config_path: Path to config.yaml file

        Returns:
            Fixed configuration dictionary
        """
        # Load existing config
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}

        # Ensure required keys exist with defaults
        if 'version' not in config:
            config['version'] = '2.1.2'

        if 'project' not in config:
            config['project'] = {}
        if 'name' not in config['project']:
            config['project']['name'] = config_path.parent.parent.name
        if 'type' not in config['project']:
            config['project']['type'] = 'web'
        if 'created' not in config['project']:
            from datetime import datetime
            config['project']['created'] = datetime.now().isoformat()

        if 'ai' not in config:
            config['ai'] = {}
        if 'primary' not in config['ai']:
            config['ai']['primary'] = 'claude'

        if 'templates' not in config:
            config['templates'] = {}
        if 'spec' not in config['templates']:
            config['templates']['spec'] = 'templates/spec.md'
        if 'plan' not in config['templates']:
            config['templates']['plan'] = 'templates/plan.md'
        if 'task' not in config['templates']:
            config['templates']['task'] = 'templates/task.md'

        return config

    def get_warnings(self) -> List[str]:
        """Get list of warnings from last validation"""
        return self.warnings

    def is_valid(self, config_path: Path) -> bool:
        """Check if configuration is valid (no errors)"""
        return len(self.validate(config_path)) == 0
