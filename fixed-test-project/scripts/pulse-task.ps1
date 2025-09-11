# SpecPulse Task Generation Script
# Cross-platform PowerShell equivalent of pulse-task.sh

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureDir,
    
    [string]$TaskContent = ""
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Configuration
$ScriptName = $MyInvocation.MyCommand.Name
$ProjectRoot = $PSScriptRoot | Split-Path -Parent | Split-Path -Parent
$MemoryDir = Join-Path $ProjectRoot "memory"
$ContextFile = Join-Path $MemoryDir "context.md"
$TemplatesDir = Join-Path $ProjectRoot "resources" "templates"

function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$Timestamp] $ScriptName : $Message" -ForegroundColor Yellow
}

function Exit-WithError {
    param([string]$Message)
    Write-Log "ERROR: $Message"
    exit 1
}

function Sanitize-FeatureDir {
    param([string]$Dir)
    
    if ([string]::IsNullOrWhiteSpace($Dir)) {
        Exit-WithError "Feature directory cannot be empty"
    }
    
    # Remove non-alphanumeric characters except hyphens and underscores
    $Sanitized = $Dir -replace '[^a-zA-Z0-9_-]', ''
    
    if ([string]::IsNullOrWhiteSpace($Sanitized)) {
        Exit-WithError "Invalid feature directory: '$Dir'"
    }
    
    return $Sanitized
}

function Find-FeatureDirectory {
    if (-not (Test-Path $ContextFile)) {
        Exit-WithError "No context file found and no feature directory provided"
    }
    
    try {
        $Content = Get-Content $ContextFile -Raw -Encoding UTF8
        # Look for "Active Feature" section
        if ($Content -match 'Active Feature:\s*(.+)') {
            $FeatureDir = $matches[1].Trim()
            Write-Log "Using active feature from context: $FeatureDir"
            return $FeatureDir
        } else {
            Exit-WithError "No active feature found in context file"
        }
    } catch {
        Exit-WithError "Failed to read context file: $_"
    }
}

function Get-CurrentFeatureDir {
    param([string]$ProvidedDir)
    
    if ($ProvidedDir) {
        return Sanitize-FeatureDir -Dir $ProvidedDir
    } else {
        return Find-FeatureDirectory
    }
}

function Validate-TaskStructure {
    param([string]$TaskFile)
    
    if (-not (Test-Path $TaskFile)) {
        Exit-WithError "Task file does not exist: $TaskFile"
    }
    
    # Required sections
    $RequiredSections = @(
        "# Task List:",
        "## Progress Tracking",
        "### Parallel Group"
    )
    
    $Content = Get-Content $TaskFile -Raw -Encoding UTF8
    $MissingSections = @()
    
    foreach ($Section in $RequiredSections) {
        if ($Content -notmatch [regex]::Escape($Section)) {
            $MissingSections += $Section
        }
    }
    
    if ($MissingSections.Count -gt 0) {
        Write-Log "WARNING: Missing required sections: $($MissingSections -join ', ')"
    }
    
    return $MissingSections.Count
}

function Check-ConstitutionalGates {
    param([string]$TaskFile)
    
    if (-not (Test-Path $TaskFile)) {
        Exit-WithError "Task file does not exist: $TaskFile"
    }
    
    $Content = Get-Content $TaskFile -Raw -Encoding UTF8
    $GatesStatus = @{}
    
    # Check for constitutional gates compliance
    $Gates = @{
        "Simplicity Gate" = "Simplicity Gate"
        "Test-First Gate" = "Test-First Gate"
        "Integration-First Gate" = "Integration-First Gate"
        "Research Gate" = "Research Gate"
    }
    
    foreach ($Gate in $Gates.GetEnumerator()) {
        if ($Content -match $Gate.Value) {
            $GatesStatus[$Gate.Key] = "COMPLETED"
        } else {
            $GatesStatus[$Gate.Key] = "PENDING"
        }
    }
    
    return $GatesStatus
}

