#!/usr/bin/env python3
"""
Комплексное тестирование системы ЮрПомощника РБ
Проверяет все компоненты: конфигурацию, модули, ML фильтр, базу знаний
"""

import os
import sys
import logging
import importlib
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemTester:
    """Класс для комплексного тестирования системы."""
    
    def __init__(self):
        self.test_results = {}
        self.errors = []
        self.warnings = []
        
    def test_configuration(self):
        """Тестирует конфигурацию системы."""
        logger.info("🔧 Тестирование конфигурации...")
        
        try:
            # Проверяем наличие основных файлов
            required_files = [
                'config.py',
                'main.py',
                'modules/bot_handler.py',
                'requirements.txt'
            ]
            
            for file_path in required_files:
                if os.path.exists(file_path):
                    logger.info(f"✅ {file_path} - найден")
                else:
                    logger.error(f"❌ {file_path} - НЕ НАЙДЕН")
                    self.errors.append(f"Файл {file_path} отсутствует")
            
            # Проверяем конфигурацию
            try:
                import config
                logger.info("✅ Модуль config импортирован успешно")
            except Exception as e:
                logger.error(f"❌ Ошибка импорта config: {e}")
                self.errors.append(f"Ошибка импорта config: {e}")
            
            # Проверяем переменные окружения
            env_file = '.env'
            if not os.path.exists(env_file):
                logger.warning(f"⚠️ Файл {env_file} не найден, создаем тестовый...")
                self.create_test_env()
            
            self.test_results['configuration'] = len(self.errors) == 0
            
        except Exception as e:
            logger.error(f"❌ Ошибка тестирования конфигурации: {e}")
            self.errors.append(f"Ошибка тестирования конфигурации: {e}")
            self.test_results['configuration'] = False
    
    def test_modules(self):
        """Тестирует основные модули системы."""
        logger.info("📦 Тестирование модулей...")
        
        modules_to_test = [
            'modules.bot_handler',
            'modules.knowledge_base',
            'modules.llm_service',
            'modules.web_scraper',
            'modules.ml_question_filter',
            'modules.text_processing'
        ]
        
        for module_name in modules_to_test:
            try:
                module = importlib.import_module(module_name)
                logger.info(f"✅ {module_name} - импортирован успешно")
            except Exception as e:
                logger.error(f"❌ Ошибка импорта {module_name}: {e}")
                self.errors.append(f"Ошибка импорта {module_name}: {e}")
        
        self.test_results['modules'] = len([e for e in self.errors if 'модуля' in e]) == 0
    
    def test_ml_filter(self):
        """Тестирует ML фильтр вопросов."""
        logger.info("🤖 Тестирование ML фильтра...")
        
        try:
            from modules.ml_question_filter import is_legal_question_ml
            
            # Тестовые вопросы
            test_questions = [
                "Как зарегистрировать ИП в Беларуси?",
                "Какая погода сегодня?",
                "Как оформить трудовой договор?",
                "Что приготовить на ужин?",
                "Какие документы нужны для развода?",
                "Какой фильм посмотреть?"
            ]
            
            legal_count = 0
            for question in test_questions:
                try:
                    is_legal = is_legal_question_ml(question)
                    if is_legal:
                        legal_count += 1
                        logger.info(f"✅ '{question}' - юридический вопрос")
                    else:
                        logger.info(f"❌ '{question}' - не юридический вопрос")
                except Exception as e:
                    logger.error(f"❌ Ошибка обработки вопроса '{question}': {e}")
                    self.errors.append(f"Ошибка ML фильтра для '{question}': {e}")
            
            accuracy = legal_count / len(test_questions) * 100
            logger.info(f"📊 Точность ML фильтра: {accuracy:.1f}%")
            
            self.test_results['ml_filter'] = accuracy >= 80  # Ожидаем минимум 80%
            
        except Exception as e:
            logger.error(f"❌ Ошибка тестирования ML фильтра: {e}")
            self.errors.append(f"Ошибка тестирования ML фильтра: {e}")
            self.test_results['ml_filter'] = False
    
    def test_knowledge_base(self):
        """Тестирует базу знаний."""
        logger.info("📚 Тестирование базы знаний...")
        
        try:
            from modules.knowledge_base import get_knowledge_base
            
            # Проверяем доступность базы знаний
            kb = get_knowledge_base()
            if kb:
                logger.info("✅ База знаний доступна")
                self.test_results['knowledge_base'] = True
            else:
                logger.warning("⚠️ База знаний недоступна")
                self.warnings.append("База знаний недоступна")
                self.test_results['knowledge_base'] = False
                
        except Exception as e:
            logger.error(f"❌ Ошибка тестирования базы знаний: {e}")
            self.errors.append(f"Ошибка тестирования базы знаний: {e}")
            self.test_results['knowledge_base'] = False
    
    def test_dependencies(self):
        """Тестирует зависимости проекта."""
        logger.info("📋 Тестирование зависимостей...")
        
        try:
            import aiogram
            import openai
            import chromadb
            import numpy
            import sklearn
            import pandas
            
            logger.info("✅ Все основные зависимости доступны")
            self.test_results['dependencies'] = True
            
        except ImportError as e:
            logger.error(f"❌ Ошибка импорта зависимостей: {e}")
            self.errors.append(f"Ошибка импорта зависимостей: {e}")
            self.test_results['dependencies'] = False
    
    def test_docker_config(self):
        """Тестирует Docker конфигурацию."""
        logger.info("🐳 Тестирование Docker конфигурации...")
        
        docker_files = [
            'Dockerfile',
            'Dockerfile.prod',
            'docker-compose.prod.yml',
            'docker-compose.test.yml'
        ]
        
        all_exist = True
        for file_path in docker_files:
            if os.path.exists(file_path):
                logger.info(f"✅ {file_path} - найден")
            else:
                logger.warning(f"⚠️ {file_path} - НЕ НАЙДЕН")
                all_exist = False
        
        self.test_results['docker_config'] = all_exist
    
    def create_test_env(self):
        """Создает тестовый .env файл."""
        try:
            env_content = """# Test Configuration для ЮрПомощника
TELEGRAM_TOKEN=test_token_for_local_testing
OPENAI_API_KEY=test_openai_key_for_local_testing
SECRET_KEY=test_secret_key_for_local_development_only_32chars
ADMIN_PASSWORD=test_admin_password
CHROMA_DB_PATH=db/chroma
LOG_LEVEL=INFO
MAX_TOKENS=2000
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000
"""
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
            logger.info("✅ Создан тестовый .env файл")
        except Exception as e:
            logger.error(f"❌ Ошибка создания .env файла: {e}")
    
    def run_all_tests(self):
        """Запускает все тесты."""
        logger.info("🚀 Начинаем комплексное тестирование системы...")
        
        self.test_configuration()
        self.test_dependencies()
        self.test_modules()
        self.test_ml_filter()
        self.test_knowledge_base()
        self.test_docker_config()
        
        self.print_results()
    
    def print_results(self):
        """Выводит результаты тестирования."""
        logger.info("\n" + "="*60)
        logger.info("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        logger.info("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        
        for test_name, result in self.test_results.items():
            status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
            logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
        
        logger.info(f"\n📈 Общий результат: {passed_tests}/{total_tests} тестов пройдено")
        
        if self.errors:
            logger.info(f"\n❌ ОШИБКИ ({len(self.errors)}):")
            for error in self.errors:
                logger.info(f"  - {error}")
        
        if self.warnings:
            logger.info(f"\n⚠️ ПРЕДУПРЕЖДЕНИЯ ({len(self.warnings)}):")
            for warning in self.warnings:
                logger.info(f"  - {warning}")
        
        if passed_tests == total_tests:
            logger.info("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Система готова к работе.")
        else:
            logger.info(f"\n⚠️ {total_tests - passed_tests} тестов провалено. Требуется исправление.")

def main():
    """Главная функция."""
    tester = SystemTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 