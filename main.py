"""
Главный файл приложения - точка входа для запуска бота.
"""
import sys
import os

# --- Проверка запуска из виртуального окружения ---
venv_env = os.environ.get('VIRTUAL_ENV')
python_path = sys.executable.lower().replace('\\', '/')
if not venv_env or not (
    python_path.endswith('/venv/scripts/python.exe') or  # Windows
    '/venv/bin/python' in python_path                   # Linux/macOS
):
    print('❌ Ошибка: Бот должен запускаться только из виртуального окружения venv!')
    print(f'Текущий python: {sys.executable}')
    print('Активируйте venv и запустите снова:')
    print('  Windows:   .\\venv\\Scripts\\Activate.ps1')
    print('  Linux/Mac: source venv/bin/activate')
    sys.exit(1)
# --- Конец проверки ---

import logging
import config  # Импортируем модуль, чтобы он выполнился и загрузил .env
from modules.bot_handler import start_bot

# --- PROMETHEUS METRICS ---
from modules.metrics import REQUESTS, ERRORS, RESPONSE_TIME, ensure_metrics_server
ensure_metrics_server(8000)
# --- END PROMETHEUS METRICS ---

def main():
    """Главная функция запуска приложения."""
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Проверяем конфигурацию
    try:
        config.check_env_vars()
    except ValueError as e:
        logging.error(f"Ошибка конфигурации: {e}")
        return
    
    # Запускаем бота
    logging.info("СТАРТ: Запуск юридического чат-бота...")
    try:
        # Оборачиваем запуск бота в метрику времени отклика
        with RESPONSE_TIME.time():
            REQUESTS.inc()
            start_bot()
    except Exception as e:
        ERRORS.inc()
        logging.error(f"Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main() 