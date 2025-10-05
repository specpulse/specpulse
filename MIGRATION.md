# Migration Guide: v1.7.0 Context System

## Overview

v1.7.0 introduces a tagged memory system that requires migration from the old unstructured `context.md` format. This document covers the migration process and edge cases discovered during testing.

## Automatic Migration

### Running Migration

```bash
# Preview migration (dry run)
specpulse memory migrate --dry-run

# Execute migration
specpulse memory migrate
```

The migration:
1. Creates backup: `memory/context.md.backup.{timestamp}`
2. Categorizes existing content using keyword heuristics
3. Restructures with tagged sections: `[tag:decision]`, `[tag:pattern]`, etc.
4. Preserves ALL original content

### Rollback

If migration doesn't work as expected:

```bash
# Rollback to latest backup
specpulse memory rollback

# Rollback to specific backup
specpulse memory rollback --backup memory/context.md.backup.20241006_120000
```

## Edge Cases Discovered

### 1. Empty Context Files
**Issue**: Empty or minimal context.md files
**Solution**: Migration creates default tagged structure

### 2. Uncategorized Content
**Issue**: Content that doesn't match decision/pattern/constraint keywords
**Solution**: Placed in "Other Notes" section at end

### 3. Multi-line Content with Code Blocks
**Issue**: Code blocks in patterns could break parsing
**Solution**: Pattern matching uses DOTALL regex, preserves formatting

### 4. Mixed Language Projects
**Issue**: pyproject.toml + package.json in same project
**Solution**: Auto-detect merges both, prioritizes most recent file

### 5. Feature ID Extraction
**Issue**: Feature IDs in various formats ("001", "001-feature", "Feature 001")
**Solution**: Regex extracts 3-digit IDs: `\b(\d{3})\b`

## Testing Checklist

Tested on 3 types of projects:

### Minimal Project (New SpecPulse Init)
- ✅ Empty context.md migrates to tagged structure
- ✅ No data loss
- ✅ All commands work after migration

### Standard Project (Active Development)
- ✅ 5-10 existing sections categorized correctly
- ✅ Decisions identified by keywords: "decided", "chose", "selected"
- ✅ Patterns identified by keywords: "convention", "standard", "format"
- ✅ Content preserved exactly

### Complex Project (Production)
- ✅ 20+ sections with mixed content
- ✅ Code blocks in patterns preserved
- ✅ Multi-feature relationships maintained
- ✅ Performance under 2 seconds for migration

## Manual Migration Steps

If automatic migration fails, follow these steps:

1. **Backup manually**:
   ```bash
   cp memory/context.md memory/context.md.backup.manual
   ```

2. **Create tagged structure**:
   ```markdown
   # Memory: Context

   ## Active [tag:current]
   [Current feature info]

   ## Decisions [tag:decision]

   ### DEC-001: [Your decision title]
   Rationale: [Why this decision was made]
   Date: YYYY-MM-DD
   Related: [Feature IDs]

   ## Patterns [tag:pattern]

   ### PATTERN-001: [Pattern title]
   [Pattern description or code example]
   Used in: [Feature IDs]
   Date: YYYY-MM-DD

   ## Constraints [tag:constraint]

   ### CONST-001: [Constraint title]
   [Constraint description]
   Applies to: [Scope]
   Date: YYYY-MM-DD
   ```

3. **Categorize existing content**:
   - Move architectural decisions → Decisions section
   - Move code patterns/conventions → Patterns section
   - Move requirements/limitations → Constraints section
   - Move active feature info → Active section

4. **Add required metadata**:
   - Ensure each entry has Date, Related/Used in/Applies to fields
   - Use auto-incrementing IDs: DEC-001, PATTERN-001, etc.

## Validation

After migration, verify:

```bash
# Query decisions
specpulse memory query --tag decision

# Query patterns
specpulse memory query --tag pattern

# Check relevant memory for a feature
specpulse memory relevant 001
```

All queries should return properly formatted entries.

## Known Limitations

1. **Keyword-based categorization**: Some content may be miscategorized. Review and adjust manually if needed.
2. **Date detection**: If no date found in original content, uses current date.
3. **Feature relationships**: Only extracts 3-digit IDs. Other formats may be missed.
4. **Backup retention**: Backups are NOT auto-deleted. Clean up old backups manually.

## Support

If migration fails or produces unexpected results:
1. Check backup exists in `memory/`
2. Rollback using `specpulse memory rollback`
3. Report issue with backup file attached
4. Try manual migration steps above
