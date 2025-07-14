@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Скрипт автоматического развертывания ЮрПомощника в production для Windows
:: Поддерживает развертывание на Windows Server и десктопных версиях

echo.
echo 🚀 Начинаем развертывание ЮрПомощника в production
echo ================================================

:: Проверка Docker
echo 📦 Проверяем Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не найден! Установите Docker Desktop и повторите попытку.
    echo Скачать: https://www.docker.com/products/docker-desktop
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

:: Подготовка конфигурации
echo 🔧 Подготавливаем конфигурацию...
if not exist ".env.prod" (
    if exist "env.prod.example" (
        copy env.prod.example .env.prod >nul
        echo ⚠️  Создан файл .env.prod
        echo 📝 ОБЯЗАТЕЛЬНО отредактируйте файл .env.prod перед продолжением!
        echo Путь к файлу: %cd%\.env.prod
        echo.
        echo Нажмите любую клавишу после редактирования .env.prod...
        pause >nul
    ) else (
        echo ❌ Файл env.prod.example не найден!
        exit /b 1
    )
)

:: Создание необходимых директорий
echo 📁 Создаем необходимые директории...
if not exist "logs" mkdir logs
if not exist "logs\nginx" mkdir logs\nginx
if not exist "backups" mkdir backups
if not exist "nginx" mkdir nginx
if not exist "nginx\ssl" mkdir nginx\ssl
if not exist "monitoring" mkdir monitoring
if not exist "monitoring\grafana" mkdir monitoring\grafana
if not exist "monitoring\grafana\dashboards" mkdir monitoring\grafana\dashboards
if not exist "monitoring\grafana\datasources" mkdir monitoring\grafana\datasources
if not exist "redis" mkdir redis

:: Создание самоподписанного SSL сертификата
echo 🔐 Создаем SSL сертификат...
if not exist "nginx\ssl\cert.pem" (
    echo Создаем самоподписанный сертификат...
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx\ssl\key.pem -out nginx\ssl\cert.pem -subj "/C=BY/ST=Minsk/L=Minsk/O=LegalBot/CN=localhost" 2>nul
    if %errorlevel% neq 0 (
        echo ⚠️  OpenSSL не найден. Создайте SSL сертификат вручную или установите OpenSSL.
    ) else (
        echo ✅ SSL сертификат создан
    )
)

:: Остановка старых контейнеров
echo 🛑 Останавливаем старые контейнеры...
docker-compose -f docker-compose.prod.yml down 2>nul

:: Сборка образов
echo 🏗️  Собираем Docker образы...
docker-compose -f docker-compose.prod.yml build
if %errorlevel% neq 0 (
    echo ❌ Ошибка сборки образов!
    pause
    exit /b 1
)

:: Запуск сервисов
echo 🚀 Запускаем сервисы...
docker-compose -f docker-compose.prod.yml up -d
if %errorlevel% neq 0 (
    echo ❌ Ошибка запуска сервисов!
    pause
    exit /b 1
)

:: Ожидание запуска
echo ⏳ Ожидаем запуска сервисов (30 секунд)...
timeout /t 30 /nobreak >nul

:: Проверка статуса
echo 🔍 Проверяем статус сервисов...
docker-compose -f docker-compose.prod.yml ps

:: Проверка доступности
echo 🌐 Проверяем доступность...
curl -f -s http://localhost/health >nul 2>&1
if %errorlevel% eq 0 (
    echo ✅ Сервис доступен
) else (
    echo ⚠️  Сервис может быть недоступен. Проверьте логи.
)

:: Отображение информации
echo.
echo 🎉 Развертывание завершено!
echo ========================
echo.
echo 📊 Доступные сервисы:
echo • Основное приложение: https://localhost/
echo • Админ-панель: https://localhost/admin/
echo • Grafana: http://localhost:3000/
echo • Prometheus: http://localhost:9090/
echo.
echo 📋 Полезные команды:
echo • Просмотр логов: docker-compose -f docker-compose.prod.yml logs -f
echo • Остановка: docker-compose -f docker-compose.prod.yml down
echo • Перезапуск: docker-compose -f docker-compose.prod.yml restart
echo.
echo ⚠️  Не забудьте:
echo • Настроить регулярные бэкапы
echo • Мониторить ресурсы системы
echo • Обновлять SSL сертификаты
echo.
echo ✅ Развертывание успешно завершено!

pause 