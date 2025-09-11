# /pulse

Initialize a new feature with SpecPulse framework.

## Usage
```
/pulse init <feature-name>
```

## Description
Creates a structured feature development environment with:
- Feature branch (git)
- Specification directory
- Plan directory
- Task directory
- Context updates

## Process
1. Creates feature ID (e.g., 001, 002)
2. Creates branch name (e.g., 001-user-auth)
3. Sets up directory structure
4. Switches to feature branch
5. Updates project context

## Output
Returns JSON with:
- branch_name: Created git branch
- feature_id: Numeric feature ID
- spec_dir: Specification directory path
- plan_dir: Plan directory path
- task_dir: Task directory path

## Example
```
/pulse init "user authentication"
```

Creates:
- Branch: 001-user-authentication
- Directories: specs/001-user-authentication/, etc.