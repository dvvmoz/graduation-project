# 📊 Варианты системы аналитики для дообучения ML-фильтра

## 🎯 Цель
Создать систему сбора, анализа и использования данных о вопросах пользователей для улучшения точности ML-фильтра юридических вопросов.

## 🔧 Варианты реализации

### **Вариант 1: SQLite база данных** ⭐ (Рекомендуемый)

**Файлы:**
- `modules/user_analytics.py` - основной модуль аналитики
- `modules/ml_analytics_integration.py` - интеграция с существующей системой

**Преимущества:**
- ✅ Структурированное хранение данных
- ✅ SQL-запросы для сложной аналитики
- ✅ ACID-транзакции
- ✅ Компактность и производительность
- ✅ Встроенные индексы для быстрого поиска
- ✅ Возможность экспорта в CSV/JSON

**Структура данных:**
```sql
-- Принятые вопросы
user_questions: id, user_id, question_text, ml_confidence, search_quality, source_type, etc.

-- Отклоненные вопросы  
rejected_questions: id, user_id, question_text, ml_confidence, manual_review, etc.

-- Статистика производительности
ml_performance: date, total_questions, accuracy_estimate, false_positives, etc.
```

**Применение:**
```python
from modules.ml_analytics_integration import create_question_context, finalize_question_context

# В bot_handler.py
context = create_question_context(user_id, question_text, ml_result)
# ... обработка вопроса ...
finalize_question_context(context, response_text)
```

---

### **Вариант 2: JSON файлы по дням**

**Структура:**
```
analytics/
  2024-07-13.json    # Данные за день
  2024-07-14.json
  summary.json       # Агрегированная статистика
```

**Преимущества:**
- ✅ Простота реализации
- ✅ Человекочитаемый формат
- ✅ Легкий бэкап и перенос
- ✅ Возможность ручного редактирования

**Недостатки:**
- ❌ Медленные запросы по большим объемам
- ❌ Нет встроенной индексации
- ❌ Сложность агрегации данных

---

### **Вариант 3: CSV файлы + pandas**

**Структура:**
```
analytics/
  questions_log.csv      # Основной лог
  rejected_log.csv       # Отклоненные вопросы
  daily_stats.csv        # Дневная статистика
```

**Преимущества:**
- ✅ Совместимость с Excel
- ✅ Мощные возможности pandas для анализа
- ✅ Простота экспорта и импорта
- ✅ Визуализация через matplotlib/seaborn

**Применение:**
```python
import pandas as pd

# Анализ данных
df = pd.read_csv('analytics/questions_log.csv')
accuracy = df.groupby('date')['ml_confidence'].mean()
```

---

### **Вариант 4: ChromaDB интеграция**

**Преимущества:**
- ✅ Использование существующей инфраструктуры
- ✅ Векторный поиск по похожим вопросам
- ✅ Автоматическое embedding'и
- ✅ Единая база для документов и аналитики

**Применение:**
```python
# Добавляем вопросы как документы с метаданными
collection.add(
    documents=[question_text],
    metadatas=[{'ml_confidence': 0.85, 'category': 'tax_law'}],
    ids=[f"question_{timestamp}"]
)
```

---

### **Вариант 5: Гибридный подход** 🚀 (Максимальный функционал)

**Сочетает:**
- SQLite для структурированной аналитики
- ChromaDB для семантического поиска
- CSV экспорт для внешнего анализа
- JSON для конфигурации и кеширования

## 📈 Методы анализа и дообучения

### 1. **Автоматическое дообучение**

```python
def retrain_ml_filter():
    """Автоматическое дообучение ML-фильтра."""
    
    # 1. Экспорт данных с высокой уверенностью
    analytics.export_training_data(min_confidence=0.8)
    
    # 2. Объединение с существующими данными
    combine_training_datasets()
    
    # 3. Переобучение модели
    retrain_model('legal_question_classifier.pkl')
    
    # 4. Валидация на тестовой выборке
    validate_model_performance()
```

### 2. **Выявление проблемных паттернов**

```python
def analyze_problem_patterns():
    """Анализ паттернов ошибок ML-фильтра."""
    
    # Вопросы с низкой уверенностью
    low_confidence = analytics.get_low_confidence_questions(threshold=0.7)
    
    # Часто отклоняемые категории
    rejected_categories = analytics.get_rejected_categories_stats()
    
    # Временные паттерны ошибок
    time_patterns = analytics.get_temporal_error_patterns()
    
    return {
        'needs_manual_review': low_confidence,
        'problem_categories': rejected_categories,
        'time_patterns': time_patterns
    }
```

