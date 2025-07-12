# 🛠️ Веб-панель администратора ЮрПомощника

## 🎯 Описание

Веб-панель администратора предоставляет удобный интерфейс для управления системой ЮрПомощника через браузер. Панель включает мониторинг системы, управление процессами, просмотр логов и выполнение административных команд.

## 🚀 Быстрый запуск

### Через Telegram бота
1. Запустите основного бота: `python main.py`
2. Отправьте команду `/admin` в Telegram
3. Следуйте инструкциям для запуска панели

### Прямой запуск
**Windows:**
```bash
start_admin_panel.bat
```

**Linux/macOS:**
```bash
./start_admin_panel.sh
```

**Или вручную:**
```bash
python admin_panel.py
```

## 🔑 Доступ к панели

- **URL:** http://127.0.0.1:5000
- **Логин:** admin
- **Пароль:** admin123

⚠️ **Важно:** Обязательно смените пароль по умолчанию в production!

## 📊 Возможности панели

### 🎛️ Дашборд
- Системная статистика в реальном времени
- Мониторинг CPU и памяти
- Статистика базы знаний
- Счетчик файлов логов
- Быстрые действия

### 📈 Статистика
- Детальная системная информация
- Статистика процессов
- Информация о дисковом пространстве
- Сетевая статистика

### 📋 Логи
- Просмотр файлов логов:
  - `bot.log` - основной лог бота
  - `scraping.log` - логи скрапинга
  - `admin_panel.log` - логи админ-панели
  - `populate_db.log` - логи наполнения БД
  - `incremental_scraping.log` - логи инкрементального скрапинга
  - `dynamic_search.log` - логи динамического поиска
- Терминальный интерфейс для просмотра
- Автообновление логов

### 🔧 Команды
Выполнение административных команд:
- **populate_db** - Наполнение базы знаний из документов
- **scrape_websites** - Скрапинг веб-сайтов
- **update_documents** - Обновление документов
- **demo_bot** - Запуск демо-бота
- **test_demo** - Тестирование системы

### ⚙️ Процессы
- Мониторинг запущенных процессов
- Просмотр stdout/stderr
- Статус выполнения
- Время выполнения
- Коды возврата

### 📁 Документы
- Управление базой знаний
- Просмотр статистики документов
- Информация о коллекциях

## 🛡️ Безопасность

### Аутентификация
- SHA-256 хеширование паролей
- Сессионная аутентификация
- Защита всех API маршрутов

### Настройка безопасности
1. Создайте файл `.env` если его нет
2. Добавьте переменную для хешированного пароля:
```env
ADMIN_PASSWORD_HASH=ваш_хеш_пароля
```

3. Для генерации хеша пароля используйте:
```python
import hashlib
password = "ваш_новый_пароль"
hash_value = hashlib.sha256(password.encode()).hexdigest()
print(f"ADMIN_PASSWORD_HASH={hash_value}")
```

### Настройка ID администраторов
Для команды `/admin` в Telegram боте:
```env
ADMIN_IDS=123456789,987654321
```

## 🌐 API Endpoints

### Основные маршруты
- `GET /` - Главная страница (перенаправление на логин)
- `GET /login` - Страница входа
- `POST /login` - Аутентификация
- `GET /logout` - Выход из системы
- `GET /dashboard` - Главная панель

### API маршруты
- `GET /api/stats` - Системная статистика
- `GET /api/logs` - Список файлов логов
- `GET /api/logs/<filename>` - Содержимое лог-файла
- `POST /api/execute` - Выполнение команды
- `GET /api/processes` - Список процессов

### WebSocket
- `/socket.io/` - Real-time уведомления

## 🔧 Технические детали

### Стек технологий
- **Backend:** Flask 3.0.0
- **WebSocket:** Flask-SocketIO
- **Frontend:** Bootstrap 5, Font Awesome
- **Мониторинг:** psutil
- **Безопасность:** Flask-CORS

### Архитектура
```
admin_panel.py          # Основной сервер
├── AdminPanel         # Класс управления системой
├── admin_auth.py      # Система аутентификации
├── templates/admin/   # HTML шаблоны
│   ├── index.html     # Главная панель
│   └── login.html     # Страница входа
└── static/           # Статические файлы (CSS, JS)
```

### Системные требования
- Python 3.8+
- Flask 3.0.0+
- 512MB RAM (минимум)
- 10MB дискового пространства

## 🐳 Развертывание

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "admin_panel.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  admin-panel:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ADMIN_PASSWORD_HASH=your_hash_here
    volumes:
      - ./db:/app/db
      - ./logs:/app/logs
```

### Nginx (Production)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📝 Логирование

Панель ведет собственный лог `admin_panel.log` со следующими событиями:
- Входы/выходы пользователей
- Выполнение команд
- Системные ошибки
- WebSocket соединения

## 🔍 Мониторинг

### Системные метрики
- CPU usage (%)
- Memory usage (%)
- Disk usage (%)
- Network I/O
- Процессы системы

### Метрики приложения
- Количество документов в базе знаний
- Размеры файлов логов
- Активные процессы
- Время работы системы

## 🚨 Устранение неполадок

### Панель не запускается
1. Проверьте наличие всех зависимостей: `pip install -r requirements.txt`
2. Убедитесь что порт 5000 свободен
3. Проверьте права доступа к файлам

### Ошибки аутентификации
1. Проверьте правильность логина/пароля
2. Убедитесь что ADMIN_PASSWORD_HASH корректен
3. Очистите cookies браузера

### Проблемы с WebSocket
1. Проверьте настройки CORS
2. Убедитесь что JavaScript включен
3. Проверьте консоль браузера на ошибки

## 📚 Дополнительные ресурсы

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.0/)
- [Font Awesome Icons](https://fontawesome.com/icons)

## 🎉 Готово!

Веб-панель администратора готова к использованию. Откройте http://127.0.0.1:5000 в браузере и войдите с учетными данными admin/admin123.

Для получения ссылки на панель в Telegram боте используйте команду `/admin`. 