# SpecPulse Specification Generation Script
# Cross-platform PowerShell equivalent of pulse-spec.sh

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureDir,
    
    [string]$SpecContent = ""
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

function Validate-Specification {
    param([string]$SpecFile)
    
    if (-not (Test-Path $SpecFile)) {
        Exit-WithError "Specification file does not exist: $SpecFile"
    }
    
    # Required sections
    $RequiredSections = @(
        "## Specification:",
        "## Metadata", 
        "## Functional Requirements",
        "## Acceptance Scenarios"
    )
    
    $Content = Get-Content $SpecFile -Raw -Encoding UTF8
    $MissingSections = @()
    
    foreach ($Section in $RequiredSections) {
        if ($Content -notmatch [regex]::Escape($Section)) {
            $MissingSections += $Section
        }
    }
    
    if ($MissingSections.Count -gt 0) {
        Write-Log "WARNING: Missing required sections: $($MissingSections -join ', ')"
    }
    
    # Check for clarifications needed
    $ClarificationMatches = [regex]::Matches($Content, 'NEEDS CLARIFICATION')
    if ($ClarificationMatches.Count -gt 0) {
        $ClarificationCount = $ClarificationMatches.Count
        Write-Log "WARNING: Specification has $ClarificationCount clarifications needed"
        return $ClarificationCount
    }
    
    return 0
}

# Main execution
Write-Log "Processing specification..."

# Get and sanitize feature directory
$SanitizedDir = Get-CurrentFeatureDir -ProvidedDir $FeatureDir

# Set file paths
$SpecFile = Join-Path $ProjectRoot "specs" $SanitizedDir "spec.md"
$TemplateFile = Join-Path $TemplatesDir "spec.md"

# Ensure specs directory exists
$SpecDir = Split-Path $SpecFile -Parent
New-Item -ItemType Directory -Path $SpecDir -Force | Out-Null

# Handle specification content
if ($SpecContent) {
    Write-Log "Updating specification: $SpecFile"
    try {
        Set-Content -Path $SpecFile -Value $SpecContent -Encoding UTF8
    } catch {
        Exit-WithError "Failed to write specification content: $_"
    }
} else {
    # Ensure specification exists from template
    if (-not (Test-Path $SpecFile)) {
        if (-not (Test-Path $TemplateFile)) {
            Exit-WithError "Template not found: $TemplateFile"
        }
        
        Write-Log "Creating specification from template: $SpecFile"
        try {
            Copy-Item $TemplateFile $SpecFile -Force
        } catch {
            Exit-WithError "Failed to copy specification template: $_"
        }
    } else {
        Write-Log "Specification already exists: $SpecFile"
    }
}

# Validate specification
Write-Log "Validating specification..."
$ClarificationCount = Validate-Specification -SpecFile $SpecFile

# Check for missing sections
$Content = Get-Content $SpecFile -Raw -Encoding UTF8
$RequiredSections = @(
    "## Specification:",
    "## Metadata", 
    "## Functional Requirements",
    "## Acceptance Scenarios"
)

$MissingSections = @()
foreach ($Section in $RequiredSections) {
    if ($Content -notmatch [regex]::Escape($Section)) {
        $MissingSections += $Section
    }
}

Write-Log "Specification processing completed successfully"

# Output results
Write-Host "SPEC_FILE=$SpecFile"
Write-Host "CLARIFICATIONS_NEEDED=$ClarificationCount"
Write-Host "MISSING_SECTIONS=$($MissingSections.Count)"
Write-Host "STATUS=updated"