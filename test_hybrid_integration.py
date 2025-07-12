#!/usr/bin/env python3
"""
Тест интеграции гибридного фильтра в bot_handler.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.bot_handler import is_legal_question, get_rejection_message

def test_hybrid_integration():
    """Тестирует интеграцию гибридного фильтра."""
    print("🔬 ТЕСТ ИНТЕГРАЦИИ ГИБРИДНОГО ФИЛЬТРА")
    print("=" * 50)
    
    # Тестовые случаи
    test_cases = [
        ("Как подать иск в суд?", True, "стандартный юридический"),
        ("Меня кинули с деньгами", True, "разговорный юридический"),
        ("Что такое эстоппель?", True, "специализированный термин"),
        ("Habeas corpus что это?", True, "иностранный термин"),
        ("Жилищные вопросы в Витебске", True, "региональный вопрос"),
        ("Как приготовить борщ?", False, "неюридический"),
        ("Права доступа к базе данных", False, "технический термин"),
        ("Суд присяжных в кино", False, "ложное срабатывание"),
    ]
    
    print("📊 Результаты тестирования:")
    print("-" * 80)
    print(f"{'Вопрос':<40} {'Ожид.':<6} {'Результат':<8} {'Балл':<8} {'Объяснение':<30}")
    print("-" * 80)
    
    correct = 0
    total = len(test_cases)
    
    for question, expected, category in test_cases:
        try:
            is_legal, score, explanation = is_legal_question(question)
            
            result_icon = "✅" if is_legal == expected else "❌"
            status = "ЮР" if is_legal else "НЕ ЮР"
            expected_status = "ЮР" if expected else "НЕ ЮР"
            
            # Сокращаем объяснение для красивого вывода
            short_explanation = explanation[:28] + "..." if len(explanation) > 28 else explanation
            
            print(f"{result_icon} {question[:38]:<38} {expected_status:<6} {status:<8} {score:<8.3f} {short_explanation}")
            
            if is_legal == expected:
                correct += 1
                
        except Exception as e:
            print(f"❌ {question[:38]:<38} ОШИБКА: {e}")
    
    print("-" * 80)
    accuracy = correct / total * 100
    print(f"📈 ИТОГОВАЯ ТОЧНОСТЬ: {correct}/{total} ({accuracy:.1f}%)")
    
    # Тестируем сообщение об отклонении
    print(f"\n📝 СООБЩЕНИЕ ОБ ОТКЛОНЕНИИ:")
    try:
        rejection_msg = get_rejection_message()
        print(f"✅ Сообщение получено: {rejection_msg[:100]}...")
    except Exception as e:
        print(f"❌ Ошибка получения сообщения: {e}")
    
    # Итоговая оценка
    print(f"\n🎯 ИТОГОВАЯ ОЦЕНКА:")
    if accuracy >= 90:
        print("🎉 ОТЛИЧНО! Гибридный фильтр работает превосходно")
    elif accuracy >= 80:
        print("👍 ХОРОШО! Гибридный фильтр работает стабильно")
    elif accuracy >= 70:
        print("⚠️ УДОВЛЕТВОРИТЕЛЬНО! Требуется дополнительная настройка")
    else:
        print("❌ ПЛОХО! Требуется серьезная доработка")
    
    return accuracy

if __name__ == "__main__":
    try:
        accuracy = test_hybrid_integration()
        print(f"\n✅ ТЕСТ ЗАВЕРШЕН! Точность: {accuracy:.1f}%")
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc() 