# Execute tasks continuously from task list - PowerShell Version

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$Command = "next",

    [Parameter(Mandatory=$false, Position=1)]
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

# Find active feature if not provided
if ([string]::IsNullOrEmpty($FeatureDir)) {
    $ContextFile = Join-Path $ProjectRoot "memory\context.md"
    if (Test-Path $ContextFile) {
        # Extract active feature from context
        $contextContent = Get-Content $ContextFile -Raw
        if ($contextContent -match "Active Feature:\s*(.+)") {
            $FeatureName = $matches[1].Trim()
        }
        if ($contextContent -match "Feature ID:\s*(.+)") {
            $FeatureId = $matches[1].Trim()
        }

        if ($FeatureId -and $FeatureName) {
            # Convert to branch name format
            $BranchSafeName = $FeatureName.ToLower() -replace '[^a-z0-9-]', '-' -replace '--+', '-' -replace '^-|-$', ''
            $FeatureDir = "$FeatureId-$BranchSafeName"
            Log-Message "Using active feature: $FeatureDir"
        } else {
            Exit-WithError "No active feature found in context file"
        }
    } else {
        Exit-WithError "No feature directory provided and no context file found"
    }
}

$TaskDir = Join-Path $ProjectRoot "tasks\$FeatureDir"

# Ensure tasks directory exists
if (-not (Test-Path $TaskDir)) {
    Exit-WithError "Tasks directory not found: $TaskDir"
}

# Find latest task file
$taskFiles = Get-ChildItem -Path $TaskDir -Filter "*.md" -ErrorAction SilentlyContinue |
             Sort-Object LastWriteTime -Descending |
             Select-Object -First 1

if (-not $taskFiles) {
    Exit-WithError "No task files found in $TaskDir"
}

$TaskFile = $taskFiles.FullName
Log-Message "Analyzing task file: $TaskFile"

# Read task content
$taskContent = Get-Content $TaskFile -Raw

# Detect if decomposed (service-specific tasks)
$IsDecomposed = $false
if ($taskContent -match "AUTH-T[0-9]|USER-T[0-9]|INT-T[0-9]") {
    $IsDecomposed = $true
    Log-Message "Detected decomposed architecture with service-specific tasks"
}

# Count task status using regex
$taskPattern = '^- \[.\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})'
$allTasks = [regex]::Matches($taskContent, $taskPattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
$TotalTasks = $allTasks.Count

$CompletedTasks = ([regex]::Matches($taskContent, '^- \[x\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
$PendingTasks = ([regex]::Matches($taskContent, '^- \[ \] (T[0-9]{3}|[A-Z]+-T[0-9]{3})', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
$InProgressTasks = ([regex]::Matches($taskContent, '^- \[>\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
$BlockedTasks = ([regex]::Matches($taskContent, '^- \[!\] (T[0-9]{3}|[A-Z]+-T[0-9]{3})', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count

# Find next task to execute
$NextTask = ""
$TaskDetails = ""

switch ($Command) {
    { $_ -in "next", "continue" } {
        # Find first in-progress task
        $inProgressMatch = [regex]::Match($taskContent, '^- \[>\] ((T[0-9]{3}|[A-Z]+-T[0-9]{3}): .+)$', [System.Text.RegularExpressions.RegexOptions]::Multiline)
        if ($inProgressMatch.Success) {
            $NextTask = $inProgressMatch.Groups[1].Value
            $TaskDetails = "RESUMING IN-PROGRESS TASK"
        } else {
            # Find first pending task
            $pendingMatch = [regex]::Match($taskContent, '^- \[ \] ((T[0-9]{3}|[A-Z]+-T[0-9]{3}): .+)$', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            if ($pendingMatch.Success) {
                $NextTask = $pendingMatch.Groups[1].Value
                $TaskDetails = "STARTING NEW TASK"
            }
        }
    }
    "all" {
        if ($PendingTasks -gt 0 -or $InProgressTasks -gt 0) {
            $NextTask = "ALL_REMAINING"
            $TaskDetails = "EXECUTE ALL TASKS WITHOUT STOPPING"
        }
    }
    default {
        # Specific task requested
        $specificMatch = [regex]::Match($taskContent, "^- \[.\] (($Command): .+)$", [System.Text.RegularExpressions.RegexOptions]::Multiline)
        if ($specificMatch.Success) {
            $NextTask = $specificMatch.Groups[1].Value
            $TaskDetails = "EXECUTE SPECIFIC TASK"
        }
    }
}

# Calculate progress
if ($TotalTasks -gt 0) {
    $Progress = [math]::Round(($CompletedTasks / $TotalTasks) * 100)
} else {
    $Progress = 0
}

# Output status
Write-Output "TASK_FILE=$TaskFile"
Write-Output "TOTAL_TASKS=$TotalTasks"
Write-Output "COMPLETED_TASKS=$CompletedTasks"
Write-Output "PENDING_TASKS=$PendingTasks"
Write-Output "IN_PROGRESS_TASKS=$InProgressTasks"
Write-Output "BLOCKED_TASKS=$BlockedTasks"
Write-Output "PROGRESS=$Progress%"

if ($IsDecomposed) {
    Write-Output "ARCHITECTURE=Microservices"
} else {
    Write-Output "ARCHITECTURE=Monolithic"
}

if ($NextTask) {
    Write-Output "NEXT_TASK=$NextTask"
    Write-Output "ACTION=$TaskDetails"
    if ($Command -eq "all") {
        Write-Output "MODE=CONTINUOUS"
        Write-Output "INSTRUCTION=Execute all tasks without stopping, no explanations between tasks"
    } else {
        Write-Output "MODE=SINGLE"
        Write-Output "INSTRUCTION=Execute this task and report results"
    }
} else {
    if ($CompletedTasks -eq $TotalTasks -and $TotalTasks -gt 0) {
        Write-Output "STATUS=ALL_COMPLETE"
        Write-Output "MESSAGE=Congratulations! All tasks have been completed!"
    } elseif ($BlockedTasks -gt 0) {
        Write-Output "STATUS=BLOCKED"
        Write-Output "MESSAGE=All remaining tasks are blocked. Resolve blockers first."
    } else {
        Write-Output "STATUS=NO_TASKS"
        Write-Output "MESSAGE=No tasks available to execute"
    }
}

Log-Message "Task analysis complete"
exit 0