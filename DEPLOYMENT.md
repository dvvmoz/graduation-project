# 🚀 Руководство по развертыванию ЮрПомощника в продакшене

## 📋 Содержание

1. [Требования к серверу](#требования-к-серверу)
2. [Быстрое развертывание](#быстрое-развертывание)
3. [Ручная настройка](#ручная-настройка)
4. [Мониторинг и обслуживание](#мониторинг-и-обслуживание)
5. [Безопасность](#безопасность)
6. [Резервное копирование](#резервное-копирование)
7. [Устранение неполадок](#устранение-неполадок)

## 🖥️ Требования к серверу

### Минимальные требования:
- **CPU**: 2 ядра (2 vCPU)
- **RAM**: 4 GB
- **Диск**: 20 GB SSD
- **ОС**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **Сеть**: Публичный IP адрес

### Рекомендуемые требования:
- **CPU**: 4 ядра (4 vCPU)
- **RAM**: 8 GB
- **Диск**: 50 GB SSD
- **ОС**: Ubuntu 22.04 LTS
- **Сеть**: Публичный IP + домен

### Облачные провайдеры:
- **DigitalOcean**: Droplet 4GB ($20/месяц)
- **AWS**: t3.medium EC2 instance
- **VPS.BY**: VPS-4 (аналог для Беларуси)
- **Yandex.Cloud**: s2.medium

## ⚡ Быстрое развертывание

### Автоматическое развертывание (Linux/macOS):

```bash
# 1. Клонируем репозиторий
git clone https://github.com/your-repo/legal-assistant-bot.git
cd legal-assistant-bot

# 2. Запускаем автоматическое развертывание
chmod +x deploy.sh
./deploy.sh
```

### Автоматическое развертывание (Windows):

```cmd
# 1. Клонируем репозиторий
git clone https://github.com/your-repo/legal-assistant-bot.git
cd legal-assistant-bot

# 2. Запускаем автоматическое развертывание
deploy.bat
```

### Что делает автоматический скрипт:
✅ Устанавливает Docker и Docker Compose  
✅ Настраивает firewall  
✅ Создает SSL сертификат  
✅ Настраивает конфигурацию  
✅ Запускает все сервисы  
✅ Проверяет работоспособность  

## 🔧 Ручная настройка

### 1. Установка зависимостей

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезайдите в систему для применения изменений
```

### 2. Подготовка конфигурации

```bash
# Создаем production конфигурацию
cp env.prod.example .env.prod

# Редактируем конфигурацию
nano .env.prod
```

**Обязательно заполните:**
```env
TELEGRAM_TOKEN=ваш_реальный_telegram_токен
OPENAI_API_KEY=ваш_реальный_openai_ключ
SECRET_KEY=ваш_супер_секретный_ключ_минимум_32_символа
ADMIN_PASSWORD=надежный_пароль_админа
GRAFANA_PASSWORD=пароль_для_grafana
```

### 3. Настройка SSL

#### Вариант A: Let's Encrypt (рекомендуется)
```bash
# Установка Certbot
sudo apt install certbot

# Получение сертификата
sudo certbot certonly --standalone -d yourdomain.com

# Копируем сертификаты
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*
```

#### Вариант B: Самоподписанный сертификат
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/key.pem \
    -out nginx/ssl/cert.pem \
    -subj "/C=BY/ST=Minsk/L=Minsk/O=LegalBot/CN=yourdomain.com"
```

### 4. Запуск сервисов

```bash
# Создаем необходимые директории
mkdir -p logs/nginx backups monitoring/grafana/{dashboards,datasources} redis

# Сборка и запуск
docker-compose -f docker-compose.prod.yml up -d --build

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

## 📊 Мониторинг и обслуживание

### Доступные сервисы:

| Сервис | URL | Описание |
|--------|-----|----------|
| Основное приложение | `https://yourdomain.com/` | Главная страница |
| Админ-панель | `https://yourdomain.com/admin/` | Управление системой |
| Grafana | `http://yourdomain.com:3000/` | Дашборды мониторинга |
| Prometheus | `http://yourdomain.com:9090/` | Сбор метрик |

### Основные команды:

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Просмотр логов конкретного сервиса
docker-compose -f docker-compose.prod.yml logs -f legal-bot

# Перезапуск сервиса
docker-compose -f docker-compose.prod.yml restart legal-bot

# Обновление системы
git pull
docker-compose -f docker-compose.prod.yml up -d --build

# Остановка всех сервисов
docker-compose -f docker-compose.prod.yml down
```

### Мониторинг ресурсов:

```bash
# Использование ресурсов контейнерами
docker stats

# Использование диска
df -h

# Мониторинг процессов
htop
```

## 🔒 Безопасность

### Firewall настройки:

```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp  # Grafana (можно ограничить по IP)
sudo ufw allow 9090/tcp  # Prometheus (можно ограничить по IP)

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --permanent --add-port=9090/tcp
sudo firewall-cmd --reload
```

### Обновления безопасности:

```bash
# Регулярные обновления системы
sudo apt update && sudo apt upgrade -y

# Обновление Docker образов
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### Ограничение доступа:

1. **Изменить порты по умолчанию**
2. **Настроить VPN для админ-доступа**
3. **Использовать fail2ban**
4. **Регулярно ротировать пароли**

## 💾 Резервное копирование

### Автоматические бэкапы:

Система автоматически создает бэкапы:
- **База знаний**: Ежедневно в 2:00
- **ML-модели**: Ежедневно в 2:00  
- **Конфигурации**: Ежедневно в 2:00

### Ручное создание бэкапа:

```bash
# Создание бэкапа
docker-compose -f docker-compose.prod.yml exec backup /app/backup.sh

# Проверка бэкапов
ls -la backups/
```

### Восстановление из бэкапа:

```bash
# Остановка сервисов
docker-compose -f docker-compose.prod.yml down

# Восстановление базы знаний
tar -xzf backups/db_YYYYMMDD_HHMMSS.tar.gz

# Восстановление ML-моделей
tar -xzf backups/models_YYYYMMDD_HHMMSS.tar.gz

# Запуск сервисов
docker-compose -f docker-compose.prod.yml up -d
```

### Настройка облачных бэкапов:

Добавьте в `.env.prod`:
```env
S3_BACKUP_BUCKET=your-backup-bucket
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

## 🔄 Обновление системы

### Обновление кода:

```bash
# 1. Создание бэкапа
docker-compose -f docker-compose.prod.yml exec backup /app/backup.sh

# 2. Получение обновлений
git pull origin main

# 3. Пересборка и перезапуск
docker-compose -f docker-compose.prod.yml up -d --build

# 4. Проверка работоспособности
docker-compose -f docker-compose.prod.yml ps
curl -f http://localhost/health
```

### Обновление зависимостей:

```bash
# Обновление Docker образов
docker-compose -f docker-compose.prod.yml pull

# Перезапуск с новыми образами
docker-compose -f docker-compose.prod.yml up -d
```

## 🛠️ Устранение неполадок

### Проверка статуса сервисов:

```bash
# Статус всех контейнеров
docker-compose -f docker-compose.prod.yml ps

# Логи с ошибками
docker-compose -f docker-compose.prod.yml logs --tail=100

# Проверка ресурсов
docker stats
```

### Частые проблемы:

#### 1. Контейнер не запускается
```bash
# Проверить логи
docker-compose -f docker-compose.prod.yml logs legal-bot

# Проверить конфигурацию
docker-compose -f docker-compose.prod.yml config
```

#### 2. Недостаточно памяти
```bash
# Проверить использование памяти
free -h
docker stats

# Увеличить swap (временно)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 3. Проблемы с SSL
```bash
# Проверить сертификаты
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Обновить сертификат Let's Encrypt
sudo certbot renew
```

#### 4. База знаний недоступна
```bash
# Проверить состояние ChromaDB
docker-compose -f docker-compose.prod.yml exec legal-bot python -c "from modules.knowledge_base import get_knowledge_base; print(get_knowledge_base().get_collection_stats())"

# Пересоздать базу знаний
docker-compose -f docker-compose.prod.yml exec legal-bot python scripts/populate_db.py
```

### Контактная информация для поддержки:

При возникновении проблем:
1. Проверьте логи сервисов
2. Создайте issue в репозитории
3. Опишите проблему с приложением логов

## 📈 Оптимизация производительности

### Настройка ресурсов:

```yaml
# В docker-compose.prod.yml
services:
  legal-bot:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### Мониторинг производительности:

- **Grafana дашборды**: Просмотр метрик в реальном времени
- **Prometheus alerts**: Уведомления о проблемах
- **Логи приложения**: Анализ ошибок и производительности

---

## 🎉 Успешное развертывание!

После завершения настройки у вас будет:

✅ **Полностью автоматизированная система**  
✅ **Мониторинг и алерты**  
✅ **Автоматические бэкапы**  
✅ **SSL шифрование**  
✅ **Масштабируемая архитектура**  

Ваш ЮрПомощник готов к работе в продакшене! 🚀 