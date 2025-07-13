#!/usr/bin/env python3
"""
Тест улучшенного ML-фильтра для проверки классификации коротких юридических вопросов.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from modules.ml_question_filter import is_legal_question_ml

def test_ml_filter():
    """Тестирует ML-фильтр на различных типах вопросов."""
    
    print("🔍 Тестирование улучшенного ML-фильтра...")
    print("=" * 60)
    
    # Тестовые вопросы
    test_cases = [
        # Короткие юридические вопросы (должны пройти)
        ("открытие ип", True, "Основная проблема"),
        ("регистрация ип", True, "Вариант основной проблемы"),
        ("как открыть ип", True, "Расширенный вариант"),
        ("документы для ип", True, "Связанный вопрос"),
        ("налоги ип", True, "Другой аспект ИП"),
        ("развод документы", True, "Другая тема"),
        ("трудовой договор", True, "Трудовое право"),
        ("штраф гаи", True, "Административное право"),
        ("алименты размер", True, "Семейное право"),
        ("жалоба в суд", True, "Процессуальное право"),
        
        # Короткие неюридические вопросы (должны не пройти)
        ("приготовить еду", False, "Бытовой вопрос"),
        ("купить телефон", False, "Покупка товара"),
        ("погода завтра", False, "Прогноз погоды"),
        ("установить игру", False, "IT вопрос"),
        ("изучить язык", False, "Образование"),
        
        # Длинные юридические вопросы (должны пройти)
        ("Как подать иск в суд в Беларуси?", True, "Длинный юридический"),
        ("Какие документы нужны для развода в РБ?", True, "Длинный юридический"),
        
        # Длинные неюридические вопросы (должны не пройти)
        ("Как приготовить вкусный борщ с мясом?", False, "Длинный неюридический"),
        ("Где можно скачать хорошие фильмы?", False, "Длинный неюридический"),
    ]
    
    correct_predictions = 0
    total_predictions = 0
    
    for question, expected, description in test_cases:
        is_legal, confidence, explanation = is_legal_question_ml(question)
        
        # Проверяем правильность предсказания
        is_correct = is_legal == expected
        if is_correct:
            correct_predictions += 1
        total_predictions += 1
        
        # Форматируем результат
        status = "✅ ВЕРНО" if is_correct else "❌ ОШИБКА"
        expected_text = "ДА" if expected else "НЕТ"
        actual_text = "ДА" if is_legal else "НЕТ"
        
        print(f"{status} | {question:25} | Ожидалось: {expected_text:3} | Получено: {actual_text:3} | Уверенность: {confidence:.3f}")
        print(f"        Описание: {description}")
        print(f"        Объяснение: {explanation}")
        print()
    
    # Итоговая статистика
    accuracy = correct_predictions / total_predictions
    print("=" * 60)
    print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"   Правильных предсказаний: {correct_predictions}/{total_predictions}")
    print(f"   Точность: {accuracy:.1%}")
    print()
    
    if accuracy >= 0.8:
        print("🎉 ОТЛИЧНО! Фильтр работает хорошо!")
    elif accuracy >= 0.6:
        print("⚠️  СРЕДНЕ. Фильтр нуждается в улучшении.")
    else:
        print("❌ ПЛОХО. Фильтр работает неудовлетворительно.")
    
    return accuracy

if __name__ == "__main__":
    test_ml_filter() 