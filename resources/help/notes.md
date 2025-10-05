# Quick Notes (v1.7.0)

## Overview

Capture development insights quickly without breaking flow. Notes can be reviewed later and merged into specifications.

## Workflow

### During Development

```bash
# Quick insight capture
specpulse note "Stripe webhooks require HTTPS in production" --feature 003

specpulse note "Rate limit: 100 req/min per user" --feature 003

specpulse note "Consider pagination for large datasets"
# Auto-detects current feature from context
```

### Review Notes

```bash
# List notes for current feature
specpulse notes list

# List notes for specific feature
specpulse notes list 003

# Output:
# ID              Timestamp        Preview                    Status
# 20241006120000  2024-10-06 12:00 Stripe webhooks require... Active
# 20241006130000  2024-10-06 13:00 Rate limit: 100 req/min... Active
```

### Merge to Spec

```bash
# Auto-detect section
specpulse notes merge 003 --note 20241006120000

# Specify section
specpulse notes merge 003 --note 20241006130000 --section "Performance Requirements"
```

## Section Auto-Detection

Notes are auto-merged to appropriate spec sections based on keywords:

| Keywords | Target Section |
|----------|---------------|
| security, auth, permission | Security Considerations |
| performance, speed, optimize | Performance Requirements |
| constraint, limitation, requirement | Technical Constraints |
| risk, issue, concern | Risks and Mitigations |
| (default) | Additional Notes |

## Note Format

Notes are stored in `memory/notes/{feature_id}.md`:

```markdown
### Note 20241006120000
Timestamp: 2024-10-06 12:00:00
Status: Active

Stripe webhooks require HTTPS in production

---
```

After merging, status changes to `Merged`.

## Commands

### Add Note

```bash
specpulse note "message" [--feature 001]
```

- Auto-detects current feature from `memory/context.md` if not specified
- Returns note ID (timestamp-based)

### List Notes

```bash
specpulse notes list [feature_id]
```

- Shows ID, timestamp, preview, status
- Highlights merged vs active notes
- Counts unmerged notes

### Merge Note

```bash
specpulse notes merge feature_id --note note_id [--section "Section Name"]
```

- Merges note content into latest spec file
- Auto-detects appropriate section if not specified
- Marks note as merged
- Adds comment: `<!-- Merged from note {id} -->`

## Use Cases

### Capture Technical Debt

```bash
specpulse note "TODO: Refactor payment validation logic" --feature 003
```

### Document Discoveries

```bash
specpulse note "API returns 429 after 100 requests, need exponential backoff"
```

### Security Findings

```bash
specpulse note "Must validate JWT signature on all protected routes"
# Merges to "Security Considerations" automatically
```

### Performance Observations

```bash
specpulse note "Database query taking 2s, needs index on user_id column"
# Merges to "Performance Requirements" automatically
```

## Integration with Status

```bash
specpulse sync
# Shows: "Unmerged Notes: 3 notes" if notes exist
```

Reminds you to review and merge notes before completing features.

## Tips

- **Note early, merge later**: Don't interrupt coding flow
- **Review regularly**: Use `specpulse notes list` after coding sessions
- **Merge important insights**: Keep specs up-to-date with learnings
- **Use descriptive content**: Makes merging easier later
