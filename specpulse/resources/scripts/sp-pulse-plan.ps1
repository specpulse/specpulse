# Generate implementation plan - PowerShell Version

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

$PlanDir = Join-Path $ProjectRoot "plans\$FeatureDir"
$SpecDir = Join-Path $ProjectRoot "specs\$FeatureDir"
$TemplateFile = Join-Path $ProjectRoot "templates\plan.md"

# Ensure plans directory exists
if (-not (Test-Path $PlanDir)) {
    New-Item -ItemType Directory -Path $PlanDir -Force | Out-Null
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

# Find next available plan number or create new one
$existingPlans = Get-ChildItem -Path $PlanDir -Filter "plan-*.md" -ErrorAction SilentlyContinue
$planNumber = if ($existingPlans) { $existingPlans.Count + 1 } else { 1 }
$PlanFile = Join-Path $PlanDir ("plan-{0:D3}.md" -f $planNumber)

# Ensure plan template exists
if (-not (Test-Path $TemplateFile)) {
    Exit-WithError "Template not found: $TemplateFile"
}

# Create plan
Log-Message "Creating implementation plan from template: $PlanFile"
try {
    Copy-Item -Path $TemplateFile -Destination $PlanFile -Force
} catch {
    Exit-WithError "Failed to copy plan template: $_"
}

# Validate plan structure
Log-Message "Validating implementation plan..."

# Check for required sections
$RequiredSections = @(
    "## Implementation Plan:",
    "## Specification Reference",
    "## Phase -1: Pre-Implementation Gates",
    "## Implementation Phases"
)

$content = Get-Content -Path $PlanFile -Raw
$MissingSections = @()

foreach ($section in $RequiredSections) {
    if ($content -notmatch [regex]::Escape($section)) {
        $MissingSections += $section
    }
}

if ($MissingSections.Count -gt 0) {
    Log-Message "WARNING: Missing required sections: $($MissingSections -join ', ')"
}

# Check SDD Gates
Log-Message "Checking SDD Gates..."

$SDDGates = @(
    "Specification First",
    "Incremental Planning",
    "Task Decomposition",
    "Traceable Implementation",
    "Continuous Validation",
    "Quality Assurance",
    "Architecture Documentation",
    "Iterative Refinement",
    "Stakeholder Alignment"
)

foreach ($gate in $SDDGates) {
    if ($content -notmatch [regex]::Escape($gate)) {
        Log-Message "WARNING: Missing SDD gate: $gate"
    }
}

# Check if specification has clarifications needed
$specContent = Get-Content -Path $SpecFile -Raw
if ($specContent -match "NEEDS CLARIFICATION") {
    $ClarificationCount = ([regex]::Matches($specContent, "NEEDS CLARIFICATION")).Count
    Log-Message "WARNING: Specification has $ClarificationCount clarifications needed - resolve before proceeding"
}

# Validate gate compliance
$GateStatus = "PENDING"
if ($content -match "Gate Status:.*\[(.*?)\]") {
    $GateStatus = $Matches[1]
}

if ($GateStatus -ne "COMPLETED") {
    Log-Message "WARNING: SDD gates not completed. Status: $GateStatus"
}

Log-Message "Implementation plan processing completed successfully"

# Output results
Write-Output "PLAN_FILE=$PlanFile"
Write-Output "SPEC_FILE=$SpecFile"
Write-Output "MISSING_SECTIONS=$($MissingSections.Count)"
Write-Output "SDD_GATES_STATUS=$GateStatus"
Write-Output "STATUS=ready"