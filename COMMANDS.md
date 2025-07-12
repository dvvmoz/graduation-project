# 🎛️ Команды для управления проектом ЮрПомощник

## 🚀 Быстрый старт (демонстрация)

```bash
# 1. Интерактивная демонстрация поиска
python demo_bot.py

# 2. Автоматические тесты функциональности  
python test_demo.py

# 3. Запуск всех тестов
pytest
```

## 🤖 Полноценный Telegram бот

```bash
# После настройки API ключей в .env
python main.py
```

## 📚 Управление базой знаний

```bash
# Создание/обновление базы знаний из PDF
python scripts/populate_db.py

# Просмотр статистики базы знаний
python -c "from modules.knowledge_base import get_knowledge_base; print(get_knowledge_base().get_collection_stats())"

# Тест поиска в базе знаний
python -c "from modules.knowledge_base import search_relevant_docs; print(search_relevant_docs('налоги', 3))"
```

## 🔧 Настройка окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/macOS)  
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
copy env.example .env  # Windows
cp env.example .env    # Linux/macOS
```

## 🐳 Docker команды

```bash
# Сборка образа
docker build -t legal-bot .

# Запуск контейнера
docker run --env-file .env legal-bot

# Запуск через docker-compose
docker-compose up -d

# Остановка
docker-compose down
```

## 🧪 Тестирование

```bash
# Все тесты
pytest

# Тесты с подробным выводом
pytest -v

# Конкретный тест
pytest tests/test_config.py

# Тест конфигурации
python -c "from config import load_config; load_config(); print('Конфигурация OK')"
```

## 📄 Работа с документами

```bash
# Добавление PDF файлов
# 1. Поместите файлы в папку data/
# 2. Запустите обновление базы
python scripts/populate_db.py

# Проверка обработки PDF
python -c "from modules.text_processing import extract_text_from_pdf; print(len(extract_text_from_pdf('data/your_file.pdf')))"
```

## 🔍 Отладка и диагностика

```bash
# Проверка ChromaDB
python -c "from modules.knowledge_base import get_knowledge_base; kb = get_knowledge_base(); print(f'Документов: {kb.get_collection_stats()}')"

# Проверка OpenAI (требует API ключ)
python -c "from modules.llm_service import get_llm_service; print(get_llm_service().get_model_info())"

# Логи в реальном времени
tail -f bot.log  # Linux/macOS
Get-Content bot.log -Wait  # Windows PowerShell
```

## 🎯 Автоматические скрипты

```bash
# Windows
start.bat

# Linux/macOS
./start.sh

# Установка прав (Linux/macOS)
chmod +x start.sh
chmod +x scripts/populate_db.py
```

## 📊 Статистика и мониторинг

```bash
# Размер базы знаний
python -c "from modules.knowledge_base import get_knowledge_base; stats = get_knowledge_base().get_collection_stats(); print(f'Документов: {stats[\"total_documents\"]}')"

# Тест производительности поиска
python -c "import time; from modules.knowledge_base import search_relevant_docs; start = time.time(); search_relevant_docs('тест', 5); print(f'Поиск занял: {time.time() - start:.2f} сек')"

# Очистка базы знаний (осторожно!)
python -c "from modules.knowledge_base import get_knowledge_base; get_knowledge_base().clear_collection()"
```

## 🛠️ Разработка

```bash
# Форматирование кода
black .
flake8 .

# Обновление зависимостей
pip freeze > requirements.txt

# Создание нового модуля
touch modules/new_module.py
touch tests/test_new_module.py
```

## ❗ Устранение проблем

```bash
# Переустановка зависимостей
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Сброс базы знаний
rm -rf db/chroma/*  # Linux/macOS
rmdir /s db\chroma  # Windows

# Проверка версий
python --version
pip list | grep -E "(chromadb|openai|aiogram)"

# Исправление проблем с NumPy
pip install "numpy<2.0"
```

## 🎓 Для демонстрации/защиты

```bash
# Полная демонстрация функциональности
python test_demo.py

# Интерактивная сессия
python demo_bot.py

# Показ статистики проекта
find . -name "*.py" | wc -l  # Количество Python файлов
wc -l $(find . -name "*.py")  # Строки кода
``` 