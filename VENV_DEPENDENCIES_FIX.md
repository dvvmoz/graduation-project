# Исправление зависимостей на основе виртуального окружения

## Проблема
Изначально файл `requirements.txt` содержал только 20 основных пакетов, в то время как в виртуальном окружении проекта было установлено более 100 пакетов. Это могло привести к проблемам при развертывании контейнеров.

## Что было сделано

### 1. Анализ виртуального окружения
- Обнаружено виртуальное окружение в папке `venv/` с Python 3.10.10
- Проанализирован полный список установленных пакетов (135 пакетов)
- Выявлены важные зависимости, которые отсутствовали в `requirements.txt`

### 2. Обновление requirements.txt
**Было:**
```
aiogram==3.3.0
openai==1.12.0
chromadb==0.4.22
PyMuPDF==1.23.14
python-dotenv==1.0.0
pytest==7.4.4
pytest-vcr==1.0.2
httpx==0.26.0
numpy<2.0.0
requests==2.31.0
beautifulsoup4==4.12.2
aiohttp==3.9.1
lxml==4.9.3
python-docx==0.8.11
pywin32==306; sys_platform == "win32"
flask==3.0.0
flask-cors==4.0.0
flask-socketio==5.3.6
psutil==5.9.6
scikit-learn==1.3.2
```

**Стало:** Полный список из 135 пакетов из виртуального окружения, включая:
- `scikit-learn==1.7.0` (обновлено с 1.3.2)
- `pandas==2.3.1` (добавлено)
- `scipy==1.15.3` (добавлено)
- `numpy==1.26.4` (обновлено)
- Все зависимости ML и аналитики
- Все зависимости для веб-интерфейса
- Все зависимости для мониторинга и логирования

### 3. Обновление requirements.minimal.txt
Обновлен минимальный набор зависимостей для тестового развертывания:
```
aiogram==3.3.0
openai==1.12.0
chromadb==0.4.22
PyMuPDF==1.23.14
python-dotenv==1.0.0
httpx==0.26.0
numpy==1.26.4
requests==2.31.0
beautifulsoup4==4.12.2
aiohttp==3.9.1
lxml==4.9.3
python-docx==0.8.11
Flask==3.0.0
Flask-Cors==4.0.0
psutil==5.9.6
scikit-learn==1.7.0
pandas==2.3.1
scipy==1.15.3
```

### 4. Обновление Dockerfile
- Добавлен комментарий о том, что зависимости основаны на виртуальном окружении
- Обновлен для использования полного `requirements.txt`

### 5. Обновление Dockerfile.simple
- Изменен для использования `requirements.minimal.txt`
- Оптимизирован для тестового развертывания

## Результат
Теперь контейнеры будут использовать точно те же версии пакетов, что и в локальном виртуальном окружении, что обеспечивает:
- Совместимость между локальной разработкой и продакшеном
- Отсутствие конфликтов зависимостей
- Правильную работу ML-компонентов
- Стабильную работу всех модулей системы

## Файлы, которые были изменены:
- `requirements.txt` - полный список зависимостей из venv
- `requirements.minimal.txt` - минимальный набор для тестов
- `Dockerfile` - обновлен с комментарием
- `Dockerfile.simple` - использует минимальные зависимости
- `requirements.from_venv.txt` - создан для справки

## Рекомендации
1. Всегда использовать `pip freeze > requirements.txt` для создания зависимостей
2. Регулярно обновлять зависимости при добавлении новых пакетов
3. Тестировать контейнеры с обновленными зависимостями
4. Использовать виртуальное окружение для разработки 