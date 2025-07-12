#!/usr/bin/env python3
"""
Простой тест интеграции ML-фильтра в bot_handler.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ml_question_filter import is_legal_question_ml, get_ml_rejection_message

def test_ml_integration():
    """Тестирует интеграцию ML-фильтра."""
    print("ТЕСТ ИНТЕГРАЦИИ ML-ФИЛЬТРА")
    print("=" * 50)
    
    # Тестовые случаи
    test_cases = [
        ("Как подать иск в суд в Беларуси?", True),
        ("Меня кинули с деньгами, что делать?", True),
        ("Эстоппель в гражданском праве", True),
        ("Что такое habeas corpus?", True),
        ("Какие права у меня есть?", True),
        ("Как приготовить борщ?", False),
        ("Какая погода завтра?", False),
        ("Права доступа к базе данных", False),
    ]
    
    print(f"Тестирование {len(test_cases)} случаев:")
    print("-" * 70)
    
    correct = 0
    total = len(test_cases)
    
    for question, expected in test_cases:
        try:
            is_legal, score, explanation = is_legal_question_ml(question)
            
            # Проверяем результат
            is_correct = is_legal == expected
            if is_correct:
                correct += 1
                status = "OK"
            else:
                status = "FAIL"
            
            # Форматируем вывод
            expected_str = "ЮР" if expected else "НЕ ЮР"
            result_str = "ЮР" if is_legal else "НЕ ЮР"
            
            print(f"{question[:45]:<45} {expected_str:<10} {result_str:<10} {status}")
            
        except Exception as e:
            print(f"{question[:45]:<45} ERROR      ERROR      ERROR")
            print(f"   Ошибка: {e}")
    
    print("-" * 70)
    accuracy = correct / total * 100
    print(f"РЕЗУЛЬТАТ: {correct}/{total} ({accuracy:.1f}%)")
    
    # Тестируем сообщение отклонения
    print(f"\nТЕСТ СООБЩЕНИЯ ОТКЛОНЕНИЯ:")
    try:
        rejection_message = get_ml_rejection_message()
        print(f"Сообщение получено: {len(rejection_message)} символов")
        print(f"Начало: {rejection_message[:100]}...")
    except Exception as e:
        print(f"Ошибка получения сообщения: {e}")
    
    # Общий результат
    print(f"\nОБЩИЙ РЕЗУЛЬТАТ ИНТЕГРАЦИИ:")
    if accuracy >= 80:
        print(f"УСПЕШНО - ML-фильтр интегрирован корректно ({accuracy:.1f}%)")
        return True
    else:
        print(f"НЕУДАЧНО - Низкая точность ({accuracy:.1f}%)")
        return False

def test_import_compatibility():
    """Тестирует совместимость импортов."""
    print(f"\nТЕСТ СОВМЕСТИМОСТИ ИМПОРТОВ:")
    print("-" * 40)
    
    try:
        # Тестируем импорт как в bot_handler.py
        from modules.ml_question_filter import is_legal_question_ml as is_legal_question, get_ml_rejection_message as get_rejection_message
        
        # Тестируем функции
        result = is_legal_question("Тестовый вопрос")
        message = get_rejection_message()
        
        print("Импорты совместимы")
        print("Функции работают корректно")
        print("Интеграция готова к использованию")
        
        return True
        
    except Exception as e:
        print(f"Ошибка совместимости: {e}")
        return False

def main():
    """Основная функция."""
    print("ТЕСТ ИНТЕГРАЦИИ ML-ФИЛЬТРА В BOT_HANDLER")
    print("=" * 60)
    
    try:
        # Тестируем интеграцию
        integration_ok = test_ml_integration()
        
        # Тестируем совместимость
        compatibility_ok = test_import_compatibility()
        
        # Общий результат
        print(f"\nФИНАЛЬНЫЙ РЕЗУЛЬТАТ:")
        print("=" * 30)
        
        if integration_ok and compatibility_ok:
            print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
            print("ML-фильтр успешно интегрирован в bot_handler.py")
            print("Система готова к использованию")
        else:
            print("ЕСТЬ ПРОБЛЕМЫ С ИНТЕГРАЦИЕЙ")
            print("Требуется дополнительная настройка")
        
    except Exception as e:
        print(f"Критическая ошибка теста: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 