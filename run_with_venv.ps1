# PowerShell скрипт для запуска команд в виртуальном окружении
# Использование: .\run_with_venv.ps1 "команда"

param(
    [Parameter(Mandatory=$true)]
    [string]$Command
)

Write-Host "========================================" -ForegroundColor Green
Write-Host "Запуск команды в виртуальном окружении" -ForegroundColor Green
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

Write-Host "Выполнение команды: $Command" -ForegroundColor Cyan
Invoke-Expression $Command

Write-Host "========================================" -ForegroundColor Green
Write-Host "Команда завершена" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green 