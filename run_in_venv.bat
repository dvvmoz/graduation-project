@echo off
REM Проверка и активация venv
if not defined VIRTUAL_ENV (
    echo Активация виртуального окружения...
    call .\venv\Scripts\activate.bat
    REM Перезапуск скрипта уже внутри venv
    call "%~f0" %*
    exit /b
) 