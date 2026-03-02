Param(
  [Parameter(Mandatory=$true)][string]$PackDir,
  [Parameter(Mandatory=$true)][string]$InputFile,
  [string]$ImageName = "paygod/runner:dev",
  [ValidateSet("strict","canonical")][string]$Mode = "strict",
  [string]$Clock = "2026-02-15T00:00:00Z",
  [string]$TmpRoot = "_witness_tmp_cloud"
)

$ErrorActionPreference = "Stop"

$root = (Get-Location).Path
$packFull  = (Resolve-Path (Join-Path $root $PackDir)).Path
$inputFull = (Resolve-Path (Join-Path $root $InputFile)).Path

$tmp = Join-Path $root $TmpRoot
$inputDir = Join-Path $tmp "input"
$out1 = Join-Path $tmp "out1"
$out2 = Join-Path $tmp "out2"

function New-CleanDir([string]$p) {
  if (Test-Path $p) { Remove-Item -Recurse -Force $p }
  New-Item -ItemType Directory -Force -Path $p | Out-Null
}

# Clean temp only (never touch repo root)
New-CleanDir $tmp
New-Item -ItemType Directory -Force -Path $inputDir | Out-Null
Copy-Item -Force $inputFull (Join-Path $inputDir "input.json")
New-CleanDir $out1
New-CleanDir $out2

# Run 1 (deterministic clock)
docker run --rm `
  -e "PAYGOD_CLOCK=$Clock" `
  -e "PAYGOD_STRICT=1" `
  -v "${packFull}:/pack:ro" `
  -v "${inputDir}:/input:ro" `
  -v "${out1}:/out:rw" `
  $ImageName `
  run --pack /pack --input /input/input.json --out /out | Write-Host

# Run 2 (same clock)
docker run --rm `
  -e "PAYGOD_CLOCK=$Clock" `
  -e "PAYGOD_STRICT=1" `
  -v "${packFull}:/pack:ro" `
  -v "${inputDir}:/input:ro" `
  -v "${out2}:/out:rw" `
  $ImageName `
  run --pack /pack --input /input/input.json --out /out | Write-Host

$mf1 = Join-Path $out1 "manifest.json"
$mf2 = Join-Path $out2 "manifest.json"
if (!(Test-Path $mf1)) { throw "Missing: $mf1" }
if (!(Test-Path $mf2)) { throw "Missing: $mf2" }

$m1 = Get-Content $mf1 -Raw | ConvertFrom-Json
$m2 = Get-Content $mf2 -Raw | ConvertFrom-Json
$bd1 = $m1.bundle.bundle_digest
$bd2 = $m2.bundle.bundle_digest

if (!$bd1 -or !$bd2) { throw "bundle_digest missing in manifest(s)" }
if ($bd1 -ne $bd2) { throw "FAIL ($Mode): bundle_digest mismatch`n  out1=$bd1`n  out2=$bd2" }

Write-Host "PASS ($Mode): bundle_digest=$bd1"

$runs = Join-Path $root "runs"
New-Item -ItemType Directory -Force -Path $runs | Out-Null
$dst = Join-Path $runs $bd1
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Recurse -Force (Join-Path $out1 "*") $dst

Write-Host "OK: run exported to $dst"
