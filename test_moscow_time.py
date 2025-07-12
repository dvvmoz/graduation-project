#!/usr/bin/env python3
"""
Тест для проверки работы с временем МСК
"""
import sys
from pathlib import Path
import logging

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.llm_service import LLMService

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_moscow_time():
    """Тестирует работу с временем МСК"""
    
    print("Тестирование работы с временем МСК...")
    
    llm_service = LLMService()
    
    # Тестовые документы с разными форматами времени
    test_cases = [
        {
            'name': 'Один документ с полным временем',
            'docs': [
                {
                    'content': 'Документ с полным временем',
                    'metadata': {
                        'scraped_at': '20250712_170540',
                        'source_type': 'pravo.by_dynamic',
                        'title': 'Документ с временем'
                    }
                }
            ]
        },
        {
            'name': 'Документы с разным временем в один день',
            'docs': [
                {
                    'content': 'Первый документ',
                    'metadata': {
                        'scraped_at': '20250712_100000',
                        'source_type': 'pravo.by_dynamic',
                        'title': 'Утренний документ'
                    }
                },
                {
                    'content': 'Второй документ',
                    'metadata': {
                        'scraped_at': '20250712_180000',
                        'source_type': 'pravo.by_dynamic',
                        'title': 'Вечерний документ'
                    }
                }
            ]
        },
        {
            'name': 'Документы с разными датами',
            'docs': [
                {
                    'content': 'Старый документ',
                    'metadata': {
                        'scraped_at': '20250601_120000',
                        'source_type': 'pravo.by_dynamic',
                        'title': 'Июньский документ'
                    }
                },
                {
                    'content': 'Новый документ',
                    'metadata': {
                        'scraped_at': '20250712_170000',
                        'source_type': 'pravo.by_dynamic',
                        'title': 'Июльский документ'
                    }
                }
            ]
        },
        {
            'name': 'Смешанные источники',
            'docs': [
                {
                    'content': 'PDF документ',
                    'metadata': {
                        'added_date': '2025-05-15T10:30:00.000000',
                        'source_type': 'pdf_document',
                        'title': 'PDF документ'
                    }
                },
                {
                    'content': 'Веб документ',
                    'metadata': {
                        'scraped_at': '20250712_170540',
                        'source_type': 'pravo.by_dynamic',
                        'title': 'Веб документ'
                    }
                }
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n=== {test_case['name']} ===")
        
        # Анализируем даты
        analyzed_date = llm_service._analyze_document_dates(test_case['docs'])
        print(f"Результат: {analyzed_date}")
        
        # Показываем исходные данные
        print("Исходные данные:")
        for i, doc in enumerate(test_case['docs'], 1):
            metadata = doc['metadata']
            scraped_at = metadata.get('scraped_at', '')
            added_date = metadata.get('added_date', '')
            source_type = metadata.get('source_type', '')
            
            if scraped_at:
                print(f"  Документ {i}: {scraped_at} ({source_type})")
            elif added_date:
                print(f"  Документ {i}: {added_date} ({source_type})")
    
    print(f"\nТест завершен!")

if __name__ == "__main__":
    test_moscow_time() 