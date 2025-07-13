# Скрипт для активации виртуального окружения
# Использование: .\activate_env.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Активация виртуального окружения..." -ForegroundColor Yellow

# Проверяем наличие виртуального окружения
if (!(Test-Path "venv")) {
    Write-Host "Виртуальное окружение не найдено. Создаю..." -ForegroundColor Cyan
    python -m venv venv
}

# Активируем виртуальное окружение
& "venv\Scripts\Activate.ps1"

Write-Host "Виртуальное окружение активировано!" -ForegroundColor Green
Write-Host "Рабочая папка: $(Get-Location)" -ForegroundColor Cyan
Write-Host "Python: $(python --version)" -ForegroundColor Magenta
Write-Host "Pip: $(pip --version)" -ForegroundColor Magenta

# Показываем установленные пакеты
Write-Host "`nОсновные установленные пакеты:" -ForegroundColor Yellow
pip list | Select-String "aiogram|openai|flask|scikit-learn|chromadb" | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray } 