#!/bin/bash

# Скрипт автоматического развертывания ЮрПомощника в production
# Поддерживает развертывание на VPS, DigitalOcean, AWS EC2

set -euo pipefail

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция логирования
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

# Проверяем права root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "Не запускайте скрипт от root! Используйте sudo только когда необходимо."
    fi
}

# Проверяем зависимости
check_dependencies() {
    log "Проверяем зависимости..."
    
    # Docker
    if ! command -v docker &> /dev/null; then
        warn "Docker не найден. Устанавливаем..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
        log "Docker установлен. Перезайдите в систему для применения изменений."
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        warn "Docker Compose не найден. Устанавливаем..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    # Git
    if ! command -v git &> /dev/null; then
        error "Git не найден. Установите Git и повторите попытку."
    fi
    
    log "Все зависимости проверены ✓"
}

# Настройка firewall
setup_firewall() {
    log "Настраиваем firewall..."
    
    if command -v ufw &> /dev/null; then
        sudo ufw --force enable
        sudo ufw allow ssh
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        sudo ufw allow 3000/tcp  # Grafana
        sudo ufw allow 9090/tcp  # Prometheus
        log "UFW firewall настроен ✓"
    elif command -v firewall-cmd &> /dev/null; then
        sudo systemctl enable firewalld
        sudo systemctl start firewalld
        sudo firewall-cmd --permanent --add-service=ssh
        sudo firewall-cmd --permanent --add-service=http
        sudo firewall-cmd --permanent --add-service=https
        sudo firewall-cmd --permanent --add-port=3000/tcp
        sudo firewall-cmd --permanent --add-port=9090/tcp
        sudo firewall-cmd --reload
        log "Firewalld настроен ✓"
    else
        warn "Firewall не найден. Настройте вручную."
    fi
}

# Генерация SSL сертификата
setup_ssl() {
    log "Настраиваем SSL сертификат..."
    
    mkdir -p nginx/ssl
    
    if [[ -z "${DOMAIN:-}" ]]; then
        warn "Домен не указан. Создаем самоподписанный сертификат..."
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/key.pem \
            -out nginx/ssl/cert.pem \
            -subj "/C=BY/ST=Minsk/L=Minsk/O=LegalBot/CN=localhost"
    else
        log "Получаем Let's Encrypt сертификат для домена: $DOMAIN"
        # Здесь можно добавить Certbot для автоматического получения сертификата
    fi
    
    log "SSL сертификат настроен ✓"
}

# Подготовка конфигурации
prepare_config() {
    log "Подготавливаем конфигурацию..."
    
    # Копируем пример конфигурации
    if [[ ! -f .env.prod ]]; then
        cp env.prod.example .env.prod
        warn "Создан файл .env.prod. ОБЯЗАТЕЛЬНО отредактируйте его перед продолжением!"
        echo "Путь к файлу: $(pwd)/.env.prod"
        read -p "Нажмите Enter после редактирования .env.prod..."
    fi
    
    # Проверяем обязательные переменные
    source .env.prod
    
    if [[ "$TELEGRAM_TOKEN" == "your_production_telegram_token_here" ]]; then
        error "Не заполнен TELEGRAM_TOKEN в .env.prod"
    fi
    
    if [[ "$OPENAI_API_KEY" == "your_production_openai_key_here" ]]; then
        error "Не заполнен OPENAI_API_KEY в .env.prod"
    fi
    
    log "Конфигурация проверена ✓"
}

# Сборка и запуск
deploy() {
    log "Запускаем развертывание..."
    
    # Останавливаем старые контейнеры
    docker-compose -f docker-compose.prod.yml down || true
    
    # Создаем необходимые директории
    mkdir -p logs/nginx backups monitoring/grafana/{dashboards,datasources} redis
    
    # Сборка образов
    log "Собираем Docker образы..."
    docker-compose -f docker-compose.prod.yml build
    
    # Запуск сервисов
    log "Запускаем сервисы..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Ожидание запуска
    log "Ожидаем запуска сервисов..."
    sleep 30
    
    # Проверка статуса
    check_health
}

# Проверка работоспособности
check_health() {
    log "Проверяем работоспособность сервисов..."
    
    local services=("legal-bot" "nginx" "redis" "prometheus" "grafana")
    
    for service in "${services[@]}"; do
        if docker-compose -f docker-compose.prod.yml ps | grep -q "$service.*Up"; then
            log "✓ $service работает"
        else
            error "✗ $service не работает"
        fi
    done
    
    # Проверяем HTTP доступность
    if curl -f -s http://localhost/health > /dev/null; then
        log "✓ HTTP доступность подтверждена"
    else
        warn "✗ HTTP недоступен"
    fi
    
    log "Проверка завершена ✓"
}

# Отображение информации о развертывании
show_info() {
    log "🎉 Развертывание завершено!"
    echo
    echo -e "${BLUE}📊 Доступные сервисы:${NC}"
    echo "• Основное приложение: https://localhost/"
    echo "• Админ-панель: https://localhost/admin/"
    echo "• Grafana: http://localhost:3000/ (admin/${GRAFANA_PASSWORD:-admin})"
    echo "• Prometheus: http://localhost:9090/"
    echo
    echo -e "${BLUE}📋 Полезные команды:${NC}"
    echo "• Просмотр логов: docker-compose -f docker-compose.prod.yml logs -f"
    echo "• Остановка: docker-compose -f docker-compose.prod.yml down"
    echo "• Перезапуск: docker-compose -f docker-compose.prod.yml restart"
    echo "• Обновление: git pull && docker-compose -f docker-compose.prod.yml up -d --build"
    echo
    echo -e "${YELLOW}⚠️  Не забудьте:${NC}"
    echo "• Настроить регулярные бэкапы"
    echo "• Мониторить ресурсы"
    echo "• Обновлять SSL сертификаты"
}

# Основная функция
main() {
    log "🚀 Начинаем развертывание ЮрПомощника в production"
    
    check_root
    check_dependencies
    setup_firewall
    setup_ssl
    prepare_config
    deploy
    show_info
    
    log "✅ Развертывание успешно завершено!"
}

# Запуск с обработкой ошибок
trap 'error "Произошла ошибка в строке $LINENO"' ERR

main "$@" 