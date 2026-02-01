$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $scriptDir "..")
$ocrDir = Join-Path $root "src\assets\ocr"
$outPath = Join-Path $ocrDir "wordlist.txt"

if (-not (Test-Path $ocrDir)) {
    throw "OCR directory not found: $ocrDir"
}

Get-ChildItem -Path $ocrDir -Filter *.txt |
    Where-Object { $_.Name -ne "wordlist.txt" } |
    ForEach-Object { Get-Content $_.FullName } |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -ne "" } |
    Sort-Object -Unique |
    Set-Content -Path $outPath -Encoding ASCII

Write-Host "Wrote wordlist to $outPath"
