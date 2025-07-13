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
from modules.user_analytics import get_analytics
from modules.ml_analytics_integration import get_analytics_summary
from admin_auth import setup_auth_routes, require_auth
from scripts.populate_db import populate_from_directory, update_document_file
from scripts.scrape_websites import scrape_multiple_sites, get_legal_sites_list
from scripts.update_documents import update_all_documents

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
                'test_demo': ['python', 'test_demo.py'],
                'full_update': ['python', 'quick_update_knowledge_base.py', '--automated'],
                'check_knowledge_base': ['python', 'check_knowledge_base.py']
            }
            
            if command not in allowed_commands:
                return {'error': f'Команда {command} не разрешена'}
            
            cmd = allowed_commands[command] + args
            process_id = f"{command}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Специальная обработка для demo_bot - запуск в отдельном терминале
            if command == 'demo_bot':
                try:
                    if os.name == 'nt':  # Windows
                        # Запуск в новом окне командной строки
                        subprocess.Popen(
                            ['cmd', '/c', 'start', 'cmd', '/k', 'python', 'demo_bot.py'],
                            cwd=os.getcwd(),
                            creationflags=subprocess.CREATE_NEW_CONSOLE
                        )
                    else:  # Linux/macOS
                        # Пробуем разные терминалы
                        terminals = [
                            ['gnome-terminal', '--', 'python', 'demo_bot.py'],
                            ['xterm', '-e', 'python', 'demo_bot.py'],
                            ['konsole', '-e', 'python', 'demo_bot.py'],
                            ['x-terminal-emulator', '-e', 'python', 'demo_bot.py']
                        ]
                        
                        terminal_launched = False
                        for terminal_cmd in terminals:
                            try:
                                subprocess.Popen(terminal_cmd, cwd=os.getcwd())
                                terminal_launched = True
                                break
                            except FileNotFoundError:
                                continue
                        
                        if not terminal_launched:
                            # Fallback: запуск в фоне с выводом в лог
                            return self._run_background_process(cmd, process_id)
                    
                    return {
                        'success': True,
                        'process_id': process_id,
                        'message': 'Демо-бот запущен в отдельном терминале'
                    }
                    
                except Exception as e:
                    logger.error(f"Ошибка запуска демо-бота в терминале: {e}")
                    # Fallback: запуск в фоне
                    return self._run_background_process(cmd, process_id)
            
            # Для остальных команд - запуск в фоне
            return self._run_background_process(cmd, process_id)
            
        except Exception as e:
            logger.error(f"Ошибка выполнения команды {command}: {e}")
            return {'error': str(e)}
    
    def _run_background_process(self, cmd, process_id):
        """Запуск процесса в фоне."""
        # Запуск процесса в фоне
        def run_process():
            try:
                # Для Windows устанавливаем кодировку консоли
                env = os.environ.copy()
                if os.name == 'nt':  # Windows
                    env['PYTHONIOENCODING'] = 'utf-8'
                    env['PYTHONLEGACYWINDOWSSTDIO'] = '0'
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',  # Заменяем проблемные символы
                    timeout=300,  # 5 минут таймаут
                    env=env,
                    shell=True if os.name == 'nt' else False  # Для Windows используем shell
                )
                
                # Сохраняем исходные данные и обновляем статус
                original_data = running_processes.get(process_id, {})
                running_processes[process_id] = {
                    **original_data,  # Сохраняем все исходные данные
                    'status': 'completed',
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'command': ' '.join(cmd),
                    'finished_at': datetime.now().isoformat()
                }
                
                # Отправляем обновление через WebSocket
                socketio.emit('process_completed', {
                    'process_id': process_id,
                    'status': 'completed',
                    'returncode': result.returncode
                })
                
            except subprocess.TimeoutExpired:
                # Сохраняем исходные данные и обновляем статус
                original_data = running_processes.get(process_id, {})
                running_processes[process_id] = {
                    **original_data,  # Сохраняем все исходные данные
                    'status': 'timeout',
                    'error': 'Процесс превысил время ожидания (5 минут)'
                }
            except Exception as e:
                # Сохраняем исходные данные и обновляем статус
                original_data = running_processes.get(process_id, {})
                running_processes[process_id] = {
                    **original_data,  # Сохраняем все исходные данные
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
            'started_at': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'process_id': process_id,
            'message': f'Команда {" ".join(cmd)} запущена в фоне'
        }
    
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

