# Управление зависимостями проекта

## Автоматическое обновление requirements.txt

### Для Windows (PowerShell)
```powershell
.\update_requirements.ps1
```

### Для Windows (Command Prompt)
```cmd
update_requirements.bat
```

### Для Linux/macOS
```bash
chmod +x update_requirements.sh
./update_requirements.sh
```

## Что делают скрипты

1. **Проверяют существование виртуального окружения**
2. **Активируют виртуальное окружение**
3. **Обновляют pip до последней версии**
4. **Создают полный requirements.txt** из виртуального окружения
5. **Создают минимальный requirements.minimal.txt** для тестового развертывания
6. **Создают резервную копию** requirements.backup.txt
7. **Показывают статистику** обновленных пакетов

## Рекомендуемый рабочий процесс

### 1. При добавлении нового пакета
```bash
# Активируйте виртуальное окружение
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Установите новый пакет
pip install новый_пакет

# Обновите requirements.txt
.\update_requirements.ps1  # Windows
./update_requirements.sh   # Linux/macOS
```

### 2. При обновлении пакетов
```bash
# Активируйте виртуальное окружение
venv\Scripts\activate

# Обновите пакеты
pip install --upgrade пакет1 пакет2

# Обновите requirements.txt
.\update_requirements.ps1
```

### 3. При удалении пакетов
```bash
# Активируйте виртуальное окружение
venv\Scripts\activate

# Удалите пакет
pip uninstall ненужный_пакет

# Обновите requirements.txt
.\update_requirements.ps1
```

## Структура файлов зависимостей

### requirements.txt
- **Полный список** всех пакетов из виртуального окружения
- **Используется для продакшена** и полного развертывания
- **Содержит точные версии** всех зависимостей

### requirements.minimal.txt
- **Минимальный набор** основных зависимостей
- **Используется для тестового развертывания**
- **Содержит только критически важные пакеты**

### requirements.backup.txt
- **Резервная копия** предыдущей версии requirements.txt
- **Автоматически создается** при каждом обновлении
- **Помогает откатиться** к предыдущему состоянию

## Интеграция с Git

### .gitignore настроен для исключения:
- `requirements.backup.txt` - резервные копии
- `venv/` - виртуальное окружение
- `*.backup` - все backup файлы

### Рекомендуемые коммиты:
```bash
# После обновления зависимостей
git add requirements.txt requirements.minimal.txt
git commit -m "Обновлены зависимости: добавлен новый_пакет"
```

## Мониторинг зависимостей

### Проверка устаревших пакетов
```bash
pip list --outdated
```

### Проверка безопасности
```bash
pip-audit
```

### Проверка совместимости
```bash
pip check
```

## Автоматизация в CI/CD

### GitHub Actions (пример)
```yaml
- name: Update dependencies
  run: |
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip freeze > requirements.txt
```

### Pre-commit hooks
```bash
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: update-requirements
      name: Update requirements.txt
      entry: ./update_requirements.sh
      language: system
      files: requirements.txt
```

## Troubleshooting

### Проблема: Виртуальное окружение не найдено
**Решение:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Проблема: Конфликт версий
**Решение:**
```bash
# Откатитесь к backup
cp requirements.backup.txt requirements.txt
# Или обновите конкретный пакет
pip install --upgrade проблемный_пакет
```

### Проблема: Слишком много зависимостей
**Решение:**
```bash
# Используйте requirements.minimal.txt для тестов
pip install -r requirements.minimal.txt
```

## Лучшие практики

1. **Всегда используйте виртуальное окружение**
2. **Регулярно обновляйте зависимости**
3. **Тестируйте после обновления зависимостей**
4. **Документируйте изменения в зависимостях**
5. **Используйте точные версии** (== вместо >=)
6. **Проверяйте совместимость** перед обновлением
7. **Создавайте резервные копии** перед массовыми изменениями 