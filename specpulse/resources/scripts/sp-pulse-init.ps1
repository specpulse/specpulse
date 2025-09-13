# SpecPulse Feature Initialization - PowerShell Version
# Initialize a new feature with SpecPulse

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$FeatureName,

    [Parameter(Mandatory=$false, Position=1)]
    [string]$CustomId
)

# Configuration
$ScriptName = Split-Path -Leaf $PSCommandPath
$ScriptDir = Split-Path -Parent $PSCommandPath
$ProjectRoot = Split-Path -Parent $ScriptDir

# Logging function
function Log-Message {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] ${ScriptName}: $Message" -ForegroundColor Cyan
}

# Error handling function
function Exit-WithError {
    param([string]$Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

# Sanitize feature name
$BranchSafeName = $FeatureName.ToLower() -replace '[^a-z0-9-]', '-' -replace '--+', '-' -replace '^-|-$', ''

if ([string]::IsNullOrEmpty($BranchSafeName)) {
    Exit-WithError "Invalid feature name: '$FeatureName'"
}

# Get feature ID
if ($CustomId) {
    $FeatureId = "{0:D3}" -f [int]$CustomId
} else {
    $existingDirs = Get-ChildItem -Path "$ProjectRoot\specs" -Directory -Filter "[0-9]*" -ErrorAction SilentlyContinue
    $nextId = if ($existingDirs) { $existingDirs.Count + 1 } else { 1 }
    $FeatureId = "{0:D3}" -f $nextId
}

$BranchName = "$FeatureId-$BranchSafeName"

# Create directories
$SpecsDir = Join-Path $ProjectRoot "specs\$BranchName"
$PlansDir = Join-Path $ProjectRoot "plans\$BranchName"
$TasksDir = Join-Path $ProjectRoot "tasks\$BranchName"

Log-Message "Creating feature directories for '$FeatureName'"

try {
    New-Item -ItemType Directory -Path $SpecsDir -Force | Out-Null
    New-Item -ItemType Directory -Path $PlansDir -Force | Out-Null
    New-Item -ItemType Directory -Path $TasksDir -Force | Out-Null
} catch {
    Exit-WithError "Failed to create directories: $_"
}

# Create initial files from templates
$TemplateDir = Join-Path $ProjectRoot "templates"

$specTemplate = Join-Path $TemplateDir "spec.md"
$planTemplate = Join-Path $TemplateDir "plan.md"
$taskTemplate = Join-Path $TemplateDir "task.md"

if (-not (Test-Path $specTemplate)) {
    Exit-WithError "Template not found: $specTemplate"
}

try {
    Copy-Item -Path $specTemplate -Destination "$SpecsDir\spec-$FeatureId.md" -Force
    Copy-Item -Path $planTemplate -Destination "$PlansDir\plan-$FeatureId.md" -Force
    Copy-Item -Path $taskTemplate -Destination "$TasksDir\task-$FeatureId.md" -Force
} catch {
    Exit-WithError "Failed to copy templates: $_"
}

# Update context
$ContextFile = Join-Path $ProjectRoot "memory\context.md"
$memoryDir = Split-Path -Parent $ContextFile

if (-not (Test-Path $memoryDir)) {
    New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null
}

$contextEntry = @"

## Active Feature: $FeatureName
- Feature ID: $FeatureId
- Branch: $BranchName
- Started: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
"@

try {
    Add-Content -Path $ContextFile -Value $contextEntry
} catch {
    Exit-WithError "Failed to update context file: $_"
}

# Create git branch if in git repo
$gitDir = Join-Path $ProjectRoot ".git"
if (Test-Path $gitDir) {
    Push-Location $ProjectRoot
    try {
        $branchExists = git rev-parse --verify $BranchName 2>$null
        if ($LASTEXITCODE -eq 0) {
            Log-Message "Git branch '$BranchName' already exists, checking out"
            git checkout $BranchName | Out-Null
        } else {
            Log-Message "Creating new git branch '$BranchName'"
            git checkout -b $BranchName | Out-Null
        }
    } catch {
        Log-Message "Warning: Git operations failed: $_"
    } finally {
        Pop-Location
    }
}

Log-Message "Successfully initialized feature '$FeatureName' with ID $FeatureId"

# Output results
Write-Output "BRANCH_NAME=$BranchName"
Write-Output "SPEC_DIR=$SpecsDir"
Write-Output "FEATURE_ID=$FeatureId"
Write-Output "STATUS=initialized"