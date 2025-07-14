# PowerShell скрипт для обновления requirements.txt из виртуального окружения

Write-Host "========================================" -ForegroundColor Green
Write-Host "Обновление requirements.txt из venv" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Проверяем существование виртуального окружения
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "ОШИБКА: Виртуальное окружение не найдено!" -ForegroundColor Red
    Write-Host "Создайте виртуальное окружение: python -m venv venv" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "Активация виртуального окружения..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

Write-Host "Обновление pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "Создание полного requirements.txt..." -ForegroundColor Yellow
pip freeze | Out-File -FilePath "requirements.txt" -Encoding UTF8

Write-Host "Создание минимального requirements.minimal.txt..." -ForegroundColor Yellow
@"
aiogram==3.3.0
openai==1.12.0
chromadb==0.4.22
PyMuPDF==1.23.14
python-dotenv==1.0.0
httpx==0.26.0
numpy==1.26.4
requests==2.31.0
beautifulsoup4==4.12.2
aiohttp==3.9.1
lxml==4.9.3
python-docx==0.8.11
Flask==3.0.0
Flask-Cors==4.0.0
psutil==5.9.6
scikit-learn==1.7.0
pandas==2.3.1
scipy==1.15.3
"@ | Out-File -FilePath "requirements.minimal.txt" -Encoding UTF8

Write-Host "Создание backup файла..." -ForegroundColor Yellow
Copy-Item "requirements.txt" "requirements.backup.txt"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Обновление завершено!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Файлы обновлены:" -ForegroundColor Cyan
Write-Host "- requirements.txt (полный список)" -ForegroundColor White
Write-Host "- requirements.minimal.txt (минимальный набор)" -ForegroundColor White
Write-Host "- requirements.backup.txt (резервная копия)" -ForegroundColor White
Write-Host ""
Write-Host "Количество пакетов в requirements.txt:" -ForegroundColor Cyan
$packageCount = (Get-Content "requirements.txt" | Where-Object { $_ -match "==" }).Count
Write-Host $packageCount -ForegroundColor White
Write-Host ""
Read-Host "Нажмите Enter для выхода" 