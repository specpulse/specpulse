# SpecPulse Feature Initialization - PowerShell Version
# Initialize a new feature with SpecPulse

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$FeatureName,

    [Parameter(Mandatory=$false, Position=1)]
    [string]$CustomId,

    [Parameter(Mandatory=$false)]
    [switch]$Help,

    [Parameter(Mandatory=$false)]
    [switch]$Version,

    [Parameter(Mandatory=$false)]
    [switch]$VerboseMode
)

# Import common utilities
$ScriptDir = Split-Path -Parent $PSCommandPath
$utilsPath = Join-Path $ScriptDir "script_utils.ps1"

if (Test-Path $utilsPath) {
    . $utilsPath
} else {
    Write-Host "ERROR: Script utilities not found at $utilsPath" -ForegroundColor Red
    exit 1
}

# Configuration
$ScriptName = Split-Path -Leaf $PSCommandPath
$ProjectRoot = Split-Path -Parent $ScriptDir

# Initialize script environment with error handling and rollback support
Initialize-ScriptEnvironment -ScriptName $ScriptName -ScriptDir $ScriptDir

# Handle command line switches
if ($Help) {
    Write-Usage -ScriptName $ScriptName -UsageText "<feature-name> [feature-id]"
    exit 0
}

if ($Version) {
    Write-Version -ScriptName $ScriptName -ScriptVersion "1.0.0"
    exit 0
}

if ($VerboseMode) {
    $VerbosePreference = "Continue"
}

# Validate arguments
if ([string]::IsNullOrEmpty($FeatureName)) {
    Write-Usage -ScriptName $ScriptName -UsageText "<feature-name> [feature-id]"
    exit 1
}

# Sanitize feature name using utility function
$BranchSafeName = Get-SanitizedFeatureName -FeatureName $FeatureName
if (-not $BranchSafeName) {
    Write-ScriptError -Message "Invalid feature name: '$FeatureName'"
}

# Get feature ID using utility function
$FeatureId = Get-FeatureId -ProjectRoot $ProjectRoot -CustomId $CustomId

$BranchName = "$FeatureId-$BranchSafeName"

# Create directories
$SpecsDir = Join-Path $ProjectRoot "specs\$BranchName"
$PlansDir = Join-Path $ProjectRoot "plans\$BranchName"
$TasksDir = Join-Path $ProjectRoot "tasks\$BranchName"

Write-LogInfo "Creating feature directories for '$FeatureName'"

# Validate project structure first
if (-not (Test-ProjectStructure -ProjectRoot $ProjectRoot)) {
    Write-ScriptError -Message "Invalid project structure"
}

# Create directories with progress tracking
Show-Progress -Current 1 -Total 4 -Description "Creating directories"
New-Item -ItemType Directory -Path $SpecsDir -Force | Out-Null
Show-Progress -Current 2 -Total 4 -Description "Creating directories"
New-Item -ItemType Directory -Path $PlansDir -Force | Out-Null
Show-Progress -Current 3 -Total 4 -Description "Creating directories"
New-Item -ItemType Directory -Path $TasksDir -Force | Out-Null
Show-Progress -Current 4 -Total 4 -Description "Creating directories"

# Validate templates exist but don't copy them directly
$TemplateDir = Join-Path $ProjectRoot "templates"

# Validate all required templates exist
if (-not (Test-Templates -TemplateDir $TemplateDir)) {
    Write-ScriptError -Message "Template validation failed"
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

# Update context with backup
$ContextFile = Join-Path $ProjectRoot "memory\context.md"
$memoryDir = Split-Path -Parent $ContextFile

if (-not (Test-Path $memoryDir)) {
    New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null
}

# Backup context file before modification
Backup-File -FilePath $ContextFile

$contextEntry = @"

## Active Feature: $FeatureName
- Feature ID: $FeatureId
- Branch: $BranchName
- Started: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
"@

Add-Content -Path $ContextFile -Value $contextEntry

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

Write-LogSuccess "Successfully initialized feature '$FeatureName' with ID $FeatureId"

# Output results for consumption by other scripts
Write-Output "BRANCH_NAME=$BranchName"
Write-Output "SPEC_DIR=$SpecsDir"
Write-Output "FEATURE_ID=$FeatureId"
Write-Output "STATUS=initialized"
Write-Output "BACKUP_DIR=$global:BackupDir"