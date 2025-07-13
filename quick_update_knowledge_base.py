#!/usr/bin/env python3
"""
Быстрое обновление базы знаний - интерактивный скрипт
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.knowledge_base import get_knowledge_base
from scripts.populate_db import populate_from_directory
from scripts.scrape_websites import scrape_multiple_sites, get_legal_sites_list
from scripts.update_documents import update_all_documents

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def show_menu():
    """Показать главное меню"""
    print("\n" + "="*50)
    print("🔧 БЫСТРОЕ ОБНОВЛЕНИЕ БАЗЫ ЗНАНИЙ")
    print("="*50)
    print("1. 📊 Проверить состояние базы знаний")
    print("2. 📄 Обновить из документов")
    print("3. 🌐 Скрапить сайты")
    print("4. 🔄 Полное обновление")
    print("5. 🧹 Очистить базу знаний")
    print("6. 🔍 Тестировать поиск")
    print("7. 📈 Анализ качества")
    print("0. ❌ Выход")
    print("="*50)

def check_knowledge_base_status():
    """Проверить состояние базы знаний"""
    try:
        print("\n🔍 Проверка состояния базы знаний...")
        kb = get_knowledge_base()
        stats = kb.get_collection_stats()
        
        print(f"📂 Путь к базе: {stats.get('db_path', 'не указан')}")
        print(f"📚 Коллекция: {stats.get('collection_name', 'не указана')}")
        print(f"📝 Всего документов: {stats.get('total_documents', 0)}")
        
        if stats.get('total_documents', 0) == 0:
            print("⚠️ ВНИМАНИЕ: База знаний пуста!")
            print("💡 Рекомендация: Запустите 'Обновить из документов' или 'Полное обновление'")
        elif stats.get('total_documents', 0) < 100:
            print("⚠️ ВНИМАНИЕ: Мало документов в базе знаний")
            print("💡 Рекомендация: Добавьте больше документов или запустите скрапинг")
        else:
            print("✅ База знаний содержит достаточно документов")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке базы знаний: {e}")
        return False

def update_from_documents():
    """Обновить базу знаний из документов"""
    try:
        print("\n📄 Обновление из документов...")
        
        # Проверяем наличие папки с документами
        docs_dir = Path("data/documents")
        if not docs_dir.exists():
            print(f"❌ Папка {docs_dir} не найдена")
            return False
        
        # Получаем список файлов
        doc_files = list(docs_dir.glob("*.pdf")) + list(docs_dir.glob("*.docx")) + list(docs_dir.glob("*.doc"))
        
        if not doc_files:
            print("❌ Не найдено документов для обновления")
            print("💡 Поместите PDF, DOCX или DOC файлы в папку data/documents/")
            return False
        
        print(f"📋 Найдено документов: {len(doc_files)}")
        for doc in doc_files:
            print(f"  - {doc.name}")
        
        # Спрашиваем подтверждение
        choice = input("\n🤔 Обновить базу знаний из этих документов? (y/n): ").lower()
        if choice != 'y':
            print("❌ Отменено пользователем")
            return False
        
        # Запускаем обновление
        print("\n🔄 Обновление документов...")
        stats = update_all_documents()
        
        print(f"\n✅ Обновление завершено:")
        print(f"📝 Обработано файлов: {stats.get('processed_files', 0)}")
        print(f"📊 Добавлено блоков: {stats.get('total_blocks', 0)}")
        
        if stats.get('failed_files'):
            print(f"❌ Ошибки при обработке: {len(stats['failed_files'])}")
            for failed_file in stats['failed_files']:
                print(f"  - {failed_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении документов: {e}")
        return False

def scrape_websites():
    """Скрапить юридические сайты"""
    try:
        print("\n🌐 Скрапинг юридических сайтов...")
        
        # Получаем список сайтов
        sites = get_legal_sites_list()
        if not sites:
            print("❌ Список сайтов пуст")
            return False
        
        print(f"🔗 Найдено сайтов: {len(sites)}")
        for site in sites[:5]:  # Показываем первые 5
            print(f"  - {site}")
        if len(sites) > 5:
            print(f"  ... и еще {len(sites) - 5} сайтов")
        
        # Спрашиваем параметры
        print("\n⚙️ Настройки скрапинга:")
        max_pages = input("📄 Максимум страниц с каждого сайта (по умолчанию 10): ").strip()
        if not max_pages:
            max_pages = 10
        else:
            max_pages = int(max_pages)
        
        max_sites = input("🔗 Максимум сайтов для скрапинга (по умолчанию 5): ").strip()
        if not max_sites:
            max_sites = 5
        else:
            max_sites = int(max_sites)
        
        # Спрашиваем подтверждение
        choice = input(f"\n🤔 Скрапить {max_sites} сайтов по {max_pages} страниц? (y/n): ").lower()
        if choice != 'y':
            print("❌ Отменено пользователем")
            return False
        
        # Запускаем скрапинг
        print("\n🔄 Скрапинг сайтов...")
        limited_sites = sites[:max_sites]
        results = scrape_multiple_sites(limited_sites, max_pages)
        
        print(f"\n✅ Скрапинг завершен:")
        print(f"🌐 Обработано сайтов: {results.get('sites_processed', 0)}")
        print(f"📄 Всего страниц: {results.get('total_pages', 0)}")
        print(f"📊 Добавлено чанков: {results.get('total_chunks', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при скрапинге: {e}")
        return False

def full_update():
    """Полное обновление базы знаний"""
    try:
        print("\n🔄 ПОЛНОЕ ОБНОВЛЕНИЕ БАЗЫ ЗНАНИЙ")
        print("Это займет несколько минут...")
        
        choice = input("\n🤔 Продолжить полное обновление? (y/n): ").lower()
        if choice != 'y':
            print("❌ Отменено пользователем")
            return False
        
        success_count = 0
        
        # 1. Обновление документов
        print("\n📄 Шаг 1: Обновление документов...")
        if update_from_documents():
            success_count += 1
            print("✅ Документы обновлены")
        else:
            print("⚠️ Ошибка при обновлении документов")
        
        # 2. Скрапинг сайтов
        print("\n🌐 Шаг 2: Скрапинг сайтов...")
        if scrape_websites():
            success_count += 1
            print("✅ Сайты обработаны")
        else:
            print("⚠️ Ошибка при скрапинге сайтов")
        
        # 3. Проверка результата
        print("\n📊 Шаг 3: Проверка результата...")
        if check_knowledge_base_status():
            success_count += 1
            print("✅ Проверка завершена")
        
        print(f"\n🎉 Полное обновление завершено: {success_count}/3 шагов успешно")
        return success_count >= 2
        
    except Exception as e:
        print(f"❌ Ошибка при полном обновлении: {e}")
        return False

def clear_knowledge_base():
    """Очистить базу знаний"""
    try:
        print("\n🧹 ОЧИСТКА БАЗЫ ЗНАНИЙ")
        print("⚠️ ВНИМАНИЕ: Это действие необратимо!")
        
        # Показываем текущую статистику
        kb = get_knowledge_base()
        stats = kb.get_collection_stats()
        print(f"📊 Текущее количество документов: {stats.get('total_documents', 0)}")
        
        # Двойное подтверждение
        choice1 = input("\n🤔 Вы уверены, что хотите очистить базу знаний? (yes/no): ").lower()
        if choice1 != 'yes':
            print("❌ Отменено пользователем")
            return False
        
        choice2 = input("🤔 Окончательное подтверждение - очистить базу? (YES/no): ")
        if choice2 != 'YES':
            print("❌ Отменено пользователем")
            return False
        
        # Очищаем базу
        print("\n🗑️ Очистка базы знаний...")
        if kb.clear_collection():
            print("✅ База знаний очищена")
            return True
        else:
            print("❌ Ошибка при очистке базы знаний")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при очистке базы знаний: {e}")
        return False

def test_search():
    """Тестировать поиск в базе знаний"""
    try:
        print("\n🔍 ТЕСТИРОВАНИЕ ПОИСКА")
        
        kb = get_knowledge_base()
        
        # Предустановленные тестовые запросы
        test_queries = [
            "регистрация ИП",
            "налоговые льготы",
            "трудовые отношения",
            "пенсия",
            "документы для суда"
        ]
        
        print("📋 Предустановленные тестовые запросы:")
        for i, query in enumerate(test_queries, 1):
            print(f"  {i}. {query}")
        
        choice = input("\n🤔 Выберите запрос (1-5) или введите свой: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(test_queries):
            query = test_queries[int(choice) - 1]
        else:
            query = choice
        
        if not query:
            print("❌ Пустой запрос")
            return False
        
        print(f"\n🔍 Поиск для запроса: '{query}'")
        
        # Выполняем поиск
        results = kb.search_relevant_docs(query, n_results=3)
        
        if not results:
            print("❌ Документы не найдены")
            return False
        
        print(f"✅ Найдено документов: {len(results)}")
        
        for i, doc in enumerate(results, 1):
            print(f"\n📄 Документ {i}:")
            print(f"  📊 Релевантность: {doc.get('distance', 'н/д'):.3f}")
            print(f"  📂 Источник: {doc.get('metadata', {}).get('source_file', 'неизвестен')}")
            print(f"  📝 Текст: {doc.get('content', '')[:200]}...")
        
        # Проверяем необходимость динамического поиска
        should_search, _ = kb.should_use_dynamic_search(query)
        if should_search:
            print("\n⚠️ Рекомендация: Качество результатов низкое, нужен поиск на pravo.by")
        else:
            print("\n✅ Качество результатов хорошее, найдены релевантные документы")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании поиска: {e}")
        return False

def analyze_quality():
    """Анализ качества базы знаний"""
    try:
        print("\n📈 АНАЛИЗ КАЧЕСТВА БАЗЫ ЗНАНИЙ")
        
        kb = get_knowledge_base()
        
        # Тестовые запросы для анализа
        test_queries = [
            "регистрация ИП",
            "налоговые льготы", 
            "трудовые отношения",
            "пенсия по возрасту",
            "семейное право",
            "уголовная ответственность",
            "договор купли-продажи",
            "права потребителей"
        ]
        
        print("🔍 Анализ качества поиска по тестовым запросам...")
        
        total_queries = len(test_queries)
        good_quality = 0
        avg_distances = []
        
        for query in test_queries:
            results = kb.search_relevant_docs(query, n_results=3)
            
            if results:
                avg_distance = sum(doc.get('distance', 1.0) for doc in results) / len(results)
                avg_distances.append(avg_distance)
                
                if avg_distance < 0.5:
                    good_quality += 1
                    quality_status = "✅ Хорошее"
                elif avg_distance < 0.8:
                    quality_status = "⚠️ Удовлетворительное"
                else:
                    quality_status = "❌ Низкое"
                
                print(f"  {query}: {quality_status} ({avg_distance:.3f})")
            else:
                print(f"  {query}: ❌ Нет результатов")
        
        # Общая статистика
        print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
        print(f"  📝 Всего запросов: {total_queries}")
        print(f"  ✅ Хорошее качество: {good_quality}")
        print(f"  📈 Процент качества: {(good_quality / total_queries * 100):.1f}%")
        
        if avg_distances:
            overall_avg = sum(avg_distances) / len(avg_distances)
            print(f"  📊 Средняя дистанция: {overall_avg:.3f}")
        
        # Рекомендации
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        if good_quality / total_queries >= 0.8:
            print("  ✅ Качество базы знаний отличное")
        elif good_quality / total_queries >= 0.6:
            print("  ⚠️ Качество базы знаний удовлетворительное")
            print("  📄 Рекомендуется добавить больше документов")
        else:
            print("  ❌ Качество базы знаний низкое")
            print("  🔄 Рекомендуется полное обновление базы знаний")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при анализе качества: {e}")
        return False

def main():
    """Главная функция"""
    print("🤖 Система обновления базы знаний юридического чат-бота")
    print(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        try:
            show_menu()
            choice = input("\n🔢 Выберите действие (0-7): ").strip()
            
            if choice == '0':
                print("👋 До свидания!")
                break
            elif choice == '1':
                check_knowledge_base_status()
            elif choice == '2':
                update_from_documents()
            elif choice == '3':
                scrape_websites()
            elif choice == '4':
                full_update()
            elif choice == '5':
                clear_knowledge_base()
            elif choice == '6':
                test_search()
            elif choice == '7':
                analyze_quality()
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
            
            # Пауза перед следующим действием
            input("\n⏸️ Нажмите Enter для продолжения...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Прервано пользователем. До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Неожиданная ошибка: {e}")
            print("💡 Попробуйте снова или обратитесь к разработчику")

if __name__ == "__main__":
    main() 