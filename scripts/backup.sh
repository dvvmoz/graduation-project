#!/bin/bash

# Скрипт резервного копирования для ЮрПомощника
# Создает бэкапы базы знаний, ML-моделей и конфигураций

set -euo pipefail

# Переменные
BACKUP_DIR="/backup/local"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}

# Функции логирования
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

error() {
    echo "[ERROR] $1" >&2
    exit 1
}

# Создание бэкапа базы знаний
backup_database() {
    log "Создаем бэкап базы знаний..."
    
    if [[ -d "/backup/db" ]]; then
        tar -czf "$BACKUP_DIR/db_$TIMESTAMP.tar.gz" -C /backup db/
        log "✅ Бэкап базы знаний создан: db_$TIMESTAMP.tar.gz"
    else
        log "⚠️ Директория базы знаний не найдена"
    fi
}

# Создание бэкапа ML-моделей
backup_models() {
    log "Создаем бэкап ML-моделей..."
    
    if [[ -d "/backup/models" ]]; then
        tar -czf "$BACKUP_DIR/models_$TIMESTAMP.tar.gz" -C /backup models/
        log "✅ Бэкап ML-моделей создан: models_$TIMESTAMP.tar.gz"
    else
        log "⚠️ Директория ML-моделей не найдена"
    fi
}

# Создание бэкапа конфигураций
backup_configs() {
    log "Создаем бэкап конфигураций..."
    
    # Создаем временную директорию для конфигураций
    CONFIG_TEMP="/tmp/config_backup_$TIMESTAMP"
    mkdir -p "$CONFIG_TEMP"
    
    # Копируем важные файлы (без секретов)
    if [[ -f "/.env.prod" ]]; then
        # Создаем версию без секретных данных
        grep -v -E "(TOKEN|KEY|PASSWORD)" /.env.prod > "$CONFIG_TEMP/env.prod.template" || true
    fi
    
    # Добавляем другие конфигурационные файлы
    cp -r /app/nginx/nginx.conf "$CONFIG_TEMP/" 2>/dev/null || true
    cp -r /app/monitoring/ "$CONFIG_TEMP/" 2>/dev/null || true
    
    tar -czf "$BACKUP_DIR/configs_$TIMESTAMP.tar.gz" -C /tmp "config_backup_$TIMESTAMP"
    rm -rf "$CONFIG_TEMP"
    
    log "✅ Бэкап конфигураций создан: configs_$TIMESTAMP.tar.gz"
}

# Загрузка в S3 (если настроено)
upload_to_s3() {
    if [[ -n "${S3_BUCKET:-}" ]] && [[ -n "${AWS_ACCESS_KEY_ID:-}" ]]; then
        log "Загружаем бэкапы в S3..."
        
        for file in "$BACKUP_DIR"/*_$TIMESTAMP.tar.gz; do
            if [[ -f "$file" ]]; then
                aws s3 cp "$file" "s3://$S3_BUCKET/backups/$(basename "$file")"
                log "✅ Загружен в S3: $(basename "$file")"
            fi
        done
    else
        log "ℹ️ S3 не настроен, пропускаем загрузку в облако"
    fi
}

# Очистка старых бэкапов
cleanup_old_backups() {
    log "Очищаем старые бэкапы (старше $RETENTION_DAYS дней)..."
    
    # Локальные бэкапы
    find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    # S3 бэкапы (если настроено)
    if [[ -n "${S3_BUCKET:-}" ]] && [[ -n "${AWS_ACCESS_KEY_ID:-}" ]]; then
        # Получаем список старых файлов в S3 и удаляем их
        aws s3 ls "s3://$S3_BUCKET/backups/" --recursive | \
        while read -r line; do
            file_date=$(echo $line | awk '{print $1 " " $2}')
            file_name=$(echo $line | awk '{print $4}')
            
            # Проверяем возраст файла
            if [[ $(date -d "$file_date" +%s) -lt $(date -d "$RETENTION_DAYS days ago" +%s) ]]; then
                aws s3 rm "s3://$S3_BUCKET/$file_name"
                log "🗑️ Удален старый бэкап из S3: $file_name"
            fi
        done
    fi
    
    log "✅ Очистка завершена"
}

# Проверка размера бэкапов
check_backup_size() {
    log "Проверяем размер созданных бэкапов..."
    
    total_size=0
    for file in "$BACKUP_DIR"/*_$TIMESTAMP.tar.gz; do
        if [[ -f "$file" ]]; then
            size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
            size_mb=$((size / 1024 / 1024))
            log "📁 $(basename "$file"): ${size_mb}MB"
            total_size=$((total_size + size))
        fi
    done
    
    total_mb=$((total_size / 1024 / 1024))
    log "📊 Общий размер бэкапов: ${total_mb}MB"
}

# Отправка уведомления (опционально)
send_notification() {
    if [[ -n "${NOTIFICATION_WEBHOOK:-}" ]]; then
        curl -X POST "$NOTIFICATION_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"text\":\"✅ Бэкап ЮрПомощника завершен: $TIMESTAMP\"}" \
            || log "⚠️ Не удалось отправить уведомление"
    fi
}

# Основная функция
main() {
    log "🔄 Начинаем процедуру резервного копирования..."
    
    # Создаем директорию для бэкапов
    mkdir -p "$BACKUP_DIR"
    
    # Выполняем бэкап
    backup_database
    backup_models
    backup_configs
    
    # Проверяем размер
    check_backup_size
    
    # Загружаем в облако
    upload_to_s3
    
    # Очищаем старые бэкапы
    cleanup_old_backups
    
    # Отправляем уведомление
    send_notification
    
    log "✅ Резервное копирование завершено успешно!"
}

# Запуск с обработкой ошибок
trap 'error "Произошла ошибка в строке $LINENO"' ERR

main "$@" 