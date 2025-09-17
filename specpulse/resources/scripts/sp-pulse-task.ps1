# Generate task breakdown - PowerShell Version

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$FeatureDir
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

# Extract feature ID
$FeatureId = if ($FeatureDir -match '^(\d{3})') { $Matches[1] } else { "001" }

# Sanitize feature directory
$SanitizedDir = $FeatureDir -replace '[^a-zA-Z0-9_-]', ''

if ([string]::IsNullOrEmpty($SanitizedDir)) {
    Exit-WithError "Invalid feature directory: '$FeatureDir'"
}

$TaskDir = Join-Path $ProjectRoot "tasks\$FeatureDir"
$PlanDir = Join-Path $ProjectRoot "plans\$FeatureDir"
$SpecDir = Join-Path $ProjectRoot "specs\$FeatureDir"
$TemplateFile = Join-Path $ProjectRoot "templates\task.md"

# Ensure tasks directory exists
if (-not (Test-Path $TaskDir)) {
    New-Item -ItemType Directory -Path $TaskDir -Force | Out-Null
}

# Find latest spec file
if (Test-Path $SpecDir) {
    $SpecFile = Get-ChildItem -Path $SpecDir -Filter "spec-*.md" -ErrorAction SilentlyContinue |
                Sort-Object LastWriteTime -Descending |
                Select-Object -First 1

    if (-not $SpecFile) {
        Exit-WithError "No specification files found in $SpecDir. Please create specification first."
    }
    $SpecFile = $SpecFile.FullName
} else {
    Exit-WithError "Specifications directory not found: $SpecDir. Please create specification first."
}

# Find latest plan file
if (Test-Path $PlanDir) {
    $PlanFile = Get-ChildItem -Path $PlanDir -Filter "plan-*.md" -ErrorAction SilentlyContinue |
                Sort-Object LastWriteTime -Descending |
                Select-Object -First 1

    if (-not $PlanFile) {
        Exit-WithError "No plan files found in $PlanDir. Please create plan first."
    }
    $PlanFile = $PlanFile.FullName
} else {
    Exit-WithError "Plans directory not found: $PlanDir. Please create plan first."
}

# Find next available task number or create new one
$existingTasks = Get-ChildItem -Path $TaskDir -Filter "task-*.md" -ErrorAction SilentlyContinue
$taskNumber = if ($existingTasks) { $existingTasks.Count + 1 } else { 1 }
$TaskFile = Join-Path $TaskDir ("task-{0:D3}.md" -f $taskNumber)

# Ensure task template exists
if (-not (Test-Path $TemplateFile)) {
    Exit-WithError "Template not found: $TemplateFile"
}

# Create task file
Log-Message "Creating task breakdown from template: $TaskFile"
try {
    Copy-Item -Path $TemplateFile -Destination $TaskFile -Force
} catch {
    Exit-WithError "Failed to copy task template: $_"
}

# Validate task structure
Log-Message "Validating task breakdown..."

# Check for required sections
$RequiredSections = @(
    "## Task List:",
    "## Task Organization",
    "## Critical Path",
    "## Execution Schedule"
)

$content = Get-Content -Path $TaskFile -Raw
$MissingSections = @()

foreach ($section in $RequiredSections) {
    if ($content -notmatch [regex]::Escape($section)) {
        $MissingSections += $section
    }
}

if ($MissingSections.Count -gt 0) {
    Log-Message "WARNING: Missing required sections: $($MissingSections -join ', ')"
}

# Count tasks and analyze structure
$TotalTasks = ([regex]::Matches($content, "^- \[.\]", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
$CompletedTasks = ([regex]::Matches($content, "^- \[x\]", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
$PendingTasks = ([regex]::Matches($content, "^- \[ \]", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
$BlockedTasks = ([regex]::Matches($content, "^- \[!\]", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count

# Check for parallel tasks
$ParallelTasks = ([regex]::Matches($content, "\[P\]")).Count

# Check SDD gates compliance
$GatesCount = 0
if ($content -match "SDD Gates Compliance") {
    $gatesSection = $content.Substring($content.IndexOf("SDD Gates Compliance"))
    if ($gatesSection.Length -gt 0) {
        $GatesCount = ([regex]::Matches($gatesSection.Substring(0, [Math]::Min(1000, $gatesSection.Length)), "\[ \]")).Count
    }
}

# Check if plan has SDD gates completed
$planContent = Get-Content -Path $PlanFile -Raw
$PlanGateStatus = "PENDING"
if ($planContent -match "Gate Status:.*\[(.*?)\]") {
    $PlanGateStatus = $Matches[1]
}

if ($PlanGateStatus -ne "COMPLETED") {
    Log-Message "WARNING: Implementation plan SDD gates not completed. Task generation may be premature."
}

# Calculate completion percentage
$CompletionPercentage = 0
if ($TotalTasks -gt 0) {
    $CompletionPercentage = [math]::Round(($CompletedTasks * 100) / $TotalTasks)
}

Log-Message "Task analysis completed - Total: $TotalTasks, Completed: $CompletedTasks ($CompletionPercentage%), Parallel: $ParallelTasks"

# Output comprehensive status
Write-Output "TASK_FILE=$TaskFile"
Write-Output "SPEC_FILE=$SpecFile"
Write-Output "PLAN_FILE=$PlanFile"
Write-Output "TOTAL_TASKS=$TotalTasks"
Write-Output "COMPLETED_TASKS=$CompletedTasks"
Write-Output "PENDING_TASKS=$PendingTasks"
Write-Output "BLOCKED_TASKS=$BlockedTasks"
Write-Output "PARALLEL_TASKS=$ParallelTasks"
Write-Output "SDD_GATES_PENDING=$GatesCount"
Write-Output "COMPLETION_PERCENTAGE=$CompletionPercentage"
Write-Output "MISSING_SECTIONS=$($MissingSections.Count)"
Write-Output "STATUS=generated"