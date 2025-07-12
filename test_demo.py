#!/usr/bin/env python3
"""
Простой тест демо-версии системы.
"""
import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from demo_bot import DemoLegalAssistant

def main():
    print("🧪 ТЕСТИРОВАНИЕ ДЕМО-ВЕРСИИ ЮРИДИЧЕСКОГО АССИСТЕНТА")
    print("=" * 60)
    
    try:
        # Инициализируем демо-ассистента
        demo = DemoLegalAssistant()
        
        # Тестовые вопросы
        test_questions = [
            "налоговые ставки",
            "права потребителя", 
            "документы для регистрации",
            "административные штрафы"
        ]
        
        print(f"📚 База знаний содержит {demo.knowledge_base.get_collection_stats().get('total_documents', 0)} документов\n")
        
        for i, question in enumerate(test_questions, 1):
            print(f"🔍 ТЕСТ {i}: '{question}'")
            print("-" * 40)
            
            answer = demo.get_demo_answer(question)
            print(answer)
            print("\n" + "="*60 + "\n")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 