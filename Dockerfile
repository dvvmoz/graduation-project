FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями (обновлен на основе виртуального окружения)
COPY requirements.txt .

# Создаём виртуальное окружение
RUN python -m venv /app/venv

# Обновляем pip внутри venv и устанавливаем зависимости
RUN /app/venv/bin/pip install --upgrade pip && /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем необходимые директории
RUN mkdir -p data db/chroma

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/app/venv

# Открываем порт (если потребуется в будущем)
EXPOSE 8000

# Запуск строго из venv!
CMD ["/app/venv/bin/python", "main.py"] 