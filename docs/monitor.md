# Task Monitor Documentation

## Overview

The SpecPulse Task Monitor provides comprehensive task progress tracking and analytics for SpecPulse projects. It automatically monitors task states, calculates progress percentages, and provides detailed insights into development workflow.

## Features

### Core Monitoring
- **Real-time Progress Tracking**: Automatic task state discovery and monitoring
- **Progress Calculation**: Percentage-based progress with visual indicators
- **State Management**: Track tasks through PENDING → IN_PROGRESS → COMPLETED/BLOCKED states
- **Historical Tracking**: Complete audit trail of task state changes

### Analytics & Insights
- **Trend Analysis**: Progress velocity and completion rate trends
- **Performance Metrics**: Execution time tracking and bottleneck identification
- **Health Scoring**: Overall project health assessment
- **Predictive Analytics**: Estimated completion times based on historical data

### CLI Integration
- **Non-intrusive**: Seamlessly integrates with existing SpecPulse CLI
- **Rich Terminal Output**: Beautiful progress bars and tables (with Rich library)
- **Fallback Support**: Plain text output for terminals without Rich support
- **Auto-discovery**: Automatically finds tasks from markdown files

## Installation

The Task Monitor is included with SpecPulse v2.6.0+. No additional installation required.

## Quick Start

### Basic Usage

```bash
# Show current task status
specpulse monitor status

# Show detailed progress analytics
specpulse monitor progress

# Show task history
specpulse monitor history

# Reset monitoring data
specpulse monitor reset --confirm
```

### Advanced Usage

```bash
# Monitor specific feature
specpulse monitor status --feature 001-user-auth

# Show verbose task details
specpulse monitor status --verbose

# Show detailed analytics with trends
specpulse monitor progress --detailed

# Show last 50 history entries
specpulse monitor history --limit 50

# Validate monitoring data integrity
specpulse monitor validate
```

## Commands Reference

### `specpulse monitor status`

Display current task status and progress information.

**Usage:**
```bash
specpulse monitor status [--feature FEATURE_ID] [--verbose]
```

**Options:**
- `--feature, -f`: Monitor specific feature (auto-discovered if not specified)
- `--verbose, -v`: Show detailed task information

**Output:**
- Task counts by state (pending, in-progress, completed, blocked)
- Progress percentage with visual progress bar
- Task details table (in verbose mode)
- Issues and warnings

**Example:**
```bash
$ specpulse monitor status --verbose

╭──────────────────────────────────────────────────────────────────────╮
│                     Task Monitor Status - Feature 001-task-monitor    │
╰──────────────────────────────────────────────────────────────────────╯

┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                  ┃ Value                                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Tasks             │ 12                                              │
│ Completed               │ 8                                               │
│ In Progress             │ 2                                               │
│ Blocked                 │ 1                                               │
│ Pending                 │ 1                                               │
│ Progress                │ ████████████████████░░░░░ 66.7%                  │
└─────────────────────────┴──────────────────────────────────────────────────┘
```

### `specpulse monitor progress`

Show detailed progress analytics and trends.

**Usage:**
```bash
specpulse monitor progress [--feature FEATURE_ID] [--detailed]
```

**Options:**
- `--feature, -f`: Analyze specific feature (auto-discovered if not specified)
- `--detailed, -d`: Show detailed analytics and trends

**Output:**
- Current progress metrics
- Historical trend analysis
- Performance metrics
- Completion predictions

**Example:**
```bash
$ specpulse monitor progress --detailed

╭──────────────────────────────────────────────────────────────────────╮
│                        Progress Analytics                             │
╰──────────────────────────────────────────────────────────────────────╯

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                         ┃ Value                                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Completion                    │ 66.7%                                           │
│ Completed Tasks               │ 8/12                                            │
│ Remaining Tasks               │ 4                                               │
│ Work Remaining                │ 0.5x current progress                           │
└───────────────────────────────┴──────────────────────────────────────────────────┘
```

### `specpulse monitor history`

Display historical task state changes.

**Usage:**
```bash
specpulse monitor history [--feature FEATURE_ID] [--limit LIMIT]
```

