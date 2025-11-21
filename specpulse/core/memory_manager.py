"""
SpecPulse Memory Manager - Enhanced memory system with auto-updates and tracking
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import yaml

from ..utils.error_handler import ValidationError, ErrorSeverity
from ..utils.console import Console


@dataclass
class DecisionRecord:
    """Architecture Decision Record (ADR) structure"""
    id: str
    title: str
    status: str  # proposed, accepted, rejected, deprecated, superseded
    date: str
    author: str
    rationale: str
    alternatives_considered: List[str]
    consequences: List[str]
    related_decisions: List[str]
    tags: List[str]
    review_date: Optional[str] = None


@dataclass
class ContextEntry:
    """Context entry structure"""
    timestamp: str
    feature_name: Optional[str]
    feature_id: Optional[str]
    action: str
    details: Dict[str, Any]
    impact: str  # low, medium, high
    category: str  # spec, plan, task, infrastructure, decision


@dataclass
class MemoryStats:
    """Memory system statistics"""
    total_decisions: int
    active_features: int
    completed_features: int
    total_context_entries: int
    last_updated: str
    memory_size_mb: float


@dataclass
class MemoryEntry:
    """Memory entry for v1.7.0 tag-based system"""
    id: str
    title: str
    content: str
    tags: List[str]
    date: str
    related_features: List[str]


class MemoryManager:
    """Enhanced memory management system"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        # Import PathManager for centralized path management
        from .path_manager import PathManager
        self.path_manager = PathManager(project_root, use_legacy_structure=False)

        self.memory_dir = self.path_manager.memory_dir
        self.context_file = self.memory_dir / "context.md"
        self.decisions_file = self.memory_dir / "decisions.md"
        self.memory_index_path = self.memory_dir / ".memory_index.json"
        self.memory_stats_path = self.memory_dir / ".memory_stats.json"

        self.console = Console()

        # Ensure memory directory exists
        self.memory_dir.mkdir(exist_ok=True)

        # Initialize memory system
        self._initialize_memory_system()

        # Load existing data
        self.memory_index = self._load_memory_index()
        self.memory_stats = self._load_memory_stats()

    def _initialize_memory_system(self):
        """Initialize memory system with required files"""
        # Create context.md if doesn't exist
        if not self.context_file.exists():
            self.context_file.write_text("""# Project Context

*This file tracks the current state and context of the SpecPulse project*

## Active Features
*No active features currently*

## Recent Changes
*Recent changes will be listed here*

## Project Information
- **Framework Version**: v1.5.0
- **Last Updated**: {date}
- **Project Type**: SpecPulse SDD Project

## Memory Index
*This file is automatically maintained by SpecPulse*

""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Create decisions.md if doesn't exist
        if not self.decisions_file.exists():
            self.decisions_file.write_text("""# Architecture Decision Records (ADRs)

*This file contains important architectural decisions and their rationale*

## ADR Template
```markdown
### ADR-XXX: [Title]

**Status**: [proposed/accepted/rejected/deprecated/superseded]
**Date**: YYYY-MM-DD
**Author**: [Name]

### Context
[What is the issue that we're seeing that is motivating this decision]

### Decision
[What is the change that we're proposing]

### Rationale
[Why is this change important? What are the benefits?]

### Alternatives Considered
[What other approaches did we consider and why did we reject them?]

### Consequences
[What are the results of this decision?]

### Related Decisions
[Links to related ADRs]
```

## Active Decisions
*No decisions recorded yet*

## Decision Categories
- **Architecture**: System architecture decisions
- **Technology**: Technology stack choices
- **Process**: Development process decisions
- **Infrastructure**: Infrastructure and deployment decisions

---

*Last Updated: {date}*
""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def _load_memory_index(self) -> Dict:
        """Load memory index from file"""
        if self.memory_index_path.exists():
            try:
                with open(self.memory_index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "features": {},
            "decisions": {},
            "context_entries": [],
            "tags": {},
            "categories": {}
        }

    def _save_memory_index(self):
        """Save memory index to file"""
        self.memory_index["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.memory_index_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory_index, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ValidationError(f"Failed to save memory index: {e}")

    def _load_memory_stats(self) -> MemoryStats:
        """Load memory statistics"""
        if self.memory_stats_path.exists():
            try:
                with open(self.memory_stats_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return MemoryStats(**data)
            except (json.JSONDecodeError, IOError, TypeError):
                pass

        # Calculate initial stats
        return self._calculate_memory_stats()

    def _save_memory_stats(self):
        """Save memory statistics"""
        try:
            with open(self.memory_stats_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.memory_stats), f, indent=2)
        except IOError as e:
            raise ValidationError(f"Failed to save memory stats: {e}")

    def _calculate_memory_stats(self) -> MemoryStats:
        """Calculate current memory statistics"""
        total_decisions = len(self.memory_index.get("decisions", {}))
        active_features = len([f for f in self.memory_index.get("features", {}).values() if f.get("status") == "active"])
        completed_features = len([f for f in self.memory_index.get("features", {}).values() if f.get("status") == "completed"])
        total_context_entries = len(self.memory_index.get("context_entries", []))

        # Calculate memory size
        memory_size = 0
        for file_path in self.memory_dir.rglob("*"):
            if file_path.is_file():
                memory_size += file_path.stat().st_size
        memory_size_mb = round(memory_size / (1024 * 1024), 2)

        return MemoryStats(
            total_decisions=total_decisions,
            active_features=active_features,
            completed_features=completed_features,
            total_context_entries=total_context_entries,
            last_updated=datetime.now().isoformat(),
            memory_size_mb=memory_size_mb
        )

    def update_context(self, feature_name: Optional[str] = None, feature_id: Optional[str] = None,
                       action: str = "general_update", details: Optional[Dict] = None,
                       impact: str = "medium", category: str = "general") -> bool:
        """Update project context with new entry"""

        try:
            # Create context entry
            entry = ContextEntry(
                timestamp=datetime.now().isoformat(),
                feature_name=feature_name,
                feature_id=feature_id,
                action=action,
                details=details or {},
                impact=impact,
                category=category
            )

            # Add to memory index
            self.memory_index["context_entries"].append(asdict(entry))

            # Update context.md file
            self._update_context_file(entry)

            # Update feature tracking if feature provided
            if feature_name and feature_id:
                self._update_feature_tracking(feature_name, feature_id, action)

            # Save changes
            self._save_memory_index()
            self.memory_stats = self._calculate_memory_stats()
            self._save_memory_stats()

            self.console.success(f"Context updated: {action}")
            return True

        except Exception as e:
            self.console.error(f"Failed to update context: {e}")
            return False

    def _update_context_file(self, entry: ContextEntry):
        """Update context.md file with new entry"""
        try:
            content = self.context_file.read_text(encoding='utf-8')

            # Find where to insert the new entry
            recent_changes_section = "## Recent Changes"
            if recent_changes_section in content:
                # Add entry after Recent Changes header
                entry_text = f"""
### {entry.action.replace('_', ' ').title()} - {entry.timestamp[:10]}
- **Feature**: {entry.feature_name or 'N/A'}
- **ID**: {entry.feature_id or 'N/A'}
- **Impact**: {entry.impact}
- **Category**: {entry.category}
- **Details**: {json.dumps(entry.details, indent=2) if entry.details else 'None'}
"""
                # Insert after Recent Changes section
                parts = content.split(recent_changes_section, 1)
                if len(parts) == 2:
                    content = parts[0] + recent_changes_section + entry_text + parts[1]
            else:
                # Add Recent Changes section if it doesn't exist
                content += f"""

## Recent Changes

### {entry.action.replace('_', ' ').title()} - {entry.timestamp[:10]}
- **Feature**: {entry.feature_name or 'N/A'}
- **ID**: {entry.feature_id or 'N/A'}
- **Impact**: {entry.impact}
- **Category**: {entry.category}
"""

            self.context_file.write_text(content)

        except Exception as e:
            raise ValidationError(f"Failed to update context file: {e}")

    def _update_feature_tracking(self, feature_name: str, feature_id: str, action: str):
        """Update feature tracking in memory index"""
        features = self.memory_index.get("features", {})

        if feature_id not in features:
            features[feature_id] = {
                "name": feature_name,
                "status": "active",
                "created": datetime.now().isoformat(),
                "last_action": action,
                "actions": []
            }

        features[feature_id]["last_action"] = action
        features[feature_id]["last_updated"] = datetime.now().isoformat()
        features[feature_id]["actions"].append({
            "action": action,
            "timestamp": datetime.now().isoformat()
        })

        # Update status based on action
        if action in ["feature_completed", "deployment_successful"]:
            features[feature_id]["status"] = "completed"
        elif action in ["feature_abandoned", "feature_cancelled"]:
            features[feature_id]["status"] = "abandoned"

        self.memory_index["features"] = features

    def add_decision_record(self, decision: DecisionRecord) -> bool:
        """Add an Architecture Decision Record"""

        try:
            # Validate decision record
            if not decision.id or not decision.title:
                raise ValidationError("Decision ID and title are required")

            # Add to memory index
            self.memory_index["decisions"][decision.id] = asdict(decision)

            # Update decisions.md file
            self._update_decisions_file(decision)

            # Save changes
            self._save_memory_index()
            self.memory_stats = self._calculate_memory_stats()
            self._save_memory_stats()

            self.console.success(f"Decision recorded: ADR-{decision.id}")
            return True

        except Exception as e:
            self.console.error(f"Failed to record decision: {e}")
            return False

    def _update_decisions_file(self, decision: DecisionRecord):
        """Update decisions.md file with new ADR"""
        try:
            content = self.decisions_file.read_text(encoding='utf-8')

            # Generate ADR entry
            adr_entry = f"""

### ADR-{decision.id}: {decision.title}

**Status**: {decision.status}
**Date**: {decision.date}
**Author**: {decision.author}

#### Context
*This section should describe the context and problem*

#### Decision
*This section should describe the decision made*

#### Rationale
{decision.rationale}

#### Alternatives Considered
{chr(10).join(f"- {alt}" for alt in decision.alternatives_considered) if decision.alternatives_considered else "No alternatives were considered."}

#### Consequences
{chr(10).join(f"- {conseq}" for conseq in decision.consequences) if decision.consequences else "No consequences identified."}

#### Related Decisions
{chr(10).join(f"- ADR-{rel}" for rel in decision.related_decisions) if decision.related_decisions else "No related decisions."}

**Tags**: {', '.join(decision.tags) if decision.tags else "None"}
**Review Date**: {decision.review_date or "Not set"}

---

"""

            # Insert before "## Decision Categories" or at the end
            decision_categories_marker = "## Decision Categories"
            if decision_categories_marker in content:
                parts = content.split(decision_categories_marker, 1)
                if len(parts) == 2:
                    content = parts[0] + adr_entry + decision_categories_marker + parts[1]
            else:
                content += adr_entry

            self.decisions_file.write_text(content)

        except Exception as e:
            raise ValidationError(f"Failed to update decisions file: {e}")

    def search_memory(self, query: str, category: Optional[str] = None,
                      date_range: Optional[Tuple[str, str]] = None) -> List[Dict]:
        """Search memory system for entries matching criteria"""

        results = []
        query_lower = query.lower()

        # Search context entries
        for entry in self.memory_index.get("context_entries", []):
            if self._matches_search_criteria(entry, query_lower, category, date_range):
                results.append({"type": "context", "data": entry})

        # Search decisions
        for decision_id, decision in self.memory_index.get("decisions", {}).items():
            if self._matches_search_criteria(decision, query_lower, category, date_range):
                results.append({"type": "decision", "data": decision, "id": decision_id})

        # Search features
        for feature_id, feature in self.memory_index.get("features", {}).items():
            if self._matches_search_criteria(feature, query_lower, category, date_range):
                results.append({"type": "feature", "data": feature, "id": feature_id})

        return results

    def _matches_search_criteria(self, item: Dict, query: str, category: Optional[str],
                                date_range: Optional[Tuple[str, str]]) -> bool:
        """Check if item matches search criteria"""

        # Text search
        text_content = json.dumps(item).lower()
        if query and query not in text_content:
            return False

        # Category filter
        if category and item.get("category", "").lower() != category.lower():
            return False

        # Date range filter
        if date_range:
            item_date = item.get("timestamp") or item.get("date") or item.get("last_updated")
            if not item_date:
                return False

            try:
                item_dt = datetime.fromisoformat(item_date.replace('Z', '+00:00'))
                start_dt = datetime.fromisoformat(date_range[0])
                end_dt = datetime.fromisoformat(date_range[1])

                if not (start_dt <= item_dt <= end_dt):
                    return False
            except ValueError:
                return False

        return True

    def get_memory_summary(self) -> Dict:
        """Get comprehensive memory summary"""

        # Update stats
        self.memory_stats = self._calculate_memory_stats()

        # Get recent activity
        recent_entries = self.memory_index.get("context_entries", [])[-10:]
        recent_decisions = list(self.memory_index.get("decisions", {}).values())[-5:]

        # Get active features
        active_features = [
            {"id": fid, **feature}
            for fid, feature in self.memory_index.get("features", {}).items()
            if feature.get("status") == "active"
        ]

        return {
            "statistics": asdict(self.memory_stats),
            "recent_activity": recent_entries,
            "recent_decisions": recent_decisions,
            "active_features": active_features,
            "categories": list(set(entry.get("category") for entry in self.memory_index.get("context_entries", []))),
            "last_updated": datetime.now().isoformat()
        }

    def cleanup_old_entries(self, days: int = 90) -> int:
        """Clean up old memory entries"""

        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_iso = cutoff_date.isoformat()

        removed_count = 0

        # Clean old context entries
        original_entries = len(self.memory_index.get("context_entries", []))
        self.memory_index["context_entries"] = [
            entry for entry in self.memory_index.get("context_entries", [])
            if entry.get("timestamp", "") > cutoff_iso
        ]
        removed_count += original_entries - len(self.memory_index["context_entries"])

        # Clean old completed features
        original_features = len(self.memory_index.get("features", {}))
        self.memory_index["features"] = {
            fid: feature for fid, feature in self.memory_index.get("features", {}).items()
            if feature.get("status") != "completed" or feature.get("last_updated", "") > cutoff_iso
        }
        removed_count += original_features - len(self.memory_index["features"])

        # Save changes
        if removed_count > 0:
            self._save_memory_index()
            self.memory_stats = self._calculate_memory_stats()
            self._save_memory_stats()

        return removed_count

    def validate_memory_structure(self) -> List[str]:
        """Validate memory system structure and return issues"""

        issues = []

        # Check required files
        required_files = [self.context_file, self.decisions_file, self.memory_index_path]
        for file_path in required_files:
            if not file_path.exists():
                issues.append(f"Missing required file: {file_path}")

        # Check memory index structure
        required_keys = ["features", "decisions", "context_entries", "categories"]
        for key in required_keys:
            if key not in self.memory_index:
                issues.append(f"Missing key in memory index: {key}")

        # Check for orphaned entries
        context_features = set()
        for entry in self.memory_index.get("context_entries", []):
            if entry.get("feature_id"):
                context_features.add(entry.get("feature_id"))

        indexed_features = set(self.memory_index.get("features", {}).keys())
        orphaned_features = context_features - indexed_features
        if orphaned_features:
            issues.append(f"Orphaned feature references: {orphaned_features}")

        return issues

    def export_memory(self, format: str = "json", output_path: Optional[Path] = None) -> str:
        """Export memory data in specified format"""

        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "memory_index": self.memory_index,
                "statistics": asdict(self.memory_stats),
                "context_content": self.context_file.read_text(encoding='utf-8'),
                "decisions_content": self.decisions_file.read_text(encoding='utf-8')
            }

            if format.lower() == "json":
                content = json.dumps(export_data, indent=2, ensure_ascii=False)
            elif format.lower() == "yaml":
                content = yaml.dump(export_data, default_flow_style=False, allow_unicode=True)
            else:
                raise ValidationError(f"Unsupported export format: {format}")

            if output_path:
                output_path.write_text(content, encoding='utf-8')
                return str(output_path)
            else:
                return content

        except Exception as e:
            raise ValidationError(f"Failed to export memory: {e}")

    # ==================== v1.7.0 Tag-Based Memory Methods ====================

    def add_decision(self, title: str, rationale: str, related_features: Optional[List[str]] = None) -> str:
        """Add a decision entry with auto-incrementing ID (v1.7.0).

        Args:
            title: Decision title
            rationale: Rationale for the decision
            related_features: List of related feature IDs

        Returns:
            Decision ID (e.g., "DEC-001")
        """
        try:
            # Get next decision ID
            decision_id = self._get_next_id("DEC")
            date_str = datetime.now().strftime("%Y-%m-%d")
            related_str = ", ".join(related_features) if related_features else "None"

            # Format entry
            entry_text = f"""
### {decision_id}: {title}
Rationale: {rationale}
Date: {date_str}
Related: {related_str}
"""

            # Append to context.md under Decisions section
            self._append_to_section("Decisions [tag:decision]", entry_text)

            self.console.success(f"Decision added: {decision_id}")
            return decision_id

        except Exception as e:
            self.console.error(f"Failed to add decision: {e}")
            raise ValidationError(f"Failed to add decision: {e}")

    def add_pattern(self, title: str, example: str, features_used: Optional[List[str]] = None) -> str:
        """Add a pattern entry with auto-incrementing ID (v1.7.0).

        Args:
            title: Pattern title
            example: Example code or description
            features_used: List of features where pattern is used

        Returns:
            Pattern ID (e.g., "PATTERN-001")
        """
        try:
            # Get next pattern ID
            pattern_id = self._get_next_id("PATTERN")
            date_str = datetime.now().strftime("%Y-%m-%d")

            # Truncate long examples
            if len(example) > 200:
                example = example[:197] + "..."

            features_str = ", ".join(features_used) if features_used else "None"

            # Format entry
            entry_text = f"""
### {pattern_id}: {title}
{example}
Used in: {features_str}
Date: {date_str}
"""

            # Append to context.md under Patterns section
            self._append_to_section("Patterns [tag:pattern]", entry_text)

            self.console.success(f"Pattern added: {pattern_id}")
            return pattern_id

        except Exception as e:
            self.console.error(f"Failed to add pattern: {e}")
            raise ValidationError(f"Failed to add pattern: {e}")

    def add_constraint(self, title: str, description: str, scope: str = "All features") -> str:
        """Add a constraint entry with auto-incrementing ID (v1.7.0).

        Args:
            title: Constraint title
            description: Constraint description
            scope: Scope of constraint (default: "All features")

        Returns:
            Constraint ID (e.g., "CONST-001")
        """
        try:
            # Get next constraint ID
            const_id = self._get_next_id("CONST")
            date_str = datetime.now().strftime("%Y-%m-%d")

            # Format entry
            entry_text = f"""
### {const_id}: {title}
{description}
Applies to: {scope}
Date: {date_str}
"""

            # Append to context.md under Constraints section
            self._append_to_section("Constraints [tag:constraint]", entry_text)

            self.console.success(f"Constraint added: {const_id}")
            return const_id

        except Exception as e:
            self.console.error(f"Failed to add constraint: {e}")
            raise ValidationError(f"Failed to add constraint: {e}")

    def query_by_tag(self, tag: str, feature: Optional[str] = None, recent: Optional[int] = None) -> List[MemoryEntry]:
        """Query memory entries by tag (v1.7.0).

        Args:
            tag: Tag to query (decision, pattern, current, constraint)
            feature: Optional feature ID filter
            recent: Optional limit to recent N entries

        Returns:
            List of MemoryEntry objects
        """
        supported_tags = {"decision", "pattern", "current", "constraint"}
        if tag not in supported_tags:
            raise ValueError(f"Unsupported tag: {tag}. Must be one of {supported_tags}")

        entries = self._parse_tagged_section(tag)

        # Filter by feature if specified
        if feature:
            entries = [e for e in entries if feature in e.related_features]

        # Sort by date (newest first)
        entries.sort(key=lambda e: e.date, reverse=True)

        # Limit to recent if specified
        if recent:
            entries = entries[:recent]

        return entries

    def query_relevant(self, feature_id: str) -> List[MemoryEntry]:
        """Get all relevant memory entries for a feature (v1.7.0).

        Args:
            feature_id: Feature ID (e.g., "001")

        Returns:
            List of relevant MemoryEntry objects
        """
        all_entries = []

        # Query all tags for this feature
        for tag in ["decision", "pattern", "current", "constraint"]:
            entries = self.query_by_tag(tag, feature=feature_id)
            all_entries.extend(entries)

        return all_entries

    def _get_next_id(self, prefix: str) -> str:
        """Get next auto-incrementing ID for a prefix.

        Args:
            prefix: ID prefix (DEC, PATTERN, CONST)

        Returns:
            Next ID (e.g., "DEC-002")
        """
        content = self.context_file.read_text(encoding='utf-8') if self.context_file.exists() else ""

        # Find all IDs with this prefix
        pattern = rf'### {prefix}-(\d+):'
        matches = re.findall(pattern, content)

        if matches:
            max_num = max(int(m) for m in matches)
            next_num = max_num + 1
        else:
            next_num = 1

        return f"{prefix}-{next_num:03d}"

    def _append_to_section(self, section_header: str, content: str) -> None:
        """Append content to a specific section in context.md.

        Args:
            section_header: Section header to append to
            content: Content to append
        """
        if not self.context_file.exists():
            self._initialize_tagged_memory()

        file_content = self.context_file.read_text(encoding='utf-8')

        # Find the section
        section_pattern = rf'(## {re.escape(section_header)})'
        if not re.search(section_pattern, file_content):
            # Add section if it doesn't exist
            file_content += f"\n\n## {section_header}\n"

        # Find where to insert (after section header, before next section)
        parts = re.split(rf'(## {re.escape(section_header)})', file_content)

        if len(parts) >= 3:
            # parts[0] = before section
            # parts[1] = section header
            # parts[2] = section content + rest

            # Find next section in parts[2]
            next_section = re.search(r'\n## ', parts[2])
            if next_section:
                section_content = parts[2][:next_section.start()]
                rest = parts[2][next_section.start():]
                new_content = parts[0] + parts[1] + section_content + content + rest
            else:
                new_content = parts[0] + parts[1] + parts[2] + content
        else:
            new_content = file_content + content

        self.context_file.write_text(new_content, encoding='utf-8')

    def _parse_tagged_section(self, tag: str) -> List[MemoryEntry]:
        """Parse entries from a tagged section.

        Args:
            tag: Tag to parse (decision, pattern, constraint, current)

        Returns:
            List of MemoryEntry objects
        """
        if not self.context_file.exists():
            return []

        content = self.context_file.read_text(encoding='utf-8')
        entries = []

        # Find section for this tag
        section_pattern = rf'## .+? \[tag:{tag}\]$(.*?)(?=^## |\Z)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)

        if not section_match:
            return []

        section_content = section_match.group(1)

        # Parse individual entries (### headers)
        entry_pattern = re.compile(r'^### (.+?)$(.*?)(?=^### |\Z)', re.MULTILINE | re.DOTALL)

        for match in entry_pattern.finditer(section_content):
            header = match.group(1).strip()
            body = match.group(2).strip()

            # Extract ID and title
            id_title_match = re.match(r'([A-Z]+-\d+):\s*(.+)', header)
            if id_title_match:
                entry_id = id_title_match.group(1)
                title = id_title_match.group(2)
            else:
                continue

            # Extract metadata
            related = self._extract_field(body, "Related")
            date = self._extract_field(body, "Date")

            related_features = []
            if related and related != "None":
                # Extract feature IDs (001, 002, etc.)
                related_features = re.findall(r'\b(\d{3})\b', related)

            entry = MemoryEntry(
                id=entry_id,
                title=title,
                content=body,
                tags=[tag],
                date=date or datetime.now().strftime("%Y-%m-%d"),
                related_features=related_features
            )
            entries.append(entry)

        return entries

    def _extract_field(self, content: str, field_name: str) -> Optional[str]:
        """Extract a field value from entry content.

        Args:
            content: Entry content
            field_name: Field name to extract

        Returns:
            Field value or None
        """
        pattern = rf'{field_name}:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _initialize_tagged_memory(self) -> None:
        """Initialize context.md with tagged structure for v1.7.0."""
        template = """# Memory: Context

## Active [tag:current]
<!-- Current feature and project state -->

## Decisions [tag:decision]
<!-- Architectural decisions with rationale -->

## Patterns [tag:pattern]
<!-- Code patterns and conventions -->

## Constraints [tag:constraint]
<!-- Technical constraints and requirements -->
"""
        self.context_file.write_text(template, encoding='utf-8')

    # ==================== Migration Methods (v1.7.0) ====================

    def needs_migration(self) -> bool:
        """Check if context.md needs migration to tagged format.

        Returns:
            True if migration needed, False otherwise
        """
        if not self.context_file.exists():
            return False

        content = self.context_file.read_text(encoding='utf-8')

        # Check for tag headers
        has_tags = bool(re.search(r'\[tag:\w+\]', content))

        return not has_tags

    def migrate_to_tagged_format(self, dry_run: bool = False) -> Dict[str, Any]:
        """Migrate old context.md to tagged format.

        Args:
            dry_run: If True, don't actually migrate, just report what would happen

        Returns:
            Migration report dictionary
        """
        if not self.context_file.exists():
            raise FileNotFoundError("context.md not found")

        if not self.needs_migration():
            return {
                "status": "no_migration_needed",
                "message": "Context file already uses tagged format"
            }

        # Read original content
        original_content = self.context_file.read_text(encoding='utf-8')
        original_lines = len(original_content.splitlines())

        # Create backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.context_file.parent / f"context.md.backup.{timestamp}"

        if not dry_run:
            backup_path.write_text(original_content, encoding='utf-8')

        # Categorize content
        categorized = self._categorize_content(original_content)

        # Build new content
        new_content = self._build_tagged_content(categorized)

        # Validate migration
        new_lines = len(new_content.splitlines())

        report = {
            "status": "success" if not dry_run else "dry_run",
            "backup_path": str(backup_path) if not dry_run else None,
            "original_lines": original_lines,
            "new_lines": new_lines,
            "categorized": {
                "decisions": len(categorized["decisions"]),
                "patterns": len(categorized["patterns"]),
                "constraints": len(categorized["constraints"]),
                "current": len(categorized["current"]),
                "uncategorized": len(categorized["uncategorized"])
            }
        }

        # Write new content
        if not dry_run:
            self.context_file.write_text(new_content, encoding='utf-8')

        return report

    def rollback_migration(self, backup_path: Optional[Path] = None) -> bool:
        """Rollback migration by restoring from backup.

        Args:
            backup_path: Path to backup file (auto-detect latest if None)

        Returns:
            True if rollback successful
        """
        if backup_path is None:
            # Find latest backup
            backups = sorted(self.context_file.parent.glob("context.md.backup.*"), reverse=True)
            if not backups:
                raise FileNotFoundError("No backup files found")
            backup_path = backups[0]

        backup_path = Path(backup_path)

        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")

        # Restore from backup
        backup_content = backup_path.read_text(encoding='utf-8')
        self.context_file.write_text(backup_content, encoding='utf-8')

        return True

    def _categorize_content(self, content: str) -> Dict[str, List[str]]:
        """Categorize content using heuristics.

        Args:
            content: Original content to categorize

        Returns:
            Dictionary with categorized entries
        """
        categorized = {
            "decisions": [],
            "patterns": [],
            "constraints": [],
            "current": [],
            "uncategorized": []
        }

        # Split into sections by headers
        sections = re.split(r'^## (.+?)$', content, flags=re.MULTILINE)

        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break

            header = sections[i].strip()
            section_content = sections[i + 1].strip()

            if not section_content:
                continue

            # Categorize based on header and content
            category = self._detect_category(header, section_content)
            categorized[category].append({
                "header": header,
                "content": section_content
            })

        return categorized

    def _detect_category(self, header: str, content: str) -> str:
        """Detect category for a section.

        Args:
            header: Section header
            content: Section content

        Returns:
            Category name (decision, pattern, constraint, current, uncategorized)
        """
        header_lower = header.lower()
        content_lower = content.lower()

        # Decision keywords
        if any(kw in header_lower or kw in content_lower for kw in [
            "decision", "decided", "adr", "architecture decision", "chose", "selected"
        ]):
            return "decisions"

        # Pattern keywords
        if any(kw in header_lower or kw in content_lower for kw in [
            "pattern", "convention", "standard", "format", "template"
        ]):
            return "patterns"

        # Constraint keywords
        if any(kw in header_lower or kw in content_lower for kw in [
            "constraint", "limitation", "requirement", "must", "shall", "restriction"
        ]):
            return "constraints"

        # Current/active keywords
        if any(kw in header_lower for kw in [
            "active", "current", "status", "state", "progress"
        ]):
            return "current"

        return "uncategorized"

    def _build_tagged_content(self, categorized: Dict[str, List[str]]) -> str:
        """Build tagged content from categorized sections.

        Args:
            categorized: Categorized content dictionary

        Returns:
            New content with tagged format
        """
        parts = ["# Memory: Context\n"]

        # Add Current section
        parts.append("\n## Active [tag:current]")
        if categorized["current"]:
            for item in categorized["current"]:
                parts.append(f"\n### {item['header']}")
                parts.append(item['content'])
        else:
            parts.append("<!-- Current feature and project state -->\n")

        # Add Decisions section
        parts.append("\n## Decisions [tag:decision]")
        if categorized["decisions"]:
            for idx, item in enumerate(categorized["decisions"], 1):
                parts.append(f"\n### DEC-{idx:03d}: {item['header']}")
                parts.append(item['content'])
                if "date" not in item['content'].lower():
                    parts.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
                if "related" not in item['content'].lower():
                    parts.append("Related: None")
        else:
            parts.append("<!-- Architectural decisions with rationale -->\n")

        # Add Patterns section
        parts.append("\n## Patterns [tag:pattern]")
        if categorized["patterns"]:
            for idx, item in enumerate(categorized["patterns"], 1):
                parts.append(f"\n### PATTERN-{idx:03d}: {item['header']}")
                parts.append(item['content'])
                if "used in" not in item['content'].lower():
                    parts.append("Used in: None")
                if "date" not in item['content'].lower():
                    parts.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        else:
            parts.append("<!-- Code patterns and conventions -->\n")

        # Add Constraints section
        parts.append("\n## Constraints [tag:constraint]")
        if categorized["constraints"]:
            for idx, item in enumerate(categorized["constraints"], 1):
                parts.append(f"\n### CONST-{idx:03d}: {item['header']}")
                parts.append(item['content'])
                if "applies to" not in item['content'].lower():
                    parts.append("Applies to: All features")
                if "date" not in item['content'].lower():
                    parts.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        else:
            parts.append("<!-- Technical constraints and requirements -->\n")

        # Add uncategorized at the end
        if categorized["uncategorized"]:
            parts.append("\n## Other Notes")
            for item in categorized["uncategorized"]:
                parts.append(f"\n### {item['header']}")
                parts.append(item['content'])

        return "\n".join(parts)