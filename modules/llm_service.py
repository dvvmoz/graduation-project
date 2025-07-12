"""
Модуль для взаимодействия с языковыми моделями (LLM).
"""
import logging
from typing import List
from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL, MAX_TOKENS
from .scraping_tracker import get_scraping_summary

logger = logging.getLogger(__name__)

# Глобальная переменная для клиента OpenAI (инициализируется при первом использовании)
client = None

def get_system_prompt() -> str:
    """Возвращает системный промпт с информацией о последнем парсинге."""
    current_date = datetime.now().strftime("%d.%m.%Y")
    scraping_info = get_scraping_summary()
    
    return f"""Вы — ведущий юрист-консультант с 15+ годами практики в правовой системе Республики Беларусь. Отвечайте на юридические вопросы, руководствуясь следующей методологией:

1. Системный анализ запроса:
   - Определите:
     • Отрасль права (с обоснованием выбора)
     • Юридическую значимость вопроса
     • Уровень подготовки спрашивающего (новичок/студент/профессионал)
   - Проверьте актуальность на {current_date} с учетом:
     ✓ Последних изменений законодательства
     ✓ Текущей правоприменительной практики

2. Многоуровневая экспертиза:
   • Обязательные элементы:
     1) Ссылки на конкретные нормы (Кодексы/Законы/Подзаконные акты)
     2) Судебная практика за последние 3 года
     3) Альтернативные точки зрения (при наличии)
   • Шкала достоверности:
     100% - прямая норма закона
     80% - устойчивая судебная практика
     60% - доктринальное толкование

3. Адаптивный ответ:
   [Для граждан]
   - Итоговый вывод (до 10 слов)
   - Объяснение "на пальцах" (3-5 предложений)
   - Чек-лист действий

   [Для специалистов]
   - Глубокий анализ с:
     • Разбором коллизий
     • Сравнением с международным опытом
     • Прогнозом развития регулирования

4. Превентивная безопасность:
   ! Важно: автоматически проверять:
   - Соответствие Конституции РБ
   - Отсутствие конфликта интересов
   - Возможные риски применения советов

⚖️ Гарантии качества:
• Ежедневная сверка с Национальным правовым порталом
• Маркировка спорных вопросов (⚡️Требует уточнения)
• Механизм обратной связи для коррекции

 Дисклеймер:
Ответы соответствуют законодательству РБ на дату: {scraping_info}
Не заменяют персональную консультацию (ст. 1014 ГК РБ)
"""

class LLMService:
    """Сервис для работы с языковыми моделями."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Инициализирует сервис.
        
        Args:
            model: Название модели OpenAI
        """
        self.model = model
        self.client = None
        logger.info(f"Инициализирован LLM сервис с моделью: {model}")
    
    def _get_client(self):
        """Получает клиент OpenAI, инициализируя его при необходимости."""
        if self.client is None:
            if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("ВАШ_") or OPENAI_API_KEY.startswith("sk-test"):
                raise ValueError(
                    "Необходимо настроить валидный OPENAI_API_KEY в файле .env. "
                    "Получите ключ на https://platform.openai.com/api-keys"
                )
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        return self.client
    
    def get_answer(self, user_question: str, context_docs: List[str]) -> str:
        """
        Генерирует ответ на основе вопроса пользователя и контекста.
        
        Args:
            user_question: Вопрос пользователя
            context_docs: Список релевантных документов из базы знаний
            
        Returns:
            Сгенерированный ответ
        """
        try:
            # Формируем контекст из найденных документов
            context = self._format_context(context_docs)
            
            # Формируем полный промпт для пользователя
            user_prompt = self._create_user_prompt(user_question, context)
            
            # Отправляем запрос к OpenAI
            response = self._get_client().chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=0.3,  # Низкая температура для более точных ответов
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Логируем статистику использования токенов
            usage = response.usage
            logger.info(f"Использовано токенов: {usage.total_tokens} "
                       f"(промпт: {usage.prompt_tokens}, ответ: {usage.completion_tokens})")
            
            return answer
            
        except Exception as e:
            logger.error(f"Ошибка при генерации ответа: {e}")
            return self._get_error_response()
    
    def _format_context(self, docs: List[str]) -> str:
        """
        Форматирует документы в контекст для промпта.
        
        Args:
            docs: Список документов
            
        Returns:
            Отформатированный контекст
        """
        if not docs:
            return "Релевантная информация в базе знаний не найдена."
        
        formatted_docs = []
        for i, doc in enumerate(docs, 1):
            formatted_docs.append(f"Документ {i}:\n{doc}")
        
        return "\n\n".join(formatted_docs)
    
    def _create_user_prompt(self, question: str, context: str) -> str:
        """
        Создает промпт для пользователя.
        
        Args:
            question: Вопрос пользователя
            context: Контекст из базы знаний
            
        Returns:
            Сформированный промпт
        """
        # Получаем информацию о парсинге для включения в ответ
        scraping_info = get_scraping_summary()
        
        return f"""
Вопрос пользователя: "{question}"

Информация из базы знаний:
{context}

ЗАДАЧА: Ответьте на вопрос пользователя, строго следуя методологии из системного промпта:

1. СИСТЕМНЫЙ АНАЛИЗ:
   - Определите отрасль права и обоснуйте выбор
   - Оцените юридическую значимость вопроса
   - Определите уровень подготовки пользователя (новичок/студент/профессионал)

2. МНОГОУРОВНЕВАЯ ЭКСПЕРТИЗА:
   - Приведите ссылки на конкретные нормы (статьи, кодексы, законы)
   - Укажите шкалу достоверности (100%/80%/60%)
   - Отметьте альтернативные точки зрения, если есть

3. АДАПТИВНЫЙ ОТВЕТ:
   - Для граждан: итоговый вывод + объяснение + чек-лист действий
   - Для специалистов: глубокий анализ с разбором коллизий

4. ПРЕВЕНТИВНАЯ БЕЗОПАСНОСТЬ:
   - Проверьте соответствие Конституции РБ
   - Укажите возможные риски применения советов

ВАЖНО: Обязательно завершите свой ответ следующим дисклеймером:
"⚖️ Ответ соответствует законодательству РБ на дату: {scraping_info}. Не заменяет персональную консультацию (ст. 1014 ГК РБ)."
"""
    
    def _get_error_response(self) -> str:
        """
        Возвращает сообщение об ошибке для пользователя.
        
        Returns:
            Сообщение об ошибке
        """
        return """
😔 Извините, произошла техническая ошибка при обработке вашего запроса.

Пожалуйста, попробуйте:
1. Переформулировать вопрос
2. Задать более конкретный вопрос
3. Обратиться позже

Если проблема повторяется, свяжитесь с технической поддержкой.
"""
    
    def get_model_info(self) -> dict:
        """
        Возвращает информацию о текущей модели.
        
        Returns:
            Информация о модели
        """
        return {
            "model": self.model,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.3
        }

# Глобальный экземпляр сервиса
_llm_service = None

def get_llm_service() -> LLMService:
    """Возвращает глобальный экземпляр LLM сервиса."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service

def get_answer(user_question: str, context_docs: List[str]) -> str:
    """
    Удобная функция для получения ответа.
    
    Args:
        user_question: Вопрос пользователя
        context_docs: Контекст из базы знаний
        
    Returns:
        Ответ от языковой модели
    """
    return get_llm_service().get_answer(user_question, context_docs) 