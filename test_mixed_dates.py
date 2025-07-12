#!/usr/bin/env python3
"""
Тест для проверки работы с документами разных дат
"""
import sys
from pathlib import Path
import logging
from datetime import datetime, timedelta

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.knowledge_base import get_knowledge_base
from modules.llm_service import LLMService

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mixed_dates():
    """Тестирует работу с документами разных дат"""
    
    print("Тестирование работы с документами разных дат...")
    
    kb = get_knowledge_base()
    llm_service = LLMService()
    
    # Создаем тестовые документы с разными датами
    test_docs = [
        {
            'content': 'Тестовый документ 1 о налоговых ставках',
            'metadata': {
                'scraped_at': '20250601_120000',
                'source_type': 'pravo.by_dynamic',
                'title': 'Старый документ'
            },
            'distance': 0.1
        },
        {
            'content': 'Тестовый документ 2 о налоговых ставках',
            'metadata': {
                'scraped_at': '20250712_170000',
                'source_type': 'pravo.by_dynamic',
                'title': 'Новый документ'
            },
            'distance': 0.2
        },
        {
            'content': 'Тестовый документ 3 о налоговых ставках',
            'metadata': {
                'added_date': '2025-05-15T10:30:00.000000',
                'source_type': 'pdf_document',
                'title': 'PDF документ'
            },
            'distance': 0.3
        }
    ]
    
    print(f"Создано {len(test_docs)} тестовых документов с разными датами:")
    for i, doc in enumerate(test_docs, 1):
        metadata = doc['metadata']
        scraped_at = metadata.get('scraped_at', '')
        added_date = metadata.get('added_date', '')
        source_type = metadata.get('source_type', '')
        
        if scraped_at:
            date_str = scraped_at[:8]
            print(f"  Документ {i}: {date_str} ({source_type})")
        elif added_date:
            date_str = added_date[:10]
            print(f"  Документ {i}: {date_str} ({source_type})")
    
    # Тестируем анализ дат
    analyzed_date = llm_service._analyze_document_dates(test_docs)
    print(f"\nАнализ дат: {analyzed_date}")
    
    # Тестируем создание промпта
    context = llm_service._format_context(test_docs)
    prompt = llm_service._create_user_prompt("налоговые ставки", context, test_docs)
    
    # Извлекаем строку с датой из промпта
    lines = prompt.split('\n')
    date_line = None
    for line in lines:
        if 'Ответ соответствует законодательству РБ на дату:' in line:
            date_line = line.strip()
            break
    
    if date_line:
        print(f"Дата в ответе найдена")
        # Извлекаем дату из строки
        if 'на дату:' in date_line:
            date_part = date_line.split('на дату:')[1].split('Не заменяет')[0].strip()
            print(f"Извлеченная дата: {date_part}")
    else:
        print("Дата в ответе не найдена")
    
    print(f"\nТест завершен!")

if __name__ == "__main__":
    test_mixed_dates() 