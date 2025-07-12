#!/usr/bin/env python3
"""
Расширенный comprehensive тест для всех фильтров юридических вопросов.
Включает 50+ тестовых случаев различных категорий и сложности.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.question_filter import QuestionFilter
from modules.improved_question_filter import ImprovedQuestionFilter
from modules.ml_question_filter import MLQuestionFilter
from modules.hybrid_question_filter import HybridQuestionFilter

class ExtendedComprehensiveTest:
    """Класс для расширенного тестирования всех фильтров."""
    
    def __init__(self):
        """Инициализация всех фильтров."""
        print("🚀 РАСШИРЕННЫЙ COMPREHENSIVE ТЕСТ")
        print("=" * 70)
        
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
    
    def get_extended_test_cases(self):
        """Возвращает расширенный набор тестовых случаев."""
        return [
            # === РАЗГОВОРНЫЕ ЮРИДИЧЕСКИЕ ВЫРАЖЕНИЯ ===
            ("Меня кинули с деньгами, что делать?", True, "разговорный"),
            ("Обманули при покупке квартиры", True, "разговорный"),
            ("Уволили незаконно с работы", True, "разговорный"),
            ("Развели на деньги в интернете", True, "разговорный"),
            ("Кидалово с автомобилем", True, "разговорный"),
            ("Облапошили при продаже дома", True, "разговорный"),
            ("Надули с кредитом в банке", True, "разговорный"),
            ("Подставили на работе", True, "разговорный"),
            ("Наехали соседи из-за забора", True, "разговорный"),
            ("Прокинули с зарплатой", True, "разговорный"),
            
            # === СПЕЦИАЛИЗИРОВАННЫЕ ЮРИДИЧЕСКИЕ ТЕРМИНЫ ===
            ("Эстоппель в гражданском праве", True, "специализированный"),
            ("Суброгация в страховом праве", True, "специализированный"),
            ("Виндикационный иск к третьему лицу", True, "специализированный"),
            ("Субсидиарная ответственность учредителей", True, "специализированный"),
            ("Негаторный иск против застройщика", True, "специализированный"),
            ("Реституция при недействительности сделки", True, "специализированный"),
            ("Цессия дебиторской задолженности", True, "специализированный"),
            ("Новация договорных обязательств", True, "специализированный"),
            ("Деликтная ответственность юридического лица", True, "специализированный"),
            ("Фидуциарные обязанности директора", True, "специализированный"),
            
            # === ИНОСТРАННЫЕ ЮРИДИЧЕСКИЕ ТЕРМИНЫ ===
            ("Что такое habeas corpus?", True, "иностранный"),
            ("Принцип res judicata в судопроизводстве", True, "иностранный"),
            ("Доктрина ultra vires в корпоративном праве", True, "иностранный"),
            ("Правило de minimis в антимонопольном праве", True, "иностранный"),
            ("Презумпция mens rea в уголовном праве", True, "иностранный"),
            ("Принцип pacta sunt servanda", True, "иностранный"),
            ("Доктрина forum non conveniens", True, "иностранный"),
            ("Правило ejusdem generis в толковании", True, "иностранный"),
            
            # === КОНТЕКСТНЫЕ ЮРИДИЧЕСКИЕ ВОПРОСЫ ===
            ("Какие права у меня есть?", True, "контекстный"),
            ("Что мне делать в такой ситуации?", True, "контекстный"),
            ("Могу ли я подать в суд?", True, "контекстный"),
            ("Какие документы нужны для суда?", True, "контекстный"),
            ("Какая ответственность предусмотрена?", True, "контекстный"),
            ("Как защитить свои интересы?", True, "контекстный"),
            ("Что говорит закон по этому поводу?", True, "контекстный"),
            ("Какие есть варианты решения?", True, "контекстный"),
            
            # === РЕГИОНАЛЬНЫЕ ЮРИДИЧЕСКИЕ ВОПРОСЫ ===
            ("Жилищные вопросы в Витебске", True, "региональный"),
            ("Трудовые споры в Гомеле", True, "региональный"),
            ("Земельные вопросы в Минской области", True, "региональный"),
            ("Налоговые споры в Бресте", True, "региональный"),
            ("Административные правонарушения в Могилеве", True, "региональный"),
            ("Семейные споры в Гродно", True, "региональный"),
            
            # === СТАНДАРТНЫЕ ЮРИДИЧЕСКИЕ ВОПРОСЫ ===
            ("Как подать иск в суд в Беларуси?", True, "стандартный"),
            ("Какие документы нужны для развода?", True, "стандартный"),
            ("Права потребителя в Беларуси", True, "стандартный"),
            ("Как оформить наследство?", True, "стандартный"),
            ("Трудовые права работника", True, "стандартный"),
            ("Защита прав собственности", True, "стандартный"),
            ("Алиментные обязательства", True, "стандартный"),
            ("Договор купли-продажи недвижимости", True, "стандартный"),
            ("Административная ответственность", True, "стандартный"),
            ("Уголовная ответственность несовершеннолетних", True, "стандартный"),
            
            # === НЕЮРИДИЧЕСКИЕ ВОПРОСЫ ===
            ("Как приготовить борщ?", False, "кулинария"),
            ("Какая погода завтра?", False, "погода"),
            ("Как установить Windows?", False, "техника"),
            ("Права доступа к базе данных", False, "IT"),
            ("Суд присяжных в кино", False, "кино"),
            ("Какие документы нужны?", False, "общий"),
            ("Как добраться до центра?", False, "транспорт"),
            ("Лучший рецепт пиццы", False, "кулинария"),
            ("Курс доллара сегодня", False, "финансы"),
            ("Как похудеть быстро?", False, "здоровье"),
            ("Настройка роутера дома", False, "техника"),
            ("Где купить цветы?", False, "покупки"),
            ("Как выучить английский?", False, "образование"),
            ("Ремонт автомобиля своими руками", False, "авто"),
            ("Как заработать в интернете?", False, "заработок"),
        ]
    
    def run_extended_test(self):
        """Запускает расширенный тест всех фильтров."""
        test_cases = self.get_extended_test_cases()
        
        print(f"\n🔍 РАСШИРЕННЫЙ ТЕСТ НА {len(test_cases)} СЛУЧАЯХ")
        print("=" * 70)
        
        # Заголовок таблицы
        print(f"{'№':<3} {'Вопрос':<45} {'Ожид.':<6} {'Баз.':<6} {'Улуч.':<6} {'ML':<6} {'Гибр.':<6}")
        print("-" * 80)
        
        results = {name: {'correct': 0, 'total': 0} for name in self.filters.keys()}
        category_results = {}
        detailed_results = []
        
        for i, (question, expected, category) in enumerate(test_cases, 1):
            expected_str = "ЮР" if expected else "НЕ ЮР"
            filter_results = {}
            
            # Инициализируем категорию если нужно
            if category not in category_results:
                category_results[category] = {name: {'correct': 0, 'total': 0} for name in self.filters.keys()}
            
            # Тестируем каждый фильтр
            for name, filter_instance in self.filters.items():
                try:
                    is_legal, score, explanation = filter_instance.is_legal_question(question)
                    result_str = "ЮР" if is_legal else "НЕ ЮР"
                    is_correct = is_legal == expected
                    
                    filter_results[name] = {
                        'result': is_legal,
                        'score': score,
                        'str': result_str,
                        'correct': is_correct
                    }
                    
                    if is_correct:
                        results[name]['correct'] += 1
                        category_results[category][name]['correct'] += 1
                    
                    results[name]['total'] += 1
                    category_results[category][name]['total'] += 1
                    
                except Exception as e:
                    filter_results[name] = {
                        'result': False,
                        'score': 0.0,
                        'str': "ERR",
                        'correct': False
                    }
                    results[name]['total'] += 1
                    category_results[category][name]['total'] += 1
            
            # Выводим результат
            question_short = question[:43] + "..." if len(question) > 43 else question
            base_result = filter_results.get('Базовый', {}).get('str', 'N/A')
            improved_result = filter_results.get('Улучшенный', {}).get('str', 'N/A')
            ml_result = filter_results.get('ML', {}).get('str', 'N/A')
            hybrid_result = filter_results.get('Гибридный', {}).get('str', 'N/A')
            
            print(f"{i:<3} {question_short:<45} {expected_str:<6} {base_result:<6} {improved_result:<6} {ml_result:<6} {hybrid_result:<6}")
            
            detailed_results.append({
                'question': question,
                'expected': expected,
                'category': category,
                'results': filter_results
            })
        
        # Выводим общую статистику
        print(f"\n📊 ОБЩАЯ СТАТИСТИКА ({len(test_cases)} случаев)")
        print("=" * 50)
        
        for name, stats in results.items():
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total'] * 100
                print(f"{name:<12}: {stats['correct']:2d}/{stats['total']:2d} ({accuracy:5.1f}%)")
        
        # Выводим статистику по категориям
        print(f"\n📋 СТАТИСТИКА ПО КАТЕГОРИЯМ")
        print("=" * 50)
        
        for category, cat_results in category_results.items():
            print(f"\n🏷️  {category.upper()}:")
            for name, stats in cat_results.items():
                if stats['total'] > 0:
                    accuracy = stats['correct'] / stats['total'] * 100
                    print(f"   {name:<12}: {stats['correct']:2d}/{stats['total']:2d} ({accuracy:5.1f}%)")
        
        # Анализируем лучшие результаты
        print(f"\n🏆 АНАЛИЗ ЛУЧШИХ РЕЗУЛЬТАТОВ")
        print("=" * 50)
        
        best_filter = max(results.items(), key=lambda x: x[1]['correct'] / max(x[1]['total'], 1))
        best_name, best_stats = best_filter
        best_accuracy = best_stats['correct'] / best_stats['total'] * 100
        
        print(f"🥇 Лучший фильтр: {best_name}")
        print(f"   Общая точность: {best_accuracy:.1f}% ({best_stats['correct']}/{best_stats['total']})")
        
        # Топ-3 фильтров
        sorted_filters = sorted(results.items(), key=lambda x: x[1]['correct'] / max(x[1]['total'], 1), reverse=True)
        print(f"\n🏅 ТОП-3 ФИЛЬТРОВ:")
        for i, (name, stats) in enumerate(sorted_filters[:3], 1):
            accuracy = stats['correct'] / stats['total'] * 100
            print(f"   {i}. {name}: {accuracy:.1f}% ({stats['correct']}/{stats['total']})")
        
        # Анализируем проблемные случаи
        print(f"\n🔍 АНАЛИЗ ПРОБЛЕМНЫХ СЛУЧАЕВ")
        print("=" * 50)
        
        problem_cases = []
        for result in detailed_results:
            question = result['question']
            expected = result['expected']
            
            # Проверяем ошибки лучшего фильтра
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
            print(f"❌ Проблемные случаи для {best_name} фильтра ({len(problem_cases)} из {best_stats['total']}):")
            for case in problem_cases:
                expected_str = "ЮР" if case['expected'] else "НЕ ЮР"
                got_str = "ЮР" if case['got'] else "НЕ ЮР"
                print(f"   • {case['question']}")
                print(f"     Ожидалось: {expected_str}, Получено: {got_str} (балл: {case['score']:.3f})")
                print(f"     Категория: {case['category']}")
        else:
            print(f"🎉 {best_name} фильтр справился со всеми тестами!")
        
        return results, category_results, detailed_results

def main():
    """Основная функция."""
    print("🎯 РАСШИРЕННЫЙ COMPREHENSIVE ТЕСТ ФИЛЬТРОВ")
    print("=" * 70)
    
    try:
        test = ExtendedComprehensiveTest()
        results, category_results, detailed_results = test.run_extended_test()
        
        print(f"\n✅ РАСШИРЕННЫЙ ТЕСТ ЗАВЕРШЕН!")
        print("=" * 50)
        print("📈 Результаты показывают производительность каждого фильтра")
        print("📊 на большом наборе разнообразных тестовых случаев")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении теста: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 