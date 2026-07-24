$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$started = Get-Date

function Invoke-PythonStep {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Python step failed: python $($Arguments -join ' ')" }
}

Invoke-PythonStep scripts/rebuild_weather_features.py
Invoke-PythonStep scripts/run_audit.py --config configs/fidelity_gate.yaml --stage all
Invoke-PythonStep scripts/build_audit_v2_assets.py
Invoke-PythonStep -m unittest discover -s tests -v
Invoke-PythonStep scripts/reference_audit.py
Invoke-PythonStep scripts/build_paper.py --target ictai2026_blind
Invoke-PythonStep scripts/audit_pdf.py submission/ictai2026_paper_blind.pdf
Invoke-PythonStep scripts/verify_artifacts.py --manifest artifacts/audit_manifest.json
Invoke-PythonStep scripts/verify_artifacts.py --manifest artifacts/audit_manifest.json --verify-only
Invoke-PythonStep scripts/build_anonymous_artifact.py --out submission/ictai2026_anonymous_artifact.zip
Invoke-PythonStep scripts/audit_anonymity.py submission/ictai2026_anonymous_artifact.zip
Invoke-PythonStep scripts/build_anonymous_artifact.py --out submission/ictai2026_anonymous_artifact.zip
Invoke-PythonStep scripts/audit_anonymity.py submission/ictai2026_anonymous_artifact.zip
Invoke-PythonStep scripts/final_submission_audit.py
Invoke-PythonStep scripts/final_pdf_numerical_crosscheck.py
Invoke-PythonStep scripts/write_upload_manifest.py
Invoke-PythonStep scripts/write_easychair_upload_checklist.py
$elapsed = ((Get-Date) - $started).TotalSeconds
Invoke-PythonStep scripts/write_reproduction_log.py --duration-seconds "$elapsed"
Invoke-PythonStep scripts/check_submission_checklist.py
