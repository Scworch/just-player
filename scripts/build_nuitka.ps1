param(
    [switch]$OneFile
)

$ErrorActionPreference = "Stop"

python -m pip install --upgrade nuitka ordered-set zstandard

$cmd = @(
    "python", "-m", "nuitka",
    "--standalone",
    "--assume-yes-for-downloads",
    "--enable-plugin=tk-inter",
    "--windows-console-mode=disable",
    "--output-dir=build",
    "run.py"
)

if ($OneFile) {
    $cmd += "--onefile"
}

if (Test-Path ".\mpv-2.dll") {
    $cmd += "--include-data-files=mpv-2.dll=mpv-2.dll"
}

Write-Host "Running: $($cmd -join ' ')"
& $cmd[0] $cmd[1..($cmd.Count - 1)]
