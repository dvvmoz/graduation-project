# Правило: Всегда использовать виртуальное окружение

## 🎯 Правило
**При запуске команд в терминале всегда использовать виртуальное окружение в папке проекта**

## ✅ Подтверждение работы правила

### Текущее состояние:
- ✅ **Виртуальное окружение активировано**: `(venv)` в промпте
- ✅ **Python из venv**: `F:\graduation project\venv\Scripts\python.exe`
- ✅ **Версия Python**: `3.10.10`
- ✅ **Pip из venv**: `pip 25.1.1 from F:\graduation project\venv\lib\site-packages\pip`

## 🛠️ Инструменты для соблюдения правила

### 1. Скрипты автоматического запуска
- **`run_with_venv.bat`** - для Windows Command Prompt
- **`run_with_venv.ps1`** - для Windows PowerShell

### 2. Использование скриптов
```bash
# Windows Command Prompt
run_with_venv.bat "python main.py"

# Windows PowerShell
.\run_with_venv.ps1 "python main.py"
```

### 3. Ручная активация
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

## 📋 Что означает соблюдение правила

### ✅ Всегда делать:
1. **Активировать виртуальное окружение** перед выполнением команд
2. **Проверять активацию** по наличию `(venv)` в промпте
3. **Использовать Python из venv** для всех Python-команд
4. **Использовать pip из venv** для установки пакетов
5. **Проверять путь к Python** через `python -c "import sys; print(sys.executable)"`

### ❌ Никогда не делать:
1. **Запускать Python без активации venv**
2. **Использовать системный Python** вместо venv
3. **Устанавливать пакеты глобально** вместо venv
4. **Игнорировать активацию** виртуального окружения

## 🔍 Проверка соблюдения правила

### Команды для проверки:
```bash
# Проверка активации venv
echo $env:VIRTUAL_ENV  # PowerShell
echo %VIRTUAL_ENV%      # Command Prompt

# Проверка пути к Python
python -c "import sys; print(sys.executable)"

# Проверка версии Python
python --version

# Проверка пути к pip
pip --version
```

### Ожидаемые результаты:
- **VIRTUAL_ENV**: `F:\graduation project\venv`
- **Python path**: `F:\graduation project\venv\Scripts\python.exe`
- **Pip path**: `F:\graduation project\venv\lib\site-packages\pip`

## 🚀 Автоматизация соблюдения правила

### 1. Pre-commit hooks
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: check-venv
      name: Check virtual environment
      entry: python -c "import sys; assert 'venv' in sys.executable"
      language: system
```

### 2. Скрипты проверки
```bash
# check_venv.bat
@echo off
python -c "import sys; assert 'venv' in sys.executable" 2>nul
if errorlevel 1 (
    echo ОШИБКА: Виртуальное окружение не активировано!
    echo Активируйте venv: venv\Scripts\activate
    pause
    exit /b 1
)
echo Виртуальное окружение активировано ✓
```

### 3. Интеграция с IDE
- **VS Code**: Автоматический выбор Python интерпретатора из venv
- **PyCharm**: Настройка проекта на использование venv
- **Jupyter**: Использование kernel из venv

## 📊 Преимущества соблюдения правила

### ✅ Изоляция зависимостей
- Каждый проект имеет свои зависимости
- Нет конфликтов между проектами
- Чистая среда разработки

### ✅ Воспроизводимость
- Одинаковые версии пакетов на всех машинах
- Точное соответствие requirements.txt
- Стабильная работа приложения

### ✅ Безопасность
- Изоляция от системных пакетов
- Контроль версий зависимостей
- Защита от случайных изменений

### ✅ Удобство развертывания
- Простое создание контейнеров
- Точное воспроизведение среды
- Минимальные конфликты зависимостей

## 🔧 Настройка для разных сценариев

### Разработка
```bash
# Активация для разработки
venv\Scripts\activate
python main.py
```

### Тестирование
```bash
# Активация для тестов
venv\Scripts\activate
python -m pytest
```

### Установка пакетов
```bash
# Активация для установки
venv\Scripts\activate
pip install новый_пакет
```

### Обновление зависимостей
```bash
# Активация для обновления
venv\Scripts\activate
.\update_requirements.bat
```

## 🚨 Troubleshooting

### Проблема: venv не активируется
```bash
# Решение: Пересоздайте venv
python -m venv venv --clear
venv\Scripts\activate
```

### Проблема: Python не из venv
```bash
# Решение: Проверьте активацию
echo $env:VIRTUAL_ENV
python -c "import sys; print(sys.executable)"
```

### Проблема: Пакеты не устанавливаются в venv
```bash
# Решение: Убедитесь в активации
venv\Scripts\activate
pip install пакет
```

## 📈 Мониторинг соблюдения правила

### Автоматические проверки
- ✅ Pre-commit hooks
- ✅ CI/CD проверки
- ✅ IDE интеграция

### Ручные проверки
- ✅ Проверка промпта на `(venv)`
- ✅ Проверка пути к Python
- ✅ Проверка переменной VIRTUAL_ENV

## 🎯 Результат

Соблюдение этого правила обеспечивает:

1. **Надежную изоляцию** зависимостей проекта
2. **Воспроизводимую среду** разработки
3. **Стабильную работу** приложения
4. **Простое развертывание** в продакшене
5. **Контроль версий** всех зависимостей

**Правило активно соблюдается!** ✅ 