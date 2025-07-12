#!/usr/bin/env python3
"""
Финальное сравнение всех фильтров для юридических вопросов.
Включает базовый, улучшенный, ML и гибридный фильтры.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.question_filter import QuestionFilter
from modules.improved_question_filter import ImprovedQuestionFilter
from modules.ml_question_filter import MLQuestionFilter
from modules.hybrid_question_filter import HybridQuestionFilter

class UltimateFilterComparison:
    """Класс для сравнения всех фильтров."""
    
    def __init__(self):
        """Инициализация всех фильтров."""
        print("🚀 ИНИЦИАЛИЗАЦИЯ ВСЕХ ФИЛЬТРОВ")
        print("=" * 60)
        
        # Инициализируем фильтры
        self.filters = {}
        
        try:
            self.filters['Базовый'] = QuestionFilter()
            print("✅ Базовый фильтр инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации базового фильтра: {e}")
        
        try:
            self.filters['Улучшенный'] = ImprovedQuestionFilter()
            print("✅ Улучшенный фильтр инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации улучшенного фильтра: {e}")
        
        try:
            self.filters['ML'] = MLQuestionFilter()
            print("✅ ML-фильтр инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации ML-фильтра: {e}")
        
        try:
            self.filters['Гибридный'] = HybridQuestionFilter()
            print("✅ Гибридный фильтр инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации гибридного фильтра: {e}")
        
        print(f"\n📊 Инициализировано {len(self.filters)} фильтров")
    
    def get_test_cases(self):
        """Возвращает тестовые случаи для сравнения."""
        return [
            # Ключевые проблемные случаи из предыдущих тестов
            ("Меня кинули с деньгами, что делать?", True, "разговорный"),
            ("Эстоппель в гражданском праве", True, "специализированный"),
            ("Что такое habeas corpus?", True, "иностранный"),
            ("Какие права у меня есть?", True, "контекстный"),
            ("Купил телефон, а он сломался через неделю", True, "разговорный"),
            ("Врач сделал неправильную операцию", True, "разговорный"),
            ("Суброгация в страховом праве", True, "специализированный"),
            ("Жилищные вопросы в Витебске", True, "региональный"),
            
            # Стандартные юридические вопросы
            ("Как подать иск в суд в Беларуси?", True, "стандартный"),
            ("Какие документы нужны для развода?", True, "стандартный"),
            ("Права потребителя в Беларуси", True, "стандартный"),
            
            # Неюридические вопросы
            ("Как приготовить борщ?", False, "обычное"),
            ("Какая погода завтра?", False, "обычное"),
            ("Как установить Windows?", False, "обычное"),
            ("Права доступа к базе данных", False, "техническое"),
            ("Суд присяжных в кино", False, "техническое"),
            ("Какие документы нужны?", False, "контекстный_не_юр"),
        ]
    
    def run_comparison(self):
        """Запускает сравнение всех фильтров."""
        test_cases = self.get_test_cases()
        
        print("\n🔍 СРАВНЕНИЕ ВСЕХ ФИЛЬТРОВ")
        print("=" * 60)
        
        # Заголовок таблицы
        print(f"{'Вопрос':<45} {'Ожид.':<6} {'Баз.':<8} {'Улуч.':<8} {'ML':<8} {'Гибр.':<8}")
        print("-" * 90)
        
        results = {name: {'correct': 0, 'total': 0} for name in self.filters.keys()}
        detailed_results = []
        
        for question, expected, category in test_cases:
            expected_str = "ЮР" if expected else "НЕ ЮР"
            filter_results = {}
            
            # Тестируем каждый фильтр
            for name, filter_instance in self.filters.items():
                try:
                    is_legal, score, explanation = filter_instance.is_legal_question(question)
                    result_str = "ЮР" if is_legal else "НЕ ЮР"
                    filter_results[name] = {
                        'result': is_legal,
                        'score': score,
                        'str': result_str,
                        'correct': is_legal == expected
                    }
                    
                    if is_legal == expected:
                        results[name]['correct'] += 1
                    results[name]['total'] += 1
                    
                except Exception as e:
                    filter_results[name] = {
                        'result': False,
                        'score': 0.0,
                        'str': "ОШИБКА",
                        'correct': False
                    }
                    results[name]['total'] += 1
            
            # Выводим результат
            question_short = question[:43] + "..." if len(question) > 43 else question
            base_result = filter_results.get('Базовый', {}).get('str', 'N/A')
            improved_result = filter_results.get('Улучшенный', {}).get('str', 'N/A')
            ml_result = filter_results.get('ML', {}).get('str', 'N/A')
            hybrid_result = filter_results.get('Гибридный', {}).get('str', 'N/A')
            
            print(f"{question_short:<45} {expected_str:<6} {base_result:<8} {improved_result:<8} {ml_result:<8} {hybrid_result:<8}")
            
            detailed_results.append({
                'question': question,
                'expected': expected,
                'category': category,
                'results': filter_results
            })
        
        # Выводим статистику
        print("\n📊 СТАТИСТИКА ТОЧНОСТИ")
        print("=" * 40)
        
        for name, stats in results.items():
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total'] * 100
                print(f"{name:<12}: {stats['correct']:2d}/{stats['total']:2d} ({accuracy:5.1f}%)")
        
        # Анализируем лучшие результаты
        print("\n🏆 АНАЛИЗ ЛУЧШИХ РЕЗУЛЬТАТОВ")
        print("=" * 40)
        
        best_filter = max(results.items(), key=lambda x: x[1]['correct'] / max(x[1]['total'], 1))
        best_name, best_stats = best_filter
        best_accuracy = best_stats['correct'] / best_stats['total'] * 100
        
        print(f"🥇 Лучший фильтр: {best_name}")
        print(f"   Точность: {best_accuracy:.1f}% ({best_stats['correct']}/{best_stats['total']})")
        
        # Анализируем проблемные случаи
        print("\n🔍 АНАЛИЗ ПРОБЛЕМНЫХ СЛУЧАЕВ")
        print("=" * 40)
        
        problem_cases = []
        for result in detailed_results:
            question = result['question']
            expected = result['expected']
            
            # Проверяем, есть ли ошибки у лучшего фильтра
            if best_name in result['results']:
                best_filter_result = result['results'][best_name]
                if not best_filter_result['correct']:
                    problem_cases.append({
                        'question': question,
                        'expected': expected,
                        'got': best_filter_result['result'],
                        'score': best_filter_result['score'],
                        'category': result['category']
                    })
        
        if problem_cases:
            print(f"❌ Проблемные случаи для {best_name} фильтра:")
            for case in problem_cases:
                expected_str = "ЮР" if case['expected'] else "НЕ ЮР"
                got_str = "ЮР" if case['got'] else "НЕ ЮР"
                print(f"   • {case['question'][:50]}...")
                print(f"     Ожидалось: {expected_str}, Получено: {got_str} (балл: {case['score']:.3f})")
                print(f"     Категория: {case['category']}")
        else:
            print(f"🎉 {best_name} фильтр справился со всеми тестами!")
        
        return results, detailed_results

def main():
    """Основная функция."""
    print("🎯 ФИНАЛЬНОЕ СРАВНЕНИЕ ВСЕХ ФИЛЬТРОВ")
    print("=" * 60)
    
    try:
        comparison = UltimateFilterComparison()
        results, detailed_results = comparison.run_comparison()
        
        print("\n✅ СРАВНЕНИЕ ЗАВЕРШЕНО!")
        print("Рекомендация: Используйте фильтр с наивысшей точностью для продакшена.")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении сравнения: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 