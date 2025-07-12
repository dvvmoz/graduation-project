#!/usr/bin/env python3
"""
Расширенный тест для выявления ограничений фильтров и тестирования сложных случаев.
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
from modules.legal_content_filter import LegalContentFilter
from typing import List, Dict, Tuple

class AdvancedFilterTester:
    """Расширенный тестер фильтров для выявления ограничений."""
    
    def __init__(self):
        """Инициализирует расширенный тестер."""
        self.question_filter = QuestionFilter()
        self.content_filter = LegalContentFilter()
        
        # Сложные тестовые случаи
        self.complex_test_cases = {
            "ambiguous_questions": [
                # Вопросы, которые могут быть как юридическими, так и нет
                "Как заработать на недвижимости?",  # Может быть инвестиционный вопрос ИЛИ налоговый
                "Что делать с долгами?",  # Может быть финансовый совет ИЛИ юридический
                "Как защитить свои интересы?",  # Очень общий вопрос
                "Права человека в интернете",  # Может быть техническая тема ИЛИ правовая
                "Как оформить наследство?",  # Должен быть юридическим
                "Страхование жизни и здоровья",  # Может быть коммерческая тема ИЛИ правовая
                "Банковские услуги для бизнеса",  # Может быть коммерческая тема ИЛИ правовая
                "Защита персональных данных",  # Может быть IT-тема ИЛИ правовая
                "Трудовые споры с работодателем",  # Должен быть юридическим
                "Медицинская ответственность врачей",  # Может быть медицинская тема ИЛИ правовая
            ],
            
            "context_dependent": [
                # Вопросы, где контекст определяет юридичность
                "Как подать документы?",  # Слишком общий - куда? какие?
                "Какие права у меня есть?",  # Слишком общий - в какой ситуации?
                "Что мне делать?",  # Совсем общий
                "Куда обращаться за помощью?",  # Зависит от типа помощи
                "Какие документы нужны?",  # Для чего?
                "Сколько это стоит?",  # Что именно?
                "Какие сроки?",  # Для чего?
                "Кто несет ответственность?",  # За что?
                "Можно ли это сделать?",  # Что именно?
                "Законно ли это?",  # Что именно?
            ],
            
            "specialized_legal": [
                # Специализированные юридические термины
                "Эстоппель в гражданском праве",
                "Субсидиарная ответственность учредителей",
                "Виндикационный иск против добросовестного приобретателя",
                "Негаторный иск в отношении недвижимости",
                "Реституция при недействительности сделки",
                "Цессия требования по договору подряда",
                "Новация долга в обязательственном праве",
                "Суброгация в страховом праве",
                "Деликтная ответственность за причинение вреда",
                "Виндикация бездокументарных ценных бумаг",
            ],
            
            "colloquial_legal": [
                # Разговорные формулировки юридических вопросов
                "Меня кинули с деньгами, что делать?",
                "Начальник не платит зарплату уже месяц",
                "Соседи шумят по ночам, как их утихомирить?",
                "Развожусь с мужем, он не дает денег на ребенка",
                "Купил телефон, а он сломался через неделю",
                "Меня уволили без предупреждения",
                "Банк списал деньги без моего согласия",
                "Врач сделал неправильную операцию",
                "Полиция задержала без причины",
                "Управляющая компания не делает ремонт",
            ],
            
            "false_positives": [
                # Вопросы, которые могут ошибочно считаться юридическими
                "Как работает суд присяжных в кино?",  # О кинематографе
                "Права доступа к базе данных",  # IT-термин
                "Защита растений от вредителей",  # Сельское хозяйство
                "Договор с интернет-провайдером не работает",  # Технические проблемы
                "Налоговая декларация в Excel",  # Технический вопрос
                "Трудовой стаж в компьютерной игре",  # Игровая механика
                "Права администратора в Windows",  # IT-права
                "Наследование классов в программировании",  # Программирование
                "Защита авторских прав в интернете",  # Может быть техническим
                "Юридическая фирма ищет программиста",  # Вакансия
            ],
            
            "multi_language": [
                # Вопросы с иностранными терминами
                "Что такое habeas corpus?",
                "Принцип pacta sunt servanda",
                "Доктрина res ipsa loquitur",
                "Правило de minimis non curat lex",
                "Принцип ultra vires в корпоративном праве",
                "Что означает pro bono в юриспруденции?",
                "Концепция force majeure в договорах",
                "Принцип caveat emptor при покупке",
                "Доктрина respondeat superior",
                "Правило nemo dat quod non habet",
            ],
            
            "regional_specific": [
                # Вопросы, специфичные для разных регионов
                "Как работает мировой суд в Минске?",
                "Особенности регистрации ИП в Гомеле",
                "Налоговые льготы в ПВТ",
                "Земельное законодательство в Брестской области",
                "Жилищные вопросы в Витебске",
                "Трудовое право в свободных экономических зонах",
                "Административное право в Могилеве",
                "Семейное право в сельской местности",
                "Права потребителей в интернет-магазинах РБ",
                "Экологическое право в Гродненской области",
            ]
        }
    
    def test_ambiguous_cases(self) -> Dict:
        """Тестирует неоднозначные случаи."""
        print("🔍 ТЕСТИРОВАНИЕ НЕОДНОЗНАЧНЫХ СЛУЧАЕВ")
        print("=" * 50)
        
        results = {}
        
        for category, questions in self.complex_test_cases.items():
            print(f"\n📋 {category.upper()}:")
            category_results = {"questions": [], "scores": [], "decisions": []}
            
            for question in questions:
                is_legal, score, explanation = self.question_filter.is_legal_question(question)
                category_results["questions"].append(question)
                category_results["scores"].append(score)
                category_results["decisions"].append(is_legal)
                
                status = "✅ ЮРИДИЧЕСКИЙ" if is_legal else "❌ НЕ ЮРИДИЧЕСКИЙ"
                confidence = "высокая" if score > 0.3 else "средняя" if score > 0.15 else "низкая"
                
                print(f"  {status} ({score:.3f}, {confidence}): {question}")
                if not is_legal and score > 0.05:
                    print(f"    Пограничный случай: {explanation}")
            
            results[category] = category_results
        
        return results
    
    def analyze_filter_gaps(self) -> Dict:
        """Анализирует пробелы в фильтрации."""
        print("\n🔍 АНАЛИЗ ПРОБЕЛОВ В ФИЛЬТРАЦИИ")
        print("=" * 50)
        
        gaps = {
            "missed_legal": [],      # Пропущенные юридические вопросы
            "false_positives": [],   # Ложные срабатывания
            "low_confidence": [],    # Низкая уверенность
            "ambiguous": []          # Неоднозначные случаи
        }
        
        # Анализируем каждую категорию
        for category, questions in self.complex_test_cases.items():
            for question in questions:
                is_legal, score, explanation = self.question_filter.is_legal_question(question)
                
                # Определяем, должен ли вопрос быть юридическим
                should_be_legal = self._should_be_legal(question, category)
                
                if should_be_legal and not is_legal:
                    gaps["missed_legal"].append({
                        "question": question,
                        "score": score,
                        "category": category,
                        "explanation": explanation
                    })
                elif not should_be_legal and is_legal:
                    gaps["false_positives"].append({
                        "question": question,
                        "score": score,
                        "category": category,
                        "explanation": explanation
                    })
                elif 0.05 <= score <= 0.15:
                    gaps["low_confidence"].append({
                        "question": question,
                        "score": score,
                        "category": category,
                        "is_legal": is_legal,
                        "explanation": explanation
                    })
                elif category == "ambiguous_questions":
                    gaps["ambiguous"].append({
                        "question": question,
                        "score": score,
                        "is_legal": is_legal,
                        "explanation": explanation
                    })
        
        # Выводим результаты анализа
        print("\n❌ ПРОПУЩЕННЫЕ ЮРИДИЧЕСКИЕ ВОПРОСЫ:")
        for item in gaps["missed_legal"]:
            print(f"  • {item['question']} (балл: {item['score']:.3f})")
            print(f"    Категория: {item['category']}")
            print(f"    Объяснение: {item['explanation']}")
        
        print("\n⚠️  ЛОЖНЫЕ СРАБАТЫВАНИЯ:")
        for item in gaps["false_positives"]:
            print(f"  • {item['question']} (балл: {item['score']:.3f})")
            print(f"    Категория: {item['category']}")
        
        print("\n🤔 НИЗКАЯ УВЕРЕННОСТЬ:")
        for item in gaps["low_confidence"]:
            status = "юридический" if item['is_legal'] else "не юридический"
            print(f"  • {item['question']} → {status} (балл: {item['score']:.3f})")
        
        print("\n🔄 НЕОДНОЗНАЧНЫЕ СЛУЧАИ:")
        for item in gaps["ambiguous"]:
            status = "юридический" if item['is_legal'] else "не юридический"
            print(f"  • {item['question']} → {status} (балл: {item['score']:.3f})")
        
        return gaps
    
    def _should_be_legal(self, question: str, category: str) -> bool:
        """Определяет, должен ли вопрос считаться юридическим."""
        # Эвристики для определения ожидаемого результата
        if category == "specialized_legal":
            return True
        elif category == "colloquial_legal":
            return True
        elif category == "false_positives":
            return False
        elif category == "regional_specific":
            return True
        elif category == "multi_language":
            return True
        elif category in ["ambiguous_questions", "context_dependent"]:
            # Для этих категорий анализируем содержание
            legal_indicators = [
                "наследство", "права", "ответственность", "трудовые", "споры",
                "документы", "защита", "данных", "банковские", "страхование"
            ]
            return any(indicator in question.lower() for indicator in legal_indicators)
        
        return False
    
    def suggest_improvements(self, gaps: Dict) -> List[str]:
        """Предлагает улучшения на основе анализа пробелов."""
        print("\n💡 ПРЕДЛОЖЕНИЯ ПО УЛУЧШЕНИЮ:")
        print("=" * 50)
        
        improvements = []
        
        # Анализируем пропущенные юридические вопросы
        if gaps["missed_legal"]:
            print("\n🔧 Для улучшения распознавания юридических вопросов:")
            
            # Собираем часто встречающиеся термины
            missed_terms = []
            for item in gaps["missed_legal"]:
                words = item["question"].lower().split()
                missed_terms.extend(words)
            
            # Находим самые частые термины
            from collections import Counter
            common_terms = Counter(missed_terms).most_common(10)
            
            print("  • Добавить ключевые слова:")
            for term, count in common_terms:
                if len(term) > 3 and term not in ['как', 'что', 'где', 'для', 'это', 'при']:
                    print(f"    - '{term}' (встречается {count} раз)")
                    improvements.append(f"Добавить ключевое слово: '{term}'")
        
        # Анализируем ложные срабатывания
        if gaps["false_positives"]:
            print("\n⚠️  Для уменьшения ложных срабатываний:")
            print("  • Добавить исключающие паттерны:")
            
            false_patterns = [
                "в кино", "в игре", "в программировании", "в Excel",
                "в Windows", "программист", "база данных", "интернет-провайдер"
            ]
            
            for pattern in false_patterns:
                if any(pattern in item["question"].lower() for item in gaps["false_positives"]):
                    print(f"    - Исключить: '{pattern}'")
                    improvements.append(f"Добавить исключающий паттерн: '{pattern}'")
        
        # Анализируем случаи с низкой уверенностью
        if gaps["low_confidence"]:
            print("\n🎯 Для повышения уверенности:")
            print("  • Улучшить контекстный анализ")
            print("  • Добавить семантические правила")
            print("  • Использовать комбинации ключевых слов")
            improvements.extend([
                "Улучшить контекстный анализ",
                "Добавить семантические правила",
                "Использовать комбинации ключевых слов"
            ])
        
        return improvements
    
    def run_advanced_analysis(self):
        """Запускает полный расширенный анализ."""
        print("🚀 РАСШИРЕННЫЙ АНАЛИЗ ФИЛЬТРОВ")
        print("=" * 60)
        
        # Тестируем сложные случаи
        complex_results = self.test_ambiguous_cases()
        
        # Анализируем пробелы
        gaps = self.analyze_filter_gaps()
        
        # Предлагаем улучшения
        improvements = self.suggest_improvements(gaps)
        
        # Сводка
        print("\n📊 СВОДКА РАСШИРЕННОГО АНАЛИЗА:")
        print("=" * 50)
        
        total_questions = sum(len(questions) for questions in self.complex_test_cases.values())
        missed_count = len(gaps["missed_legal"])
        false_positive_count = len(gaps["false_positives"])
        low_confidence_count = len(gaps["low_confidence"])
        
        print(f"Всего протестировано вопросов: {total_questions}")
        print(f"Пропущено юридических: {missed_count}")
        print(f"Ложных срабатываний: {false_positive_count}")
        print(f"Низкая уверенность: {low_confidence_count}")
        print(f"Предложено улучшений: {len(improvements)}")
        
        accuracy = (total_questions - missed_count - false_positive_count) / total_questions * 100
        print(f"\nТочность на сложных случаях: {accuracy:.1f}%")
        
        return {
            "complex_results": complex_results,
            "gaps": gaps,
            "improvements": improvements,
            "accuracy": accuracy
        }

def main():
    """Главная функция расширенного тестирования."""
    try:
        tester = AdvancedFilterTester()
        results = tester.run_advanced_analysis()
        
        print("\n✅ РАСШИРЕННЫЙ АНАЛИЗ ЗАВЕРШЕН!")
        
    except Exception as e:
        print(f"❌ Ошибка при расширенном анализе: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 