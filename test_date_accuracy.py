#!/usr/bin/env python3
"""
Тест для проверки точности дат в ответах бота
"""
import sys
from pathlib import Path
import logging

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.knowledge_base import get_knowledge_base
from modules.llm_service import LLMService

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_date_accuracy():
    """Тестирует точность дат в ответах бота"""
    
    print("Тестирование точности дат в ответах бота...")
    
    kb = get_knowledge_base()
    llm_service = LLMService()
    
    # Тестовые запросы
    test_queries = [
        "налоговые ставки",
        "административные штрафы", 
        "права потребителя"
    ]
    
    for query in test_queries:
        print(f"\n=== Тест для запроса: '{query}' ===")
        
        # Получаем документы
        docs = kb.search_relevant_docs(query, n_results=3)
        
        if docs:
            print(f"Найдено документов: {len(docs)}")
            
            # Анализируем даты документов
            dates_info = []
            for i, doc in enumerate(docs, 1):
                metadata = doc.get('metadata', {})
                
                scraped_at = metadata.get('scraped_at')
                added_date = metadata.get('added_date')
                source_type = metadata.get('source_type', 'unknown')
                
                if scraped_at:
                    date_str = scraped_at[:8] if len(scraped_at) >= 8 else scraped_at
                    dates_info.append(f"  Документ {i}: {date_str} ({source_type})")
                elif added_date:
                    date_str = added_date[:10] if len(added_date) >= 10 else added_date
                    dates_info.append(f"  Документ {i}: {date_str} ({source_type})")
                else:
                    dates_info.append(f"  Документ {i}: дата не найдена ({source_type})")
            
            print("Даты документов:")
            for date_info in dates_info:
                print(date_info)
            
            # Тестируем новую функцию анализа дат
            analyzed_date = llm_service._analyze_document_dates(docs)
            print(f"Анализ дат: {analyzed_date}")
            
            # Тестируем создание промпта с новой датой
            context = llm_service._format_context(docs)
            prompt = llm_service._create_user_prompt(query, context, docs)
            
            # Извлекаем строку с датой из промпта
            lines = prompt.split('\n')
            date_line = None
            for line in lines:
                if 'Ответ соответствует законодательству РБ на дату:' in line:
                    date_line = line.strip()
                    break
            
            if date_line:
                print(f"Дата в ответе найдена: {len(date_line)} символов")
                # Извлекаем только дату из строки
                if 'на дату:' in date_line:
                    date_part = date_line.split('на дату:')[1].split('.')[0]
                    print(f"Извлеченная дата: {date_part}")
            else:
                print("Дата в ответе не найдена")
        else:
            print(f"Документы не найдены для запроса '{query}'")
    
    print(f"\nТест завершен!")

if __name__ == "__main__":
    test_date_accuracy() 