[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InputDeck,

    [string]$Solver,

    [ValidateRange(1, 256)]
    [int]$Ncpu = 1,

    [string]$Memory,

    [string]$WorkDir,

    [string]$License,

    [switch]$Clean,

    [switch]$RequireNormalTermination,

    [switch]$ModelCheck
)

$ErrorActionPreference = 'Stop'

function Find-LsdynaSolvers {
    $candidates = @()

    foreach ($envName in @('LS_DYNA_SOLVER', 'LSDYNA_SOLVER')) {
        $value = [Environment]::GetEnvironmentVariable($envName)
        if ($value -and (Test-Path -LiteralPath $value -PathType Leaf)) {
            $candidates += (Resolve-Path -LiteralPath $value).Path
        }
    }

    foreach ($name in @('lsdyna_dp.exe', 'lsdyna_sp.exe', 'LSDYNA.exe', 'lsdyna.exe', 'ls-dyna.exe')) {
        $command = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($command -and $command.Source) {
            $candidates += $command.Source
        }
    }

    $roots = @()
    foreach ($envName in @('LSDYNA_HOME', 'LS_DYNA_HOME', 'LSTC_ROOT')) {
        $value = [Environment]::GetEnvironmentVariable($envName)
        if ($value) {
            $roots += [string]$value
        }
    }
    foreach ($entry in [Environment]::GetEnvironmentVariables().GetEnumerator()) {
        if ([string]$entry.Key -match '^AWP_ROOT\d+$' -and $entry.Value) {
            $roots += (Join-Path ([string]$entry.Value) 'ansys\bin\winx64')
        }
    }

    foreach ($root in $roots | Sort-Object -Unique) {
        if (-not (Test-Path -LiteralPath $root -PathType Container)) {
            continue
        }
        foreach ($candidate in Get-ChildItem -LiteralPath $root -File -ErrorAction SilentlyContinue) {
            if ($candidate.Name -match '^(lsdyna|ls-dyna).*\.exe$') {
                $candidates += $candidate.FullName
            }
        }
    }

    $candidates | Sort-Object -Unique
}

function Resolve-LsdynaSolver {
    param([string]$RequestedSolver)

    if ($RequestedSolver) {
        if (-not (Test-Path -LiteralPath $RequestedSolver -PathType Leaf)) {
            throw "Requested LS-DYNA solver does not exist: $RequestedSolver"
        }
        return (Resolve-Path -LiteralPath $RequestedSolver).Path
    }

    $candidates = @(Find-LsdynaSolvers)
    if ($candidates.Count -eq 0) {
        throw 'No LS-DYNA solver found through PATH or LS_DYNA_SOLVER/LSDYNA_HOME/LSTC_ROOT/AWP_ROOT*. Pass -Solver explicitly.'
    }
    if ($candidates.Count -gt 1) {
        $listed = $candidates -join [Environment]::NewLine
        throw "Multiple LS-DYNA solvers found; specify the version explicitly with -Solver:`n$listed"
    }
    return $candidates[0]
}

function Remove-LsdynaOutputs {
    param([string]$Directory)

    $resolved = (Resolve-Path -LiteralPath $Directory).Path
    $outputFamilies = @(
        'd3plot', 'd3dump', 'd3hsp', 'd3thdt', 'd3iter', 'd3eigv',
        'd3mode', 'd3mean', 'd3part', 'd3drfl', 'd3kil', 'd3ssd',
        'd3rlb', 'd3rms', 'd3max', 'd3min', 'messag', 'glstat',
        'matsum', 'nodout', 'binout', 'adptmp', 'elout', 'rcforc',
        'secforc', 'spcforc', 'swforc', 'rbdout', 'sleout', 'deforc',
        'jntforc', 'part_des'
    )
    $familyPattern = ($outputFamilies | ForEach-Object { [regex]::Escape($_) }) -join '|'
    $exactOutputs = @('status.out', 'lsrun.out', 'run.log', 'run_manifest.json')

    Get-ChildItem -LiteralPath $resolved -File -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Extension.ToLowerInvariant() -notin @('.k', '.key', '.dyn') -and
            ($_.Name -match "^(?:$familyPattern)(?:\d+)?$" -or $_.Name -in $exactOutputs)
        } |
        Remove-Item -Force
}

function Get-KeywordFileInventory {
    param([string]$Directory)

    $resolved = (Resolve-Path -LiteralPath $Directory).Path.TrimEnd('\', '/')
    $prefixLength = $resolved.Length + 1
    @(
        Get-ChildItem -LiteralPath $resolved -File -Recurse -ErrorAction Stop |
            Where-Object { $_.Extension.ToLowerInvariant() -in @('.k', '.key', '.dyn') } |
            Sort-Object FullName |
            ForEach-Object {
                $relativePath = if ($_.FullName.Length -ge $prefixLength) {
                    $_.FullName.Substring($prefixLength)
                }
                else {
                    $_.Name
                }
                [ordered]@{
                    relative_path = $relativePath
                    bytes = $_.Length
                    sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
                }
            }
    )
}

function Get-LsdynaInspectionOutputSignatures {
    param([string]$Directory)

    $signatures = [ordered]@{}
    # The inspector accepts arbitrary --require filenames. Snapshot every top-level
    # file so an unlisted output cannot be confused with an unchanged older file.
    Get-ChildItem -LiteralPath $Directory -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne 'run_manifest.json' } |
        Sort-Object Name |
        ForEach-Object {
            $signatures[$_.Name] = [ordered]@{
                bytes = $_.Length
                modified_at_utc = $_.LastWriteTimeUtc.ToString('o')
                sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
            }
        }
    return $signatures
}

