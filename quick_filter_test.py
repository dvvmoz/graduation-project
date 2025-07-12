#!/usr/bin/env python3
"""
Быстрый тест всех фильтров для проверки их работы.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_filters():
    """Быстрый тест всех фильтров."""
    print("🔍 БЫСТРАЯ ПРОВЕРКА ВСЕХ ФИЛЬТРОВ")
    print("=" * 50)
    
    # Тестовые вопросы
    test_questions = [
        ("Как подать иск в суд?", True, "стандартный юридический"),
        ("Меня кинули с деньгами", True, "разговорный юридический"),
        ("Что такое эстоппель?", True, "специализированный термин"),
        ("Как приготовить борщ?", False, "неюридический"),
        ("Права доступа к базе данных", False, "технический термин"),
    ]
    
    # Тестируем каждый фильтр
    filters_to_test = [
        ("Базовый", "modules.question_filter", "QuestionFilter"),
        ("Улучшенный", "modules.improved_question_filter", "ImprovedQuestionFilter"),
        ("ML", "modules.ml_question_filter", "MLQuestionFilter"),
        ("Гибридный", "modules.hybrid_question_filter", "HybridQuestionFilter"),
    ]
    
    results = {}
    
    for filter_name, module_name, class_name in filters_to_test:
        print(f"\n📊 Тестирование {filter_name} фильтра:")
        print("-" * 30)
        
        try:
            # Динамический импорт
            module = __import__(module_name, fromlist=[class_name])
            filter_class = getattr(module, class_name)
            filter_instance = filter_class()
            
            correct = 0
            total = len(test_questions)
            
            for question, expected, category in test_questions:
                try:
                    is_legal, score, explanation = filter_instance.is_legal_question(question)
                    result = "✅" if is_legal == expected else "❌"
                    status = "ЮР" if is_legal else "НЕ ЮР"
                    expected_status = "ЮР" if expected else "НЕ ЮР"
                    
                    print(f"{result} {question[:30]:30} | {expected_status:6} → {status:6} | {score:.3f}")
                    
                    if is_legal == expected:
                        correct += 1
                        
                except Exception as e:
                    print(f"❌ {question[:30]:30} | ОШИБКА: {e}")
            
            accuracy = correct / total * 100
            results[filter_name] = accuracy
            print(f"📈 Точность: {correct}/{total} ({accuracy:.1f}%)")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации {filter_name} фильтра: {e}")
            results[filter_name] = 0
    
    # Итоговые результаты
    print("\n🏆 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 30)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    for i, (name, accuracy) in enumerate(sorted_results):
        medal = ["🥇", "🥈", "🥉", "🏅"][min(i, 3)]
        print(f"{medal} {name:12}: {accuracy:5.1f}%")
    
    # Рекомендация
    if sorted_results:
        best_filter = sorted_results[0][0]
        best_accuracy = sorted_results[0][1]
        
        print(f"\n💡 РЕКОМЕНДАЦИЯ:")
        if best_accuracy >= 90:
            print(f"✅ Используйте {best_filter} фильтр ({best_accuracy:.1f}%) для продакшена")
        elif best_accuracy >= 80:
            print(f"👍 {best_filter} фильтр ({best_accuracy:.1f}%) подходит для использования")
        else:
            print(f"⚠️ Требуется дополнительная настройка фильтров")

if __name__ == "__main__":
    test_filters() 