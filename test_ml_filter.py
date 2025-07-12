#!/usr/bin/env python3
"""
Тестирование ML-фильтра для юридических вопросов.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ml_question_filter import MLQuestionFilter, is_legal_question_ml

def test_ml_filter():
    """Тестирует ML-фильтр на различных примерах."""
    print("🤖 ТЕСТИРОВАНИЕ ML-ФИЛЬТРА")
    print("=" * 50)
    
    # Тестовые случаи
    test_cases = [
        # Юридические вопросы
        ("Как подать иск в суд?", True),
        ("Меня кинули с деньгами", True),
        ("Эстоппель в праве", True),
        ("Habeas corpus что это?", True),
        ("Права потребителя", True),
        
        # Неюридические вопросы
        ("Как приготовить борщ?", False),
        ("Какая погода завтра?", False),
        ("Как установить Windows?", False),
        ("Права доступа к базе данных", False),
        ("Суд присяжных в кино", False),
    ]
    
    print("Инициализация ML-фильтра...")
    try:
        ml_filter = MLQuestionFilter()
        print("✅ ML-фильтр инициализирован")
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        return
    
    print("\nТестирование на примерах:")
    print("-" * 50)
    
    correct = 0
    total = len(test_cases)
    
    for question, expected in test_cases:
        try:
            is_legal, confidence, explanation = ml_filter.is_legal_question(question)
            
            result = "✅" if is_legal == expected else "❌"
            status = "ЮР" if is_legal else "НЕ ЮР"
            expected_status = "ЮР" if expected else "НЕ ЮР"
            
            print(f"{result} {question[:40]:40} | Ожидалось: {expected_status:6} | Получено: {status:6} | Уверенность: {confidence:.3f}")
            
            if is_legal == expected:
                correct += 1
                
        except Exception as e:
            print(f"❌ {question[:40]:40} | ОШИБКА: {e}")
    
    accuracy = correct / total * 100
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"Правильных ответов: {correct}/{total}")
    print(f"Точность: {accuracy:.1f}%")
    
    if accuracy >= 90:
        print("🎉 Отличный результат!")
    elif accuracy >= 80:
        print("👍 Хороший результат!")
    else:
        print("⚠️ Требуется улучшение")

if __name__ == "__main__":
    test_ml_filter() 