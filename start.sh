#!/bin/bash

# Скрипт для быстрого запуска проекта ЮрПомощник

echo "🚀 Запуск ЮрПомощника..."

# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env на основе env.example"
    echo "   cp env.example .env"
    echo "   nano .env"
    exit 1
fi

# Проверяем наличие Python
if ! command -v python &> /dev/null; then
    echo "❌ Python не найден! Установите Python 3.8+"
    exit 1
fi

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создаю виртуальное окружение..."
    python -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активирую виртуальное окружение..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📚 Устанавливаю зависимости..."
pip install -r requirements.txt

# Проверяем наличие PDF файлов
if [ ! -d "data" ] || [ -z "$(ls -A data/*.pdf 2>/dev/null)" ]; then
    echo "📁 Создаю папку data..."
    mkdir -p data
    echo "📄 Добавьте PDF файлы в папку data/ и запустите скрипт снова"
    echo "   python scripts/populate_db.py"
    echo ""
fi

# Проверяем наличие базы знаний
if [ ! -d "db/chroma" ]; then
    echo "🧠 Создаю базу знаний..."
    python scripts/populate_db.py
fi

# Запускаем бота
echo "🤖 Запуск бота..."
python main.py 