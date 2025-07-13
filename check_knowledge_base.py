#!/usr/bin/env python3
"""
Быстрая проверка состояния базы знаний
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_knowledge_base_quick():
    """Быстрая проверка состояния базы знаний"""
    try:
        from modules.knowledge_base import get_knowledge_base
        
        print("🔍 Проверка базы знаний...")
        print(f"📅 Время проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # Получаем базу знаний
        kb = get_knowledge_base()
        stats = kb.get_collection_stats()
        
        # Основная статистика
        print(f"📂 Путь к базе: {stats.get('db_path', 'не указан')}")
        print(f"📚 Коллекция: {stats.get('collection_name', 'не указана')}")
        print(f"📝 Всего документов: {stats.get('total_documents', 0)}")
        
        # Оценка состояния
        doc_count = stats.get('total_documents', 0)
        if doc_count == 0:
            print("❌ База знаний пуста!")
            print("💡 Запустите: python scripts/populate_db.py")
            return False
        elif doc_count < 50:
            print("⚠️ Мало документов в базе")
            print("💡 Рекомендуется добавить больше документов")
        elif doc_count < 200:
            print("✅ Умеренное количество документов")
        else:
            print("🎉 Отличное количество документов!")
        
        # Тест поиска
        print("\n🔍 Тест поиска...")
        test_queries = ["регистрация ИП", "налоги", "трудовые отношения"]
        
        for query in test_queries:
            results = kb.search_relevant_docs(query, n_results=1)
            if results:
                distance = results[0].get('distance', 1.0)
                if distance < 0.3:
                    quality = "отличное"
                elif distance < 0.5:
                    quality = "хорошее"
                elif distance < 0.8:
                    quality = "удовлетворительное"
                else:
                    quality = "низкое"
                print(f"  '{query}': {quality} качество ({distance:.3f})")
            else:
                print(f"  '{query}': нет результатов")
        
        print("\n" + "=" * 50)
        print("✅ Проверка завершена!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке базы знаний: {e}")
        return False

def check_files_structure():
    """Проверка структуры файлов"""
    print("\n📁 Проверка структуры файлов...")
    
    required_files = [
        "modules/knowledge_base.py",
        "modules/bot_handler.py",
        "config.py",
        "scripts/populate_db.py",
        "scripts/update_documents.py",
        "scripts/scrape_websites.py",
        "data/legal_sites.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Отсутствует: {file_path}")
        else:
            print(f"✅ Найден: {file_path}")
    
    if missing_files:
        print(f"\n⚠️ Отсутствует файлов: {len(missing_files)}")
        return False
    else:
        print("\n✅ Все необходимые файлы найдены!")
        return True

def check_documents_directory():
    """Проверка папки с документами"""
    print("\n📄 Проверка папки с документами...")
    
    docs_dir = Path("data/documents")
    if not docs_dir.exists():
        print("❌ Папка data/documents не найдена")
        return False
    
    # Подсчет документов по типам
    pdf_files = list(docs_dir.glob("*.pdf"))
    docx_files = list(docs_dir.glob("*.docx"))
    doc_files = list(docs_dir.glob("*.doc"))
    
    print(f"📄 PDF файлов: {len(pdf_files)}")
    print(f"📄 DOCX файлов: {len(docx_files)}")
    print(f"📄 DOC файлов: {len(doc_files)}")
    
    total_docs = len(pdf_files) + len(docx_files) + len(doc_files)
    print(f"📊 Всего документов: {total_docs}")
    
    if total_docs == 0:
        print("⚠️ Нет документов для обработки")
        print("💡 Добавьте PDF, DOCX или DOC файлы в папку data/documents/")
        return False
    
    # Показываем первые 5 файлов
    all_files = pdf_files + docx_files + doc_files
    print("📋 Документы:")
    for i, file in enumerate(all_files[:5]):
        print(f"  {i+1}. {file.name}")
    
    if len(all_files) > 5:
        print(f"  ... и еще {len(all_files) - 5} документов")
    
    return True

def main():
    """Главная функция"""
    print("🤖 Быстрая проверка состояния базы знаний")
    print("=" * 50)
    
    try:
        # Проверка структуры файлов
        files_ok = check_files_structure()
        
        # Проверка документов
        docs_ok = check_documents_directory()
        
        # Проверка базы знаний
        if files_ok:
            kb_ok = check_knowledge_base_quick()
        else:
            kb_ok = False
        
        # Итоговая оценка
        print("\n" + "=" * 50)
        print("📊 ИТОГОВАЯ ОЦЕНКА:")
        print(f"  📁 Файлы: {'✅ OK' if files_ok else '❌ Проблемы'}")
        print(f"  📄 Документы: {'✅ OK' if docs_ok else '❌ Проблемы'}")
        print(f"  🗄️ База знаний: {'✅ OK' if kb_ok else '❌ Проблемы'}")
        
        if files_ok and docs_ok and kb_ok:
            print("\n🎉 Все системы работают отлично!")
            print("💡 Можете запускать чат-бота: python main.py")
        else:
            print("\n⚠️ Обнаружены проблемы")
            print("💡 Запустите: python quick_update_knowledge_base.py")
        
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 