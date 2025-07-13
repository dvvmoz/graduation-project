@echo off
chcp 65001 > nul

echo 🔧 Запуск среды разработки...

:: Проверяем наличие виртуального окружения
if not exist "venv" (
    echo 📦 Создаю виртуальное окружение...
    python -m venv venv
)

:: Активируем виртуальное окружение и открываем PowerShell
echo 🚀 Активирую виртуальное окружение...
call venv\Scripts\activate.bat && powershell.exe -NoExit -Command "& {Write-Host '✅ Виртуальное окружение активировано!' -ForegroundColor Green; Write-Host '📂 Рабочая папка: ' -NoNewline; Write-Host (Get-Location) -ForegroundColor Cyan}" 