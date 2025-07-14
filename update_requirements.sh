#!/bin/bash

echo "========================================"
echo "Обновление requirements.txt из venv"
echo "========================================"

# Проверяем существование виртуального окружения
if [ ! -f "venv/bin/activate" ]; then
    echo "ОШИБКА: Виртуальное окружение не найдено!"
    echo "Создайте виртуальное окружение: python3 -m venv venv"
    exit 1
fi

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Обновление pip..."
python -m pip install --upgrade pip

echo "Создание полного requirements.txt..."
pip freeze > requirements.txt

echo "Создание минимального requirements.minimal.txt..."
cat > requirements.minimal.txt << EOF
aiogram==3.3.0
openai==1.12.0
chromadb==0.4.22
PyMuPDF==1.23.14
python-dotenv==1.0.0
httpx==0.26.0
numpy==1.26.4
requests==2.31.0
beautifulsoup4==4.12.2
aiohttp==3.9.1
lxml==4.9.3
python-docx==0.8.11
Flask==3.0.0
Flask-Cors==4.0.0
psutil==5.9.6
scikit-learn==1.7.0
pandas==2.3.1
scipy==1.15.3
EOF

echo "Создание backup файла..."
cp requirements.txt requirements.backup.txt

echo "========================================"
echo "Обновление завершено!"
echo "========================================"
echo ""
echo "Файлы обновлены:"
echo "- requirements.txt (полный список)"
echo "- requirements.minimal.txt (минимальный набор)"
echo "- requirements.backup.txt (резервная копия)"
echo ""
echo "Количество пакетов в requirements.txt:"
grep -c "==" requirements.txt
echo "" 