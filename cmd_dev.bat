@echo off
chcp 65001 > nul

echo 🔧 Запуск среды разработки (CMD)...

:: Проверяем наличие виртуального окружения
if not exist "venv" (
    echo 📦 Создаю виртуальное окружение...
    python -m venv venv
)

:: Активируем виртуальное окружение
echo 🚀 Активирую виртуальное окружение...
call venv\Scripts\activate.bat

echo ✅ Виртуальное окружение активировано!
echo 📂 Рабочая папка: %cd%
echo 🐍 Python: 
python --version
echo 📦 Pip:
pip --version

:: Остаемся в командной строке
cmd /k 