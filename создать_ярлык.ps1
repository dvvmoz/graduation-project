# Скрипт для создания ярлыка на рабочем столе
# Использование: .\создать_ярлык.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Создание ярлыка на рабочем столе..." -ForegroundColor Yellow

# Получаем путь к рабочему столу
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "ЮрПомощник - Среда разработки.lnk"

# Создаем объект WScript.Shell
$shell = New-Object -ComObject WScript.Shell

# Создаем ярлык
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = Join-Path (Get-Location) "dev_shell.bat"
$shortcut.WorkingDirectory = (Get-Location).ToString()
$shortcut.Description = "Запуск среды разработки ЮрПомощника с активированным виртуальным окружением"
$shortcut.IconLocation = "shell32.dll,43"
$shortcut.Save()

Write-Host "Ярлык создан на рабочем столе: $shortcutPath" -ForegroundColor Green
Write-Host "Теперь вы можете запускать среду разработки двойным щелчком по ярлыку!" -ForegroundColor Cyan 