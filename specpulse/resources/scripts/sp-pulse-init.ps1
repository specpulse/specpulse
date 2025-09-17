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

# Validate templates exist but don't copy them directly
$TemplateDir = Join-Path $ProjectRoot "templates"

# Validate all required templates exist
@("spec.md", "plan.md", "task.md") | ForEach-Object {
    $templatePath = Join-Path $TemplateDir $_
    if (-not (Test-Path $templatePath)) {
        Exit-WithError "Template not found: $templatePath. Please run 'specpulse init' to initialize templates."
    }
}

# Create marker files that indicate AI should use templates to generate content
# These are placeholder files that will be replaced by AI-generated content
try {
    $specContent = @"
# Specification for $FeatureName

<!-- INSTRUCTION: Generate specification content using template: $TemplateDir\spec.md -->
<!-- FEATURE_DIR: $BranchName -->
<!-- FEATURE_ID: $FeatureId -->
"@
    Set-Content -Path "$SpecsDir\spec-001.md" -Value $specContent

    $planContent = @"
# Implementation Plan for $FeatureName

<!-- INSTRUCTION: Generate plan using template: $TemplateDir\plan.md -->
<!-- SPEC_FILE: $SpecsDir\spec-001.md -->
<!-- FEATURE_DIR: $BranchName -->
<!-- FEATURE_ID: $FeatureId -->
"@
    Set-Content -Path "$PlansDir\plan-001.md" -Value $planContent

    $taskContent = @"
# Task Breakdown for $FeatureName

<!-- INSTRUCTION: Generate tasks using template: $TemplateDir\task.md -->
<!-- SPEC_FILE: $SpecsDir\spec-001.md -->
<!-- PLAN_FILE: $PlansDir\plan-001.md -->
<!-- FEATURE_DIR: $BranchName -->
<!-- FEATURE_ID: $FeatureId -->
"@
    Set-Content -Path "$TasksDir\task-001.md" -Value $taskContent
} catch {
    Exit-WithError "Failed to create marker files: $_"
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