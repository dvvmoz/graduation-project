#!/usr/bin/env python3
"""
Тестирование Telegram бота без реального API
Проверяет все компоненты бота в изолированной среде
"""

import asyncio
import logging
from unittest.mock import Mock, AsyncMock
from modules.bot_handler import LegalBot
from modules.ml_question_filter import is_legal_question_ml
from modules.knowledge_base import get_knowledge_base
from modules.llm_service import get_answer

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MockMessage:
    """Мок объект для имитации сообщения Telegram."""
    
    def __init__(self, text: str, user_id: int = 123456789):
        self.text = text
        self.from_user = Mock()
        self.from_user.id = user_id
        self.from_user.first_name = "Test"
        self.from_user.last_name = "User"
        self.from_user.username = "testuser"
        self.chat = Mock()
        self.chat.id = user_id
        self.chat.type = "private"
    
    async def answer(self, text: str, **kwargs):
        """Мок метод для ответа на сообщение."""
        logger.info(f"🤖 БОТ ОТВЕТИЛ: {text[:100]}...")
        return Mock()

class BotTester:
    """Класс для тестирования бота."""
    
    def __init__(self):
        self.test_results = {}
        self.errors = []
        
    async def test_ml_filter(self):
        """Тестирует ML фильтр вопросов."""
        logger.info("🤖 Тестирование ML фильтра...")
        
        test_questions = [
            ("Как зарегистрировать ИП в Беларуси?", True),
            ("Какая погода сегодня?", False),
            ("Как оформить трудовой договор?", True),
            ("Что приготовить на ужин?", False),
            ("Какие документы нужны для развода?", True),
            ("Какой фильм посмотреть?", False),
            ("Какие права у потребителя в РБ?", True),
            ("Как получить разрешение на строительство?", True),
        ]
        
        correct_predictions = 0
        for question, expected in test_questions:
            try:
                result_tuple = is_legal_question_ml(question)
                # Извлекаем булево значение из кортежа (bool, float, str)
                result = result_tuple[0] if isinstance(result_tuple, tuple) else result_tuple
                status = "✅" if result == expected else "❌"
                logger.info(f"{status} '{question}' -> {result_tuple} (ожидалось: {expected})")
                if result == expected:
                    correct_predictions += 1
            except Exception as e:
                logger.error(f"❌ Ошибка обработки '{question}': {e}")
                self.errors.append(f"Ошибка ML фильтра для '{question}': {e}")
        
        accuracy = correct_predictions / len(test_questions) * 100
        logger.info(f"📊 Точность ML фильтра: {accuracy:.1f}%")
        self.test_results['ml_filter'] = accuracy >= 80
        
    async def test_knowledge_base(self):
        """Тестирует базу знаний."""
        logger.info("📚 Тестирование базы знаний...")
        
        try:
            kb = get_knowledge_base()
            if kb:
                logger.info("✅ База знаний доступна")
                
                # Тестируем поиск - используем правильный метод
                test_query = "регистрация ИП"
                try:
                    results = kb.search_relevant_docs(test_query, n_results=3)
                    logger.info(f"✅ Поиск работает, найдено {len(results)} результатов")
                    self.test_results['knowledge_base'] = True
                except Exception as e:
                    logger.error(f"❌ Ошибка поиска: {e}")
                    self.test_results['knowledge_base'] = False
            else:
                logger.warning("⚠️ База знаний недоступна")
                self.test_results['knowledge_base'] = False
                
        except Exception as e:
            logger.error(f"❌ Ошибка тестирования базы знаний: {e}")
            self.errors.append(f"Ошибка тестирования базы знаний: {e}")
            self.test_results['knowledge_base'] = False
    
    async def test_llm_service(self):
        """Тестирует LLM сервис."""
        logger.info("🧠 Тестирование LLM сервиса...")
        
        try:
            # Тестовый запрос
            test_question = "Как зарегистрировать ИП в Беларуси?"
            test_context = "Для регистрации ИП в Беларуси необходимо подать заявление в налоговую инспекцию."
            
            response = get_answer(test_question, test_context)
            if response and len(response) > 10:
                logger.info(f"✅ LLM сервис работает, получен ответ длиной {len(response)} символов")
                self.test_results['llm_service'] = True
            else:
                logger.warning("⚠️ LLM сервис вернул пустой ответ")
                self.test_results['llm_service'] = False
                
        except Exception as e:
            logger.error(f"❌ Ошибка тестирования LLM сервиса: {e}")
            self.errors.append(f"Ошибка тестирования LLM сервиса: {e}")
            self.test_results['llm_service'] = False
    
    async def test_bot_handlers(self):
        """Тестирует обработчики бота."""
        logger.info("🤖 Тестирование обработчиков бота...")
        
        try:
            # Создаем мок бота
            bot = LegalBot()
            
            # Тестируем команду /start
            start_message = MockMessage("/start")
            await bot.handle_start(start_message)
            
            # Тестируем команду /help
            help_message = MockMessage("/help")
            await bot.handle_help(help_message)
            
            # Тестируем команду /stats
            stats_message = MockMessage("/stats")
            await bot.handle_stats(stats_message)
            
            logger.info("✅ Обработчики команд работают")
            self.test_results['bot_handlers'] = True
            
        except Exception as e:
            logger.error(f"❌ Ошибка тестирования обработчиков бота: {e}")
            self.errors.append(f"Ошибка тестирования обработчиков бота: {e}")
            self.test_results['bot_handlers'] = False
    
    async def test_question_processing(self):
        """Тестирует обработку вопросов."""
        logger.info("❓ Тестирование обработки вопросов...")
        
        test_questions = [
            "Как зарегистрировать ИП?",
            "Какие документы нужны для развода?",
            "Как оформить трудовой договор?",
            "Какие права у потребителя?",
        ]
        
        try:
            bot = LegalBot()
            
            for question in test_questions:
                message = MockMessage(question)
                await bot.handle_question(message)
            
            logger.info("✅ Обработка вопросов работает")
            self.test_results['question_processing'] = True
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки вопросов: {e}")
            self.errors.append(f"Ошибка обработки вопросов: {e}")
            self.test_results['question_processing'] = False
    
    async def run_all_tests(self):
        """Запускает все тесты."""
        logger.info("🚀 Начинаем тестирование Telegram бота...")
        
        await self.test_ml_filter()
        await self.test_knowledge_base()
        await self.test_llm_service()
        await self.test_bot_handlers()
        await self.test_question_processing()
        
        self.print_results()
    
    def print_results(self):
        """Выводит результаты тестирования."""
        logger.info("\n" + "="*60)
        logger.info("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ БОТА")
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
        
        if passed_tests == total_tests:
            logger.info("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Бот готов к работе.")
        else:
            logger.info(f"\n⚠️ {total_tests - passed_tests} тестов провалено. Требуется исправление.")

async def main():
    """Главная функция."""
    tester = BotTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 