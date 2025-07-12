"""
Конфигурация проекта - загрузка переменных окружения и настроек.
"""
import os
from dotenv import load_dotenv

# Немедленно загружаем переменные из .env файла.
# Это гарантирует, что они доступны для всех модулей, импортирующих config.
load_dotenv()

def check_env_vars():
    """Проверяет, что обязательные переменные окружения загружены."""
    required_vars = ['TELEGRAM_TOKEN', 'OPENAI_API_KEY']
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Переменная окружения {var} не найдена. Проверьте файл .env")
    
    print("✅ Конфигурация загружена успешно")

# Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db/chroma")

# Настройки ИИ
DEFAULT_MODEL = "gpt-4o-mini"
MAX_RESULTS = 10  # Максимальное количество документов для контекста
MAX_TOKENS = 2000  # Максимальное количество токенов в ответе 