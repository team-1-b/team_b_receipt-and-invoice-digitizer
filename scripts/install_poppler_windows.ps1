<#
Simple installer for Poppler (Windows).

Usage:
  Right-click -> Run with PowerShell or from an elevated PowerShell prompt:
  .\install_poppler_windows.ps1

This script downloads a Poppler release zip, extracts the `bin` folder
into `vendor/poppler/bin` inside the repository, and sets the `POPPLER_PATH`
user environment variable to that `bin` path.

If you prefer a different release, set the `$DownloadUrl` variable accordingly.
#>

$ErrorActionPreference = 'Stop'

# Default download URL (may be updated in future releases). If this link fails,
# replace with a current release from https://github.com/oschwartz10612/poppler-windows/releases
$DownloadUrl = 'https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0/Release-23.08.0-0.zip'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Resolve-Path (Join-Path $scriptRoot '..')
$dest = Join-Path $repoRoot 'vendor\poppler'
$binDest = Join-Path $dest 'bin'

Write-Host "Installing Poppler into: $binDest"
if (-Not (Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }

$tmpZip = Join-Path $env:TEMP 'poppler_download.zip'
$tmpExtract = Join-Path $env:TEMP 'poppler_extracted'

if (Test-Path $tmpZip) { Remove-Item $tmpZip -Force }
if (Test-Path $tmpExtract) { Remove-Item $tmpExtract -Recurse -Force }

Write-Host "Downloading Poppler from: $DownloadUrl"
Invoke-WebRequest -Uri $DownloadUrl -OutFile $tmpZip -UseBasicParsing

Write-Host "Extracting..."
Expand-Archive -Path $tmpZip -DestinationPath $tmpExtract -Force

# Locate the folder that contains a 'bin' subfolder
$binSource = Get-ChildItem -Path $tmpExtract -Directory -Recurse | Where-Object { Test-Path (Join-Path $_.FullName 'bin') } | Select-Object -First 1
if (-not $binSource) {
    Write-Error "Could not find 'bin' inside the downloaded archive. Inspect $tmpExtract"
    exit 1
}

if (-Not (Test-Path $binDest)) { New-Item -ItemType Directory -Path $binDest -Force | Out-Null }

Write-Host "Copying binaries to $binDest"
Copy-Item -Path (Join-Path $binSource.FullName 'bin\*') -Destination $binDest -Recurse -Force

# Set a user environment variable so `pdf2image` can find Poppler
[Environment]::SetEnvironmentVariable('POPPLER_PATH', $binDest, 'User')

Write-Host "POPPLER_PATH set to $binDest (User environment)."
Write-Host "You may need to restart your terminal or log out and log back in for changes to take effect."

# Cleanup
Remove-Item $tmpZip -Force -ErrorAction SilentlyContinue
Remove-Item $tmpExtract -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Done. Run your app; `pdf2image` will now use the vendored Poppler when `POPPLER_PATH` is set.`"
