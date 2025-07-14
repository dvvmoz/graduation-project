#!/bin/bash

# Скрипт для локального тестирования развертывания ЮрПомощника

set -euo pipefail

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции логирования
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Проверка зависимостей
check_dependencies() {
    log "Проверяем зависимости..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker не найден. Установите Docker и повторите попытку."
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose не найден. Установите Docker Compose и повторите попытку."
    fi
    
    log "Зависимости проверены ✓"
}

# Подготовка тестовой конфигурации
prepare_test_config() {
    log "Подготавливаем тестовую конфигурацию..."
    
    # Создаем тестовую конфигурацию если её нет
    if [[ ! -f env.test.example ]]; then
        warn "Файл env.test.example не найден. Создаем..."
        cat > env.test.example << EOF
TELEGRAM_TOKEN=test_token
OPENAI_API_KEY=test_key
SECRET_KEY=test_secret_key_for_local_development_only_32chars
ADMIN_PASSWORD=test_admin
GRAFANA_PASSWORD=test_grafana
CHROMA_DB_PATH=/app/db/chroma
LOG_LEVEL=INFO
MAX_TOKENS=2000
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=7
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost,https://localhost
EOF
    fi
    
    # Создаем необходимые директории
    mkdir -p logs/nginx data nginx
    
    log "Конфигурация подготовлена ✓"
}

# Очистка старых контейнеров
cleanup_old_containers() {
    log "Очищаем старые тестовые контейнеры..."
    
    docker-compose -f docker-compose.test.yml down --volumes --remove-orphans 2>/dev/null || true
    
    # Удаляем неиспользуемые образы
    docker system prune -f >/dev/null 2>&1 || true
    
    log "Очистка завершена ✓"
}

# Сборка и запуск контейнеров
build_and_run() {
    log "Собираем и запускаем тестовые контейнеры..."
    
    # Сборка образов
    log "Сборка образов..."
    docker-compose -f docker-compose.test.yml build --no-cache
    
    # Запуск контейнеров
    log "Запуск контейнеров..."
    docker-compose -f docker-compose.test.yml up -d
    
    log "Контейнеры запущены ✓"
}

# Ожидание готовности сервисов
wait_for_services() {
    log "Ожидаем готовности сервисов..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if docker-compose -f docker-compose.test.yml ps | grep -q "Up"; then
            log "Сервисы готовы ✓"
            return 0
        fi
        
        log "Попытка $attempt/$max_attempts - ожидаем..."
        sleep 5
        ((attempt++))
    done
    
    error "Сервисы не готовы после $max_attempts попыток"
}

# Проверка статуса контейнеров
check_container_status() {
    log "Проверяем статус контейнеров..."
    
    echo -e "${BLUE}Статус контейнеров:${NC}"
    docker-compose -f docker-compose.test.yml ps
    
    # Проверяем каждый контейнер
    local containers=("legal-bot-test" "legal-bot-redis-test" "legal-bot-nginx-test")
    
    for container in "${containers[@]}"; do
        if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$container.*Up"; then
            log "✓ $container работает"
        else
            warn "✗ $container не работает"
        fi
    done
}

# Проверка доступности сервисов
test_service_availability() {
    log "Проверяем доступность сервисов..."
    
    # Проверяем Nginx
    if curl -f -s http://localhost/ > /dev/null; then
        log "✓ Nginx доступен (http://localhost/)"
    else
        warn "✗ Nginx недоступен"
    fi
    
    # Проверяем Redis
    if docker exec legal-bot-redis-test redis-cli ping | grep -q "PONG"; then
        log "✓ Redis доступен"
    else
        warn "✗ Redis недоступен"
    fi
    
    # Проверяем основное приложение (если есть health endpoint)
    if curl -f -s http://localhost:5000/health > /dev/null 2>&1; then
        log "✓ Основное приложение доступно"
    else
        warn "✗ Основное приложение может быть недоступно"
    fi
}

# Показ логов
show_logs() {
    log "Показываем логи сервисов..."
    
    echo -e "${BLUE}Последние логи:${NC}"
    docker-compose -f docker-compose.test.yml logs --tail=10
}

# Показ информации о тестовом развертывании
show_test_info() {
    log "🎉 Тестовое развертывание завершено!"
    echo
    echo -e "${BLUE}📊 Доступные сервисы:${NC}"
    echo "• Основное приложение: http://localhost:5000/"
    echo "• Nginx: http://localhost/"
    echo "• Redis: localhost:6379"
    echo
    echo -e "${BLUE}📋 Полезные команды:${NC}"
    echo "• Просмотр логов: docker-compose -f docker-compose.test.yml logs -f"
    echo "• Остановка: docker-compose -f docker-compose.test.yml down"
    echo "• Перезапуск: docker-compose -f docker-compose.test.yml restart"
    echo "• Статус: docker-compose -f docker-compose.test.yml ps"
    echo
    echo -e "${BLUE}🔧 Тестирование:${NC}"
    echo "• Проверка Nginx: curl http://localhost/"
    echo "• Проверка Redis: docker exec legal-bot-redis-test redis-cli ping"
    echo "• Логи приложения: docker-compose -f docker-compose.test.yml logs legal-bot"
}

# Основная функция
main() {
    log "🧪 Начинаем локальное тестирование развертывания ЮрПомощника"
    
    check_dependencies
    prepare_test_config
    cleanup_old_containers
    build_and_run
    wait_for_services
    check_container_status
    test_service_availability
    show_logs
    show_test_info
    
    log "✅ Локальное тестирование завершено!"
}

# Обработка ошибок
trap 'error "Произошла ошибка в строке $LINENO"' ERR

# Запуск
main "$@" 