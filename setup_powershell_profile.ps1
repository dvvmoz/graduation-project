# Скрипт для настройки автоматической активации виртуального окружения в PowerShell
# Использование: .\setup_powershell_profile.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Настройка автоматической активации виртуального окружения..." -ForegroundColor Yellow

# Получаем путь к профилю PowerShell
$profilePath = $PROFILE.CurrentUserAllHosts
Write-Host "Путь к профилю: $profilePath" -ForegroundColor Cyan

# Создаем директорию для профиля, если она не существует
$profileDir = Split-Path $profilePath -Parent
if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force
    Write-Host "Создана директория профиля: $profileDir" -ForegroundColor Green
}

# Код для добавления в профиль
$profileCode = @"
# Автоматическая активация виртуального окружения для проектов
function Activate-ProjectVenv {
    `$currentPath = Get-Location
    `$projectMarkers = @('.git', 'requirements.txt', 'pyproject.toml', 'setup.py')
    
    # Ищем корень проекта
    `$searchPath = `$currentPath
    while (`$searchPath -ne `$null -and `$searchPath.Parent -ne `$null) {
        `$hasMarker = `$projectMarkers | Where-Object { Test-Path (Join-Path `$searchPath `$_) }
        if (`$hasMarker) {
            `$venvPath = Join-Path `$searchPath "venv\Scripts\Activate.ps1"
            if (Test-Path `$venvPath) {
                # Проверяем, не активировано ли уже виртуальное окружение
                if (-not `$env:VIRTUAL_ENV) {
                    & `$venvPath
                    Write-Host "✅ Виртуальное окружение активировано для проекта: `$(`$searchPath.Name)" -ForegroundColor Green
                }
                return
            }
        }
        `$searchPath = `$searchPath.Parent
    }
}

# Автоматически активируем виртуальное окружение при запуске
if ((Get-Location).Path -like "*graduation project*") {
    Activate-ProjectVenv
}
"@

# Проверяем, существует ли уже профиль
if (Test-Path $profilePath) {
    $existingContent = Get-Content $profilePath -Raw
    if ($existingContent -notlike "*Activate-ProjectVenv*") {
        # Добавляем код к существующему профилю
        Add-Content -Path $profilePath -Value "`n$profileCode"
        Write-Host "Код добавлен к существующему профилю" -ForegroundColor Green
    } else {
        Write-Host "Автоматическая активация уже настроена в профиле" -ForegroundColor Yellow
    }
} else {
    # Создаем новый профиль
    Set-Content -Path $profilePath -Value $profileCode
    Write-Host "Создан новый профиль PowerShell" -ForegroundColor Green
}

Write-Host "`nПрофиль PowerShell настроен!" -ForegroundColor Green
Write-Host "Перезапустите PowerShell или выполните: . `$PROFILE" -ForegroundColor Cyan 