### 3. **A/B тестирование**

```python
def ab_test_ml_models():
    """A/B тестирование разных версий ML-модели."""
    
    # Случайное разделение пользователей
    if user_id % 2 == 0:
        use_model_version("v1.0")
    else:
        use_model_version("v1.1_experimental")
    
    # Сравнение метрик
    compare_model_performance()
```

## 🔄 Интеграция с существующей системой

### Модификация `bot_handler.py`:

```python
# Добавляем импорты
from .ml_analytics_integration import (
    create_question_context, 
    update_search_context, 
    finalize_question_context
)

async def handle_question(self, message: Message):
    user_question = message.text
    user_id = message.from_user.id
    
    # Проверяем ML-фильтр
    is_legal, score, explanation = is_legal_question(user_question)
    
    # 📊 СОЗДАЕМ КОНТЕКСТ АНАЛИТИКИ
    analytics_context = create_question_context(
        user_id, user_question, (is_legal, score, explanation)
    )
    
    if not is_legal:
        # 📊 ФИНАЛИЗИРУЕМ БЕЗ ПОИСКА
        finalize_question_context(analytics_context, 
                                error="question_rejected_by_ml_filter")
        await message.answer(get_rejection_message())
        return
    
    try:
        # Поиск в базе знаний
        relevant_docs = search_relevant_docs(user_question)
        best_distance = min(doc['distance'] for doc in relevant_docs) if relevant_docs else None
        
        # 📊 ОБНОВЛЯЕМ КОНТЕКСТ ПОИСКА
        analytics_context = update_search_context(
            analytics_context, relevant_docs, best_distance, "knowledge_base"
        )
        
        # Генерация ответа
        answer = get_answer(user_question, relevant_docs)
        await message.answer(answer)
        
        # 📊 ФИНАЛИЗИРУЕМ С УСПЕШНЫМ ОТВЕТОМ
        finalize_question_context(analytics_context, answer)
        
    except Exception as e:
        # 📊 ФИНАЛИЗИРУЕМ С ОШИБКОЙ
        finalize_question_context(analytics_context, error=str(e))
        await message.answer("Произошла ошибка...")
```

## 📊 Примеры аналитических отчетов

### 1. **Дневная сводка**
```python
daily_stats = analytics.get_analytics_summary(days=1)
# {
#   'total_questions': 150,
#   'avg_confidence': 0.847,
#   'dynamic_searches': 23,
#   'top_categories': [
#     {'category': 'налоги', 'count': 45},
#     {'category': 'трудовые_отношения', 'count': 38}
#   ]
# }
```

### 2. **Проблемные вопросы**
```python
problems = analytics.get_low_confidence_questions(threshold=0.6)
# [
#   {'question': 'можно ли...', 'confidence': 0.58, 'needs_review': True},
#   {'question': 'как получить...', 'confidence': 0.62, 'category': 'unclear'}
# ]
```

### 3. **Экспорт для дообучения**
```python
# Экспорт качественных данных для переобучения
analytics.export_training_data(
    output_file='training_data_2024_07.csv',
    min_confidence=0.85
)
```

## 🚀 Рекомендации по внедрению

### **Этап 1: Базовый сбор данных**
1. Интегрировать SQLite аналитику
2. Модифицировать `bot_handler.py`
3. Запустить сбор данных на 1-2 недели

### **Этап 2: Анализ и улучшения**
1. Проанализировать первые результаты
2. Выявить проблемные паттерны
3. Создать датасет для дообучения

### **Этап 3: Автоматизация**
1. Настроить автоматическое дообучение
2. Внедрить мониторинг метрик
3. Добавить A/B тестирование

### **Этап 4: Расширенная аналитика**
1. Интеграция с ChromaDB
2. Семантический анализ вопросов
3. Предиктивная аналитика

## 📋 Чек-лист внедрения

- [ ] Создать базу данных аналитики
- [ ] Интегрировать с `bot_handler.py`
- [ ] Настроить логирование
- [ ] Проверить сбор данных
- [ ] Создать административную панель
- [ ] Настроить экспорт данных
- [ ] Запланировать первое дообучение

**Время внедрения:** 2-3 дня для базовой версии, 1-2 недели для полной функциональности.

**Результат:** Самообучающаяся система с улучшающейся точностью ML-фильтра на основе реальных данных пользователей! 🎉 