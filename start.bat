@echo off
chcp 65001 > nul

:: Скрипт для быстрого запуска проекта ЮрПомощник в Windows

echo 🚀 Запуск ЮрПомощника...

:: Проверяем наличие .env файла
if not exist ".env" (
    echo ❌ Файл .env не найден!
    echo 📝 Создайте файл .env на основе env.example
    echo    copy env.example .env
    echo    notepad .env
    pause
    exit /b 1
)

:: Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)

:: Проверяем наличие виртуального окружения
if not exist "venv" (
    echo 📦 Создаю виртуальное окружение...
    python -m venv venv
)

:: Активируем виртуальное окружение
echo 🔧 Активирую виртуальное окружение...
call venv\Scripts\activate.bat

:: Устанавливаем зависимости
echo 📚 Устанавливаю зависимости...
pip install -r requirements.txt

:: Проверяем наличие папки data
if not exist "data" (
    echo 📁 Создаю папку data...
    mkdir data
)

:: Проверяем наличие PDF файлов
dir data\*.pdf >nul 2>&1
if %errorlevel% neq 0 (
    echo 📄 Добавьте PDF файлы в папку data\ и запустите скрипт снова
    echo    python scripts\populate_db.py
    echo.
)

:: Проверяем наличие базы знаний
if not exist "db\chroma" (
    echo 🧠 Создаю базу знаний...
    python scripts\populate_db.py
)

:: Запускаем бота
echo 🤖 Запуск бота...
python main.py

pause 