#!/usr/bin/env python3
"""
Скрипт для проверки содержимого базы знаний
"""
import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.knowledge_base import get_knowledge_base, search_relevant_docs

def check_database():
    """Проверяет содержимое базы знаний"""
    print("🔍 Проверка базы знаний...")
    print("=" * 50)
    
    try:
        # Получаем статистику
        kb = get_knowledge_base()
        stats = kb.get_collection_stats()
        
        print(f"📊 Статистика базы знаний:")
        print(f"📚 Всего документов: {stats.get('total_documents', 0)}")
        print(f"🗂️ Коллекция: {stats.get('collection_name', 'N/A')}")
        print(f"💾 Путь к БД: {stats.get('db_path', 'N/A')}")
        print()
        
        # Проверяем размер файла базы данных
        db_path = stats.get('db_path', '')
        if db_path and os.path.exists(db_path):
            db_file = os.path.join(db_path, 'chroma.sqlite3')
            if os.path.exists(db_file):
                size_mb = os.path.getsize(db_file) / (1024 * 1024)
                print(f"📁 Размер файла БД: {size_mb:.2f} MB")
            else:
                print("❌ Файл базы данных не найден")
        else:
            print("❌ Путь к базе данных не найден")
        
        print()
        
        # Тестируем поиск
        if stats.get('total_documents', 0) > 0:
            print("🔍 Тестирование поиска...")
            
            test_queries = [
                "налог",
                "закон",
                "беларусь",
                "постановление",
                "суд"
            ]
            
            for query in test_queries:
                results = search_relevant_docs(query, n_results=3)
                print(f"  '{query}': найдено {len(results)} документов")
                if results:
                    # Показываем первые 100 символов первого результата
                    preview = results[0][:100] + "..." if len(results[0]) > 100 else results[0]
                    print(f"    Пример: {preview}")
                print()
        else:
            print("❌ База знаний пуста - нет документов для поиска")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке базы знаний: {e}")
        return False
    
    return True

def main():
    """Основная функция"""
    print("🚀 Проверка состояния базы знаний")
    print("=" * 50)
    
    if check_database():
        print("✅ Проверка завершена успешно!")
    else:
        print("❌ Обнаружены проблемы с базой знаний")
        sys.exit(1)

if __name__ == "__main__":
    main() 