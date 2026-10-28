# QA Round 11 evaluation campaign runner (E01-E04, real mode).
# Resume-safe: the harness skips run_ids already present in runs.jsonl.
# Loads root .env so the in-run LLM judge sees OPENAI_API_KEY (os.environ).
# Console per experiment is captured to _console_r11.log for QA evidence.
$ErrorActionPreference = 'Stop'
Set-Location c:\USFQ\TESIS\playground\MVP_v1
$env:PYTHONIOENCODING = 'utf-8'

# Export API keys from root .env into the process environment (idempotent).
Get-Content .env | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
        $k, $v = $line.Split('=', 2)
        if (-not [Environment]::GetEnvironmentVariable($k.Trim())) {
            [Environment]::SetEnvironmentVariable($k.Trim(), $v.Trim().Trim("'"), 'Process')
        }
    }
}
Write-Output ("OPENAI_API_KEY exported: " + [bool]$env:OPENAI_API_KEY)

$experiments = @(
    'E04_evaluator_temperature',   # 18 runs (6 done, resume completes arms 1-2)
    'E03_robustness_clones',       # 10 runs
    'E01_temperature_sweep',       # 27 runs
    'E02_rag_topk_sweep'           # 27 runs
)
foreach ($exp in $experiments) {
    $dir = "test\evaluation\experiments\$exp"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Write-Output "=== START $exp $(Get-Date -Format o) ==="
    cmd /c ".venv\Scripts\python.exe -m test.evaluation.src.harness --experiment $exp --real > $dir\_console_r11.log 2>&1"
    Write-Output "=== END $exp exit=$LASTEXITCODE $(Get-Date -Format o) ==="
    if ($LASTEXITCODE -ne 0) { throw "harness for $exp exited with $LASTEXITCODE" }
}
Write-Output "=== CAMPAIGN DONE $(Get-Date -Format o) ==="