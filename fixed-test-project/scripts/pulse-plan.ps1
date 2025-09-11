# SpecPulse Plan Generation Script
# Cross-platform PowerShell equivalent of pulse-plan.sh

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureDir,
    
    [string]$PlanContent = ""
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

function Validate-PlanStructure {
    param([string]$PlanFile)
    
    if (-not (Test-Path $PlanFile)) {
        Exit-WithError "Plan file does not exist: $PlanFile"
    }
    
    # Required sections
    $RequiredSections = @(
        "# Implementation Plan:",
        "## Technology Stack",
        "## Architecture Overview",
        "## Implementation Phases"
    )
    
    $Content = Get-Content $PlanFile -Raw -Encoding UTF8
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
    param([string]$PlanFile)
    
    if (-not (Test-Path $PlanFile)) {
        Exit-WithError "Plan file does not exist: $PlanFile"
    }
    
    $Content = Get-Content $PlanFile -Raw -Encoding UTF8
    $GatesStatus = @{}
    
    # Check for constitutional gates compliance
    $Gates = @{
        "Simplicity Gate" = "Article VII: Simplicity Gate"
        "Anti-Abstraction Gate" = "Article VII: Anti-Abstraction Gate"
        "Test-First Gate" = "Article III: Test-First Gate"
        "Integration-First Gate" = "Article VIII: Integration-First Gate"
        "Research Gate" = "Article VI: Research Gate"
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

function Analyze-Complexity {
    param([string]$PlanFile)
    
    if (-not (Test-Path $PlanFile)) {
        Exit-WithError "Plan file does not exist: $PlanFile"
    }
    
    $Content = Get-Content $PlanFile -Raw -Encoding UTF8
    
    # Count complexity exceptions
    $ExceptionMatches = [regex]::Matches($Content, "Complexity Exception")
    $ExceptionCount = $ExceptionMatches.Count
    
    # Check for complexity tracking
    $HasComplexityTracking = $Content -match "Complexity Tracking"
    
    # Count modules/projects mentioned
    $ModuleMatches = [regex]::Matches($Content, "(?i)(module|project)s?\s*[:\-]?\s*\d+")
    $ModuleCount = 0
    if ($ModuleMatches.Count -gt 0) {
        foreach ($Match in $ModuleMatches) {
            if ($Match.Value -match "\d+") {
                $ModuleCount = [int]$matches[0]
                break
            }
        }
    }
    
    return @{
        ExceptionCount = $ExceptionCount
        HasComplexityTracking = $HasComplexityTracking
        ModuleCount = $ModuleCount
    }
}

# Main execution
Write-Log "Processing plan..."

# Get and sanitize feature directory
$SanitizedDir = Get-CurrentFeatureDir -ProvidedDir $FeatureDir

# Set file paths
$PlanFile = Join-Path $ProjectRoot "plans" $SanitizedDir "plan.md"
$SpecFile = Join-Path $ProjectRoot "specs" $SanitizedDir "spec.md"
$TemplateFile = Join-Path $TemplatesDir "plan.md"

# Ensure plans directory exists
$PlanDir = Split-Path $PlanFile -Parent
New-Item -ItemType Directory -Path $PlanDir -Force | Out-Null

# Handle plan content
if ($PlanContent) {
    Write-Log "Updating plan file: $PlanFile"
    try {
        Set-Content -Path $PlanFile -Value $PlanContent -Encoding UTF8
    } catch {
        Exit-WithError "Failed to write plan content: $_"
    }
} else {
    # Ensure plan file exists from template
    if (-not (Test-Path $PlanFile)) {
        if (-not (Test-Path $TemplateFile)) {
            Exit-WithError "Template not found: $TemplateFile"
        }
        
        Write-Log "Creating plan file from template: $PlanFile"
        try {
            Copy-Item $TemplateFile $PlanFile -Force
        } catch {
            Exit-WithError "Failed to copy plan template: $_"
        }
    } else {
        Write-Log "Plan file already exists: $PlanFile"
    }
}

# Validate plan structure
Write-Log "Validating plan structure..."
$MissingSections = Validate-PlanStructure -PlanFile $PlanFile

# Check constitutional gates
Write-Log "Checking constitutional gates..."
$GatesStatus = Check-ConstitutionalGates -PlanFile $PlanFile

# Analyze complexity
Write-Log "Analyzing complexity..."
$ComplexityAnalysis = Analyze-Complexity -PlanFile $PlanFile

# Count completed constitutional gates
$CompletedGates = 0
foreach ($Status in $GatesStatus.Values) {
    if ($Status -eq "COMPLETED") {
        $CompletedGates++
    }
}

# Check if specification exists
$SpecExists = Test-Path $SpecFile

Write-Log "Plan processing completed successfully"

# Output results
Write-Host "PLAN_FILE=$PlanFile"
Write-Host "SPEC_EXISTS=$SpecExists"
Write-Host "MISSING_SECTIONS=$MissingSections"
Write-Host "COMPLETED_GATES=$CompletedGates"
Write-Host "TOTAL_GATES=$($GatesStatus.Count)"
Write-Host "COMPLEXITY_EXCEPTIONS=$($ComplexityAnalysis.ExceptionCount)"
Write-Host "HAS_COMPLEXITY_TRACKING=$($ComplexityAnalysis.HasComplexityTracking)"
Write-Host "MODULE_COUNT=$($ComplexityAnalysis.ModuleCount)"
Write-Host "STATUS=processed"