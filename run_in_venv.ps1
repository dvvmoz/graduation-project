# Проверка и активация venv
if (-not (Test-Path env:VIRTUAL_ENV)) {
    Write-Host 'Активация виртуального окружения...'
    .\venv\Scripts\Activate.ps1
    # Перезапуск скрипта уже внутри venv
    & powershell -ExecutionPolicy Bypass -File $MyInvocation.MyCommand.Path @args
    exit
} 