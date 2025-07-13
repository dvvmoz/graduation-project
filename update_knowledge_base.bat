@echo off
chcp 65001 > nul
title Обновление базы знаний юридического чат-бота

echo.
echo ==================================================
echo 🤖 ОБНОВЛЕНИЕ БАЗЫ ЗНАНИЙ ЮРИДИЧЕСКОГО ЧАТ-БОТА
echo ==================================================
echo.

REM Проверяем существование Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден! Установите Python 3.8+ и попробуйте снова.
    pause
    exit /b 1
)

REM Проверяем существование виртуального окружения
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Активация виртуального окружения...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Виртуальное окружение не найдено, используем системный Python
)

REM Проверяем существование главного скрипта
if not exist "quick_update_knowledge_base.py" (
    echo ❌ Файл quick_update_knowledge_base.py не найден!
    echo 💡 Убедитесь, что вы запускаете батч-файл из корневой папки проекта
    pause
    exit /b 1
)

REM Проверяем существование модулей
if not exist "modules\knowledge_base.py" (
    echo ❌ Модуль knowledge_base.py не найден!
    echo 💡 Убедитесь, что все файлы проекта на месте
    pause
    exit /b 1
)

echo ✅ Все проверки пройдены, запускаем интерфейс обновления...
echo.

REM Запускаем скрипт обновления
python quick_update_knowledge_base.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка при запуске скрипта обновления!
    echo 💡 Проверьте логи выше для получения подробной информации
    pause
    exit /b 1
)

echo.
echo ✅ Работа завершена!
pause 