"""
Safe Commands Implementation

These commands provide LLM-safe alternatives to existing CLI commands
with universal ID system integration and atomic operations.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import re

from ...utils.console import Console
from ...utils.llm_safe_file_operations import get_llm_safe_operations
from ...utils.llm_safe_template_system import get_template_system
from ...utils.universal_id_generator import get_universal_id_generator, IDType
from ...utils.memory_id_manager import MemoryIDManager
from ...utils.error_handler import ErrorHandler, ValidationError


class SafeCommands:
    """Safe command implementations with universal ID system"""

    def __init__(self, console: Console, project_root: Path):
        self.console = console
        self.project_root = project_root
        self.file_ops = get_llm_safe_operations(project_root)
        self.template_system = get_template_system(project_root)
        self.id_generator = get_universal_id_generator(project_root)
        self.memory_manager = MemoryIDManager(project_root)
        self.error_handler = ErrorHandler()

    def feature_init_safe(self, feature_name: str) -> Dict:
        """
        Safe feature initialization with universal ID system.

        Replaces: feature_commands.feature_init()
        Improvements: Universal IDs, atomic operations, validation
        """
        try:
            # Validate feature name
            if not feature_name or not feature_name.strip():
                raise ValidationError("Feature name cannot be empty")

            # Create feature directories with universal ID system
            feature_id, created_dirs = self.file_ops.create_feature_directories(feature_name)

            # Get feature info
            feature_dir_name = f"{feature_id}-{self.file_ops.sanitize_feature_name(feature_name)}"

            # Update context file safely
            context_content = self._generate_feature_context(feature_id, feature_name, feature_dir_name)
            context_path = self.project_root / ".specpulse" / "memory" / "context.md"
            self.file_ops.atomic_write_file(context_path, context_content)

            # Create git branch if git repository
            try:
                import shutil
                git_available = shutil.which("git") is not None
                if git_available:
                    import subprocess
                    branch_name = f"{feature_id}-{feature_dir_name}"
                    result = subprocess.run(
                        ["git", "checkout", "-b", branch_name],
                        cwd=self.project_root,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode != 0:
                        self.console.warning(f"Git branch creation failed: {result.stderr}")
                else:
                    self.console.warning("Git not available, skipping branch creation")
            except Exception as e:
                self.console.warning(f"Git operation failed: {e}")

            # Return success information
            return {
                "success": True,
                "feature_id": feature_id,
                "feature_name": feature_name,
                "feature_dir": feature_dir_name,
                "directories": {
                    "specs": str(created_dirs["specs"].relative_to(self.project_root)),
                    "plans": str(created_dirs["plans"].relative_to(self.project_root)),
                    "tasks": str(created_dirs["tasks"].relative_to(self.project_root))
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    def spec_create_safe(self, description: str, feature_name: Optional[str] = None) -> Dict:
        """
        Safe specification creation with universal ID system.

        Replaces: CLI spec creation with fallback logic
        Improvements: Universal IDs, template validation, atomic operations
        """
        try:
            # Detect current feature if not specified
            if not feature_name:
                current_feature = self._detect_current_feature()
                if not current_feature:
                    raise ValidationError("No active feature found. Run feature_init_safe first.")
                feature_dir_name = current_feature
                feature_id = feature_dir_name.split("-")[0]
                feature_name = "-".join(feature_dir_name.split("-")[1:])
            else:
                # Validate feature exists
                feature_id, dirs = self.file_ops.create_feature_directories(feature_name)
                feature_dir_name = f"{feature_id}-{self.file_ops.sanitize_feature_name(feature_name)}"

            # Create specification with template system
            additional_vars = {
                "PROJECT_TYPE": self._detect_project_type(),
                "COMPLEXITY": self._assess_complexity(description),
                "ESTIMATED_HOURS": self._estimate_hours(description),
                "KEY_REQUIREMENTS": self._extract_requirements(description)
            }

            success, spec_path, metadata = self.template_system.create_specification_safe(
                feature_name,
                description,
                additional_vars
            )

            if not success:
                raise ValidationError(f"Template rendering failed: {spec_path}")

            # Update context with spec
            self._update_context_with_spec(Path(spec_path).name, metadata)

            return {
                "success": True,
                "spec_file": str(Path(spec_path).relative_to(self.project_root)),
                "feature_id": feature_id,
                "feature_name": feature_name,
                "spec_id": metadata.get("variables_count", 0),
                "size": len(Path(spec_path).read_text(encoding='utf-8'))
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    def plan_create_safe(self, description: str, feature_name: Optional[str] = None) -> Dict:
        """
        Safe plan creation with universal ID system.

        Replaces: plan_commands.plan_create()
        Improvements: Universal plan IDs, template validation, no conflicts
        """
        try:
            # Detect current feature
            if not feature_name:
                current_feature = self._detect_current_feature()
                if not current_feature:
                    raise ValidationError("No active feature found.")
                feature_dir_name = current_feature
                feature_id = feature_dir_name.split("-")[0]
                feature_name = "-".join(feature_dir_name.split("-")[1:])
            else:
                feature_dir_name = f"{self.file_ops.sanitize_feature_name(feature_name)}"

            # Validate feature directory
            if not self.file_ops.validate_feature_dir_name(feature_dir_name):
                raise ValidationError(f"Invalid feature directory: {feature_dir_name}")

            # Create plan with universal ID system
            additional_vars = {
                "PROJECT_TYPE": self._detect_project_type(),
                "COMPLEXITY": self._assess_plan_complexity(description),
                "ESTIMATED_DURATION": self._estimate_duration(description),
                "RISKS": self._assess_risks(description)
            }

            success, plan_path, metadata = self.template_system.create_plan_safe(
                feature_dir_name,
                description,
                additional_vars
            )

            if not success:
                raise ValidationError(f"Plan creation failed: {plan_path}")

            # Update context with plan
            self._update_context_with_plan(Path(plan_path).name, metadata)

            return {
                "success": True,
                "plan_file": str(Path(plan_path).relative_to(self.project_root)),
                "feature_id": feature_id,
                "feature_name": feature_name,
                "plan_id": Path(plan_path).stem.replace("plan-", ""),
                "size": len(Path(plan_path).read_text(encoding='utf-8'))
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    def task_create_safe(self, description: str, service_prefix: Optional[str] = None,
                         feature_name: Optional[str] = None) -> Dict:
        """
        Safe task creation with universal ID system and service support.

        Replaces: Task creation logic
        Improvements: Service prefixes, universal task IDs, atomic operations
        """
        try:
            # Detect current feature
            if not feature_name:
                current_feature = self._detect_current_feature()
                if not current_feature:
                    raise ValidationError("No active feature found.")
                feature_dir_name = current_feature
                feature_id = feature_dir_name.split("-")[0]
                feature_name = "-".join(feature_dir_name.split("-")[1:])
            else:
                feature_dir_name = f"{self.file_ops.sanitize_feature_name(feature_name)}"

            # Validate service prefix
            if service_prefix and not re.match(r'^[A-Z]+$', service_prefix):
                raise ValidationError(f"Invalid service prefix: {service_prefix}")

            # Create task with universal ID system
            additional_vars = {
                "PRIORITY": self._assess_task_priority(description),
                "ESTIMATED_HOURS": self._estimate_task_hours(description),
                "COMPLEXITY": self._assess_task_complexity(description),
                "DEPENDENCIES": self._detect_dependencies(description),
                "SERVICE": service_prefix or "General",
                "TAGS": self._generate_task_tags(description)
            }

            success, task_path, metadata = self.template_system.create_task_safe(
                feature_dir_name,
                description,
                additional_vars,
                service_prefix
            )

            if not success:
                raise ValidationError(f"Task creation failed: {task_path}")

            # Update context with task
            self._update_context_with_task(Path(task_path).name, metadata)

            return {
                "success": True,
                "task_file": str(Path(task_path).relative_to(self.project_root)),
                "feature_id": feature_id,
                "feature_name": feature_name,
                "task_id": Path(task_path).stem,
                "service_prefix": service_prefix,
                "priority": additional_vars["PRIORITY"],
                "estimated_hours": additional_vars["ESTIMATED_HOURS"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    def status_report_safe(self, feature_name: Optional[str] = None,
                          verbose: bool = False, show_ids: bool = False,
                          validate_structure: bool = False) -> Dict:
        """
        Safe status reporting with validated operations.

        Replaces: status command logic
        Improvements: Validated scanning, ID statistics, comprehensive reporting
        """
        try:
            results = {
                "success": True,
                "features": [],
                "universal_ids": {},
                "validation": {}
            }

            # Validate project structure
            validation_results = self.file_ops.validate_project_structure()
            results["validation"] = validation_results

            # Get universal ID statistics
            if show_ids:
                id_stats = self.id_generator.get_statistics()
                memory_stats = self.memory_manager.get_id_statistics()
                results["universal_ids"] = {
                    "current_ids": {
                        "feature": f"{id_stats['counters']['feature']:03d}",
                        "spec": f"spec-{id_stats['counters']['spec']:03d}.md",
                        "plan": f"plan-{id_stats['counters']['plan']:03d}.md",
                        "task": f"T{id_stats['counters']['task']:03d}.md",
                        "decision": memory_stats['current_decision_id'],
                        "pattern": memory_stats['current_pattern_id'],
                        "constraint": memory_stats['current_constraint_id'],
                        "checkpoint": memory_stats['current_checkpoint_id']
                    },
                    "service_counters": id_stats['service_counters'],
                    "total_ids_used": id_stats['total_ids_used']
                }

            # Scan features safely
            if feature_name and feature_name != "all":
                # Specific feature
                feature_info = self._get_feature_info_safe(feature_name, verbose)
                if feature_info:
                    results["features"] = [feature_info]
            else:
                # All features
                all_features = self._scan_all_features_safe(verbose)
                results["features"] = all_features

            return results

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    def validate_markdown_safe(self, target: str = 'all', fix_issues: bool = False,
                              strict_mode: bool = False, output_format: str = 'table') -> Dict:
        """
        Safe markdown file validation with comprehensive checks.

        Replaces: Manual markdown validation
        Improvements: Comprehensive syntax, structure, and link validation
        """
        try:
            results = {
                "success": True,
                "validated_files": 0,
                "issues_found": 0,
                "issues_fixed": 0,
                "validation_details": {}
            }

            # Define target directories
            target_dirs = {
                'specs': self.project_root / ".specpulse" / "specs",
                'plans': self.project_root / ".specpulse" / "plans",
                'tasks': self.project_root / ".specpulse" / "tasks",
                'memory': self.project_root / ".specpulse" / "memory"
            }

            # Determine which directories to validate
            dirs_to_validate = []
            if target == 'all':
                dirs_to_validate = list(target_dirs.values())
            elif target in target_dirs:
                dirs_to_validate = [target_dirs[target]]

            # Validation patterns and rules
            validation_rules = {
                'front_matter': {
                    'pattern': r'^---\n.*?\n---\n',
                    'required': True,
                    'description': 'YAML front matter'
                },
                'title_structure': {
                    'pattern': r'^#\s+.+',
                    'required': True,
                    'description': 'Main title (H1)'
                },
                'status_field': {
                    'pattern': r'\*\*Status\*\*:.*',
                    'required': True,
                    'description': 'Status field'
                },
                'created_field': {
                    'pattern': r'\*\*Created\*\*:.*',
                    'required': True,
                    'description': 'Created date field'
                },
                'internal_links': {
                    'pattern': r'\[.*?\]\([^)]+\.md\)',
                    'required': False,
                    'description': 'Internal markdown links'
                }
            }

            # Validate each directory
            for target_dir in dirs_to_validate:
                if not target_dir.exists():
                    continue

                validation_results = []
                md_files = list(target_dir.rglob("*.md"))

                for md_file in md_files:
                    if not self.file_ops.validate_file_operation(md_file, "read"):
                        continue

                    file_issues = []
                    content = md_file.read_text(encoding='utf-8')

                    # Apply validation rules
                    for rule_name, rule_config in validation_rules.items():
                        if strict_mode or rule_config['required']:
                            if not re.search(rule_config['pattern'], content, re.DOTALL | re.MULTILINE):
                                file_issues.append({
                                    'type': rule_name,
                                    'severity': 'error' if rule_config['required'] else 'warning',
                                    'description': f"Missing or invalid {rule_config['description']}",
                                    'line': self._find_line_number(content, rule_config['pattern'])
                                })

                    # Check for common markdown issues
                    file_issues.extend(self._check_markdown_issues(content, strict_mode))

                    # Validate internal links
                    link_issues = self._validate_internal_links(content, md_file.parent)
                    file_issues.extend(link_issues)

                    validation_results.append({
                        'file': str(md_file.relative_to(self.project_root)),
                        'issues': file_issues,
                        'status': 'valid' if not file_issues else 'invalid'
                    })

                    results['validated_files'] += 1
                    results['issues_found'] += len(file_issues)

                    # Auto-fix issues if requested
                    if fix_issues and file_issues:
                        fixed_content = self._fix_markdown_issues(content, file_issues)
                        if fixed_content != content:
                            md_file.write_text(fixed_content, encoding='utf-8')
                            results['issues_fixed'] += len([i for i in file_issues if i.get('fixable', False)])

                results['validation_details'][target_dir.name] = validation_results

            # Determine overall success
            results['success'] = results['issues_found'] == 0

            # Format output
            if output_format == 'json':
                return results
            elif output_format == 'summary':
                return self._format_validation_summary(results)
            else:  # table format
                self.console.success(f"Markdown Validation Complete")
                self.console.info(f"Files validated: {results['validated_files']}")
                self.console.info(f"Issues found: {results['issues_found']}")
                if fix_issues:
                    self.console.info(f"Issues fixed: {results['issues_fixed']}")

                return results

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    def _find_line_number(self, content: str, pattern: str) -> int:
        """Find line number where pattern should appear or first occurrence."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                return i
        return 1

    def _check_markdown_issues(self, content: str, strict_mode: bool) -> List[Dict]:
        """Check for common markdown formatting issues."""
        issues = []

        # Check for trailing whitespace
        if re.search(r'[ \t]+$', content, re.MULTILINE):
            issues.append({
                'type': 'trailing_whitespace',
                'severity': 'warning',
                'description': 'Lines with trailing whitespace',
                'fixable': True
            })

        # Check for multiple consecutive blank lines
        if re.search(r'\n{3,}', content):
            issues.append({
                'type': 'multiple_blank_lines',
                'severity': 'warning',
                'description': 'Multiple consecutive blank lines',
                'fixable': True
            })

        return issues

    def _validate_internal_links(self, content: str, base_path: Path) -> List[Dict]:
        """Validate internal markdown links."""
        issues = []

        # Find all internal markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)

        for link_text, link_path in links:
            # Skip external links
            if link_path.startswith(('http://', 'https://', 'mailto:', '#')):
                continue

            # Resolve relative path
            full_path = base_path / link_path
            if not full_path.exists() and not full_path.with_suffix('.md').exists():
                issues.append({
                    'type': 'broken_internal_link',
                    'severity': 'error',
                    'description': f"Broken link: [{link_text}]({link_path})",
                    'fixable': False
                })

        return issues

    def _fix_markdown_issues(self, content: str, issues: List[Dict]) -> str:
        """Fix auto-fixable markdown issues."""
        fixed_content = content

        for issue in issues:
            if not issue.get('fixable', False):
                continue

            if issue['type'] == 'trailing_whitespace':
                fixed_content = re.sub(r'[ \t]+$', '', fixed_content, flags=re.MULTILINE)
            elif issue['type'] == 'multiple_blank_lines':
                fixed_content = re.sub(r'\n{3,}', '\n\n', fixed_content)

        return fixed_content

    def _format_validation_summary(self, results: Dict) -> Dict:
        """Format validation results as a summary."""
        summary = {
            'success': results['success'],
            'summary': {
                'files_validated': results['validated_files'],
                'total_issues': results['issues_found'],
                'issues_fixed': results.get('issues_fixed', 0),
                'overall_status': 'PASS' if results['success'] else 'FAIL'
            }
        }

        # Count issue types
        issue_counts = {}
        for category, files in results['validation_details'].items():
            for file_info in files:
                for issue in file_info['issues']:
                    issue_type = issue['type']
                    issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

        summary['issue_breakdown'] = issue_counts
        return summary

    # Helper methods
    def _detect_current_feature(self) -> Optional[str]:
        """Detect current feature using safe operations."""
        context_file = self.project_root / ".specpulse" / "memory" / "context.md"
        if self.file_ops.validate_file_operation(context_file, "read"):
            try:
                content = context_file.read_text(encoding='utf-8')
                for line in content.split('\n'):
                    if '**Directory**:' in line:
                        feature_dir = line.split(':')[1].strip()
                        if self.file_ops.validate_feature_dir_name(feature_dir):
                            return feature_dir
            except:
                pass

        # Fallback to scanning specs directory
        specs_dir = self.project_root / ".specpulse" / "specs"
        if self.file_ops.validate_file_operation(specs_dir, "read"):
            try:
                feature_dirs = []
                for item in specs_dir.iterdir():
                    if item.is_dir() and self.file_ops.validate_feature_dir_name(item.name):
                        feature_dirs.append(item)

                if feature_dirs:
                    feature_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    return feature_dirs[0].name
            except:
                pass

        return None

    def _generate_feature_context(self, feature_id: str, feature_name: str, feature_dir_name: str) -> str:
        """Generate context content for feature."""
        return f"""# Feature Context

## Current Feature
- **ID**: {feature_id}
- **Name**: {feature_name}
- **Directory**: {feature_dir_name}
- **Status**: active
- **Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Created By**: Safe SpecPulse Commands

## Feature Structure Created
✓ specs/{feature_dir_name}/
✓ plans/{feature_dir_name}/
✓ tasks/{feature_dir_name}/

## Next Steps
1. Create specification: spec_create_safe "{feature_name} specification"
2. Generate implementation plan: plan_create_safe
3. Break down into tasks: task_create_safe
4. Execute tasks: [Execution commands to be implemented]

## Safe Command Benefits
- Atomic operations (no race conditions)
- Universal ID system (consistent numbering)
- Validated file operations (security)
- Template-based content (consistency)
"""

    def _detect_project_type(self) -> str:
        """Detect project type from structure."""
        project_root = self.project_root

        if (project_root / "package.json").exists() or (project_root / "index.html").exists():
            return "web"
        elif (project_root / "requirements.txt").exists() or (project_root / "setup.py").exists():
            return "python"
        elif (project_root / "pom.xml").exists() or (project_root / "build.gradle").exists():
            return "java"
        elif (project_root / "go.mod").exists():
            return "go"
        elif (project_root / "Cargo.toml").exists():
            return "rust"
        else:
            return "general"

    def _assess_complexity(self, description: str) -> str:
        """Assess complexity from description."""
        indicators = {
            "simple": ["basic", "simple", "straightforward", "minimal"],
            "medium": ["integration", "multiple", "database", "api"],
            "complex": ["microservices", "distributed", "real-time", "scalable", "enterprise"]
        }

        description_lower = description.lower()
        for complexity, keywords in indicators.items():
            if any(keyword in description_lower for keyword in keywords):
                return complexity
        return "medium"

    def _estimate_hours(self, description: str) -> int:
        """Estimate development hours."""
        word_count = len(description.split())
        complexity = self._assess_complexity(description)

        base_hours = {
            "simple": max(4, word_count // 10),
            "medium": max(8, word_count // 8),
            "complex": max(16, word_count // 5)
        }

        return base_hours[complexity]

    def _get_feature_info_safe(self, feature_dir_name: str, verbose: bool) -> Dict:
        """Get feature information using safe operations."""
        if not self.file_ops.validate_feature_dir_name(feature_dir_name):
            return None

        feature_id = feature_dir_name.split("-")[0]
        feature_name = "-".join(feature_dir_name.split("-")[1:])

        info = {
            "feature_id": feature_id,
            "feature_name": feature_name,
            "specifications": 0,
            "plans": 0,
            "tasks": 0,
            "latest_files": {}
        }

        # Count specifications
        specs_dir = self.project_root / ".specpulse" / "specs" / feature_dir_name
        if self.file_ops.validate_file_operation(specs_dir, "read"):
            spec_files = list(specs_dir.glob("spec-*.md"))
            info["specifications"] = len(spec_files)
            if spec_files:
                info["latest_files"]["spec"] = spec_files[-1].name

        # Count plans
        plans_dir = self.project_root / ".specpulse" / "plans" / feature_dir_name
        if self.file_ops.validate_file_operation(plans_dir, "read"):
            plan_files = list(plans_dir.glob("plan-*.md"))
            info["plans"] = len(plan_files)
            if plan_files:
                info["latest_files"]["plan"] = plan_files[-1].name

        # Count tasks
        tasks_dir = self.project_root / ".specpulse" / "tasks" / feature_dir_name
        if self.file_ops.validate_file_operation(tasks_dir, "read"):
            task_files = []
            for item in tasks_dir.glob("*.md"):
                is_valid, id_type, _ = self.id_generator.validate_id_format(item.name)
                if id_type in [IDType.TASK, IDType.SERVICE_TASK]:
                    task_files.append(item)
            info["tasks"] = len(task_files)
            if task_files:
                info["latest_files"]["task"] = task_files[-1].name

        return info

    def _scan_all_features_safe(self, verbose: bool) -> List[Dict]:
        """Scan all features using safe operations."""
        specs_dir = self.project_root / ".specpulse" / "specs"
        features = []

        if not self.file_ops.validate_file_operation(specs_dir, "read"):
            return features

        try:
            for item in specs_dir.iterdir():
                if item.is_dir() and self.file_ops.validate_feature_dir_name(item.name):
                    feature_info = self._get_feature_info_safe(item.name, verbose)
                    if feature_info:
                        features.append(feature_info)
        except:
            pass

        return sorted(features, key=lambda x: x["feature_id"])

    # Additional helper methods for assessment, validation, etc.
    # ... (other helper methods would be implemented here)