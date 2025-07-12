#!/usr/bin/env python3
"""
Сравнение базового и продвинутого фильтров вопросов.
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
from modules.advanced_question_filter import AdvancedQuestionFilter
from typing import List, Dict, Tuple

class FilterComparison:
    """Класс для сравнения базового и продвинутого фильтров."""
    
    def __init__(self):
        """Инициализирует сравнение фильтров."""
        self.basic_filter = QuestionFilter()
        self.advanced_filter = AdvancedQuestionFilter()
        
        # Тестовые случаи из расширенного анализа
        self.test_cases = [
            # Пропущенные юридические вопросы (должны быть юридическими)
            ("Права человека в интернете", True),
            ("Страхование жизни и здоровья", True),
            ("Защита персональных данных", True),
            ("Трудовые споры с работодателем", True),
            ("Меня кинули с деньгами, что делать?", True),
            ("Начальник не платит зарплату уже месяц", True),
            ("Соседи шумят по ночам, как их утихомирить?", True),
            ("Развожусь с мужем, он не дает денег на ребенка", True),
            ("Купил телефон, а он сломался через неделю", True),
            ("Меня уволили без предупреждения", True),
            ("Банк списал деньги без моего согласия", True),
            ("Врач сделал неправильную операцию", True),
            ("Полиция задержала без причины", True),
            ("Эстоппель в гражданском праве", True),
            ("Субсидиарная ответственность учредителей", True),
            ("Виндикационный иск против добросовестного приобретателя", True),
            ("Негаторный иск в отношении недвижимости", True),
            ("Реституция при недействительности сделки", True),
            ("Что такое habeas corpus?", True),
            ("Принцип pacta sunt servanda", True),
            ("Доктрина res ipsa loquitur", True),
            ("Принцип ultra vires в корпоративном праве", True),
            ("Что означает pro bono в юриспруденции?", True),
            ("Концепция force majeure в договорах", True),
            ("Принцип caveat emptor при покупке", True),
            
            # Ложные срабатывания (НЕ должны быть юридическими)
            ("Как работает суд присяжных в кино?", False),
            ("Права доступа к базе данных", False),
            ("Защита растений от вредителей", False),
            ("Договор с интернет-провайдером не работает", False),
            ("Налоговая декларация в Excel", False),
            ("Трудовой стаж в компьютерной игре", False),
            ("Права администратора в Windows", False),
            ("Наследование классов в программировании", False),
            ("Юридическая фирма ищет программиста", False),
            
            # Стандартные юридические вопросы (должны быть юридическими)
            ("Как подать иск в суд в Беларуси?", True),
            ("Какие документы нужны для развода в РБ?", True),
            ("Как оформить трудовой договор по ТК РБ?", True),
            ("Какие права у потребителя в Беларуси?", True),
            ("Как обжаловать решение административного органа?", True),
            
            # Неюридические вопросы (НЕ должны быть юридическими)
            ("Как приготовить борщ?", False),
            ("Какая погода завтра?", False),
            ("Как похудеть на 10 кг?", False),
            ("Где скачать фильм?", False),
            ("Как установить Windows?", False),
        ]
    
    def compare_filters(self) -> Dict:
        """Сравнивает производительность базового и продвинутого фильтров."""
        print("🔍 СРАВНЕНИЕ БАЗОВОГО И ПРОДВИНУТОГО ФИЛЬТРОВ")
        print("=" * 60)
        
        results = {
            "basic": {"correct": 0, "total": 0, "details": []},
            "advanced": {"correct": 0, "total": 0, "details": []},
            "improvements": []
        }
        
        print(f"\n{'Вопрос':<50} {'Ожидается':<12} {'Базовый':<15} {'Продвинутый':<15} {'Улучшение'}")
        print("-" * 100)
        
        for question, expected in self.test_cases:
            # Тестируем базовый фильтр
            basic_is_legal, basic_score, basic_explanation = self.basic_filter.is_legal_question(question)
            basic_correct = basic_is_legal == expected
            
            # Тестируем продвинутый фильтр
            advanced_is_legal, advanced_score, advanced_explanation = self.advanced_filter.is_legal_question(question)
            advanced_correct = advanced_is_legal == expected
            
            # Обновляем статистику
            results["basic"]["total"] += 1
            results["advanced"]["total"] += 1
            
            if basic_correct:
                results["basic"]["correct"] += 1
            if advanced_correct:
                results["advanced"]["correct"] += 1
            
            # Записываем детали
            results["basic"]["details"].append({
                "question": question,
                "expected": expected,
                "predicted": basic_is_legal,
                "correct": basic_correct,
                "score": basic_score,
                "explanation": basic_explanation
            })
            
            results["advanced"]["details"].append({
                "question": question,
                "expected": expected,
                "predicted": advanced_is_legal,
                "correct": advanced_correct,
                "score": advanced_score,
                "explanation": advanced_explanation
            })
            
            # Отмечаем улучшения
            improved = ""
            if not basic_correct and advanced_correct:
                improved = "✅ УЛУЧШЕНО"
                results["improvements"].append(question)
            elif basic_correct and not advanced_correct:
                improved = "❌ УХУДШЕНО"
            elif basic_correct and advanced_correct:
                improved = "✓ ОК"
            else:
                improved = "❌ ОБА НЕВЕРНО"
            
            # Форматируем вывод
            expected_str = "ЮР" if expected else "НЕ ЮР"
            basic_str = f"{'ЮР' if basic_is_legal else 'НЕ ЮР'} ({basic_score:.3f})"
            advanced_str = f"{'ЮР' if advanced_is_legal else 'НЕ ЮР'} ({advanced_score:.3f})"
            
            print(f"{question[:48]:<50} {expected_str:<12} {basic_str:<15} {advanced_str:<15} {improved}")
        
        return results
    
    def print_summary(self, results: Dict):
        """Выводит сводку сравнения."""
        print("\n📊 СВОДКА СРАВНЕНИЯ")
        print("=" * 50)
        
        basic_accuracy = results["basic"]["correct"] / results["basic"]["total"] * 100
        advanced_accuracy = results["advanced"]["correct"] / results["advanced"]["total"] * 100
        improvement = advanced_accuracy - basic_accuracy
        
        print(f"Базовый фильтр:")
        print(f"  Точность: {basic_accuracy:.1f}% ({results['basic']['correct']}/{results['basic']['total']})")
        
        print(f"\nПродвинутый фильтр:")
        print(f"  Точность: {advanced_accuracy:.1f}% ({results['advanced']['correct']}/{results['advanced']['total']})")
        
        print(f"\nУлучшение: {improvement:+.1f}%")
        print(f"Количество улучшенных случаев: {len(results['improvements'])}")
        
        if results["improvements"]:
            print("\n✅ УЛУЧШЕННЫЕ СЛУЧАИ:")
            for question in results["improvements"]:
                print(f"  • {question}")
        
        # Анализ ошибок
        print("\n🔍 АНАЛИЗ ОШИБОК:")
        
        basic_errors = [item for item in results["basic"]["details"] if not item["correct"]]
        advanced_errors = [item for item in results["advanced"]["details"] if not item["correct"]]
        
        print(f"\nОшибки базового фильтра: {len(basic_errors)}")
        for error in basic_errors[:5]:  # Показываем первые 5
            print(f"  • {error['question'][:50]}... (ожидалось: {'ЮР' if error['expected'] else 'НЕ ЮР'}, получено: {'ЮР' if error['predicted'] else 'НЕ ЮР'})")
        
        print(f"\nОшибки продвинутого фильтра: {len(advanced_errors)}")
        for error in advanced_errors[:5]:  # Показываем первые 5
            print(f"  • {error['question'][:50]}... (ожидалось: {'ЮР' if error['expected'] else 'НЕ ЮР'}, получено: {'ЮР' if error['predicted'] else 'НЕ ЮР'})")
    
    def analyze_score_distribution(self, results: Dict):
        """Анализирует распределение баллов."""
        print("\n📈 АНАЛИЗ РАСПРЕДЕЛЕНИЯ БАЛЛОВ")
        print("=" * 50)
        
        basic_scores = [item["score"] for item in results["basic"]["details"]]
        advanced_scores = [item["score"] for item in results["advanced"]["details"]]
        
        print(f"Базовый фильтр:")
        print(f"  Средний балл: {sum(basic_scores) / len(basic_scores):.3f}")
        print(f"  Минимальный: {min(basic_scores):.3f}")
        print(f"  Максимальный: {max(basic_scores):.3f}")
        
        print(f"\nПродвинутый фильтр:")
        print(f"  Средний балл: {sum(advanced_scores) / len(advanced_scores):.3f}")
        print(f"  Минимальный: {min(advanced_scores):.3f}")
        print(f"  Максимальный: {max(advanced_scores):.3f}")
        
        # Анализ по категориям
        legal_questions = [item for item in results["advanced"]["details"] if item["expected"]]
        non_legal_questions = [item for item in results["advanced"]["details"] if not item["expected"]]
        
        if legal_questions:
            legal_scores = [item["score"] for item in legal_questions]
            print(f"\nЮридические вопросы (продвинутый):")
            print(f"  Средний балл: {sum(legal_scores) / len(legal_scores):.3f}")
            print(f"  Распознано: {sum(1 for item in legal_questions if item['predicted'])}/{len(legal_questions)}")
        
        if non_legal_questions:
            non_legal_scores = [item["score"] for item in non_legal_questions]
            print(f"\nНеюридические вопросы (продвинутый):")
            print(f"  Средний балл: {sum(non_legal_scores) / len(non_legal_scores):.3f}")
            print(f"  Правильно отклонено: {sum(1 for item in non_legal_questions if not item['predicted'])}/{len(non_legal_questions)}")
    
    def run_comparison(self):
        """Запускает полное сравнение фильтров."""
        print("🚀 ПОЛНОЕ СРАВНЕНИЕ ФИЛЬТРОВ")
        print("=" * 60)
        
        # Сравниваем фильтры
        results = self.compare_filters()
        
        # Выводим сводку
        self.print_summary(results)
        
        # Анализируем распределение баллов
        self.analyze_score_distribution(results)
        
        return results

def main():
    """Главная функция сравнения."""
    try:
        comparison = FilterComparison()
        results = comparison.run_comparison()
        
        print("\n✅ СРАВНЕНИЕ ЗАВЕРШЕНО!")
        
        # Рекомендации
        basic_accuracy = results["basic"]["correct"] / results["basic"]["total"] * 100
        advanced_accuracy = results["advanced"]["correct"] / results["advanced"]["total"] * 100
        
        if advanced_accuracy > basic_accuracy:
            print(f"\n🎯 РЕКОМЕНДАЦИЯ: Использовать продвинутый фильтр")
            print(f"   Улучшение точности: {advanced_accuracy - basic_accuracy:+.1f}%")
        else:
            print(f"\n⚠️  ВНИМАНИЕ: Продвинутый фильтр не показал улучшений")
        
    except Exception as e:
        print(f"❌ Ошибка при сравнении: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 