**Options:**
- `--feature, -f`: Show history for specific feature (auto-discovered if not specified)
- `--limit, -l`: Maximum number of history entries (default: 20)

**Output:**
- Timestamped task state changes
- State transitions (PENDING → IN_PROGRESS → COMPLETED)
- Error messages and notes

### `specpulse monitor reset`

Reset monitoring data for a feature.

**Usage:**
```bash
specpulse monitor reset [--feature FEATURE_ID] --confirm
```

**Options:**
- `--feature, -f`: Reset specific feature (auto-discovered if not specified)
- `--confirm`: Confirm the reset operation

**Warning:** This will permanently delete all monitoring data for the specified feature.

### `specpulse monitor validate`

Validate monitoring data integrity.

**Usage:**
```bash
specpulse monitor validate
```

**Output:**
- Data integrity report
- File validation status
- Issues and recommendations

## Task Discovery

The monitor automatically discovers tasks from your `.specpulse/tasks/` directory:

### Supported Task Formats

1. **Task Files**: `task-001.md`, `task-002.md`, etc.
2. **Service Tasks**: `auth-service-tasks.md`, `user-service-tasks.md`
3. **Integration Tasks**: `integration-tasks.md`

### Task State Detection

The monitor parses task files and determines states based on:

- **Checkboxes**: `- [x]` for completed, `- [>]` for in-progress, `- [!]` for blocked
- **Keywords**: "error", "failed", "exception" indicate blocked state
- **Default**: Tasks without explicit state markers are considered pending

### Task Metadata Extraction

- **Task ID**: Extracted from filename or content (T001, AUTH-T001, etc.)
- **Title**: Extracted from headings or content
- **Description**: First paragraph after title
- **State**: Determined from checkbox patterns

## Configuration

### Monitor Configuration

The monitor uses a configuration file at `.specpulse/memory/monitor-config.json`:

```json
{
  "auto_discovery": true,
  "history_retention_days": 30,
  "max_tasks_per_feature": 1000,
  "progress_calculation_method": "simple",
  "backup_enabled": true,
  "max_backups": 5,
  "update_interval_seconds": 60
}
```

### Configuration Options

- `auto_discovery`: Automatically discover tasks from files
- `history_retention_days`: How long to keep historical data
- `max_tasks_per_feature`: Maximum tasks per feature for performance
- `progress_calculation_method`: "simple", "weighted", or "trending"
- `backup_enabled`: Create automatic backups of state files
- `max_backups`: Number of backups to retain
- `update_interval_seconds`: Cache refresh interval

## Data Storage

### File Structure

```
.specpulse/
├── memory/
│   ├── task-states.json      # Current task states
│   ├── task-progress.json    # Progress data
│   ├── task-history.json     # Historical changes
│   ├── monitor-config.json   # Monitor configuration
│   └── workflow-log.json     # Workflow events
└── tasks/
    └── XXX-feature/          # Task files (read-only)
```

### Data Format

#### Task States
```json
{
  "tasks": {
    "001-task-monitor": {
      "T001": {
        "id": "T001",
        "title": "Create Core Data Models",
        "state": "completed",
        "last_updated": "2025-11-12T02:01:00",
        "execution_time": 0.25,
        "description": "Implement data models..."
      }
    }
  },
  "metadata": {
    "last_updated": "2025-11-12T02:01:00"
  }
}
```

#### Progress Data
```json
{
  "features": {
    "001-task-monitor": {
      "total_tasks": 12,
      "completed_tasks": 8,
      "in_progress_tasks": 2,
      "blocked_tasks": 1,
      "pending_tasks": 1,
      "percentage": 66.7,
      "last_updated": "2025-11-12T02:01:00",
      "feature_id": "001-task-monitor"
    }
  }
}
```

## Integration with SpecPulse Workflow

### Automatic Integration

The monitor automatically integrates with SpecPulse commands:

- **Task Execution**: Automatically tracks state changes during `/sp-execute`
- **Progress Updates**: Updates progress when tasks complete
- **Error Handling**: Tracks blocked tasks with error messages

### Manual Integration

For custom workflows, use the Python API:

