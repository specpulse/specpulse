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


class MemoryManager:
    """Enhanced memory management system"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memory_dir = project_root / "memory"
        self.context_file = self.memory_dir / "context.md"
        self.decisions_file = self.memory_dir / "decisions.md"
        self.memory_index = self.memory_dir / ".memory_index.json"
        self.memory_stats = self.memory_dir / ".memory_stats.json"

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
        if self.memory_index.exists():
            try:
                with open(self.memory_index, 'r', encoding='utf-8') as f:
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
            with open(self.memory_index, 'w', encoding='utf-8') as f:
                json.dump(self.memory_index, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ValidationError(f"Failed to save memory index: {e}")

    def _load_memory_stats(self) -> MemoryStats:
        """Load memory statistics"""
        if self.memory_stats.exists():
            try:
                with open(self.memory_stats, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return MemoryStats(**data)
            except (json.JSONDecodeError, IOError, TypeError):
                pass

        # Calculate initial stats
        return self._calculate_memory_stats()

    def _save_memory_stats(self):
        """Save memory statistics"""
        try:
            with open(self.memory_stats, 'w', encoding='utf-8') as f:
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
- **Impact**: {entryimpact}
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
        required_files = [self.context_file, self.decisions_file, self.memory_index]
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