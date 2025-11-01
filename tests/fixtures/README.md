# Test Fixtures for SpecPulse v1.7.0

This directory contains test fixtures for validating v1.7.0 features.

## Files

### context.md
Sample .specpulse/memory/context.md file with tagged entries:
- 1 current entry
- 3 decisions (DEC-001, DEC-002, DEC-003)
- 2 patterns (PATTERN-001, PATTERN-002)
- 2 constraints (CONST-001, CONST-002)

### project_context.yaml
Sample project context with:
- Project info (name, type, description, version)
- Full tech stack (frontend, backend, database, cache, message_queue)
- Team size (1)
- 5 development preferences

### notes/
Sample notes for 3 features:
- `001-feature.md`: 3 notes (2 active, 1 merged)
- `002-feature.md`: 2 notes (2 active)
- `003-feature.md`: 1 note (1 active)

## Usage in Tests

```python
import pytest
from pathlib import Path

@pytest.fixture
def fixture_dir():
    return Path(__file__).parent / "fixtures"

@pytest.fixture
def sample_context(fixture_dir):
    return (fixture_dir / "context.md").read_text()

@pytest.fixture
def sample_project_context(fixture_dir):
    return fixture_dir / "project_context.yaml"

@pytest.fixture
def sample_notes_dir(fixture_dir):
    return fixture_dir / "notes"
```

## Edge Cases Covered

- **Empty sections**: No entries in a tagged section
- **Malformed entries**: Missing fields, invalid dates
- **Merged vs Active**: Notes with different statuses
- **Feature relationships**: Decisions/patterns related to multiple features
- **Complex tech stack**: Multiple technologies per category