```python
from specpulse.monitor.integration import get_integration, monitor_command_execution

# Get integration instance
integration = get_integration(Path.cwd())

# Start monitoring a task
integration.start_task_monitoring("001-feature", "T001")

# Complete a task
integration.complete_task_monitoring("001-feature", "T001", execution_time=0.5)

# Block a task with error
integration.block_task_monitoring("001-feature", "T002", "Connection failed")

# Or use the decorator
@monitor_command_execution(feature_id="001-feature", task_id="T003")
def my_task_function():
    # Your task implementation
    pass
```

## Performance and Limitations

### Performance Characteristics

- **Memory Usage**: <50MB for typical projects (1000 tasks max)
- **Response Time**: <3 seconds for CLI commands
- **File I/O**: Efficient JSON storage with lazy loading
- **Scalability**: Optimized for projects with up to 1000 tasks

### Known Limitations

1. **Task Discovery**: Only monitors tasks in `.specpulse/tasks/` directory
2. **File Format**: Limited to markdown task files
3. **Real-time Updates**: No real-time updates between CLI runs
4. **Concurrent Access**: Limited support for simultaneous monitoring

### Troubleshooting

#### Common Issues

**Monitor shows "No active features found"**
- Ensure you're in a SpecPulse project directory
- Check that `.specpulse/memory/context.md` exists
- Initialize a feature with `specpulse feature init <name>`

**Tasks not being discovered**
- Verify task files are in `.specpulse/tasks/XXX-feature/` directory
- Check task files follow naming convention (`task-XXX.md`)
- Ensure tasks have proper markdown structure

**Progress calculations seem incorrect**
- Run `specpulse monitor validate` to check data integrity
- Verify task states are properly marked in files
- Check for duplicate task IDs

**Performance is slow**
- Reduce `max_tasks_per_feature` in configuration
- Clean up old history with shorter `history_retention_days`
- Use `--no-color` flag for faster terminal output

#### Error Recovery

**Corrupted state files**
```bash
# Validate and report issues
specpulse monitor validate

# Reset monitoring data if needed
specpulse monitor reset --confirm
```

**Missing data after system crash**
```bash
# The monitor automatically creates backups
# Check .specpulse/memory/backups/ directory
# Restore from backup if needed
```

## API Reference

### Core Classes

#### `TaskStateManager`
Manages task state transitions and discovery.

```python
state_manager = TaskStateManager(storage, config)
tasks = state_manager.get_tasks("001-feature")
state_manager.update_task_state("001-feature", "T001", TaskState.COMPLETED)
```

#### `ProgressCalculator`
Calculates progress metrics and analytics.

```python
calculator = ProgressCalculator()
progress = calculator.calculate_progress(tasks, "001-feature")
trends = calculator.analyze_progress_trend(history)
```

#### `StatusDisplay`
Formats and displays monitoring information.

```python
display = StatusDisplay(no_color=False)
output = display.show_status(progress, tasks, verbose=True)
```

#### `StateStorage`
Handles data persistence and backup.

```python
storage = StateStorage(project_path)
storage.save_tasks(tasks, "001-feature")
progress = storage.load_progress("001-feature")
```

### Integration Hooks

#### `WorkflowIntegration`
Provides workflow integration capabilities.

```python
integration = WorkflowIntegration(project_path)
integration.start_task_monitoring("001-feature", "T001")
integration.complete_task_monitoring("001-feature", "T001", 0.5)
```

#### `MonitoringHooks`
Decorator-based task monitoring.

```python
hooks = MonitoringHooks(integration)

@hooks.monitor_task_execution("001-feature", "T001")
def my_function():
    pass
```

## Contributing

The Task Monitor is part of the SpecPulse project. Contributions are welcome!

### Development Setup

1. Clone the SpecPulse repository
2. Install development dependencies: `pip install -e .[dev]`
3. Run tests: `pytest tests/monitor/`
4. Check code quality: `flake8 specpulse/monitor/`

### Testing

```bash
# Run all monitor tests
pytest tests/monitor/

# Run with coverage
pytest tests/monitor/ --cov=specpulse.monitor

# Run performance tests
pytest tests/monitor/test_performance.py
```

## License

The Task Monitor is licensed under the same MIT License as SpecPulse.