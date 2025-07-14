from prometheus_client import Counter, Summary, start_http_server
import logging
import threading

REQUESTS = Counter('requests_total', 'Всего запросов к боту')
ERRORS = Counter('errors_total', 'Ошибки приложения')
RESPONSE_TIME = Summary('response_time_seconds', 'Время отклика бота')
ML_ERRORS = Counter('ml_errors_total', 'Ошибки ML-фильтра')
ML_RESPONSE_TIME = Summary('ml_response_time_seconds', 'Время ответа ML-фильтра')
DB_ERRORS = Counter('db_errors_total', 'Ошибки базы данных')
SCRAPING_ERRORS = Counter('scraping_errors_total', 'Ошибки скрапинга')
DB_RESPONSE_TIME = Summary('db_response_time_seconds', 'Время ответа базы данных')
ACTIVE_USERS = Counter('active_users_total', 'Количество уникальных пользователей за сутки')

_metrics_server_started = False

def start_metrics_server(port=8000):
    global _metrics_server_started
    if not _metrics_server_started:
        start_http_server(port, addr="0.0.0.0")
        logging.info(f'Prometheus metrics endpoint доступен на 0.0.0.0:{port}/metrics')
        _metrics_server_started = True

def ensure_metrics_server(port=8000):
    # Запускает сервер метрик в отдельном потоке, если он ещё не запущен
    if not _metrics_server_started:
        threading.Thread(target=start_metrics_server, args=(port,), daemon=True).start() 