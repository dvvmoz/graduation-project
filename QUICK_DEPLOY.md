# ⚡ Быстрое развертывание ЮрПомощника

## 🎯 За 5 минут до продакшена

### 1. Подготовка сервера (1 минута)

```bash
# Получите сервер с минимальными требованиями:
# - 4GB RAM, 2 CPU, 20GB SSD
# - Ubuntu 20.04+
# - Публичный IP
```

### 2. Автоматическое развертывание (3 минуты)

#### Linux/macOS:
```bash
git clone https://github.com/your-repo/legal-assistant-bot.git
cd legal-assistant-bot
chmod +x deploy.sh
./deploy.sh
```

#### Windows:
```cmd
git clone https://github.com/your-repo/legal-assistant-bot.git
cd legal-assistant-bot
deploy.bat
```

### 3. Настройка API ключей (1 минута)

Отредактируйте файл `.env.prod`:
```env
TELEGRAM_TOKEN=ваш_telegram_token
OPENAI_API_KEY=ваш_openai_key
ADMIN_PASSWORD=ваш_админ_пароль
```

## ✅ Готово!

Ваши сервисы доступны по адресам:
- **Бот**: работает в Telegram
- **Админ-панель**: `https://ваш-ip/admin/`
- **Мониторинг**: `http://ваш-ip:3000/`

## 🔧 Полезные команды

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Остановка
docker-compose -f docker-compose.prod.yml down

# Обновление
git pull && docker-compose -f docker-compose.prod.yml up -d --build
```

## 📞 Нужна помощь?

- Полная документация: [DEPLOYMENT.md](DEPLOYMENT.md)
- Устранение неполадок: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Issues: [GitHub Issues](https://github.com/your-repo/issues) 