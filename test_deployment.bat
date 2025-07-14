@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Скрипт для локального тестирования развертывания ЮрПомощника в Windows

echo.
echo 🧪 Начинаем локальное тестирование развертывания ЮрПомощника
echo ========================================================

:: Проверка Docker
echo 📦 Проверяем Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не найден! Установите Docker Desktop и повторите попытку.
    pause
    exit /b 1
)
echo ✅ Docker найден

:: Проверка Docker Compose
echo 📦 Проверяем Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose не найден! Убедитесь, что Docker Desktop установлен корректно.
    pause
    exit /b 1
)
echo ✅ Docker Compose найден

:: Создание тестовой конфигурации
echo 🔧 Подготавливаем тестовую конфигурацию...
if not exist "env.test.example" (
    echo Создаем тестовую конфигурацию...
    (
        echo TELEGRAM_TOKEN=test_token
        echo OPENAI_API_KEY=test_key
        echo SECRET_KEY=test_secret_key_for_local_development_only_32chars
        echo ADMIN_PASSWORD=test_admin
        echo GRAFANA_PASSWORD=test_grafana
        echo CHROMA_DB_PATH=/app/db/chroma
        echo LOG_LEVEL=INFO
        echo MAX_TOKENS=2000
        echo BACKUP_SCHEDULE=0 2 * * *
        echo BACKUP_RETENTION_DAYS=7
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo CORS_ORIGINS=http://localhost,https://localhost
    ) > env.test.example
)

:: Создание необходимых директорий
echo 📁 Создаем необходимые директории...
if not exist "logs" mkdir logs
if not exist "logs\nginx" mkdir logs\nginx
if not exist "nginx" mkdir nginx

:: Очистка старых контейнеров
echo 🧹 Очищаем старые тестовые контейнеры...
docker-compose -f docker-compose.test.yml down --volumes --remove-orphans 2>nul

:: Сборка образов
echo 🏗️ Собираем Docker образы...
docker-compose -f docker-compose.test.yml build --no-cache
if %errorlevel% neq 0 (
    echo ❌ Ошибка сборки образов!
    pause
    exit /b 1
)

:: Запуск контейнеров
echo 🚀 Запускаем тестовые контейнеры...
docker-compose -f docker-compose.test.yml up -d
if %errorlevel% neq 0 (
    echo ❌ Ошибка запуска контейнеров!
    pause
    exit /b 1
)

:: Ожидание готовности сервисов
echo ⏳ Ожидаем готовности сервисов (30 секунд)...
timeout /t 30 /nobreak >nul

:: Проверка статуса контейнеров
echo 🔍 Проверяем статус контейнеров...
docker-compose -f docker-compose.test.yml ps

:: Проверка доступности сервисов
echo 🌐 Проверяем доступность сервисов...

:: Проверяем Nginx
curl -f -s http://localhost/ >nul 2>&1
if %errorlevel% eq 0 (
    echo ✅ Nginx доступен (http://localhost/^)
) else (
    echo ⚠️ Nginx может быть недоступен
)

:: Проверяем Redis
docker exec legal-bot-redis-test redis-cli ping >nul 2>&1
if %errorlevel% eq 0 (
    echo ✅ Redis доступен
) else (
    echo ⚠️ Redis может быть недоступен
)

:: Проверяем основное приложение
curl -f -s http://localhost:5000/health >nul 2>&1
if %errorlevel% eq 0 (
    echo ✅ Основное приложение доступно
) else (
    echo ⚠️ Основное приложение может быть недоступно
)

:: Показываем логи
echo 📄 Показываем последние логи...
docker-compose -f docker-compose.test.yml logs --tail=5

:: Отображение информации
echo.
echo 🎉 Тестовое развертывание завершено!
echo =======================================
echo.
echo 📊 Доступные сервисы:
echo • Основное приложение: http://localhost:5000/
echo • Nginx: http://localhost/
echo • Redis: localhost:6379
echo.
echo 📋 Полезные команды:
echo • Просмотр логов: docker-compose -f docker-compose.test.yml logs -f
echo • Остановка: docker-compose -f docker-compose.test.yml down
echo • Перезапуск: docker-compose -f docker-compose.test.yml restart
echo • Статус: docker-compose -f docker-compose.test.yml ps
echo.
echo 🔧 Тестирование:
echo • Проверка Nginx: curl http://localhost/
echo • Проверка Redis: docker exec legal-bot-redis-test redis-cli ping
echo • Логи приложения: docker-compose -f docker-compose.test.yml logs legal-bot
echo.
echo ✅ Локальное тестирование завершено!

pause 