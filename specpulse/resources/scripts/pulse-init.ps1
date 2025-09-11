# SpecPulse Feature Initialization Script
# Cross-platform PowerShell equivalent of pulse-init.sh

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName,
    
    [string]$CustomId = ""
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

function Sanitize-FeatureName {
    param([string]$Name)
    
    if ([string]::IsNullOrWhiteSpace($Name)) {
        Exit-WithError "Feature name cannot be empty"
    }
    
    # Convert to lowercase, replace spaces and special chars with hyphens
    $Sanitized = $Name.ToLower() -replace '[^a-z0-9-]', '-'
    $Sanitized = $Sanitized -replace '-+', '-'  # Remove consecutive hyphens
    $Sanitized = $Sanitized.Trim('-')  # Remove leading/trailing hyphens
    
    if ([string]::IsNullOrWhiteSpace($Sanitized)) {
        Exit-WithError "Invalid feature name: '$Name'"
    }
    
    return $Sanitized
}

function Get-FeatureId {
    param([string]$CustomId)
    
    if ($CustomId) {
        return "{0:D3}" -f [int]$CustomId
    }
    
    # Find existing feature directories
    $SpecsDir = Join-Path $ProjectRoot "specs"
    if (Test-Path $SpecsDir) {
        $Existing = Get-ChildItem -Path $SpecsDir -Directory | 
                  Where-Object { $_.Name -match '^\d+$' } |
                  Sort-Object Name
        $NextId = $Existing.Count + 1
    } else {
        $NextId = 1
    }
    
    return "{0:D3}" -f $NextId
}

function Create-Directories {
    param([string]$BranchName)
    
    $Directories = @(
        (Join-Path $ProjectRoot "specs" $BranchName),
        (Join-Path $ProjectRoot "plans" $BranchName),
        (Join-Path $ProjectRoot "tasks" $BranchName)
    )
    
    foreach ($Directory in $Directories) {
        try {
            New-Item -ItemType Directory -Path $Directory -Force | Out-Null
            Write-Log "Created directory: $Directory"
        } catch {
            Exit-WithError "Failed to create directory $Directory : $_"
        }
    }
}

function Copy-Templates {
    param([string]$BranchName)
    
    $Templates = @{
        "spec.md" = (Join-Path $ProjectRoot "specs" $BranchName "spec.md")
        "plan.md" = (Join-Path $ProjectRoot "plans" $BranchName "plan.md")
        "task.md" = (Join-Path $ProjectRoot "tasks" $BranchName "tasks.md")
    }
    
    foreach ($Template in $Templates.GetEnumerator()) {
        $TemplatePath = Join-Path $TemplatesDir $Template.Key
        $TargetPath = $Template.Value
        
        if (-not (Test-Path $TemplatePath)) {
            Exit-WithError "Template not found: $TemplatePath"
        }
        
        try {
            Copy-Item $TemplatePath $TargetPath -Force
            Write-Log "Copied template to: $TargetPath"
        } catch {
            Exit-WithError "Failed to copy template $TemplatePath : $_"
        }
    }
}

function Update-Context {
    param(
        [string]$FeatureName,
        [string]$FeatureId,
        [string]$BranchName
    )
    
    try {
        New-Item -ItemType Directory -Path $MemoryDir -Force | Out-Null
        
        $ContextEntry = @"

## Active Feature: $FeatureName
- Feature ID: $FeatureId
- Branch: $BranchName
- Started: $(Get-Date -Format "o")
"@
        
        Add-Content -Path $ContextFile -Value $ContextEntry -Encoding UTF8
        Write-Log "Updated context file: $ContextFile"
    } catch {
        Exit-WithError "Failed to update context file: $_"
    }
}

function New-GitBranch {
    param([string]$BranchName)
    
    $GitDir = Join-Path $ProjectRoot ".git"
    if (-not (Test-Path $GitDir)) {
        return
    }
    
    try {
        # Check if branch already exists
        $ExistingBranch = git branch --list $BranchName
        if ($ExistingBranch) {
            Write-Log "Git branch '$BranchName' already exists, checking out"
            git checkout $BranchName
        } else {
            Write-Log "Creating new git branch '$BranchName'"
            git checkout -b $BranchName
        }
    } catch {
        Exit-WithError "Git operation failed: $_"
    }
}

# Main execution
Write-Log "Initializing feature: $FeatureName"

# Sanitize and generate identifiers
$SanitizedName = Sanitize-FeatureName -Name $FeatureName
$FeatureId = Get-FeatureId -CustomId $CustomId
$BranchName = "$FeatureId-$SanitizedName"

# Create structure
Create-Directories -BranchName $BranchName
Copy-Templates -BranchName $BranchName
Update-Context -FeatureName $FeatureName -FeatureId $FeatureId -BranchName $BranchName
New-GitBranch -BranchName $BranchName

# Output results
Write-Host "BRANCH_NAME=$BranchName"
Write-Host "SPEC_DIR=specs/$BranchName"
Write-Host "FEATURE_ID=$FeatureId"
Write-Host "STATUS=initialized"

Write-Log "Successfully initialized feature '$FeatureName' with ID $FeatureId"