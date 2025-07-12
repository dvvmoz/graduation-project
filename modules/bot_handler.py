"""
Модуль для обработки сообщений Telegram бота.
"""
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
import config
from .knowledge_base import search_relevant_docs, get_knowledge_base
from .llm_service import get_answer

logger = logging.getLogger(__name__)

class LegalBot:
    """Класс для управления юридическим ботом."""
    
    def __init__(self):
        """Инициализирует бота."""
        self.bot = Bot(token=config.TELEGRAM_TOKEN)
        self.dp = Dispatcher()
        self._setup_handlers()
        logger.info("Бот инициализирован")
    
    def _setup_handlers(self):
        """Настраивает обработчики сообщений."""
        # Обработчик команды /start
        self.dp.message.register(self.handle_start, Command("start"))
        
        # Обработчик команды /help
        self.dp.message.register(self.handle_help, Command("help"))
        
        # Обработчик команды /stats
        self.dp.message.register(self.handle_stats, Command("stats"))
        
        # Обработчик всех текстовых сообщений
        self.dp.message.register(self.handle_question, F.text)
    
    async def handle_start(self, message: Message):
        """
        Обрабатывает команду /start.
        
        Args:
            message: Сообщение от пользователя
        """
        welcome_text = """
🤖 **Добро пожаловать в ЮрПомощник!**

Я ваш персональный юридический ассистент, готовый помочь с правовыми вопросами.

**Что я умею:**
📋 Отвечаю на юридические вопросы
📚 Ссылаюсь на конкретные законы и нормативные акты
📝 Даю пошаговые рекомендации
⚖️ Помогаю разобраться в правовых процедурах

**Как пользоваться:**
Просто напишите ваш вопрос обычным языком.

**Доступные команды:**
/help - справка по использованию
/stats - статистика базы знаний

⚠️ **Важно:** Мои ответы носят информационный характер. Для решения серьезных правовых вопросов обратитесь к квалифицированному юристу.

Задайте свой первый вопрос! 👇
"""
        try:
            await message.answer(welcome_text, parse_mode="Markdown")
            logger.info(f"Пользователь {message.from_user.id} запустил бота")
        except TelegramAPIError as e:
            logger.error(f"Ошибка отправки приветствия: {e}")
    
    async def handle_help(self, message: Message):
        """
        Обрабатывает команду /help.
        
        Args:
            message: Сообщение от пользователя
        """
        help_text = """
📖 **Справка по использованию ЮрПомощника**

**Примеры вопросов:**
• "Какие документы нужны для регистрации ИП?"
• "Как оформить договор купли-продажи?"
• "Что делать при увольнении?"
• "Какие права у потребителя?"

**Советы для лучших результатов:**
✅ Формулируйте вопросы конкретно
✅ Указывайте контекст (например, "для физического лица")
✅ Задавайте по одному вопросу за раз

**Что я НЕ делаю:**
❌ Не заменяю профессиональную юридическую консультацию
❌ Не составляю документы
❌ Не даю советы по незаконным действиям

**Команды:**
/start - главное меню
/help - эта справка
/stats - информация о базе знаний

❓ Если у вас есть вопросы, просто спросите!
"""
        try:
            await message.answer(help_text, parse_mode="Markdown")
            logger.info(f"Пользователь {message.from_user.id} запросил справку")
        except TelegramAPIError as e:
            logger.error(f"Ошибка отправки справки: {e}")
    
    async def handle_stats(self, message: Message):
        """
        Обрабатывает команду /stats.
        
        Args:
            message: Сообщение от пользователя
        """
        try:
            kb = get_knowledge_base()
            stats = kb.get_collection_stats()
            
            stats_text = f"""
📊 **Статистика базы знаний**

📚 Всего документов: {stats.get('total_documents', 0)}
🗂️ Коллекция: {stats.get('collection_name', 'N/A')}
💾 Путь к БД: {stats.get('db_path', 'N/A')}

✅ Бот готов отвечать на ваши вопросы!
"""
            await message.answer(stats_text, parse_mode="Markdown")
            logger.info(f"Пользователь {message.from_user.id} запросил статистику")
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            await message.answer("Извините, не удалось получить статистику.")
    
    async def handle_question(self, message: Message):
        """
        Обрабатывает вопросы пользователя.
        
        Args:
            message: Сообщение от пользователя
        """
        user_question = message.text
        user_id = message.from_user.id
        
        logger.info(f"Получен вопрос от пользователя {user_id}: {user_question[:100]}...")
        
        try:
            # Отправляем сообщение о том, что обрабатываем запрос
            processing_msg = await message.answer("🔍 Ищу информацию по вашему вопросу...")
            
            # Ищем релевантные документы в базе знаний
            relevant_docs = search_relevant_docs(user_question, n_results=config.MAX_RESULTS)
            
            if not relevant_docs:
                no_info_response = """
😔 К сожалению, я не нашел информации по вашему вопросу в своей базе знаний.

**Попробуйте:**
• Переформулировать вопрос
• Задать более конкретный вопрос
• Уточнить сферу права

**Пример:** вместо "Что делать?" спросите "Что делать при увольнении?"

Или обратитесь к квалифицированному юристу для получения персональной консультации.
"""
                await processing_msg.edit_text(no_info_response, parse_mode="Markdown")
                return
            
            # Генерируем ответ с помощью LLM
            answer = get_answer(user_question, relevant_docs)
            
            # Отправляем ответ пользователю
            await processing_msg.edit_text(answer, parse_mode="Markdown")
            
            logger.info(f"Ответ отправлен пользователю {user_id}")
            
        except TelegramAPIError as e:
            logger.error(f"Ошибка Telegram API: {e}")
            await message.answer("Извините, произошла ошибка при отправке ответа.")
        except Exception as e:
            logger.error(f"Неожиданная ошибка при обработке вопроса: {e}")
            error_response = """
😔 Произошла техническая ошибка при обработке вашего запроса.

Пожалуйста, попробуйте:
• Переформулировать вопрос
• Задать вопрос позже
• Обратиться в поддержку

Приносим извинения за неудобства!
"""
            await message.answer(error_response)
    
    async def start_polling(self):
        """Запускает бота в режиме polling."""
        try:
            logger.info("Запуск бота в режиме polling...")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Ошибка при запуске polling: {e}")
            raise
    
    async def stop(self):
        """Останавливает бота."""
        await self.bot.session.close()
        logger.info("Бот остановлен")

# Глобальный экземпляр бота
_bot_instance = None

def get_bot() -> LegalBot:
    """Возвращает глобальный экземпляр бота."""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = LegalBot()
    return _bot_instance

def start_bot():
    """Запускает бота."""
    import asyncio
    
    bot = get_bot()
    
    try:
        asyncio.run(bot.start_polling())
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise
    finally:
        logger.info("Бот завершает работу") 