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
from .web_scraper import create_scraper_from_config

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
        
        # Обработчик команды /scrape
        self.dp.message.register(self.handle_scrape, Command("scrape"))
        
        # Обработчик всех текстовых сообщений
        self.dp.message.register(self.handle_question, F.text)
    
    async def handle_start(self, message: Message):
        """
        Обрабатывает команду /start.
        
        Args:
            message: Сообщение от пользователя
        """
        welcome_text = """
🤖 **Добро пожаловать в ЮрПомощник РБ!**

Я ваш персональный юридический ассистент по законодательству Республики Беларусь.

🇧🇾 **Специализация:**
📋 Белорусское законодательство и правоприменение
📚 Кодексы, законы и подзаконные акты РБ
📝 Пошаговые рекомендации по белорусскому праву
⚖️ Процедуры в государственных органах РБ

**Что я знаю:**
• Гражданское право РБ
• Трудовое законодательство
• Хозяйственное право
• Административные процедуры
• Семейное право
• Жилищное законодательство

**Как пользоваться:**
Просто напишите ваш вопрос обычным языком.

**Доступные команды:**
/help - справка по использованию
/stats - статистика базы знаний
/scrape - скрапинг сайтов (только для администраторов)

⚠️ **Важно:** Консультации основаны на законодательстве РБ. Не заменяют персональную юридическую помощь.

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
📖 **Справка по использованию ЮрПомощника РБ**

🇧🇾 **Примеры вопросов по белорусскому праву:**
• "Как зарегистрировать ИП в Беларуси?"
• "Какие документы нужны для развода в РБ?"
• "Как оформить трудовой договор по ТК РБ?"
• "Какие права у потребителя в Беларуси?"
• "Как получить разрешение на строительство?"
• "Что делать при увольнении в РБ?"

**Советы для лучших результатов:**
✅ Формулируйте вопросы конкретно
✅ Указывайте контекст (для ИП, организации, гражданина)
✅ Уточняйте регион (Минск, области РБ)
✅ Задавайте по одному вопросу за раз

**Что я НЕ делаю:**
❌ Не заменяю профессиональную юридическую консультацию
❌ Не составляю документы
❌ Не даю советы по незаконным действиям
❌ Не консультирую по российскому праву

**Специализация:**
• Гражданское право РБ (ГК РБ)
• Трудовое право (ТК РБ)
• Хозяйственное право (ХК РБ)
• Административное право (КоАП РБ)
• Семейное право (КоБС РБ)

**Команды:**
/start - главное меню
/help - эта справка
/stats - информация о базе знаний
/scrape - скрапинг сайтов (только для администраторов)

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
            
            stats_text = f"""📊 Статистика базы знаний

📚 Всего документов: {stats.get('total_documents', 0)}
🗂️ Коллекция: {stats.get('collection_name', 'N/A')}
💾 Путь к БД: {stats.get('db_path', 'N/A')}

✅ Бот готов отвечать на ваши вопросы!"""
            
            await message.answer(stats_text)
            logger.info(f"Пользователь {message.from_user.id} запросил статистику")
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            await message.answer("Извините, не удалось получить статистику.")
    
    async def handle_scrape(self, message: Message):
        """
        Обрабатывает команду /scrape для веб-скрапинга.
        
        Args:
            message: Сообщение от пользователя
        """
        try:
            # Проверяем права администратора (можно настроить список разрешенных ID)
            admin_ids = [123456789]  # Замените на реальные ID администраторов
            
            if message.from_user.id not in admin_ids:
                await message.answer("⛔ У вас нет прав для выполнения этой команды.")
                return
            
            # Парсим аргументы команды
            args = message.text.split()[1:]  # Убираем /scrape
            
            if not args:
                help_text = """
🔍 **Команда скрапинга сайтов**

**Использование:**
`/scrape <URL> [количество_страниц]`

**Примеры:**
• `/scrape https://www.garant.ru/ 10`
• `/scrape https://www.consultant.ru/ 5`

**Параметры:**
• URL - адрес сайта для скрапинга
• количество_страниц - максимум страниц (по умолчанию 20)

⚠️ **Внимание:** Скрапинг может занять время!
"""
                await message.answer(help_text, parse_mode="Markdown")
                return
            
            url = args[0]
            max_pages = int(args[1]) if len(args) > 1 else 20
            
            # Проверяем валидность URL
            if not url.startswith(('http://', 'https://')):
                await message.answer("❌ Неверный формат URL. Используйте полный адрес с http:// или https://")
                return
            
            # Отправляем сообщение о начале скрапинга
            status_msg = await message.answer(f"🚀 Начинаю скрапинг сайта: {url}\n⏳ Это может занять несколько минут...")
            
            # Выполняем скрапинг
            scraper = create_scraper_from_config()
            result = scraper.scrape_and_add(url, max_pages)
            
            if result['success']:
                success_text = f"""
✅ **Скрапинг завершен успешно!**

📄 Обработано страниц: {result['pages_scraped']}
📝 Добавлено чанков: {result['chunks_added']}
🌐 Сайт: {result['start_url']}

База знаний пополнена! Теперь бот знает больше.
"""
                await status_msg.edit_text(success_text, parse_mode="Markdown")
            else:
                error_text = f"""
❌ **Ошибка скрапинга**

🔍 Сайт: {url}
⚠️ Причина: {result['message']}

Попробуйте:
• Проверить доступность сайта
• Уменьшить количество страниц
• Использовать другой URL
"""
                await status_msg.edit_text(error_text, parse_mode="Markdown")
            
            logger.info(f"Пользователь {message.from_user.id} выполнил скрапинг {url}")
            
        except ValueError:
            await message.answer("❌ Неверный формат количества страниц. Используйте число.")
        except Exception as e:
            logger.error(f"Ошибка при скрапинге: {e}")
            await message.answer("😔 Произошла ошибка при скрапинге. Попробуйте позже.")
    
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
            
            # Отправляем ответ пользователю (без Markdown чтобы избежать ошибок парсинга)
            await processing_msg.edit_text(answer)
            
            logger.info(f"Ответ отправлен пользователю {user_id}")
            
        except TelegramAPIError as e:
            logger.error(f"Ошибка Telegram API: {e}")
            # Если ошибка парсинга, отправляем ответ без форматирования
            try:
                answer = get_answer(user_question, relevant_docs)
                await message.answer(answer)
            except:
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