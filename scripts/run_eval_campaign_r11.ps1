# QA Round 11 evaluation campaign runner (E01-E04, real mode).
# Runs experiments in cost order, flushing stdout per line. Windows-safe.
$ErrorActionPreference = 'Stop'
Set-Location c:\USFQ\TESIS\playground\MVP_v1
$env:PYTHONIOENCODING = 'utf-8'
$experiments = @(
    'E04_evaluator_temperature',   # 18 runs, cheapest first
    'E03_robustness_clones',       # 10 runs
    'E01_temperature_sweep',       # 27 runs
    'E02_rag_topk_sweep'           # 27 runs
)
foreach ($exp in $experiments) {
    Write-Output "=== START $exp $(Get-Date -Format o) ==="
    & .venv\Scripts\python.exe -m test.evaluation.src.harness --experiment $exp --real 2>&1 | ForEach-Object { "$_" }
    Write-Output "=== END $exp exit=$LASTEXITCODE $(Get-Date -Format o) ==="
}
Write-Output "=== CAMPAIGN DONE $(Get-Date -Format o) ==="