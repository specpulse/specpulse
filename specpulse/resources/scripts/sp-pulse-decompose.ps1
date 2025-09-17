# SpecPulse Decomposition Orchestrator - PowerShell Version
# Validates decomposition request and returns status for AI processing

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$SpecId,

    [Parameter(Mandatory=$false, Position=1)]
    [string]$Action = "validate"
)

# Configuration
$ScriptDir = Split-Path -Parent $PSCommandPath
$ProjectRoot = Split-Path -Parent $ScriptDir

# Colors for output
$Green = "Green"
$Yellow = "Yellow"

Write-Host "[SpecPulse Decompose]" -ForegroundColor $Green -NoNewline
Write-Host " Processing spec: $($SpecId ?? 'current')"

# Find specification
if ([string]::IsNullOrEmpty($SpecId)) {
    $specDirs = Get-ChildItem -Path "$ProjectRoot\specs" -Directory -ErrorAction SilentlyContinue |
                Sort-Object Name -Descending |
                Select-Object -First 1
    $SpecDir = if ($specDirs) { $specDirs.FullName } else { $null }
} else {
    $specDirs = Get-ChildItem -Path "$ProjectRoot\specs" -Directory -Filter "${SpecId}*" -ErrorAction SilentlyContinue |
                Select-Object -First 1
    $SpecDir = if ($specDirs) { $specDirs.FullName } else { $null }
}

if (-not $SpecDir -or -not (Test-Path $SpecDir)) {
    Write-Host "ERROR: No specification found" -ForegroundColor Red
    Write-Host "SUGGESTION: Run /sp-spec create first"
    exit 1
}

# Check complexity (simple heuristic)
$specFiles = Get-ChildItem -Path $SpecDir -Filter "spec-*.md" -ErrorAction SilentlyContinue |
             Sort-Object Name |
             Select-Object -Last 1

if ($specFiles) {
    $SpecFile = $specFiles.FullName
    $LineCount = (Get-Content $SpecFile | Measure-Object -Line).Lines

    Write-Output "SPEC_FILE=$SpecFile"
    Write-Output "COMPLEXITY=$LineCount lines"

    if ($LineCount -gt 100) {
        Write-Output "RECOMMENDATION=Decomposition advised (complex spec)"
    } else {
        Write-Output "RECOMMENDATION=Single service may suffice"
    }
}

# Check for existing decomposition
$DecompositionPath = Join-Path $SpecDir "decomposition"
if (Test-Path $DecompositionPath) {
    Write-Output "STATUS=Decomposition exists"
    Write-Output "PATH=$DecompositionPath"
} else {
    Write-Output "STATUS=Ready for decomposition"
    Write-Output "PATH=$SpecDir"
}

# Return template paths for AI
Write-Output "TEMPLATES_DIR=templates/decomposition"
Write-Output "MEMORY_FILE=memory/context.md"

exit 0