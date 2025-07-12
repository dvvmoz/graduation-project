#!/usr/bin/env python3
"""
Веб-панель администратора для ЮрПомощника.
"""
import os
import sys
import json
import logging
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import psutil

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.knowledge_base import get_knowledge_base
from modules.scraping_tracker import get_scraping_tracker
from admin_auth import setup_auth_routes, require_auth

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('admin_panel.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация Flask приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Глобальные переменные
running_processes = {}
log_files = [
    'bot.log',
    'scraping.log', 
    'admin_panel.log',
    'add_scraped_to_knowledge_base.log',
    'rebuild_knowledge_base.log',
    'test_caching_fixed.log'
]

class AdminPanel:
    """Класс для управления админ-панелью."""
    
    def __init__(self):
        """Инициализация админ-панели."""
        self.knowledge_base = None
        self.scraping_tracker = None
        self.init_services()
    
    def init_services(self):
        """Инициализация сервисов."""
        try:
            self.knowledge_base = get_knowledge_base()
            self.scraping_tracker = get_scraping_tracker()
            logger.info("Сервисы админ-панели инициализированы")
        except Exception as e:
            logger.error(f"Ошибка инициализации сервисов: {e}")
    
    def get_system_stats(self):
        """Получение системной статистики."""
        try:
            # Статистика системы
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            # Статистика базы знаний
            kb_stats = {}
            if self.knowledge_base:
                kb_stats = self.knowledge_base.get_collection_stats()
            
            # Статистика файлов логов
            log_stats = {}
            for log_file in log_files:
                if os.path.exists(log_file):
                    stat = os.stat(log_file)
                    log_stats[log_file] = {
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    }
            
            return {
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used': memory.used,
                    'memory_total': memory.total,
                    'disk_percent': disk.percent,
                    'disk_used': disk.used,
                    'disk_total': disk.total
                },
                'knowledge_base': kb_stats,
                'logs': log_stats,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {'error': str(e)}
    
    def get_log_content(self, log_file, lines=100):
        """Получение содержимого лог-файла."""
        try:
            if log_file not in log_files:
                return {'error': 'Недопустимый файл лога'}
            
            if not os.path.exists(log_file):
                return {'error': 'Файл лога не найден'}
            
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                
            return {
                'content': ''.join(recent_lines),
                'total_lines': len(all_lines),
                'shown_lines': len(recent_lines),
                'file': log_file
            }
        except Exception as e:
            logger.error(f"Ошибка чтения лога {log_file}: {e}")
            return {'error': str(e)}
    
    def execute_command(self, command, args=None):
        """Выполнение команды."""
        try:
            if args is None:
                args = []
            
            # Безопасность: разрешенные команды
            allowed_commands = {
                'populate_db': ['python', 'scripts/populate_db.py'],
                'scrape_websites': ['python', 'scripts/scrape_websites.py'],
                'update_documents': ['python', 'scripts/update_documents.py'],
                'demo_bot': ['python', 'demo_bot.py'],
                'test_demo': ['python', 'test_demo.py']
            }
            
            if command not in allowed_commands:
                return {'error': f'Команда {command} не разрешена'}
            
            cmd = allowed_commands[command] + args
            process_id = f"{command}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Запуск процесса в фоне
            def run_process():
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        timeout=300  # 5 минут таймаут
                    )
                    
                    running_processes[process_id] = {
                        'status': 'completed',
                        'returncode': result.returncode,
                        'stdout': result.stdout,
                        'stderr': result.stderr,
                        'command': ' '.join(cmd),
                        'finished_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Отправляем обновление через WebSocket
                    socketio.emit('process_completed', {
                        'process_id': process_id,
                        'status': 'completed',
                        'returncode': result.returncode
                    })
                    
                except subprocess.TimeoutExpired:
                    running_processes[process_id] = {
                        'status': 'timeout',
                        'error': 'Процесс превысил время ожидания (5 минут)'
                    }
                except Exception as e:
                    running_processes[process_id] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            # Запуск в отдельном потоке
            thread = threading.Thread(target=run_process)
            thread.daemon = True
            thread.start()
            
            running_processes[process_id] = {
                'status': 'running',
                'command': ' '.join(cmd),
                'started_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return {
                'success': True,
                'process_id': process_id,
                'message': f'Команда {command} запущена'
            }
            
        except Exception as e:
            logger.error(f"Ошибка выполнения команды {command}: {e}")
            return {'error': str(e)}
    
    def get_process_status(self, process_id=None):
        """Получение статуса процессов."""
        if process_id:
            return running_processes.get(process_id, {'error': 'Процесс не найден'})
        return running_processes

# Создание экземпляра админ-панели
admin = AdminPanel()

# Настройка аутентификации
setup_auth_routes(app)

@app.route('/')
@require_auth
def index():
    """Главная страница админ-панели."""
    return render_template('admin/index.html')

@app.route('/api/stats')
@require_auth
def get_stats():
    """API для получения статистики."""
    return jsonify(admin.get_system_stats())

@app.route('/api/logs/<log_file>')
@require_auth
def get_log(log_file):
    """API для получения содержимого лога."""
    lines = request.args.get('lines', 100, type=int)
    return jsonify(admin.get_log_content(log_file, lines))

@app.route('/api/logs')
@require_auth
def list_logs():
    """API для получения списка доступных логов."""
    available_logs = []
    for log_file in log_files:
        if os.path.exists(log_file):
            stat = os.stat(log_file)
            available_logs.append({
                'name': log_file,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify(available_logs)

@app.route('/api/execute', methods=['POST'])
@require_auth
def execute_command():
    """API для выполнения команд."""
    data = request.json
    command = data.get('command')
    args = data.get('args', [])
    
    if not command:
        return jsonify({'error': 'Команда не указана'}), 400
    
    result = admin.execute_command(command, args)
    return jsonify(result)

@app.route('/api/processes')
@require_auth
def get_processes():
    """API для получения статуса процессов."""
    return jsonify(admin.get_process_status())

@app.route('/api/processes/<process_id>')
@require_auth
def get_process(process_id):
    """API для получения статуса конкретного процесса."""
    return jsonify(admin.get_process_status(process_id))

@socketio.on('connect')
def handle_connect():
    """Обработка подключения WebSocket."""
    logger.info(f"Клиент подключился: {request.sid}")
    emit('connected', {'message': 'Подключение установлено'})

@socketio.on('disconnect')
def handle_disconnect():
    """Обработка отключения WebSocket."""
    logger.info(f"Клиент отключился: {request.sid}")

@socketio.on('subscribe_logs')
def handle_subscribe_logs(data):
    """Подписка на обновления логов."""
    log_file = data.get('log_file')
    if log_file in log_files:
        # Здесь можно добавить логику для отправки обновлений логов в реальном времени
        emit('log_subscribed', {'log_file': log_file})

def run_admin_panel(host='127.0.0.1', port=5000, debug=False):
    """Запуск админ-панели."""
    logger.info(f"Запуск админ-панели на http://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Веб-панель администратора ЮрПомощника')
    parser.add_argument('--host', default='127.0.0.1', help='Хост для запуска')
    parser.add_argument('--port', type=int, default=5000, help='Порт для запуска')
    parser.add_argument('--debug', action='store_true', help='Режим отладки')
    
    args = parser.parse_args()
    
    run_admin_panel(args.host, args.port, args.debug) 