#!/usr/bin/env python3
"""
Демо-версия юридического бота для тестирования без реальных API ключей.
"""
import logging
import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.knowledge_base import search_relevant_docs, get_knowledge_base

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DemoLegalAssistant:
    """Демо-версия юридического ассистента без OpenAI."""
    
    def __init__(self):
        """Инициализирует демо-ассистента."""
        self.knowledge_base = get_knowledge_base()
        logger.info("Демо-ассистент инициализирован")
    
    def get_demo_answer(self, user_question: str) -> str:
        """
        Генерирует демо-ответ на основе найденных документов.
        
        Args:
            user_question: Вопрос пользователя
            
        Returns:
            Демо-ответ
        """
        try:
            # Ищем релевантные документы
            relevant_docs = search_relevant_docs(user_question, n_results=3)
            
            if not relevant_docs:
                return self._get_no_info_response()
            
            # Формируем демо-ответ
            response = self._format_demo_response(user_question, relevant_docs)
            return response
            
        except Exception as e:
            logger.error(f"Ошибка при генерации демо-ответа: {e}")
            return self._get_error_response()
    
    def _format_demo_response(self, question: str, docs: list) -> str:
        """Форматирует демо-ответ."""
        # Укорачиваем документы для читаемости
        short_docs = []
        for doc in docs[:2]:  # Берем только первые 2 документа
            if len(doc) > 150:
                short_doc = doc[:150] + "..."
            else:
                short_doc = doc
            short_docs.append(short_doc)
        
        response = f"""
📋 **Демо-ответ на вопрос:** "{question}"

🔍 **Найдено в базе знаний:**

{chr(10).join([f"• {doc}" for doc in short_docs])}

📝 **Демо-рекомендации:**
1. Изучите найденные документы выше
2. Обратитесь к соответствующим статьям закона
3. При необходимости проконсультируйтесь с юристом

⚠️ **Важно:** Это демо-версия. Для получения полноценных ответов с анализом ИИ настройте OpenAI API ключ в файле .env

📚 **База знаний содержит:** {self.knowledge_base.get_collection_stats().get('total_documents', 0)} документов
"""
        return response
    
    def _get_no_info_response(self) -> str:
        """Ответ когда информация не найдена."""
        return """
😔 К сожалению, информация по вашему вопросу не найдена в базе знаний.

**Попробуйте:**
• Переформулировать вопрос
• Задать более конкретный вопрос
• Добавить больше PDF документов в папку data/

⚠️ **Это демо-версия** - для полноценной работы настройте API ключи.
"""
    
    def _get_error_response(self) -> str:
        """Ответ при ошибке."""
        return """
😔 Произошла ошибка при обработке запроса.

⚠️ **Это демо-версия** - для полноценной работы настройте OpenAI API ключ.
"""

def interactive_demo():
    """Интерактивная демо-сессия."""
    print("=" * 60)
    print("🤖 ДЕМО-ВЕРСИЯ ЮРИДИЧЕСКОГО АССИСТЕНТА")
    print("=" * 60)
    
    try:
        assistant = DemoLegalAssistant()
        kb_stats = assistant.knowledge_base.get_collection_stats()
        print(f"📚 База знаний содержит: {kb_stats.get('total_documents', 0)} документов")
        print("💡 Это демо без ИИ - показывает только поиск в базе знаний")
        print("\n" + "=" * 60)
        
        example_questions = [
            "налоги",
            "документы для регистрации",
            "права потребителя",
            "трудовой договор"
        ]
        
        print("📝 Примеры вопросов:")
        for i, q in enumerate(example_questions, 1):
            print(f"  {i}. {q}")
        
        print("\n" + "=" * 60)
        print("Введите ваш вопрос (или 'выход' для завершения):")
        
        while True:
            question = input("\n❓ Ваш вопрос: ").strip()
            
            if question.lower() in ['выход', 'exit', 'quit', 'q']:
                print("👋 До свидания!")
                break
            
            if not question:
                print("❌ Введите непустой вопрос")
                continue
            
            print("\n🔍 Поиск в базе знаний...")
            answer = assistant.get_demo_answer(question)
            print(answer)
            print("\n" + "-" * 60)
            
    except Exception as e:
        logger.error(f"Ошибка в демо-режиме: {e}")
        print(f"❌ Ошибка: {e}")

def test_search_functionality():
    """Тестирует функциональность поиска."""
    print("\n🧪 ТЕСТИРОВАНИЕ ФУНКЦИОНАЛЬНОСТИ ПОИСКА")
    print("=" * 60)
    
    try:
        assistant = DemoLegalAssistant()
        
        test_queries = [
            "налог",
            "документы",
            "регистрация",
            "несуществующий_термин_12345"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Тест запроса: '{query}'")
            docs = search_relevant_docs(query, n_results=2)
            if docs:
                print(f"✅ Найдено {len(docs)} документов")
                for i, doc in enumerate(docs, 1):
                    preview = doc[:100] + "..." if len(doc) > 100 else doc
                    print(f"  {i}. {preview}")
            else:
                print("❌ Документы не найдены")
                
    except Exception as e:
        logger.error(f"Ошибка в тестах: {e}")
        print(f"❌ Ошибка тестирования: {e}")

def main():
    """Главная функция демо."""
    print("🚀 Запуск демо-версии юридического ассистента...\n")
    
    # Проверяем наличие базы знаний
    try:
        kb = get_knowledge_base()
        stats = kb.get_collection_stats()
        if stats.get('total_documents', 0) == 0:
            print("❌ База знаний пуста!")
            print("📝 Запустите сначала: python scripts/populate_db.py")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения к базе знаний: {e}")
        return
    
    # Выбор режима
    print("Выберите режим:")
    print("1. Интерактивная демонстрация")
    print("2. Тестирование поиска")
    print("3. Оба режима")
    
    choice = input("\nВаш выбор (1-3): ").strip()
    
    if choice == "1":
        interactive_demo()
    elif choice == "2":
        test_search_functionality()
    elif choice == "3":
        test_search_functionality()
        interactive_demo()
    else:
        print("❌ Неверный выбор. Запуск интерактивной демонстрации...")
        interactive_demo()

if __name__ == "__main__":
    main() 