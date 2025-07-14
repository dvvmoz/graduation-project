# ⚡ Быстрый старт Legal Bot в продакшене (15 минут)

## 🎯 Цель
Развернуть Legal Bot в продакшене за 15 минут с полной инфраструктурой.

## 📋 Предварительные требования

- Docker и Docker Compose установлены
- Домен настроен (например, legal-bot.com)
- SSL сертификат (Let's Encrypt)
- Минимум 4 GB RAM, 2 CPU

## 🚀 Быстрый деплой

### 1. Клонирование репозитория (1 мин)
```bash
git clone https://github.com/your-repo/legal-bot.git
cd legal-bot
```

### 2. Настройка переменных окружения (2 мин)
```bash
# Копирование шаблона
cp env.prod.example .env.prod

# Редактирование конфигурации
nano .env.prod
```

**Обязательные переменные:**
```bash
ENVIRONMENT=production
DOMAIN=legal-bot.com
DATABASE_URL=postgresql://user:password@localhost:5432/legal_bot
JWT_SECRET=your-super-secret-jwt-key
OPENAI_API_KEY=your-openai-api-key
REDIS_PASSWORD=your-redis-password
GRAFANA_PASSWORD=admin123
```

### 3. Запуск продакшн-инфраструктуры (5 мин)
```bash
# Запуск всех сервисов
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

### 4. Настройка SSL сертификата (3 мин)
```bash
# Установка Certbot
apt-get update && apt-get install -y certbot

# Получение SSL сертификата
certbot --nginx -d legal-bot.com

# Автоматическое обновление
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

### 5. Проверка работоспособности (2 мин)
```bash
# Проверка здоровья приложения
curl https://legal-bot.com/health

# Проверка метрик
curl https://legal-bot.com/metrics

# Проверка Grafana
# Откройте https://legal-bot.com:3000
# Логин: admin, Пароль: admin123
```

### 6. Настройка мониторинга (2 мин)
```bash
# Импорт дашбордов в Grafana
# 1. Откройте Grafana
# 2. Импортируйте monitoring/grafana/dashboards/legal-bot-overview.json
# 3. Импортируйте monitoring/grafana/dashboards/security-monitoring.json
```

## ✅ Проверка развертывания

### Основные эндпоинты
- **Приложение**: https://legal-bot.com
- **API**: https://legal-bot.com/api
- **Мониторинг**: https://legal-bot.com:3000
- **Метрики**: https://legal-bot.com/metrics
- **Здоровье**: https://legal-bot.com/health

### Проверка логов
```bash
# Логи приложения
docker-compose -f docker-compose.prod.yml logs legal-bot

# Логи Nginx
docker-compose -f docker-compose.prod.yml logs nginx

# Логи базы данных
docker-compose -f docker-compose.prod.yml logs postgres
```

### Проверка производительности
```bash
# Нагрузочное тестирование
ab -n 1000 -c 10 https://legal-bot.com/health

# Проверка метрик
curl https://legal-bot.com/metrics | grep legal_bot
```

## 🔧 Быстрые команды

### Управление сервисами
```bash
# Остановка
docker-compose -f docker-compose.prod.yml down

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Обновление
docker-compose -f docker-compose.prod.yml up -d --build
```

### Масштабирование
```bash
# Увеличение количества экземпляров
docker-compose -f docker-compose.prod.yml up -d --scale legal-bot=3

# Проверка масштабирования
docker-compose -f docker-compose.prod.yml ps
```

### Резервное копирование
```bash
# Создание бэкапа
./scripts/backup.sh

# Восстановление
./scripts/restore.sh --database backup.sql
```

## 🚨 Экстренные действия

### Если приложение не отвечает
```bash
# Перезапуск приложения
docker-compose -f docker-compose.prod.yml restart legal-bot

# Проверка логов
docker-compose -f docker-compose.prod.yml logs -f legal-bot
```

### Если база данных недоступна
```bash
# Перезапуск PostgreSQL
docker-compose -f docker-compose.prod.yml restart postgres

# Проверка подключений
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d legal_bot
```

### Если высокое потребление ресурсов
```bash
# Масштабирование
docker-compose -f docker-compose.prod.yml up -d --scale legal-bot=5

# Очистка кэша
docker-compose -f docker-compose.prod.yml exec redis redis-cli FLUSHALL
```

## 📊 Мониторинг

### Grafana дашборды
1. **Production Overview**: Общий обзор системы
2. **Security Monitoring**: Мониторинг безопасности
3. **Performance Metrics**: Метрики производительности

### Ключевые метрики
- **Response Time**: < 500ms
- **Error Rate**: < 1%
- **CPU Usage**: < 80%
- **Memory Usage**: < 85%
- **Disk Usage**: < 90%

## 🔒 Безопасность

### Проверка безопасности
```bash
# Проверка SSL
curl -I https://legal-bot.com

# Проверка заголовков безопасности
curl -I https://legal-bot.com | grep -E "(X-Frame-Options|X-Content-Type-Options|X-XSS-Protection)"

# Проверка WAF
curl -X POST https://legal-bot.com/api/test -d "<script>alert('xss')</script>"
```

### Обновление паролей
```bash
# Обновление JWT секрета
docker-compose -f docker-compose.prod.yml down
# Измените JWT_SECRET в .env.prod
docker-compose -f docker-compose.prod.yml up -d
```

## 📞 Поддержка

### Полезные команды
```bash
# Статус всех сервисов
docker-compose -f docker-compose.prod.yml ps

# Использование ресурсов
docker stats

# Логи всех сервисов
docker-compose -f docker-compose.prod.yml logs

# Проверка сети
docker network ls
```

### Контакты
- **Email**: support@legal-bot.com
- **Slack**: #legal-bot-support
- **Документация**: https://docs.legal-bot.com

---

**Время развертывания**: 15 минут  
**Версия**: Legal Bot 2.0  
**Поддержка**: 24/7 