function Get-ChangedOutputNames {
    param(
        [Collections.IDictionary]$Before,
        [Collections.IDictionary]$After
    )

    @(
        foreach ($name in $After.Keys) {
            if (-not $Before.Contains($name)) {
                $name
                continue
            }
            $old = $Before[$name]
            $new = $After[$name]
            if (
                $old.bytes -ne $new.bytes -or
                $old.modified_at_utc -ne $new.modified_at_utc -or
                $old.sha256 -ne $new.sha256
            ) {
                $name
            }
        }
    )
}

$deckPath = (Resolve-Path -LiteralPath $InputDeck).Path
$deckDir = Split-Path -Parent $deckPath
$runDir = if ($WorkDir) {
    if (-not (Test-Path -LiteralPath $WorkDir -PathType Container)) {
        New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
    }
    (Resolve-Path -LiteralPath $WorkDir).Path
}
else {
    $deckDir
}

if (-not [string]::Equals($runDir, $deckDir, [StringComparison]::OrdinalIgnoreCase)) {
    throw "The run directory must match the input deck directory so relative *INCLUDE paths resolve. deck=$deckDir, WorkDir=$runDir"
}

$solverPath = Resolve-LsdynaSolver -RequestedSolver $Solver

if ($Clean) {
    Remove-LsdynaOutputs -Directory $runDir
}

$solverArgs = @("i=$deckPath", "ncpu=$Ncpu")
if ($Memory) {
    $solverArgs += "memory=$Memory"
}
if ($ModelCheck) {
    $solverArgs += 'mcheck=y'
}

$startedAt = Get-Date
$previousLicense = $env:LSTC_LICENSE
if ($License) {
    $env:LSTC_LICENSE = $License
}

$solverVersion = [Diagnostics.FileVersionInfo]::GetVersionInfo($solverPath).FileVersion
$manifestPath = Join-Path $runDir 'run_manifest.json'
$keywordFiles = @(Get-KeywordFileInventory -Directory $runDir)
$preRunOutputSignatures = Get-LsdynaInspectionOutputSignatures -Directory $runDir
$manifest = [ordered]@{
    manifest_schema_version = 5
    status = 'running'
    manifest_created_before_solver = $true
    solver = $solverPath
    solver_file_version = $solverVersion
    input_deck = $deckPath
    input_sha256 = (Get-FileHash -LiteralPath $deckPath -Algorithm SHA256).Hash
    keyword_file_count = $keywordFiles.Count
    keyword_files = $keywordFiles
    pre_run_output_signatures = $preRunOutputSignatures
    current_run_outputs = @()
    normal_termination_evidence = @()
    work_dir = $runDir
    ncpu = $Ncpu
    memory = $Memory
    model_check = [bool]$ModelCheck
    license_source = if ($License) {
        'argument'
    }
    elseif ($previousLicense) {
        'environment'
    }
    else {
        'unset'
    }
    command = @($solverPath) + $solverArgs
    started_at = $startedAt.ToString('o')
    finished_at = $null
    elapsed_seconds = $null
    exit_code = $null
    normal_termination = $false
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$exitCode = $null
Push-Location $runDir
try {
    & $solverPath @solverArgs 2>&1 | Tee-Object -FilePath 'run.log'
    $exitCode = $LASTEXITCODE
}
finally {
    Pop-Location
    if ($License) {
        $env:LSTC_LICENSE = $previousLicense
    }
}
$finishedAt = Get-Date

$messagePath = Join-Path $runDir 'messag'
$d3hspPath = Join-Path $runDir 'd3hsp'
$runLogPath = Join-Path $runDir 'run.log'
$postRunOutputSignatures = Get-LsdynaInspectionOutputSignatures -Directory $runDir
$currentRunOutputs = @(Get-ChangedOutputNames -Before $preRunOutputSignatures -After $postRunOutputSignatures)
$normalTerminationEvidence = @()
foreach ($candidateName in $currentRunOutputs) {
    if ($candidateName -notmatch '^(?:messag\d*|run\.log)$') {
        continue
    }
    $candidate = Join-Path $runDir $candidateName
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        $content = Get-Content -LiteralPath $candidate -Raw
        if (($content -replace '\s+', '').ToLowerInvariant() -match 'normaltermination') {
            $normalTerminationEvidence += $candidateName
        }
    }
}
$normalTermination = $normalTerminationEvidence.Count -gt 0

$manifest.status = if ($exitCode -eq 0 -and $normalTermination) {
    'completed'
}
elseif ($exitCode -eq 0) {
    'completed_without_normal_termination'
}
else {
    'failed'
}
$manifest.finished_at = $finishedAt.ToString('o')
$manifest.elapsed_seconds = ($finishedAt - $startedAt).TotalSeconds
$manifest.exit_code = $exitCode
$manifest.normal_termination = $normalTermination
$manifest.current_run_outputs = $currentRunOutputs
$manifest.normal_termination_evidence = $normalTerminationEvidence
$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

if ($exitCode -ne 0) {
    throw "LS-DYNA exited with code $exitCode. Check $runLogPath and $messagePath."
}
if ($RequireNormalTermination -and -not $normalTermination) {
    throw "No Normal termination found in messag/run.log. Check $messagePath."
}

[PSCustomObject]@{
    Solver = $solverPath
    InputDeck = $deckPath
    WorkDir = $runDir
    Ncpu = $Ncpu
    Memory = $Memory
    ModelCheck = [bool]$ModelCheck
    ExitCode = $exitCode
    NormalTermination = $normalTermination
    Message = $messagePath
    D3hsp = $d3hspPath
    RunLog = $runLogPath
    Manifest = $manifestPath
    PhysicalStatus = 'pending'
}
