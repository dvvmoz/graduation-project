#!/usr/bin/env python3
"""
Пример использования веб-скрапера для пополнения базы знаний
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь
sys.path.append(str(Path(__file__).parent.parent))

from modules.web_scraper import create_scraper_from_config


def example_single_site_scraping():
    """Пример скрапинга одного сайта"""
    print("🔍 Пример скрапинга одного сайта")
    
    # Создаем скрапер
    scraper = create_scraper_from_config()
    
    # Скрапим небольшой сайт
    result = scraper.scrape_and_add(
        start_url="https://www.garant.ru/",
        max_pages=5
    )
    
    if result['success']:
        print(f"✅ Успешно обработано {result['pages_scraped']} страниц")
        print(f"📝 Добавлено {result['chunks_added']} чанков в базу знаний")
    else:
        print(f"❌ Ошибка: {result['message']}")


def example_multiple_sites_scraping():
    """Пример скрапинга нескольких сайтов"""
    print("\n🌐 Пример скрапинга нескольких сайтов")
    
    # Список сайтов для скрапинга
    sites = [
        "https://www.garant.ru/",
        "https://www.consultant.ru/",
        "https://www.pravo.gov.ru/"
    ]
    
    scraper = create_scraper_from_config()
    total_pages = 0
    total_chunks = 0
    
    for i, site in enumerate(sites, 1):
        print(f"\n📋 Сайт {i}/{len(sites)}: {site}")
        
        result = scraper.scrape_and_add(site, max_pages=3)
        
        if result['success']:
            total_pages += result['pages_scraped']
            total_chunks += result['chunks_added']
            print(f"✅ {result['pages_scraped']} страниц, {result['chunks_added']} чанков")
        else:
            print(f"❌ Ошибка: {result['message']}")
    
    print(f"\n🎉 Общий результат:")
    print(f"📄 Всего страниц: {total_pages}")
    print(f"📝 Всего чанков: {total_chunks}")


def example_custom_scraping():
    """Пример настройки кастомного скрапера"""
    print("\n⚙️ Пример кастомного скрапера")
    
    from modules.knowledge_base import KnowledgeBase
    from modules.text_processing import TextProcessor
    from modules.web_scraper import WebScraper
    
    # Создаем компоненты
    knowledge_base = KnowledgeBase()
    text_processor = TextProcessor()
    
    # Создаем скрапер с кастомными настройками
    scraper = WebScraper(knowledge_base, text_processor)
    scraper.max_pages = 10  # Ограничиваем количество страниц
    scraper.delay = 2       # Увеличиваем задержку
    
    # Скрапим сайт
    result = scraper.scrape_and_add(
        start_url="https://www.law.ru/",
        max_pages=5
    )
    
    if result['success']:
        print(f"✅ Кастомный скрапинг завершен")
        print(f"📄 Страниц: {result['pages_scraped']}")
        print(f"📝 Чанков: {result['chunks_added']}")
    else:
        print(f"❌ Ошибка: {result['message']}")


def example_check_knowledge_base():
    """Пример проверки базы знаний после скрапинга"""
    print("\n📊 Проверка базы знаний")
    
    from modules.knowledge_base import get_knowledge_base
    
    kb = get_knowledge_base()
    stats = kb.get_collection_stats()
    
    print(f"📚 Всего документов в базе: {stats.get('total_documents', 0)}")
    print(f"🗂️ Коллекция: {stats.get('collection_name', 'N/A')}")
    print(f"💾 Путь к БД: {stats.get('db_path', 'N/A')}")


def main():
    """Основная функция с примерами"""
    print("🚀 Примеры использования веб-скрапера")
    print("=" * 50)
    
    try:
        # Пример 1: Скрапинг одного сайта
        example_single_site_scraping()
        
        # Пример 2: Скрапинг нескольких сайтов
        example_multiple_sites_scraping()
        
        # Пример 3: Кастомный скрапер
        example_custom_scraping()
        
        # Пример 4: Проверка базы знаний
        example_check_knowledge_base()
        
        print("\n✅ Все примеры выполнены успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении примеров: {e}")
        print("💡 Убедитесь, что:")
        print("   - Установлены все зависимости")
        print("   - Настроен файл .env")
        print("   - Есть доступ к интернету")


if __name__ == "__main__":
    main() 