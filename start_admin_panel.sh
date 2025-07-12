#!/bin/bash

# Скрипт для быстрого запуска админ-панели ЮрПомощника (Linux/macOS)

echo "🛠️ Запуск админ-панели ЮрПомощника..."

# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env на основе env.example"
    echo "   cp env.example .env"
    echo "   nano .env"
    exit 1
fi

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python не найден! Установите Python 3.8+"
    exit 1
fi

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создаю виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активирую виртуальное окружение..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📚 Устанавливаю зависимости..."
pip install -r requirements.txt

# Проверяем наличие базы знаний
if [ ! -d "db/chroma" ]; then
    echo "🧠 База знаний не найдена. Создайте её командой:"
    echo "   python scripts/populate_db.py"
    echo ""
fi

# Запускаем админ-панель
echo "🌐 Запуск админ-панели на http://127.0.0.1:5000"
echo "🔑 Логин: admin, Пароль: admin123"
echo ""
echo "Нажмите Ctrl+C для остановки"
echo ""

python3 admin_panel.py 