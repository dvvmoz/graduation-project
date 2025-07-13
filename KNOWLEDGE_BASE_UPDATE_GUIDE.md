# Руководство по обновлению базы знаний

## Обзор системы

База знаний построена на **ChromaDB** - векторной базе данных для семантического поиска документов. Система автоматически создает эмбеддинги для документов и позволяет быстро находить релевантную информацию.

### Структура базы знаний

- **Путь к базе:** `db/chroma_db/` (согласно `config.py`)
- **Коллекция:** `legal_docs` (по умолчанию)
- **Тип поиска:** Косинусное сходство векторов
- **Формат данных:** Текстовые блоки с метаданными

### Источники данных

1. **Документы:** `data/documents/` - PDF, DOCX, DOC файлы
2. **Веб-скрапинг:** Сайты из `data/legal_sites.txt`
3. **Ручное добавление:** Через API или скрипты

## Способы обновления базы знаний

### 1. Обновление из документов

#### Добавление новых документов
```bash
# Поместите документы в папку data/documents/
# Затем запустите скрипт для их обработки
python scripts/populate_db.py
```

#### Обновление существующих документов
```bash
# Обновление всех документов в папке
python scripts/update_documents.py

# Обновление конкретного документа
python scripts/update_documents.py --file "data/documents/Налоговый кодекс.pdf"
```

#### Поддерживаемые форматы
- **PDF** (`.pdf`)
- **Word** (`.docx`, `.doc`)
- **Текст** (`.txt`) - планируется

### 2. Обновление через веб-скрапинг

#### Скрапинг всех сайтов
```bash
python scripts/scrape_websites.py
```

#### Скрапинг конкретного сайта
```bash
python scripts/scrape_websites.py --url "https://pravo.by/"
```

#### Настройка списка сайтов
Отредактируйте файл `data/legal_sites.txt`:
```
# Добавьте новые сайты
https://example.com/
https://newsite.by/
```

### 3. Программное обновление

#### Через API базы знаний
```python
from modules.knowledge_base import get_knowledge_base

# Получить инстанс базы знаний
kb = get_knowledge_base()

# Добавить документ
kb.add_document(
    doc_id="unique_id_001",
    document_text="Текст документа...",
    metadata={
        "source": "manual",
        "category": "налоги",
        "date": "2024-01-01"
    }
)

# Проверить существование
exists = kb.document_exists("unique_id_001")

# Получить статистику
stats = kb.get_collection_stats()
print(f"Всего документов: {stats['total_documents']}")
```

#### Через административную панель
```bash
# Запуск админ-панели
python admin_panel.py

# Или через батч-файл
start_admin_panel.bat
```

## Проверка состояния базы знаний

### Получение статистики
```python
from modules.knowledge_base import get_knowledge_base

kb = get_knowledge_base()
stats = kb.get_collection_stats()

print(f"База данных: {stats['db_path']}")
print(f"Коллекция: {stats['collection_name']}")
print(f"Документов: {stats['total_documents']}")
```

### Тестирование поиска
```python
# Тест поиска
results = kb.search_relevant_docs("регистрация ИП", n_results=3)
for doc in results:
    print(f"Источник: {doc['metadata'].get('source_file', 'неизвестен')}")
    print(f"Дистанция: {doc['distance']:.3f}")
    print(f"Текст: {doc['content'][:100]}...")
```

### Проверка качества результатов
```python
# Проверка необходимости динамического поиска
should_search, docs = kb.should_use_dynamic_search("как оплатить налоги")
if should_search:
    print("Качество результатов низкое - нужен поиск на pravo.by")
else:
    print("Найдены релевантные документы в базе знаний")
```

## Мониторинг и обслуживание

### Регулярное обновление

#### Еженедельное обновление документов
```bash
# Создайте bat-файл для автоматизации
@echo off
echo Обновление базы знаний...
cd /d "F:\graduation project"
python scripts/update_documents.py
python scripts/scrape_websites.py
echo Обновление завершено!
pause
```

#### Ежемесячное полное обновление
```bash
# Полная переиндексация
python scripts/populate_db.py --force-reindex
```

### Очистка базы знаний
```python
# ОСТОРОЖНО: Полная очистка базы знаний
kb = get_knowledge_base()
kb.clear_collection()
print("База знаний очищена")
```

### Удаление конкретных документов
```python
# Удаление документа
kb.delete_document("doc_id_to_delete")
```

## Оптимизация производительности

### Контроль размера документов
- **Максимальный размер блока:** 2000 символов
- **Минимальный размер блока:** 100 символов
- **Перекрытие блоков:** 200 символов

