#!/usr/bin/env python3
"""
Простой тест продвинутого фильтра.
"""
import disable_telemetry
import os
import sys
from pathlib import Path

# Отключаем телеметрию ChromaDB
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Тестирует импорты."""
    try:
        print("Тестирование импортов...")
        from modules.question_filter import QuestionFilter
        print("✅ Базовый фильтр импортирован")
        
        from modules.advanced_question_filter import AdvancedQuestionFilter
        print("✅ Продвинутый фильтр импортирован")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Тестирует базовую функциональность."""
    try:
        from modules.question_filter import QuestionFilter
        from modules.advanced_question_filter import AdvancedQuestionFilter
        
        print("\nИнициализация фильтров...")
        basic_filter = QuestionFilter()
        advanced_filter = AdvancedQuestionFilter()
        print("✅ Фильтры инициализированы")
        
        # Тестовые вопросы
        test_questions = [
            "Как подать иск в суд?",
            "Меня кинули с деньгами",
            "Как приготовить борщ?",
            "Эстоппель в гражданском праве",
            "Что такое habeas corpus?"
        ]
        
        print("\nТестирование вопросов:")
        for question in test_questions:
            print(f"\nВопрос: {question}")
            
            # Базовый фильтр
            basic_result = basic_filter.is_legal_question(question)
            print(f"  Базовый: {'ЮР' if basic_result[0] else 'НЕ ЮР'} ({basic_result[1]:.3f})")
            
            # Продвинутый фильтр
            advanced_result = advanced_filter.is_legal_question(question)
            print(f"  Продвинутый: {'ЮР' if advanced_result[0] else 'НЕ ЮР'} ({advanced_result[1]:.3f})")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Главная функция."""
    print("🧪 ТЕСТИРОВАНИЕ ПРОДВИНУТОГО ФИЛЬТРА")
    print("=" * 50)
    
    if not test_imports():
        return
    
    if not test_basic_functionality():
        return
    
    print("\n✅ ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")

if __name__ == "__main__":
    main() 