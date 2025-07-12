#!/usr/bin/env python3
"""
Финальное сравнение всех фильтров: базового, оптимизированного и улучшенного.
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

from modules.question_filter import QuestionFilter
from modules.improved_question_filter import ImprovedQuestionFilter
from typing import List, Dict, Tuple

class FinalFilterComparison:
    """Финальное сравнение всех фильтров."""
    
    def __init__(self):
        """Инициализирует сравнение фильтров."""
        print("Инициализация фильтров...")
        self.basic_filter = QuestionFilter()
        self.improved_filter = ImprovedQuestionFilter()
        print("✅ Фильтры инициализированы")
        
        # Комплексные тестовые случаи
        self.test_cases = [
            # === ДОЛЖНЫ БЫТЬ ЮРИДИЧЕСКИМИ ===
            
            # 1. Стандартные юридические вопросы
            ("Как подать иск в суд в Беларуси?", True, "стандартный"),
            ("Какие документы нужны для развода в РБ?", True, "стандартный"),
            ("Как оформить трудовой договор по ТК РБ?", True, "стандартный"),
            ("Какие права у потребителя в Беларуси?", True, "стандартный"),
            ("Как обжаловать решение административного органа?", True, "стандартный"),
            
            # 2. Разговорные юридические вопросы
            ("Меня кинули с деньгами, что делать?", True, "разговорный"),
            ("Начальник не платит зарплату уже месяц", True, "разговорный"),
            ("Соседи шумят по ночам, как их утихомирить?", True, "разговорный"),
            ("Развожусь с мужем, он не дает денег на ребенка", True, "разговорный"),
            ("Купил телефон, а он сломался через неделю", True, "разговорный"),
            ("Меня уволили без предупреждения", True, "разговорный"),
            ("Банк списал деньги без моего согласия", True, "разговорный"),
            ("Врач сделал неправильную операцию", True, "разговорный"),
            ("Полиция задержала без причины", True, "разговорный"),
            ("Управляющая компания не делает ремонт", True, "разговорный"),
            
            # 3. Специализированные юридические термины
            ("Эстоппель в гражданском праве", True, "специализированный"),
            ("Субсидиарная ответственность учредителей", True, "специализированный"),
            ("Виндикационный иск против добросовестного приобретателя", True, "специализированный"),
            ("Негаторный иск в отношении недвижимости", True, "специализированный"),
            ("Реституция при недействительности сделки", True, "специализированный"),
            ("Цессия требования по договору подряда", True, "специализированный"),
            ("Новация долга в обязательственном праве", True, "специализированный"),
            ("Суброгация в страховом праве", True, "специализированный"),
            ("Деликтная ответственность за причинение вреда", True, "специализированный"),
            ("Виндикация бездокументарных ценных бумаг", True, "специализированный"),
            
            # 4. Иностранные юридические термины
            ("Что такое habeas corpus?", True, "иностранный"),
            ("Принцип pacta sunt servanda", True, "иностранный"),
            ("Доктрина res ipsa loquitur", True, "иностранный"),
            ("Правило de minimis non curat lex", True, "иностранный"),
            ("Принцип ultra vires в корпоративном праве", True, "иностранный"),
            ("Что означает pro bono в юриспруденции?", True, "иностранный"),
            ("Концепция force majeure в договорах", True, "иностранный"),
            ("Принцип caveat emptor при покупке", True, "иностранный"),
            ("Доктрина respondeat superior", True, "иностранный"),
            ("Правило nemo dat quod non habet", True, "иностранный"),
            
            # 5. Контекстно-зависимые юридические вопросы
            ("Права человека в интернете", True, "контекстный"),
            ("Страхование жизни и здоровья", True, "контекстный"),
            ("Защита персональных данных", True, "контекстный"),
            ("Трудовые споры с работодателем", True, "контекстный"),
            ("Медицинская ответственность врачей", True, "контекстный"),
            ("Банковские услуги для бизнеса", True, "контекстный"),
            ("Как оформить наследство?", True, "контекстный"),
            ("Какие права у меня есть?", True, "контекстный"),
            ("Как защитить свои интересы?", True, "контекстный"),
            ("Что делать с долгами?", True, "контекстный"),
            
            # 6. Региональные вопросы
            ("Как работает мировой суд в Минске?", True, "региональный"),
            ("Особенности регистрации ИП в Гомеле", True, "региональный"),
            ("Налоговые льготы в ПВТ", True, "региональный"),
            ("Земельное законодательство в Брестской области", True, "региональный"),
            ("Жилищные вопросы в Витебске", True, "региональный"),
            ("Трудовое право в свободных экономических зонах", True, "региональный"),
            ("Права потребителей в интернет-магазинах РБ", True, "региональный"),
            ("Экологическое право в Гродненской области", True, "региональный"),
            
            # === НЕ ДОЛЖНЫ БЫТЬ ЮРИДИЧЕСКИМИ ===
            
            # 7. Технические ложные срабатывания
            ("Как работает суд присяжных в кино?", False, "техническое"),
            ("Права доступа к базе данных", False, "техническое"),
            ("Защита растений от вредителей", False, "техническое"),
            ("Договор с интернет-провайдером не работает", False, "техническое"),
            ("Налоговая декларация в Excel", False, "техническое"),
            ("Трудовой стаж в компьютерной игре", False, "техническое"),
            ("Права администратора в Windows", False, "техническое"),
            ("Наследование классов в программировании", False, "техническое"),
            ("Защита авторских прав в интернете", False, "техническое"),
            ("Юридическая фирма ищет программиста", False, "техническое"),
            
            # 8. Обычные неюридические вопросы
            ("Как приготовить борщ?", False, "обычное"),
            ("Какая погода завтра?", False, "обычное"),
            ("Как похудеть на 10 кг?", False, "обычное"),
            ("Где скачать фильм?", False, "обычное"),
            ("Как установить Windows?", False, "обычное"),
            ("Что посмотреть в кино?", False, "обычное"),
            ("Как готовить пиццу?", False, "обычное"),
            ("Где купить телефон?", False, "обычное"),
            ("Как изучить английский язык?", False, "обычное"),
            ("Что делать при простуде?", False, "обычное"),
            
            # 9. Контекстно-зависимые неюридические
            ("Как подать документы?", False, "контекстный_не_юр"),
            ("Что мне делать?", False, "контекстный_не_юр"),
            ("Куда обращаться за помощью?", False, "контекстный_не_юр"),
            ("Какие документы нужны?", False, "контекстный_не_юр"),
            ("Сколько это стоит?", False, "контекстный_не_юр"),
            ("Можно ли это сделать?", False, "контекстный_не_юр"),
        ]
    
    def run_comprehensive_test(self) -> Dict:
        """Запускает комплексное тестирование всех фильтров."""
        print("\n🔍 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ФИЛЬТРОВ")
        print("=" * 70)
        
        results = {
            "basic": {"correct": 0, "total": 0, "details": [], "by_category": {}},
            "improved": {"correct": 0, "total": 0, "details": [], "by_category": {}},
            "improvements": [],
            "regressions": []
        }
        
        # Инициализируем категории
        categories = set(category for _, _, category in self.test_cases)
        for category in categories:
            results["basic"]["by_category"][category] = {"correct": 0, "total": 0}
            results["improved"]["by_category"][category] = {"correct": 0, "total": 0}
        
        print(f"\n{'Вопрос':<50} {'Ожидается':<10} {'Базовый':<12} {'Улучшенный':<12} {'Результат'}")
        print("-" * 90)
        
        for question, expected, category in self.test_cases:
            # Тестируем базовый фильтр
            basic_is_legal, basic_score, basic_explanation = self.basic_filter.is_legal_question(question)
            basic_correct = basic_is_legal == expected
            
            # Тестируем улучшенный фильтр
            improved_is_legal, improved_score, improved_explanation = self.improved_filter.is_legal_question(question)
            improved_correct = improved_is_legal == expected
            
            # Обновляем общую статистику
            results["basic"]["total"] += 1
            results["improved"]["total"] += 1
            
            if basic_correct:
                results["basic"]["correct"] += 1
            if improved_correct:
                results["improved"]["correct"] += 1
            
            # Обновляем статистику по категориям
            results["basic"]["by_category"][category]["total"] += 1
            results["improved"]["by_category"][category]["total"] += 1
            
            if basic_correct:
                results["basic"]["by_category"][category]["correct"] += 1
            if improved_correct:
                results["improved"]["by_category"][category]["correct"] += 1
            
            # Записываем детали
            results["basic"]["details"].append({
                "question": question,
                "expected": expected,
                "predicted": basic_is_legal,
                "correct": basic_correct,
                "score": basic_score,
                "category": category
            })
            
            results["improved"]["details"].append({
                "question": question,
                "expected": expected,
                "predicted": improved_is_legal,
                "correct": improved_correct,
                "score": improved_score,
                "category": category
            })
            
            # Определяем результат
            if not basic_correct and improved_correct:
                result = "✅ УЛУЧШЕНО"
                results["improvements"].append(question)
            elif basic_correct and not improved_correct:
                result = "❌ УХУДШЕНО"
                results["regressions"].append(question)
            elif basic_correct and improved_correct:
                result = "✓ ОК"
            else:
                result = "❌ ОБА НЕВЕРНО"
            
            # Форматируем вывод
            expected_str = "ЮР" if expected else "НЕ ЮР"
            basic_str = f"{'ЮР' if basic_is_legal else 'НЕ ЮР'} ({basic_score:.2f})"
            improved_str = f"{'ЮР' if improved_is_legal else 'НЕ ЮР'} ({improved_score:.2f})"
            
            print(f"{question[:48]:<50} {expected_str:<10} {basic_str:<12} {improved_str:<12} {result}")
        
        return results
    
    def print_detailed_analysis(self, results: Dict):
        """Выводит детальный анализ результатов."""
        print("\n📊 ДЕТАЛЬНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ")
        print("=" * 70)
        
        # Общая статистика
        basic_accuracy = results["basic"]["correct"] / results["basic"]["total"] * 100
        improved_accuracy = results["improved"]["correct"] / results["improved"]["total"] * 100
        improvement = improved_accuracy - basic_accuracy
        
        print(f"\n🎯 ОБЩИЕ РЕЗУЛЬТАТЫ:")
        print(f"Базовый фильтр:      {basic_accuracy:.1f}% ({results['basic']['correct']}/{results['basic']['total']})")
        print(f"Улучшенный фильтр:   {improved_accuracy:.1f}% ({results['improved']['correct']}/{results['improved']['total']})")
        print(f"Улучшение:           {improvement:+.1f}%")
        print(f"Улучшенных случаев:  {len(results['improvements'])}")
        print(f"Ухудшенных случаев:  {len(results['regressions'])}")
        
        # Анализ по категориям
        print(f"\n📋 АНАЛИЗ ПО КАТЕГОРИЯМ:")
        print(f"{'Категория':<20} {'Базовый':<12} {'Улучшенный':<12} {'Изменение'}")
        print("-" * 60)
        
        for category in sorted(results["basic"]["by_category"].keys()):
            basic_cat = results["basic"]["by_category"][category]
            improved_cat = results["improved"]["by_category"][category]
            
            basic_acc = basic_cat["correct"] / basic_cat["total"] * 100 if basic_cat["total"] > 0 else 0
            improved_acc = improved_cat["correct"] / improved_cat["total"] * 100 if improved_cat["total"] > 0 else 0
            change = improved_acc - basic_acc
            
            print(f"{category:<20} {basic_acc:>6.1f}% ({basic_cat['correct']}/{basic_cat['total']}) "
                  f"{improved_acc:>6.1f}% ({improved_cat['correct']}/{improved_cat['total']}) "
                  f"{change:>+6.1f}%")
        
        # Лучшие улучшения
        if results["improvements"]:
            print(f"\n✅ ЛУЧШИЕ УЛУЧШЕНИЯ:")
            for i, question in enumerate(results["improvements"][:10], 1):
                print(f"  {i}. {question}")
        
        # Регрессии
        if results["regressions"]:
            print(f"\n❌ РЕГРЕССИИ (требуют внимания):")
            for i, question in enumerate(results["regressions"], 1):
                print(f"  {i}. {question}")
        
        # Анализ ошибок
        print(f"\n🔍 АНАЛИЗ ОСТАВШИХСЯ ОШИБОК:")
        
        improved_errors = [item for item in results["improved"]["details"] if not item["correct"]]
        error_categories = {}
        
        for error in improved_errors:
            category = error["category"]
            if category not in error_categories:
                error_categories[category] = []
            error_categories[category].append(error)
        
        for category, errors in sorted(error_categories.items()):
            print(f"\n  {category.upper()}: {len(errors)} ошибок")
            for error in errors[:3]:  # Показываем первые 3
                expected_str = "ЮР" if error["expected"] else "НЕ ЮР"
                predicted_str = "ЮР" if error["predicted"] else "НЕ ЮР"
                print(f"    • {error['question'][:60]}...")
                print(f"      Ожидалось: {expected_str}, Получено: {predicted_str} (балл: {error['score']:.3f})")
    
    def generate_recommendations(self, results: Dict) -> List[str]:
        """Генерирует рекомендации по дальнейшему улучшению."""
        print(f"\n💡 РЕКОМЕНДАЦИИ ПО ДАЛЬНЕЙШЕМУ УЛУЧШЕНИЮ:")
        print("=" * 70)
        
        recommendations = []
        
        # Анализируем категории с наибольшими ошибками
        improved_errors = [item for item in results["improved"]["details"] if not item["correct"]]
        error_by_category = {}
        
        for error in improved_errors:
            category = error["category"]
            if category not in error_by_category:
                error_by_category[category] = []
            error_by_category[category].append(error)
        
        # Сортируем категории по количеству ошибок
        sorted_categories = sorted(error_by_category.items(), key=lambda x: len(x[1]), reverse=True)
        
        for category, errors in sorted_categories[:5]:  # Топ-5 проблемных категорий
            error_count = len(errors)
            total_in_category = results["improved"]["by_category"][category]["total"]
            error_rate = error_count / total_in_category * 100
            
            print(f"\n🎯 {category.upper()}: {error_count} ошибок из {total_in_category} ({error_rate:.1f}%)")
            
            if category == "техническое":
                print("   • Усилить исключающие паттерны для технических терминов")
                print("   • Добавить контекстный анализ для разделения IT и юридических терминов")
                recommendations.append("Улучшить фильтрацию технических терминов")
                
            elif category == "специализированный":
                print("   • Расширить словарь специализированных юридических терминов")
                print("   • Добавить распознавание латинских юридических фраз")
                recommendations.append("Улучшить распознавание специализированных терминов")
                
            elif category == "контекстный":
                print("   • Улучшить контекстный анализ для неоднозначных случаев")
                print("   • Добавить анализ намерений пользователя")
                recommendations.append("Развить контекстно-зависимый анализ")
                
            elif category == "разговорный":
                print("   • Расширить словарь разговорных юридических выражений")
                print("   • Улучшить распознавание житейских правовых ситуаций")
                recommendations.append("Улучшить понимание разговорной речи")
        
        # Общие рекомендации
        improvement = (results["improved"]["correct"] / results["improved"]["total"] * 100) - \
                     (results["basic"]["correct"] / results["basic"]["total"] * 100)
        
        if improvement > 10:
            print(f"\n🎉 ОТЛИЧНЫЙ РЕЗУЛЬТАТ! Улучшение на {improvement:.1f}%")
            print("   • Рекомендуется внедрить улучшенный фильтр в продакшен")
            recommendations.append("Внедрить улучшенный фильтр")
        elif improvement > 5:
            print(f"\n✅ ХОРОШИЙ РЕЗУЛЬТАТ! Улучшение на {improvement:.1f}%")
            print("   • Можно использовать улучшенный фильтр после дополнительного тестирования")
            recommendations.append("Дополнительное тестирование перед внедрением")
        else:
            print(f"\n⚠️  НЕЗНАЧИТЕЛЬНОЕ УЛУЧШЕНИЕ: {improvement:.1f}%")
            print("   • Требуется дальнейшая работа над алгоритмом")
            recommendations.append("Дальнейшее улучшение алгоритма")
        
        return recommendations
    
    def run_final_comparison(self):
        """Запускает финальное сравнение всех фильтров."""
        print("🚀 ФИНАЛЬНОЕ СРАВНЕНИЕ ФИЛЬТРОВ")
        print("=" * 70)
        
        # Запускаем тестирование
        results = self.run_comprehensive_test()
        
        # Детальный анализ
        self.print_detailed_analysis(results)
        
        # Рекомендации
        recommendations = self.generate_recommendations(results)
        
        return results, recommendations

def main():
    """Главная функция финального сравнения."""
    try:
        comparison = FinalFilterComparison()
        results, recommendations = comparison.run_final_comparison()
        
        print("\n✅ ФИНАЛЬНОЕ СРАВНЕНИЕ ЗАВЕРШЕНО!")
        print("\n🎯 ИТОГОВЫЕ РЕКОМЕНДАЦИИ:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
    except Exception as e:
        print(f"❌ Ошибка при сравнении: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 