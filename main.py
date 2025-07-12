"""
Главный файл приложения - точка входа для запуска бота.
"""
import logging
import config  # Импортируем модуль, чтобы он выполнился и загрузил .env
from modules.bot_handler import start_bot

def main():
    """Главная функция запуска приложения."""
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Проверяем конфигурацию
    try:
        config.check_env_vars()
    except ValueError as e:
        logging.error(f"Ошибка конфигурации: {e}")
        return
    
    # Запускаем бота
    logging.info("🚀 Запуск юридического чат-бота...")
    try:
        start_bot()
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main() 