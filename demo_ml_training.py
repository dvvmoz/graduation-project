#!/usr/bin/env python3
"""
Демонстрация работы ML-фильтра: обучение и использование
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ml_question_filter import MLQuestionFilter
import logging

# Настройка логирования для демонстрации
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_ml_training():
    """Демонстрация процесса обучения ML-фильтра."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ML-ФИЛЬТРА")
    print("=" * 60)
    
    print("\n1. ИНИЦИАЛИЗАЦИЯ ML-ФИЛЬТРА")
    print("-" * 40)
    
    # Создаем новый экземпляр фильтра
    # При первом запуске произойдет автоматическое обучение
    ml_filter = MLQuestionFilter()
    
    print("\n2. АНАЛИЗ ОБУЧАЮЩИХ ДАННЫХ")
    print("-" * 40)
    
    training_data = ml_filter._get_training_data()
    
    # Подсчитываем статистику
    legal_count = sum(1 for example in training_data if example.is_legal)
    non_legal_count = len(training_data) - legal_count
    
    categories = {}
    for example in training_data:
        category = example.category
        if category not in categories:
            categories[category] = {'legal': 0, 'non_legal': 0}
        
        if example.is_legal:
            categories[category]['legal'] += 1
        else:
            categories[category]['non_legal'] += 1
    
    print(f"Всего примеров: {len(training_data)}")
    print(f"Юридических: {legal_count}")
    print(f"Неюридических: {non_legal_count}")
    print(f"Категорий: {len(categories)}")
    
    print("\nРаспределение по категориям:")
    for category, counts in categories.items():
        total = counts['legal'] + counts['non_legal']
        print(f"  {category}: {total} примеров ({counts['legal']} юр, {counts['non_legal']} не юр)")
    
    print("\n3. ПРИМЕРЫ ОБУЧАЮЩИХ ДАННЫХ")
    print("-" * 40)
    
    # Показываем несколько примеров из каждой категории
    shown_categories = set()
    for example in training_data:
        if example.category not in shown_categories:
            status = "ЮР" if example.is_legal else "НЕ ЮР"
            print(f"[{example.category}] {status}: {example.question}")
            shown_categories.add(example.category)
            
            if len(shown_categories) >= 6:  # Показываем первые 6 категорий
                break
    
    print("\n4. ДЕМОНСТРАЦИЯ ИЗВЛЕЧЕНИЯ ПРИЗНАКОВ")
    print("-" * 40)
    
    test_question = "Меня кинули с деньгами, что делать?"
    features = ml_filter._extract_features(test_question)
    
    print(f"Вопрос: {test_question}")
    print("Извлеченные признаки:")
    for feature_name, value in features.items():
        print(f"  {feature_name}: {value}")
    
    print("\n5. ТЕСТИРОВАНИЕ ФИЛЬТРА")
    print("-" * 40)
    
    test_cases = [
        "Как подать иск в суд?",
        "Меня обманули при покупке",
        "Эстоппель в гражданском праве",
        "Как приготовить борщ?",
        "Права доступа к базе данных"
    ]
    
    print("Тестовые вопросы:")
    for question in test_cases:
        is_legal, confidence, explanation = ml_filter.is_legal_question(question)
        result = "ЮР" if is_legal else "НЕ ЮР"
        print(f"  {question[:40]:<40} -> {result} (уверенность: {confidence:.3f})")
    
    print("\n6. ИНФОРМАЦИЯ О МОДЕЛИ")
    print("-" * 40)
    
    print(f"Модель обучена: {ml_filter.is_trained}")
    print(f"Путь к модели: {ml_filter.model_path}")
    print(f"Файл модели существует: {os.path.exists(ml_filter.model_path)}")
    
    if ml_filter.vectorizer:
        print(f"Размер словаря TF-IDF: {len(ml_filter.vectorizer.vocabulary_)}")
        print(f"Максимум признаков: {ml_filter.vectorizer.max_features}")
    
    print("\n7. СОХРАНЕНИЕ И ЗАГРУЗКА МОДЕЛИ")
    print("-" * 40)
    
    # Демонстрируем сохранение модели
    if ml_filter.is_trained:
        print("Модель автоматически сохранена при обучении")
        
        # Создаем новый экземпляр для демонстрации загрузки
        print("Создаем новый экземпляр фильтра...")
        new_filter = MLQuestionFilter()
        
        if new_filter.is_trained:
            print("Модель успешно загружена из файла!")
            
            # Тестируем загруженную модель
            test_question = "Трудовые права работника"
            is_legal, confidence, explanation = new_filter.is_legal_question(test_question)
            result = "ЮР" if is_legal else "НЕ ЮР"
            print(f"Тест загруженной модели: '{test_question}' -> {result} ({confidence:.3f})")
        else:
            print("Ошибка загрузки модели")
    
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)

def main():
    """Основная функция."""
    try:
        demo_ml_training()
    except Exception as e:
        print(f"Ошибка демонстрации: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 