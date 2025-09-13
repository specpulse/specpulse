# Generate or update specification - PowerShell Version

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$FeatureDir,

    [Parameter(Mandatory=$false, Position=1)]
    [string]$SpecContent
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

# Extract feature ID from directory name
$FeatureId = if ($FeatureDir -match '^(\d{3})') { $Matches[1] } else { "001" }

# Sanitize feature directory
$SanitizedDir = $FeatureDir -replace '[^a-zA-Z0-9_-]', ''

if ([string]::IsNullOrEmpty($SanitizedDir)) {
    Exit-WithError "Invalid feature directory: '$FeatureDir'"
}

$SpecDir = Join-Path $ProjectRoot "specs\$FeatureDir"
$TemplateFile = Join-Path $ProjectRoot "templates\spec.md"

# Ensure specs directory exists
if (-not (Test-Path $SpecDir)) {
    New-Item -ItemType Directory -Path $SpecDir -Force | Out-Null
}

# Find latest spec file or create new one
if ($SpecContent) {
    # Find next available spec number
    $existingSpecs = Get-ChildItem -Path $SpecDir -Filter "spec-*.md" -ErrorAction SilentlyContinue
    $specNumber = if ($existingSpecs) { $existingSpecs.Count + 1 } else { 1 }
    $SpecFile = Join-Path $SpecDir ("spec-{0:D3}.md" -f $specNumber)

    # Update specification with provided content
    Log-Message "Creating specification: $SpecFile"
    try {
        Set-Content -Path $SpecFile -Value $SpecContent
    } catch {
        Exit-WithError "Failed to write specification content: $_"
    }
} else {
    # Find latest spec file
    $latestSpec = Get-ChildItem -Path $SpecDir -Filter "spec-*.md" -ErrorAction SilentlyContinue |
                  Sort-Object LastWriteTime -Descending |
                  Select-Object -First 1

    if ($latestSpec) {
        $SpecFile = $latestSpec.FullName
        Log-Message "Using latest specification: $SpecFile"
    } else {
        # No spec files found, create first one
        $SpecFile = Join-Path $SpecDir "spec-001.md"
        if (-not (Test-Path $TemplateFile)) {
            Exit-WithError "Template not found: $TemplateFile"
        }
        Log-Message "Creating specification from template: $SpecFile"
        try {
            Copy-Item -Path $TemplateFile -Destination $SpecFile -Force
        } catch {
            Exit-WithError "Failed to copy specification template: $_"
        }
    }
}

# Validate specification
Log-Message "Validating specification..."
if (-not (Test-Path $SpecFile)) {
    Exit-WithError "Specification file does not exist: $SpecFile"
}

# Check for required sections
$RequiredSections = @(
    "## Specification:",
    "## Metadata",
    "## Functional Requirements",
    "## Acceptance Scenarios"
)

$content = Get-Content -Path $SpecFile -Raw
$MissingSections = @()

foreach ($section in $RequiredSections) {
    if ($content -notmatch [regex]::Escape($section)) {
        $MissingSections += $section
    }
}

if ($MissingSections.Count -gt 0) {
    Log-Message "WARNING: Missing required sections: $($MissingSections -join ', ')"
}

# Check for clarifications needed
$ClarificationCount = 0
if ($content -match "NEEDS CLARIFICATION") {
    $ClarificationCount = ([regex]::Matches($content, "NEEDS CLARIFICATION")).Count
    Log-Message "WARNING: Specification has $ClarificationCount clarifications needed"
}

Log-Message "Specification processing completed successfully"

# Output results
Write-Output "SPEC_FILE=$SpecFile"
Write-Output "CLARIFICATIONS_NEEDED=$ClarificationCount"
Write-Output "MISSING_SECTIONS=$($MissingSections.Count)"
Write-Output "STATUS=updated"