# ML Analytics API endpoints
@app.route('/api/ml-analytics/summary')
@require_auth
def get_ml_analytics_summary():
    """API для получения сводки аналитики ML-фильтра."""
    try:
        summary = get_analytics_summary()
        return jsonify({'success': True, 'summary': summary})
    except Exception as e:
        logger.error(f"Ошибка получения сводки ML-аналитики: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ml-analytics/stats')
@require_auth
def get_ml_analytics_stats():
    """API для получения детальной статистики ML-фильтра."""
    try:
        days = request.args.get('days', 30, type=int)
        analytics = get_analytics()
        stats = analytics.get_analytics_summary(days=days)
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        logger.error(f"Ошибка получения статистики ML-аналитики: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ml-analytics/low-confidence')
@require_auth
def get_low_confidence_questions():
    """API для получения вопросов с низкой уверенностью."""
    try:
        threshold = request.args.get('threshold', 0.7, type=float)
        limit = request.args.get('limit', 50, type=int)
        analytics = get_analytics()
        questions = analytics.get_low_confidence_questions(threshold=threshold, limit=limit)
        return jsonify({'success': True, 'questions': questions})
    except Exception as e:
        logger.error(f"Ошибка получения вопросов с низкой уверенностью: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ml-analytics/export')
@require_auth
def export_training_data():
    """API для экспорта данных для дообучения."""
    try:
        min_confidence = request.args.get('min_confidence', 0.8, type=float)
        filename = f"ml_training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        analytics = get_analytics()
        success = analytics.export_training_data(filename, min_confidence=min_confidence)
        
        if success:
            return jsonify({'success': True, 'filename': filename, 'message': 'Данные экспортированы успешно'})
        else:
            return jsonify({'success': False, 'error': 'Ошибка экспорта данных'}), 500
    except Exception as e:
        logger.error(f"Ошибка экспорта данных: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ml-analytics/categories')
@require_auth
def get_question_categories():
    """API для получения распределения вопросов по категориям."""
    try:
        days = request.args.get('days', 30, type=int)
        analytics = get_analytics()
        
        import sqlite3
        conn = sqlite3.connect(analytics.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT question_category, COUNT(*) as count
            FROM user_questions 
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY question_category 
            ORDER BY count DESC
        """.format(days))
        
        categories = [{'category': row[0], 'count': row[1]} for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'categories': categories})
    except Exception as e:
        logger.error(f"Ошибка получения категорий: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# === API для управления базой знаний ===

@app.route('/api/knowledge-base/status')
@require_auth
def get_knowledge_base_status():
    """Получение статуса базы знаний"""
    try:
        kb = get_knowledge_base()
        stats = kb.get_collection_stats()
        
        # Проверка папки с документами
        docs_dir = Path("data/documents")
        doc_files = []
        if docs_dir.exists():
            doc_files = list(docs_dir.glob("*.pdf")) + list(docs_dir.glob("*.docx")) + list(docs_dir.glob("*.doc"))
        
        # Получение списка сайтов
        sites = get_legal_sites_list()
        
        return jsonify({
            'success': True,
            'database': {
                'total_documents': stats.get('total_documents', 0),
                'db_path': stats.get('db_path', 'не указан'),
                'collection_name': stats.get('collection_name', 'не указана')
            },
            'documents': {
                'total_files': len(doc_files),
                'files': [{'name': f.name, 'size': f.stat().st_size} for f in doc_files[:10]]
            },
            'sites': {
                'total_sites': len(sites),
                'sites': sites[:10]
            }
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения статуса базы знаний: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/knowledge-base/test-search', methods=['POST'])
@require_auth
def test_knowledge_base_search():
    """Тестирование поиска в базе знаний"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'Пустой запрос'}), 400
        
        kb = get_knowledge_base()
        results = kb.search_relevant_docs(query, n_results=3)
        
        formatted_results = []
        for i, doc in enumerate(results):
            formatted_results.append({
                'rank': i + 1,
                'distance': doc.get('distance', 1.0),
                'source': doc.get('metadata', {}).get('source_file', 'неизвестен'),
                'content': doc.get('content', '')[:200] + '...' if len(doc.get('content', '')) > 200 else doc.get('content', '')
            })
        
        # Проверка необходимости динамического поиска
        should_search, _ = kb.should_use_dynamic_search(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': formatted_results,
            'total_found': len(results),
            'should_use_dynamic_search': should_search,
            'quality_assessment': 'низкое' if should_search else 'хорошее'
        })
        
    except Exception as e:
        logger.error(f"Ошибка тестирования поиска: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/knowledge-base/update-documents', methods=['POST'])
@require_auth
def update_documents_endpoint():
    """Обновление документов в базе знаний"""
    try:
        logger.info("Начинаем обновление документов...")
        
        # Запускаем в фоновом режиме
        process_id = "update_documents"
        admin_panel.execute_command("update_documents", process_id=process_id)
        
        return jsonify({
            'success': True,
            'message': 'Обновление документов запущено',
            'process_id': process_id
        })
        
    except Exception as e:
        logger.error(f"Ошибка обновления документов: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/knowledge-base/scrape-websites', methods=['POST'])
@require_auth
def scrape_websites_endpoint():
    """Скрапинг сайтов для обновления базы знаний"""
    try:
        data = request.get_json()
        max_sites = data.get('max_sites', 5)
        max_pages = data.get('max_pages', 10)
        
        logger.info(f"Начинаем скрапинг {max_sites} сайтов по {max_pages} страниц...")
        
        # Запускаем в фоновом режиме
        process_id = "scrape_websites"
        admin_panel.execute_command("scrape_websites", 
                                   args={'max_sites': max_sites, 'max_pages': max_pages},
                                   process_id=process_id)
        
        return jsonify({
            'success': True,
            'message': f'Скрапинг запущен для {max_sites} сайтов',
            'process_id': process_id
        })
        
    except Exception as e:
        logger.error(f"Ошибка скрапинга сайтов: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/knowledge-base/full-update', methods=['POST'])
@require_auth
def full_knowledge_base_update():
    """Полное обновление базы знаний"""
    try:
        logger.info("Начинаем полное обновление базы знаний...")
        
        # Запускаем в фоновом режиме
        process_id = "full_update"
        admin_panel.execute_command("full_update", process_id=process_id)
        
        return jsonify({
            'success': True,
            'message': 'Полное обновление базы знаний запущено',
            'process_id': process_id
        })
        
    except Exception as e:
        logger.error(f"Ошибка полного обновления: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/knowledge-base/clear', methods=['POST'])
@require_auth
def clear_knowledge_base():
    """Очистка базы знаний"""
    try:
        data = request.get_json()
        confirmation = data.get('confirmation', False)
        
        if not confirmation:
            return jsonify({'success': False, 'error': 'Необходимо подтверждение'}), 400
        
        kb = get_knowledge_base()
        success = kb.clear_collection()
        
        if success:
            logger.info("База знаний очищена")
            return jsonify({'success': True, 'message': 'База знаний очищена успешно'})
        else:
            return jsonify({'success': False, 'error': 'Ошибка при очистке базы знаний'}), 500
            
    except Exception as e:
        logger.error(f"Ошибка очистки базы знаний: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/knowledge-base/analyze-quality')
@require_auth
def analyze_knowledge_base_quality():
    """Анализ качества базы знаний"""
    try:
        kb = get_knowledge_base()
        
        # Тестовые запросы
        test_queries = [
            "регистрация ИП",
            "налоговые льготы", 
            "трудовые отношения",
            "пенсия по возрасту",
            "семейное право",
            "уголовная ответственность",
            "договор купли-продажи",
            "права потребителей"
        ]
        
        results = []
        good_quality_count = 0
        avg_distances = []
        
        for query in test_queries:
            search_results = kb.search_relevant_docs(query, n_results=3)
            
            if search_results:
                avg_distance = sum(doc.get('distance', 1.0) for doc in search_results) / len(search_results)
                avg_distances.append(avg_distance)
                
                if avg_distance < 0.5:
                    good_quality_count += 1
                    quality = "хорошее"
                elif avg_distance < 0.8:
                    quality = "удовлетворительное"
                else:
                    quality = "низкое"
                
                results.append({
                    'query': query,
                    'quality': quality,
                    'distance': avg_distance,
                    'results_count': len(search_results)
                })
            else:
                results.append({
                    'query': query,
                    'quality': "нет результатов",
                    'distance': 1.0,
                    'results_count': 0
                })
        
        # Общая статистика
        total_queries = len(test_queries)
        quality_percentage = (good_quality_count / total_queries) * 100
        overall_avg_distance = sum(avg_distances) / len(avg_distances) if avg_distances else 1.0
        
        return jsonify({
            'success': True,
            'overall_stats': {
                'total_queries': total_queries,
                'good_quality_count': good_quality_count,
                'quality_percentage': quality_percentage,
                'overall_avg_distance': overall_avg_distance,
                'recommendation': 'отличное' if quality_percentage >= 80 else 'удовлетворительное' if quality_percentage >= 60 else 'требует улучшения'
            },
            'detailed_results': results
        })
        
    except Exception as e:
        logger.error(f"Ошибка анализа качества: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

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