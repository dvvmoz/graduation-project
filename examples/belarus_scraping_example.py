#!/usr/bin/env python3
"""
Пример использования веб-скрапера для белорусских юридических сайтов
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь
sys.path.append(str(Path(__file__).parent.parent))

from modules.web_scraper import create_scraper_from_config


def scrape_belarus_government_sites():
    """Скрапинг основных государственных сайтов Беларуси"""
    print("🇧🇾 Скрапинг государственных сайтов Беларуси")
    
    # Основные государственные порталы РБ
    belarus_gov_sites = [
        "https://pravo.by/",                    # Национальный правовой портал
        "https://www.government.by/",           # Совет Министров
        "https://www.house.gov.by/",            # Палата представителей
        "https://www.court.gov.by/",            # Судебная система
        "https://www.minjust.gov.by/"           # Министерство юстиции
    ]
    
    scraper = create_scraper_from_config()
    total_pages = 0
    total_chunks = 0
    
    for i, site in enumerate(belarus_gov_sites, 1):
        print(f"\n📋 Сайт {i}/{len(belarus_gov_sites)}: {site}")
        
        result = scraper.scrape_and_add(site, max_pages=5)
        
        if result['success']:
            total_pages += result['pages_scraped']
            total_chunks += result['chunks_added']
            print(f"✅ {result['pages_scraped']} страниц, {result['chunks_added']} чанков")
        else:
            print(f"❌ Ошибка: {result['message']}")
    
    print(f"\n🎉 Результат скрапинга государственных сайтов РБ:")
    print(f"📄 Всего страниц: {total_pages}")
    print(f"📝 Всего чанков: {total_chunks}")
    
    return total_pages, total_chunks


def scrape_belarus_legal_resources():
    """Скрапинг правовых ресурсов и консультационных сайтов"""
    print("\n⚖️ Скрапинг правовых ресурсов Беларуси")
    
    # Правовые ресурсы и консультации
    belarus_legal_sites = [
        "https://www.lawbelarus.com/",          # Право Беларуси
        "https://www.jurist.by/",               # Юрист.бай
        "https://www.notariat.by/",             # Белорусский нотариат
        "https://www.normativka.by/"            # Нормативные документы
    ]
    
    scraper = create_scraper_from_config()
    total_pages = 0
    total_chunks = 0
    
    for i, site in enumerate(belarus_legal_sites, 1):
        print(f"\n📋 Сайт {i}/{len(belarus_legal_sites)}: {site}")
        
        result = scraper.scrape_and_add(site, max_pages=3)
        
        if result['success']:
            total_pages += result['pages_scraped']
            total_chunks += result['chunks_added']
            print(f"✅ {result['pages_scraped']} страниц, {result['chunks_added']} чанков")
        else:
            print(f"❌ Ошибка: {result['message']}")
    
    print(f"\n🎉 Результат скрапинга правовых ресурсов РБ:")
    print(f"📄 Всего страниц: {total_pages}")
    print(f"📝 Всего чанков: {total_chunks}")
    
    return total_pages, total_chunks


def scrape_regional_sites():
    """Скрапинг региональных исполкомов"""
    print("\n🏛️ Скрапинг региональных исполкомов")
    
    # Региональные исполкомы
    regional_sites = [
        "https://minsk.gov.by/",                # Мингорисполком
        "https://www.gomel.gov.by/",            # Гомельский облисполком
        "https://www.vitebsk.gov.by/",          # Витебский облисполком
        "https://www.grodno.gov.by/"            # Гродненский облисполком
    ]
    
    scraper = create_scraper_from_config()
    total_pages = 0
    total_chunks = 0
    
    for i, site in enumerate(regional_sites, 1):
        print(f"\n📋 Сайт {i}/{len(regional_sites)}: {site}")
        
        result = scraper.scrape_and_add(site, max_pages=2)
        
        if result['success']:
            total_pages += result['pages_scraped']
            total_chunks += result['chunks_added']
            print(f"✅ {result['pages_scraped']} страниц, {result['chunks_added']} чанков")
        else:
            print(f"❌ Ошибка: {result['message']}")
    
    print(f"\n🎉 Результат скрапинга региональных сайтов:")
    print(f"📄 Всего страниц: {total_pages}")
    print(f"📝 Всего чанков: {total_chunks}")
    
    return total_pages, total_chunks


def scrape_pravo_by_focused():
    """Фокусированный скрапинг pravo.by"""
    print("\n🎯 Фокусированный скрапинг pravo.by")
    
    scraper = create_scraper_from_config()
    
    # Настраиваем скрапер для более детального изучения
    scraper.max_pages = 30
    scraper.delay = 2  # Увеличиваем задержку для вежливого скрапинга
    
    result = scraper.scrape_and_add("https://pravo.by/", max_pages=30)
    
    if result['success']:
        print(f"✅ Детальный скрапинг pravo.by завершен")
        print(f"📄 Обработано страниц: {result['pages_scraped']}")
        print(f"📝 Добавлено чанков: {result['chunks_added']}")
        print(f"🌐 Источник: {result['start_url']}")
    else:
        print(f"❌ Ошибка: {result['message']}")
    
    return result.get('pages_scraped', 0), result.get('chunks_added', 0)


def check_knowledge_base_stats():
    """Проверка статистики базы знаний после скрапинга"""
    print("\n📊 Статистика базы знаний")
    
    from modules.knowledge_base import get_knowledge_base
    
    kb = get_knowledge_base()
    stats = kb.get_collection_stats()
    
    print(f"📚 Всего документов в базе: {stats.get('total_documents', 0)}")
    print(f"🗂️ Коллекция: {stats.get('collection_name', 'N/A')}")
    print(f"💾 Путь к БД: {stats.get('db_path', 'N/A')}")
    
    return stats


def main():
    """Основная функция с примерами скрапинга для Беларуси"""
    print("🚀 Примеры скрапинга белорусских юридических сайтов")
    print("=" * 60)
    
    total_pages_all = 0
    total_chunks_all = 0
    
    try:
        # 1. Скрапинг государственных сайтов
        pages, chunks = scrape_belarus_government_sites()
        total_pages_all += pages
        total_chunks_all += chunks
        
        # 2. Скрапинг правовых ресурсов
        pages, chunks = scrape_belarus_legal_resources()
        total_pages_all += pages
        total_chunks_all += chunks
        
        # 3. Скрапинг региональных сайтов
        pages, chunks = scrape_regional_sites()
        total_pages_all += pages
        total_chunks_all += chunks
        
        # 4. Детальный скрапинг pravo.by
        pages, chunks = scrape_pravo_by_focused()
        total_pages_all += pages
        total_chunks_all += chunks
        
        # 5. Проверка статистики
        stats = check_knowledge_base_stats()
        
        print(f"\n🎉 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"📄 Всего обработано страниц: {total_pages_all}")
        print(f"📝 Всего добавлено чанков: {total_chunks_all}")
        print(f"📚 Документов в базе: {stats.get('total_documents', 0)}")
        
        print(f"\n✅ Скрапинг белорусских сайтов завершен успешно!")
        print(f"🇧🇾 База знаний пополнена белорусской правовой информацией")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении скрапинга: {e}")
        print("💡 Убедитесь, что:")
        print("   - Установлены все зависимости")
        print("   - Настроен файл .env")
        print("   - Есть доступ к интернету")
        print("   - Сайты доступны")


if __name__ == "__main__":
    main() 