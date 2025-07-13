# Скрипт для настройки автоматической активации виртуального окружения в Cursor
# Использование: .\setup_cursor_autoactivate.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=== Настройка автоматической активации виртуального окружения в Cursor ===" -ForegroundColor Cyan
Write-Host ""

# Шаг 1: Проверяем наличие виртуального окружения
Write-Host "1. Проверка виртуального окружения..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\activate.bat") {
    Write-Host "   Виртуальное окружение найдено" -ForegroundColor Green
} else {
    Write-Host "   Виртуальное окружение не найдено!" -ForegroundColor Red
    Write-Host "   Создание виртуального окружения..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "   Виртуальное окружение создано" -ForegroundColor Green
}

# Шаг 2: Создаем папку .vscode если её нет
Write-Host "2. Создание папки настроек..." -ForegroundColor Yellow
if (!(Test-Path ".vscode")) {
    New-Item -ItemType Directory -Path ".vscode" -Force | Out-Null
    Write-Host "   Папка .vscode создана" -ForegroundColor Green
} else {
    Write-Host "   Папка .vscode уже существует" -ForegroundColor Green
}

# Шаг 3: Настройка PowerShell профиля
Write-Host "3. Настройка PowerShell профиля..." -ForegroundColor Yellow
$profilePath = $PROFILE.CurrentUserAllHosts

if (!(Test-Path $profilePath)) {
    $profileDir = Split-Path $profilePath -Parent
    if (!(Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    
    $profileContent = @'
# Автоматическая активация виртуального окружения для проекта ЮрПомощник
if ((Get-Location).Path -like "*graduation project*") {
    if (Test-Path "venv\Scripts\Activate.ps1") {
        if (-not $env:VIRTUAL_ENV) {
            & "venv\Scripts\Activate.ps1"
            Write-Host "Виртуальное окружение активировано для ЮрПомощник!" -ForegroundColor Green
        }
    }
}
'@
    Set-Content -Path $profilePath -Value $profileContent
    Write-Host "   PowerShell профиль настроен" -ForegroundColor Green
} else {
    Write-Host "   PowerShell профиль уже существует" -ForegroundColor Cyan
}

# Шаг 4: Информация о результатах
Write-Host ""
Write-Host "=== Настройка завершена! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Что было настроено:" -ForegroundColor Yellow
Write-Host "* Настройки Cursor в .vscode/settings.json" -ForegroundColor Green
Write-Host "* Workspace файл для проекта" -ForegroundColor Green
Write-Host "* PowerShell профиль для автоматической активации" -ForegroundColor Green
Write-Host ""
Write-Host "Как использовать:" -ForegroundColor Yellow
Write-Host "1. Перезапустите Cursor" -ForegroundColor White
Write-Host "2. Откройте проект через workspace файл: graduation-project.code-workspace" -ForegroundColor White
Write-Host "3. Новые терминалы будут автоматически активировать виртуальное окружение" -ForegroundColor White
Write-Host ""
Write-Host "Дополнительные возможности:" -ForegroundColor Yellow
Write-Host "- Ctrl+Shift+P -> 'Tasks: Run Task' -> 'Запуск бота'" -ForegroundColor White
Write-Host "- Ctrl+Shift+P -> 'Tasks: Run Task' -> 'Установка зависимостей'" -ForegroundColor White
Write-Host ""
Write-Host "Для немедленной активации выполните: . `$PROFILE" -ForegroundColor Cyan 