### Настройка индексации
```python
# В config.py настройте параметры ChromaDB
CHROMA_SETTINGS = {
    "anonymized_telemetry": False,
    "allow_reset": True,
    "is_persistent": True
}
```

### Мониторинг метрик
```python
# Проверка качества поиска
def check_search_quality(query: str):
    kb = get_knowledge_base()
    results = kb.search_relevant_docs(query, n_results=5)
    
    if not results:
        return "Нет результатов"
    
    avg_distance = sum(doc['distance'] for doc in results) / len(results)
    
    if avg_distance < 0.3:
        return "Отличное качество"
    elif avg_distance < 0.5:
        return "Хорошее качество"
    elif avg_distance < 0.8:
        return "Удовлетворительное качество"
    else:
        return "Низкое качество"
```

## Интеграция с ML-аналитикой

### Автоматическое обновление на основе аналитики
```python
from modules.user_analytics import UserAnalytics
from modules.knowledge_base import get_knowledge_base

# Получить популярные запросы без ответов
analytics = UserAnalytics()
popular_queries = analytics.get_popular_unanswered_queries()

# Для каждого запроса проверить качество в базе знаний
kb = get_knowledge_base()
for query in popular_queries:
    should_search, docs = kb.should_use_dynamic_search(query)
    if should_search:
        print(f"Нужно добавить контент для: {query}")
```

### Отслеживание пробелов в знаниях
```python
# Анализ неотвеченных вопросов
def analyze_knowledge_gaps():
    analytics = UserAnalytics()
    
    # Запросы с низким качеством ответов
    low_quality = analytics.get_questions_by_search_quality("низкое")
    
    # Категории с наименьшим покрытием
    categories = analytics.get_category_coverage()
    
    return {
        "low_quality_queries": low_quality,
        "undercovered_categories": categories
    }
```

## Резервное копирование

### Создание резервной копии
```bash
# Копирование базы данных
xcopy "db\chroma_db" "backup\chroma_db_%date%" /E /I
```

### Восстановление из резервной копии
```bash
# Восстановление базы данных
rmdir "db\chroma_db" /S /Q
xcopy "backup\chroma_db_backup" "db\chroma_db" /E /I
```

## Устранение проблем

### Проблема: База знаний пуста
```python
# Проверка
kb = get_knowledge_base()
stats = kb.get_collection_stats()
if stats['total_documents'] == 0:
    print("База пуста. Запустите: python scripts/populate_db.py")
```

### Проблема: Низкое качество поиска
```python
# Анализ качества
def diagnose_search_quality():
    kb = get_knowledge_base()
    test_queries = [
        "регистрация ИП",
        "налоговые льготы",
        "трудовые отношения"
    ]
    
    for query in test_queries:
        results = kb.search_relevant_docs(query, n_results=3)
        if results:
            avg_distance = sum(doc['distance'] for doc in results) / len(results)
            print(f"Запрос: {query}, Качество: {avg_distance:.3f}")
```

### Проблема: Ошибки ChromaDB
```python
# Переинициализация базы
try:
    kb = get_knowledge_base()
    kb._initialize_db()
    print("База знаний переинициализирована")
except Exception as e:
    print(f"Ошибка: {e}")
    print("Попробуйте удалить папку db/chroma_db и запустить populate_db.py")
```

## Команды для быстрого старта

### Первичная настройка
```bash
# 1. Создание базы знаний
python scripts/populate_db.py

# 2. Скрапинг актуальной информации
python scripts/scrape_websites.py

# 3. Проверка работоспособности
python -c "from modules.knowledge_base import get_knowledge_base; kb = get_knowledge_base(); print(f'Документов: {kb.get_collection_stats()[\"total_documents\"]}')"
```

### Регулярное обновление
```bash
# Еженедельное обновление
python scripts/update_documents.py
python scripts/scrape_websites.py --max-pages 5

# Проверка качества
python -c "from modules.knowledge_base import get_knowledge_base; kb = get_knowledge_base(); print('Качество:', kb.search_relevant_docs('регистрация ИП')[0]['distance'] if kb.search_relevant_docs('регистрация ИП') else 'Нет данных')"
```

## Заключение

База знаний является ключевым компонентом системы юридического чат-бота. Регулярное обновление и мониторинг качества данных обеспечивают высокую точность ответов и удовлетворенность пользователей. Используйте предложенные методы для поддержания актуальности информации.

---

*Документ обновлен: 2024*  
*Версия системы: 1.0* 