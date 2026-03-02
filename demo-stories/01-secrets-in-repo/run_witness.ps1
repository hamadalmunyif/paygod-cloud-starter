Param(
  [string]$Clock = "2026-02-15T00:00:00Z"
)

$ErrorActionPreference = "Stop"

# نحن داخل paygod-cloud-starter
$root   = (Get-Location).Path
$kernel = Join-Path $root "kernel"
$runs   = Join-Path $root "runs"

if (!(Test-Path $kernel)) { throw "Kernel submodule missing at: $kernel" }
New-Item -ItemType Directory -Force -Path $runs | Out-Null

# 1) Witness strict PASS (تشغيل من داخل kernel)
pwsh -NoProfile -File (Join-Path $kernel "tools\phase4_docker_witness.ps1") `
  -Mode strict `
  -PackPath "packs/core/secrets-in-repo-guard" `
  -Clock $Clock | Write-Host

# 2) مصدر المخرجات المحكوم بها
$src = Join-Path $kernel "_witness_tmp\out1"
if (!(Test-Path $src)) { throw "Missing witness output: $src" }

# 3) اقرأ bundle_digest من manifest.json
$manifestPath = Join-Path $src "manifest.json"
$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

# بعض الإصدارات تخزنها في manifest.bundle.bundle_digest
$bundle = $null
if ($manifest.bundle -and $manifest.bundle.bundle_digest) { $bundle = $manifest.bundle.bundle_digest }
if (!$bundle) { throw "Could not find bundle_digest in manifest.json" }

$dst = Join-Path $runs $bundle
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Recurse -Force (Join-Path $src "*") $dst

# 4) status.json (UI convenience فقط - غير sealed)
$plan = Get-Content (Join-Path $dst "plan.json") -Raw | ConvertFrom-Json
$packName = $plan.pack.name
$packVer  = $plan.pack.version

$reasons = @()
$ledgerPath = Join-Path $dst "ledger.jsonl"
$last = $null
if (Test-Path $ledgerPath) {
  $lastLine = (Get-Content $ledgerPath | Where-Object { $_.Trim() -ne "" } | Select-Object -Last 1)
  if ($lastLine) { $last = $lastLine | ConvertFrom-Json }
  if ($last -and $last.data) {
    $reasons += ("{0}:{1} - {2}" -f $last.data.verdict, $last.data.rule_name, $last.data.reason)
  }
}

$findingsPath = Join-Path $dst "findings.json"
if ((Test-Path $findingsPath) -and ($reasons.Count -lt 3)) {
  $findings = (Get-Content $findingsPath -Raw | ConvertFrom-Json).findings
  foreach ($f in $findings) {
    if ($reasons.Count -ge 3) { break }
    $reasons += ("{0}:{1} - {2}" -f $f.kind, $f.code, $f.message)
  }
}

if ($reasons.Count -eq 0) { $reasons = @("No findings extracted. See ledger/findings.") }
if ($reasons.Count -gt 3) { $reasons = $reasons[0..2] }

$result = "FLAG"
if ($last -and $last.data -and $last.data.verdict) {
  if ($last.data.verdict -eq "allow") { $result = "PASS" }
  elseif ($last.data.verdict -eq "deny") { $result = "DENY" }
}

$status = [ordered]@{
  run_id = $bundle
  pack_id = $packName
  pack_version = $packVer
  result = $result
  bundle_digest = $bundle
  top_reasons = $reasons
}

$status | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 (Join-Path $dst "status.json")

Write-Host "OK: run exported to $dst"


