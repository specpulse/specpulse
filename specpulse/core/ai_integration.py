"""
SpecPulse AI Integration - Enhanced AI integration for v2.0.0
Supports multi-LLM workflows, smart context detection, and interactive features.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from .specpulse import SpecPulse
from ..utils.console import Console
from ..utils.error_handler import ErrorHandler


@dataclass
class AIContext:
    """AI context information"""
    current_feature: Optional[str]
    branch_name: Optional[str]
    git_context: Dict[str, Any]
    recent_specs: List[str]
    recent_plans: List[str]
    project_type: str
    tech_stack: Dict[str, str]
    last_activity: Optional[str]


@dataclass
class AIWorkflowState:
    """AI workflow state tracking"""
    current_phase: str  # spec, plan, task, validate
    active_llm: str  # claude, gemini, both
    last_command: Optional[str]
    suggestions: List[str]
    checkpoints: List[Dict[str, Any]]
    progress: float
    last_activity: Optional[str] = None


class AIIntegration:
    """Enhanced AI integration system for SpecPulse v2.0.0"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.console = Console()
        self.error_handler = ErrorHandler()
        self.specpulse = SpecPulse()

        # Import PathManager for centralized path management
        from .path_manager import PathManager
        self.path_manager = PathManager(project_root, use_legacy_structure=False)

        # AI integration paths
        self.ai_state_file = project_root / ".specpulse" / "ai_state.json"
        self.context_file = self.path_manager.memory_dir / "context.md"
        self.ai_cache = project_root / ".specpulse" / "ai_cache"

        # Ensure directories exist
        self.ai_cache.mkdir(exist_ok=True)
        self.ai_state_file.parent.mkdir(exist_ok=True)

        # Initialize AI state
        self.state = self._load_ai_state()

    def _load_ai_state(self) -> AIWorkflowState:
        """Load AI workflow state from file"""
        if self.ai_state_file.exists():
            try:
                with open(self.ai_state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return AIWorkflowState(**data)
            except Exception as e:
                self.console.warning(f"Failed to load AI state: {e}")

        # Default state
        return AIWorkflowState(
            current_phase="spec",
            active_llm="claude",
            last_command=None,
            suggestions=[],
            checkpoints=[],
            progress=0.0
        )

    def _save_ai_state(self):
        """Save AI workflow state to file"""
        try:
            with open(self.ai_state_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.state), f, indent=2, default=str)
        except Exception as e:
            self.console.warning(f"Failed to save AI state: {e}")

    def detect_context(self) -> AIContext:
        """Smart context auto-detection"""
        context = AIContext(
            current_feature=None,
            branch_name=None,
            git_context={},
            recent_specs=[],
            recent_plans=[],
            project_type="web",
            tech_stack={},
            last_activity=None
        )

        # Detect from git branch
        try:
            import subprocess
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.returncode == 0:
                branch_name = result.stdout.strip()

                # Only process non-empty branch names
                if branch_name:
                    context.branch_name = branch_name

                    # Extract feature ID from branch name
                    match = re.match(r'(\d{3})-(.+)', branch_name)
                    if match:
                        feature_id = match.group(1)
                        feature_name = match.group(2).replace('-', ' ')
                        context.current_feature = f"{feature_id}-{feature_name}"
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            # Expected errors - git not available or not a repository
            self.error_handler.log_warning(f"Git context detection failed: {e}")
        except Exception as e:
            # Unexpected errors - log for debugging
            self.error_handler.log_error(f"Unexpected error in git detection: {e}")

        # Detect from memory/context.md
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract current feature
                feature_match = re.search(r'current_feature:\s*(.+)', content)
                if feature_match:
                    context.current_feature = feature_match.group(1).strip()

                # Extract tech stack
                tech_match = re.search(r'tech_stack:\s*\{(.+?)\}', content, re.DOTALL)
                if tech_match:
                    tech_str = tech_match.group(1)
                    # Parse simple key-value pairs
                    for line in tech_str.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            context.tech_stack[key.strip()] = value.strip()
            except (IOError, ValueError) as e:
                # Expected errors - file read or parse errors
                self.error_handler.log_warning(f"Context file parse error: {e}")
            except Exception as e:
                # Unexpected errors - log for debugging
                self.error_handler.log_error(f"Unexpected error parsing context file: {e}")

        # Detect recent specs and plans
        specs_dir = self.path_manager.specs_dir
        plans_dir = self.path_manager.plans_dir

        if specs_dir.exists():
            for spec_file in sorted(specs_dir.glob("**/*.md"), reverse=True)[:5]:
                context.recent_specs.append(str(spec_file.relative_to(self.project_root)))

        if plans_dir.exists():
            for plan_file in sorted(plans_dir.glob("**/*.md"), reverse=True)[:5]:
                context.recent_plans.append(str(plan_file.relative_to(self.project_root)))

        return context

    def suggest_next_action(self, context: AIContext) -> List[str]:
        """AI-powered next action suggestions"""
        suggestions = []

        if not context.current_feature:
            suggestions.append("Start with /sp-pulse to create a new feature")
            return suggestions

        # Analyze current state
        if self.state.current_phase == "spec":
            if not context.recent_specs:
                suggestions.append("Create specification with /sp-spec")
            else:
                suggestions.append("Validate specification with /sp-spec validate")
                suggestions.append("Create implementation plan with /sp-plan")

        elif self.state.current_phase == "plan":
            if not context.recent_plans:
                suggestions.append("Create implementation plan with /sp-plan")
            else:
                suggestions.append("Break down tasks with /sp-task")
                suggestions.append("Validate plan with /validate")

        elif self.state.current_phase == "task":
            suggestions.append("Start implementation")
            suggestions.append("Track progress with /sp-progress")

        # Smart suggestions based on context
        if "auth" in str(context.current_feature).lower():
            suggestions.append("Consider security requirements")

        if context.tech_stack.get("database") == "postgresql":
            suggestions.append("Plan database migrations")

        return suggestions

    def get_optimal_template(self, feature_complexity: str = "medium") -> str:
        """Auto-select optimal template based on context and complexity"""
        complexity_mapping = {
            "simple": "spec-tier1-minimal",
            "medium": "spec-tier2-standard",
            "complex": "spec-tier3-complete"
        }

        return complexity_mapping.get(feature_complexity, "spec-tier2-standard")

    def track_ai_command(self, command: str, result: str = ""):
        """Track AI command execution for learning"""
        self.state.last_command = command
        self.state.last_activity = datetime.now().isoformat()

        # Update phase based on command
        if "sp-spec" in command:
            self.state.current_phase = "spec"
        elif "sp-plan" in command:
            self.state.current_phase = "plan"
        elif "sp-task" in command:
            self.state.current_phase = "task"
        elif "validate" in command:
            self.state.current_phase = "validate"

        self._save_ai_state()

    def create_ai_checkpoint(self, description: str) -> str:
        """Create AI workflow checkpoint"""
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "phase": self.state.current_phase,
            "command": self.state.last_command,
            "description": description,
            "context": self.detect_context().__dict__
        }

        checkpoint_id = f"checkpoint-{len(self.state.checkpoints) + 1:03d}"
        checkpoint["id"] = checkpoint_id

        self.state.checkpoints.append(checkpoint)
        self._save_ai_state()

        return checkpoint_id

    def get_ai_assistance(self, query: str, context: Optional[AIContext] = None) -> Dict[str, Any]:
        """Get AI assistance for specific query"""
        if context is None:
            context = self.detect_context()

        assistance = {
            "query": query,
            "context": context,
            "suggestions": [],
            "template_recommendations": [],
            "next_steps": []
        }

        # Analyze query and provide assistance
        query_lower = query.lower()

        if "template" in query_lower:
            assistance["template_recommendations"] = [
                "spec-tier1-minimal (2-3 min, quick prototypes)",
                "spec-tier2-standard (10-15 min, most features)",
                "spec-tier3-complete (30-45 min, production features)"
            ]

        if "how to" in query_lower or "help" in query_lower:
            assistance["suggestions"] = [
                "Use /sp-pulse <feature-name> to start",
                "Use /sp-spec create <description> to create specs",
                "Use /sp-plan generate to create plans",
                "Use /sp-task breakdown to create tasks"
            ]

        if context.current_feature:
            assistance["next_steps"] = self.suggest_next_action(context)
        else:
            assistance["next_steps"] = ["Start with /sp-pulse to create a new feature"]

        return assistance

    def switch_llm(self, llm: str) -> bool:
        """Switch active LLM"""
        if llm in ["claude", "gemini", "both"]:
            self.state.active_llm = llm
            self._save_ai_state()
            return True
        return False

    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get complete workflow summary"""
        context = self.detect_context()

        return {
            "current_feature": context.current_feature,
            "current_phase": self.state.current_phase,
            "active_llm": self.state.active_llm,
            "progress": self.state.progress,
            "recent_specs": context.recent_specs[:3],
            "recent_plans": context.recent_plans[:3],
            "suggestions": self.suggest_next_action(context),
            "checkpoints_count": len(self.state.checkpoints),
            "last_activity": self.state.last_activity
        }