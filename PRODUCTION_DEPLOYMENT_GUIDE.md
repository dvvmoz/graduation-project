# 🚀 Legal Bot - Полное руководство по продакшн-развертыванию

## 📋 Содержание

1. [Обзор архитектуры](#обзор-архитектуры)
2. [Требования к инфраструктуре](#требования-к-инфраструктуре)
3. [Облачное развертывание](#облачное-развертывание)
4. [Kubernetes развертывание](#kubernetes-развертывание)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Масштабирование](#масштабирование)
7. [Безопасность](#безопасность)
8. [Мониторинг](#мониторинг)
9. [Резервное копирование](#резервное-копирование)
10. [Обслуживание](#обслуживание)

## 🏗️ Обзор архитектуры

### Компоненты системы

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Nginx/WAF     │    │   Legal Bot     │
│   (HAProxy)     │───▶│   (Security)    │───▶│   (App)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Prometheus    │    │   Redis Cache   │
                       │   (Monitoring)  │    │   (Session)     │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Grafana       │    │   PostgreSQL    │
                       │   (Dashboard)   │    │   (Database)    │
                       └─────────────────┘    └─────────────────┘
```

### Технологический стек

- **Приложение**: Python Flask + ML модели
- **База данных**: PostgreSQL 15
- **Кэш**: Redis 7
- **Веб-сервер**: Nginx с WAF
- **Балансировщик**: HAProxy
- **Контейнеризация**: Docker
- **Оркестрация**: Kubernetes / Docker Swarm
- **Мониторинг**: Prometheus + Grafana
- **Безопасность**: ModSecurity, Fail2ban
- **CI/CD**: GitHub Actions / AWS CodePipeline

## 💻 Требования к инфраструктуре

### Минимальные требования

- **CPU**: 4 ядра (2.4 GHz+)
- **RAM**: 8 GB
- **Диск**: 100 GB SSD
- **Сеть**: 100 Mbps
- **ОС**: Ubuntu 20.04+ / CentOS 8+

### Рекомендуемые требования

- **CPU**: 8 ядер (3.0 GHz+)
- **RAM**: 16 GB
- **Диск**: 500 GB NVMe SSD
- **Сеть**: 1 Gbps
- **ОС**: Ubuntu 22.04 LTS

### Облачные требования

#### AWS
- **EC2**: t3.large (2 vCPU, 8 GB RAM)
- **RDS**: db.t3.micro (PostgreSQL)
- **ElastiCache**: cache.t3.micro (Redis)
- **S3**: Для хранения файлов
- **CloudFront**: CDN

#### Google Cloud
- **Compute Engine**: e2-standard-2
- **Cloud SQL**: PostgreSQL
- **Memorystore**: Redis
- **Cloud Storage**: Для файлов
- **Cloud CDN**: CDN

#### Azure
- **VM**: Standard_D2s_v3
- **Azure SQL**: PostgreSQL
- **Azure Cache**: Redis
- **Blob Storage**: Для файлов
- **CDN**: Azure CDN

## ☁️ Облачное развертывание

### AWS развертывание

```bash
# 1. Настройка AWS CLI
aws configure

# 2. Создание инфраструктуры с Terraform
cd terraform/aws
terraform init
terraform plan
terraform apply

# 3. Развертывание приложения
cd cloud/aws
docker-compose -f docker-compose.aws.yml up -d
```

### Google Cloud развертывание

```bash
# 1. Настройка gcloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Развертывание
cd cloud/gcp
docker-compose -f docker-compose.gcp.yml up -d
```

### Azure развертывание

```bash
# 1. Настройка Azure CLI
az login
az account set --subscription YOUR_SUBSCRIPTION

# 2. Развертывание
cd cloud/azure
docker-compose -f docker-compose.azure.yml up -d
```

## 🐳 Kubernetes развертывание

### Подготовка кластера

```bash
# Создание namespace
kubectl apply -f k8s/namespace.yaml

# Создание ConfigMap и Secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Развертывание приложений
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

### Масштабирование

```bash
# Автоматическое масштабирование
kubectl autoscale deployment legal-bot-deployment --cpu-percent=70 --min=2 --max=10

# Ручное масштабирование
kubectl scale deployment legal-bot-deployment --replicas=5
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# Автоматический деплой при push в main
name: Deploy to Production
on:
  push:
    branches: [main]
```

### AWS CodePipeline

```bash
# Создание pipeline
aws codepipeline create-pipeline --cli-input-json file://pipeline-definition.json
```

### Мониторинг деплоя

- **GitHub Actions**: https://github.com/your-repo/actions
- **AWS CodePipeline**: AWS Console → CodePipeline
- **Slack уведомления**: Настроены автоматически

## 📈 Масштабирование

### Горизонтальное масштабирование

```bash
# Docker Swarm
docker service scale legal-bot=5

# Kubernetes
kubectl scale deployment legal-bot-deployment --replicas=5

# Docker Compose
docker-compose -f scaling/docker-compose.scale.yml up -d
```

### Вертикальное масштабирование

```bash
# Увеличение ресурсов
docker-compose -f docker-compose.prod.yml up -d --scale legal-bot=3
```

### Автоматическое масштабирование

```bash
# Настройка HPA
kubectl apply -f k8s/hpa.yaml

# Мониторинг
kubectl get hpa
```

## 🔒 Безопасность

### WAF (Web Application Firewall)

```bash
# Установка ModSecurity
apt-get install libapache2-mod-security2

# Конфигурация
cp security/waf/nginx-waf.conf /etc/nginx/nginx.conf
nginx -t && systemctl reload nginx
```

### Fail2ban

```bash
# Установка
apt-get install fail2ban

# Конфигурация
cp security/fail2ban/jail.local /etc/fail2ban/jail.local
systemctl restart fail2ban
```

### SSL/TLS сертификаты

```bash
# Let's Encrypt
certbot --nginx -d legal-bot.com

# Автоматическое обновление
crontab -e
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### Мониторинг безопасности

```bash
# Запуск security monitor
python3 security/monitoring/security-monitor.py
```

## 📊 Мониторинг

### Prometheus

```bash
# Запуск Prometheus
docker-compose -f monitoring/prometheus/prometheus.prod.yml up -d

# Проверка метрик
curl http://localhost:9090/api/v1/query?query=up
```

### Grafana

```bash
# Доступ к дашбордам
http://your-domain:3000
# Логин: admin
# Пароль: из переменной окружения GRAFANA_PASSWORD
```

### Алерты

```bash
# Настройка Alertmanager
docker-compose -f monitoring/alertmanager/alertmanager.yml up -d

# Проверка алертов
curl http://localhost:9093/api/v1/alerts
```

### Дашборды

- **Общий обзор**: Legal Bot - Production Overview
- **Безопасность**: Legal Bot - Security Monitoring
- **Производительность**: Legal Bot - Performance Metrics

## 💾 Резервное копирование

### Автоматические бэкапы

```bash
# Настройка расписания
crontab -e
# 0 2 * * * /scripts/backup.sh

# Ручной бэкап
./scripts/backup.sh
```

### Восстановление

```bash
# Восстановление базы данных
./scripts/restore.sh --database backup_2024-01-01.sql

# Восстановление файлов
./scripts/restore.sh --files backup_2024-01-01.tar.gz
```

### Мониторинг бэкапов

```bash
# Проверка статуса
./scripts/check_backups.sh

# Логи бэкапов
tail -f /var/log/backup.log
```

## 🔧 Обслуживание

### Обновления

```bash
# Обновление приложения
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build

# Обновление зависимостей
pip install -r requirements.txt --upgrade
```

### Логи

```bash
# Просмотр логов
docker-compose logs -f legal-bot

# Ротация логов
logrotate /etc/logrotate.d/legal-bot
```

### Производительность

```bash
# Оптимизация базы данных
psql -d legal_bot -c "VACUUM ANALYZE;"

# Очистка кэша Redis
redis-cli FLUSHALL
```

### Здоровье системы

```bash
# Проверка здоровья
curl http://your-domain/health

# Метрики системы
curl http://your-domain/metrics
```

## 🚨 Устранение неполадок

### Частые проблемы

1. **Высокая нагрузка на CPU**
   ```bash
   # Проверка процессов
   top
   # Масштабирование
   docker-compose scale legal-bot=5
   ```

2. **Проблемы с памятью**
   ```bash
   # Проверка использования памяти
   free -h
   # Очистка кэша
   redis-cli FLUSHALL
   ```

3. **Ошибки базы данных**
   ```bash
   # Проверка подключений
   psql -d legal_bot -c "SELECT * FROM pg_stat_activity;"
   # Перезапуск PostgreSQL
   docker-compose restart postgres
   ```

4. **Проблемы с сетью**
   ```bash
   # Проверка портов
   netstat -tulpn
   # Проверка DNS
   nslookup your-domain.com
   ```

### Контакты поддержки

- **Email**: support@legal-bot.com
- **Slack**: #legal-bot-support
- **Документация**: https://docs.legal-bot.com
- **GitHub Issues**: https://github.com/your-repo/issues

## 📚 Дополнительные ресурсы

- [Документация API](API_DOCUMENTATION.md)
- [Руководство разработчика](DEVELOPER_GUIDE.md)
- [Архитектурные решения](ARCHITECTURE_DECISIONS.md)
- [Чек-лист безопасности](SECURITY_CHECKLIST.md)
- [Метрики и KPI](METRICS_AND_KPI.md)

---

**Версия документации**: 1.0  
**Последнее обновление**: 2024-01-01  
**Поддерживаемые версии**: Legal Bot 2.0+ 