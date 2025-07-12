# 📋 Логирование в системе ЮрПомощник

## ✅ Настроенное логирование

### 🤖 Основной бот (`main.py`)
- **Файл лога:** `bot.log`
- **Кодировка:** UTF-8
- **Формат:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Выход:** Файл + консоль

### 🌐 Веб-скрапинг (`scripts/scrape_websites.py`)
- **Файл лога:** `scraping.log`
- **Содержимое:** Все операции скрапинга сайтов
- **Размер:** ~430 КБ

### 📄 Скрипты обработки документов
- `add_scraped_to_knowledge_base.log` - Добавление scraped данных
- `rebuild_knowledge_base.log` - Перестройка базы знаний
- `test_caching_fixed.log` - Тестирование кэширования

## 📁 Расположение файлов логов

```
graduation project/
├── bot.log                           # Основной бот
├── scraping.log                      # Веб-скрапинг
├── add_scraped_to_knowledge_base.log # Добавление данных
├── rebuild_knowledge_base.log        # Перестройка БД
└── test_caching_fixed.log           # Тестирование
```

## 🔍 Команды для работы с логами

### Windows PowerShell:
```powershell
# Просмотр последних записей
Get-Content bot.log -Tail 50 -Encoding UTF8

# Мониторинг в реальном времени
Get-Content bot.log -Wait -Encoding UTF8

# Поиск ошибок
Get-Content bot.log -Encoding UTF8 | Select-String "ERROR"

# Статистика файлов логов
Get-ChildItem *.log | Select-Object Name, Length, LastWriteTime
```

### Linux/macOS:
```bash
# Просмотр последних записей
tail -50 bot.log

# Мониторинг в реальном времени
tail -f bot.log

# Поиск ошибок
grep "ERROR" bot.log

# Статистика файлов логов
ls -la *.log
```

## 📊 Уровни логирования

- **INFO** - Информационные сообщения (запуск, инициализация)
- **WARNING** - Предупреждения (неоптимальные ситуации)
- **ERROR** - Ошибки (проблемы в работе)
- **DEBUG** - Отладочная информация (если включена)

## 🔧 Настройка логирования

### Изменение уровня логирования:
```python
# В main.py
logging.basicConfig(
    level=logging.DEBUG,  # Изменить на DEBUG для подробных логов
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
```

### Ротация логов:
```python
from logging.handlers import RotatingFileHandler

# Ротация при достижении 10 МБ, хранить 5 файлов
handler = RotatingFileHandler(
    'bot.log', 
    maxBytes=10*1024*1024, 
    backupCount=5,
    encoding='utf-8'
)
```

## 📈 Мониторинг

### Типичные сообщения:
- `СТАРТ: Запуск юридического чат-бота...` - Запуск бота
- `Бот инициализирован` - Успешная инициализация
- `Запуск бота в режиме polling...` - Начало работы
- `Start polling` - Aiogram начал опрос

### Признаки проблем:
- `ERROR` - Ошибки в работе
- `Ошибка конфигурации` - Проблемы с настройкой
- `Failed to` - Неудачные операции

## 🛠️ Устранение неполадок

### Проблема: Файл лога не создается
```bash
# Проверить права доступа
ls -la bot.log

# Проверить место на диске
df -h
```

### Проблема: Кодировка в логах
```python
# Убедиться, что используется UTF-8
logging.FileHandler('bot.log', encoding='utf-8')
```

### Проблема: Слишком большие файлы логов
```bash
# Очистить старые логи
> bot.log

# Или использовать ротацию логов
```

## 📝 Рекомендации

1. **Регулярно проверяйте логи** на наличие ошибок
2. **Используйте ротацию логов** для больших систем
3. **Настройте мониторинг** для критических ошибок
4. **Архивируйте старые логи** для экономии места
5. **Используйте правильную кодировку** (UTF-8) для русского текста 