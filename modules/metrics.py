from prometheus_client import Counter, Summary, start_http_server
import logging
import threading

REQUESTS = Counter('requests_total', 'Всего запросов к боту')
ERRORS = Counter('errors_total', 'Ошибки приложения')
RESPONSE_TIME = Summary('response_time_seconds', 'Время отклика бота')

_metrics_server_started = False

def start_metrics_server(port=8000):
    global _metrics_server_started
    if not _metrics_server_started:
        start_http_server(port)
        logging.info(f'Prometheus metrics endpoint доступен на :{port}/metrics')
        _metrics_server_started = True

def ensure_metrics_server(port=8000):
    # Запускает сервер метрик в отдельном потоке, если он ещё не запущен
    if not _metrics_server_started:
        threading.Thread(target=start_metrics_server, args=(port,), daemon=True).start() 