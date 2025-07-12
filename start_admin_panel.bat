@echo off
chcp 65001 > nul

echo 🎛️ Запуск веб-панели администратора ЮрПомощник...
echo.

:: Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)

:: Проверяем наличие виртуального окружения
if exist "venv" (
    echo 🔧 Активирую виртуальное окружение...
    call venv\Scripts\activate.bat
)

:: Проверяем зависимости
echo 📦 Проверяю зависимости...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo 📚 Устанавливаю зависимости...
    pip install flask==3.0.0 flask-cors==4.0.0 flask-socketio==5.3.6 psutil==5.9.6
)

echo.
echo 🚀 Запуск админ-панели...
echo 📍 URL: http://127.0.0.1:5000
echo 👤 Логин: admin
echo 🔑 Пароль: admin123
echo.
echo ⚠️  Для остановки нажмите Ctrl+C
echo.

:: Запуск панели
python admin_panel.py

pause 