function Analyze-Tasks {
    param([string]$TaskFile)
    
    if (-not (Test-Path $TaskFile)) {
        Exit-WithError "Task file does not exist: $TaskFile"
    }
    
    $Content = Get-Content $TaskFile -Raw -Encoding UTF8
    
    # Count tasks
    $TaskMatches = [regex]::Matches($Content, '### T\d{3}:')
    $TaskCount = $TaskMatches.Count
    
    # Count parallel tasks
    $ParallelMatches = [regex]::Matches($Content, '\[P\]')
    $ParallelCount = $ParallelMatches.Count
    
    # Check for completion status
    $CompletionSection = $Content -match "## Progress Tracking"
    $CompletedTasks = 0
    $InProgressTasks = 0
    $BlockedTasks = 0
    
    if ($CompletionSection) {
        # Look for progress tracking YAML section
        if ($Content -match "completed:\s*(\d+)") {
            $CompletedTasks = [int]$matches[1]
        }
        if ($Content -match "in_progress:\s*(\d+)") {
            $InProgressTasks = [int]$matches[1]
        }
        if ($Content -match "blocked:\s*(\d+)") {
            $BlockedTasks = [int]$matches[1]
        }
    }
    
    return @{
        TotalTasks = $TaskCount
        ParallelTasks = $ParallelCount
        CompletedTasks = $CompletedTasks
        InProgressTasks = $InProgressTasks
        BlockedTasks = $BlockedTasks
    }
}

# Main execution
Write-Log "Processing tasks..."

# Get and sanitize feature directory
$SanitizedDir = Get-CurrentFeatureDir -ProvidedDir $FeatureDir

# Set file paths
$TaskFile = Join-Path $ProjectRoot "tasks" $SanitizedDir "tasks.md"
$PlanFile = Join-Path $ProjectRoot "plans" $SanitizedDir "plan.md"
$TemplateFile = Join-Path $TemplatesDir "task.md"

# Ensure tasks directory exists
$TaskDir = Split-Path $TaskFile -Parent
New-Item -ItemType Directory -Path $TaskDir -Force | Out-Null

# Handle task content
if ($TaskContent) {
    Write-Log "Updating task file: $TaskFile"
    try {
        Set-Content -Path $TaskFile -Value $TaskContent -Encoding UTF8
    } catch {
        Exit-WithError "Failed to write task content: $_"
    }
} else {
    # Ensure task file exists from template
    if (-not (Test-Path $TaskFile)) {
        if (-not (Test-Path $TemplateFile)) {
            Exit-WithError "Template not found: $TemplateFile"
        }
        
        Write-Log "Creating task file from template: $TaskFile"
        try {
            Copy-Item $TemplateFile $TaskFile -Force
        } catch {
            Exit-WithError "Failed to copy task template: $_"
        }
    } else {
        Write-Log "Task file already exists: $TaskFile"
    }
}

# Validate task structure
Write-Log "Validating task structure..."
$MissingSections = Validate-TaskStructure -TaskFile $TaskFile

# Check constitutional gates
Write-Log "Checking constitutional gates..."
$GatesStatus = Check-ConstitutionalGates -TaskFile $TaskFile

# Analyze tasks
Write-Log "Analyzing tasks..."
$TaskAnalysis = Analyze-Tasks -TaskFile $TaskFile

# Calculate completion percentage
$CompletionPercentage = 0
if ($TaskAnalysis.TotalTasks -gt 0) {
    $CompletionPercentage = [math]::Round(($TaskAnalysis.CompletedTasks / $TaskAnalysis.TotalTasks) * 100, 2)
}

# Count pending constitutional gates
$PendingGates = 0
foreach ($Status in $GatesStatus.Values) {
    if ($Status -eq "PENDING") {
        $PendingGates++
    }
}

Write-Log "Task processing completed successfully"

# Output results
Write-Host "TASK_FILE=$TaskFile"
Write-Host "TOTAL_TASKS=$($TaskAnalysis.TotalTasks)"
Write-Host "COMPLETED_TASKS=$($TaskAnalysis.CompletedTasks)"
Write-Host "IN_PROGRESS_TASKS=$($TaskAnalysis.InProgressTasks)"
Write-Host "BLOCKED_TASKS=$($TaskAnalysis.BlockedTasks)"
Write-Host "PARALLEL_TASKS=$($TaskAnalysis.ParallelTasks)"
Write-Host "COMPLETION_PERCENTAGE=$CompletionPercentage"
Write-Host "MISSING_SECTIONS=$MissingSections"
Write-Host "CONSTITUTIONAL_GATES_PENDING=$PendingGates"
Write-Host "STATUS=processed"