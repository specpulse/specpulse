# Common utility functions for SpecPulse PowerShell scripts
# This file provides standardized error handling and logging

# Configuration
$ScriptUtilsVersion = "1.0.0"

# Global variables
$global:BackupDir = ""
$global:RollbackStack = @()

# Initialize script environment
function Initialize-ScriptEnvironment {
    param(
        [string]$ScriptName,
        [string]$ScriptDir
    )

    # Create backup directory for rollback
    $global:BackupDir = Join-Path $env:TEMP "specpulse_backup_$(Get-Date -Format 'yyyyMMddHHmmss')_$PID"
    New-Item -ItemType Directory -Path $global:BackupDir -Force | Out-Null

    # Set error handling
    $ErrorActionPreference = "Stop"

    # Register cleanup on exit
    Register-EngineEvent PowerShell.Exiting -Action {
        Cleanup-OnExit
    } | Out-Null
}

# Cleanup function called on exit
function Cleanup-OnExit {
    if ($LASTEXITCODE -ne 0 -and $global:BackupDir -and (Test-Path $global:BackupDir)) {
        Write-Host "Warning: Script exited with error $LASTEXITCODE" -ForegroundColor Yellow
        Write-Host "Backup directory preserved at: $($global:BackupDir)" -ForegroundColor Yellow
    } else {
        Remove-Item $global:BackupDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Enhanced error handler
function Write-ScriptError {
    param(
        [string]$Message,
        [int]$ExitCode = 1
    )

    Write-Host "✖ ERROR: $Message" -ForegroundColor Red
    Write-Host "💡 Recovery suggestions:" -ForegroundColor Yellow
    Write-Host "   1. Check file permissions and disk space" -ForegroundColor Yellow
    Write-Host "   2. Verify all required directories exist" -ForegroundColor Yellow
    Write-Host "   3. Run with -Verbose for more details" -ForegroundColor Yellow

    if ($global:RollbackStack.Count -gt 0) {
        Write-Host "   4. Rollback is available to undo changes" -ForegroundColor Yellow
    }

    exit $ExitCode
}

# Logging functions with levels
function Write-LogDebug {
    param([string]$Message)
    if ($VerbosePreference -eq "Continue") {
        Write-Host "[DEBUG] $Message" -ForegroundColor Cyan
    }
}

function Write-LogInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-LogSuccess {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-LogWarning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Progress indicator
function Show-Progress {
    param(
        [int]$Current,
        [int]$Total,
        [string]$Description = "Processing"
    )

    $percentage = if ($Total -gt 0) { [math]::Round(($Current / $Total) * 100) } else { 0 }
    $barLength = 30
    $filledLength = [math]::Round(($percentage / 100) * $barLength)

    $bar = "=" * $filledLength + "-" * ($barLength - $filledLength)
    Write-Host -NoNewline "`r$Description [$bar] $percentage% ($Current/$Total)"

    if ($Current -eq $Total) {
        Write-Host
    }
}

# File backup for rollback
function Backup-File {
    param([string]$FilePath)

    if (Test-Path $FilePath) {
        $backupPath = Join-Path $global:BackupDir ($FilePath -replace '[\\/]', '_')
        Copy-Item $FilePath $backupPath -Force
        $global:RollbackStack += "${FilePath}:${backupPath}"
        Write-LogDebug "Backed up: $FilePath"
    }
}

# Rollback function
function Invoke-Rollback {
    Write-LogInfo "Rolling back changes..."

    $rollbackCount = 0
    foreach ($item in $global:RollbackStack) {
        $parts = $item -split ':', 2
        $originalPath = $parts[0]
        $backupPath = $parts[1]

        if (Test-Path $backupPath) {
            Copy-Item $backupPath $originalPath -Force
            Write-LogInfo "Restored: $originalPath"
            $rollbackCount++
        }
    }

    Write-LogSuccess "Rollback completed. Restored $rollbackCount files."
}

# Validate project structure
function Test-ProjectStructure {
    param([string]$ProjectRoot)

    $requiredDirs = @("specs", "plans", "tasks", "memory", "templates")
    $missingDirs = @()

    foreach ($dir in $requiredDirs) {
        $dirPath = Join-Path $ProjectRoot $dir
        if (-not (Test-Path $dirPath)) {
            $missingDirs += $dir
        }
    }

    if ($missingDirs.Count -gt 0) {
        Write-LogError "Missing required directories: $($missingDirs -join ', ')"
        Write-LogError "Run 'specpulse init' to initialize project structure"
        return $false
    }

    return $true
}

# Validate templates exist
function Test-Templates {
    param([string]$TemplateDir)

    $requiredTemplates = @("spec.md", "plan.md", "task.md")

    foreach ($template in $requiredTemplates) {
        $templatePath = Join-Path $TemplateDir $template
        if (-not (Test-Path $templatePath)) {
            Write-LogError "Template not found: $templatePath"
            Write-LogError "Run 'specpulse init' to initialize templates"
            return $false
        }
    }

    return $true
}

# Sanitize input
function Get-SanitizedFeatureName {
    param([string]$FeatureName)

    # Remove special characters, convert to lowercase, replace spaces with hyphens
    $sanitized = $FeatureName.ToLower() -replace '[^a-z0-9-]', '-' -replace '-+', '-' -replace '^-|-$', ''

    if ([string]::IsNullOrEmpty($sanitized)) {
        Write-LogError "Invalid feature name: '$FeatureName'"
        Write-LogError "Feature names must contain at least one alphanumeric character"
        return $null
    }

    return $sanitized
}

# Generate unique feature ID
function Get-FeatureId {
    param(
        [string]$ProjectRoot,
        [string]$CustomId = ""
    )

    if ($CustomId) {
        return "{0:D3}" -f [int]$CustomId
    } else {
        $specsDir = Join-Path $ProjectRoot "specs"
        if (Test-Path $specsDir) {
            $existingDirs = Get-ChildItem -Path $specsDir -Directory -Filter "[0-9]*" -ErrorAction SilentlyContinue
            $nextId = if ($existingDirs) { $existingDirs.Count + 1 } else { 1 }
            return "{0:D3}" -f $nextId
        } else {
            return "001"
        }
    }
}

# Check dependencies
function Test-Dependencies {
    param([string[]]$Dependencies)

    $missingDeps = @()

    foreach ($dep in $Dependencies) {
        try {
            $null = Get-Command $dep -ErrorAction Stop
        } catch {
            $missingDeps += $dep
        }
    }

    if ($missingDeps.Count -gt 0) {
        Write-LogError "Missing required dependencies: $($missingDeps -join ', ')"
        Write-LogError "Please install missing dependencies and try again"
        return $false
    }

    return $true
}

# Get next file number in sequence
function Get-NextFileNumber {
    param(
        [string]$Directory,
        [string]$Prefix
    )

    if (Test-Path $Directory) {
        $existingFiles = Get-ChildItem -Path $Directory -Filter "$Prefix-*.md" -ErrorAction SilentlyContinue
        if ($existingFiles) {
            $highestNumber = $existingFiles | ForEach-Object {
                if ($_.BaseName -match "$Prefix-(\d+)") { [int]$matches[1] } else { 0 }
            } | Sort-Object -Descending | Select-Object -First 1
            return $highestNumber + 1
        } else {
            return 1
        }
    } else {
        return 1
    }
}

# Print usage help
function Write-Usage {
    param(
        [string]$ScriptName,
        [string]$UsageText
    )

    Write-Host "Usage:" -ForegroundColor White -BackgroundColor Blue
    Write-Host "  $ScriptName $UsageText"
    Write-Host
    Write-Host "Common options:" -ForegroundColor White -BackgroundColor Blue
    Write-Host "  -Verbose       Show detailed output"
    Write-Host "  -Help          Show this help message"
    Write-Host "  -Version       Show version information"
}

# Print version info
function Write-Version {
    param(
        [string]$ScriptName,
        [string]$ScriptVersion = "unknown"
    )

    Write-Host "$ScriptName version $ScriptVersion" -ForegroundColor Green
    Write-Host "SpecPulse Script Utils version $ScriptUtilsVersion"
}

# Note: Functions are automatically available when this script is sourced with dot operator
# Usage: . ".\script_utils.ps1"