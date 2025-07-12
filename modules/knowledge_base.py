"""
Модуль для работы с базой знаний на основе ChromaDB.
"""
import os
import logging
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from config import CHROMA_DB_PATH

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Класс для управления базой знаний."""
    
    def __init__(self, collection_name: str = "legal_docs"):
        """
        Инициализирует базу знаний.
        
        Args:
            collection_name: Имя коллекции в ChromaDB
        """
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._initialize_db()
    
    def _initialize_db(self):
        """Инициализирует подключение к ChromaDB."""
        try:
            # Создаем директорию для базы данных, если она не существует
            os.makedirs(CHROMA_DB_PATH, exist_ok=True)
            
            # Инициализируем клиент ChromaDB
            self.client = chromadb.PersistentClient(
                path=CHROMA_DB_PATH,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Получаем или создаем коллекцию
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}  # Используем косинусное сходство
            )
            
            logger.info(f"✅ База знаний инициализирована: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации базы знаний: {e}")
            raise
    
    def add_document(self, doc_id: str, document_text: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Добавляет документ в базу знаний.
        
        Args:
            doc_id: Уникальный идентификатор документа
            document_text: Текст документа
            metadata: Метаданные документа
            
        Returns:
            True если документ добавлен успешно, False в противном случае
        """
        try:
            if not document_text or not document_text.strip():
                logger.warning(f"Пустой текст для документа {doc_id}")
                return False
            
            if metadata is None:
                metadata = {}
            
            # Добавляем текущее время и размер документа в метаданные
            metadata.update({
                "length": len(document_text),
                "doc_id": doc_id
            })
            
            self.collection.add(
                documents=[document_text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.debug(f"Документ {doc_id} добавлен в базу знаний")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка добавления документа {doc_id}: {e}")
            return False
    
    def search_relevant_docs(self, query_text: str, n_results: int = 3) -> List[str]:
        """
        Ищет релевантные документы по запросу.
        
        Args:
            query_text: Текст запроса для поиска
            n_results: Максимальное количество результатов
            
        Returns:
            Список найденных документов
        """
        try:
            if not query_text or not query_text.strip():
                logger.warning("Пустой запрос для поиска")
                return []
            
            # Получаем количество документов в коллекции
            collection_count = self.collection.count()
            if collection_count == 0:
                logger.warning("База знаний пуста")
                return []
            
            # Ограничиваем количество результатов доступным количеством документов
            n_results = min(n_results, collection_count)
            
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            documents = results.get('documents', [[]])[0]
            distances = results.get('distances', [[]])[0]
            
            # Фильтруем результаты по релевантности (расстояние < 0.8)
            relevant_docs = []
            for doc, distance in zip(documents, distances):
                if distance < 0.8:  # Порог релевантности
                    relevant_docs.append(doc)
            
            logger.info(f"Найдено {len(relevant_docs)} релевантных документов для запроса: '{query_text[:50]}...'")
            return relevant_docs
            
        except Exception as e:
            logger.error(f"Ошибка поиска документов: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Возвращает статистику коллекции.
        
        Returns:
            Словарь со статистикой
        """
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection_name,
                "db_path": CHROMA_DB_PATH
            }
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {"error": str(e)}
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Удаляет документ из базы знаний.
        
        Args:
            doc_id: Идентификатор документа для удаления
            
        Returns:
            True если документ удален успешно
        """
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Документ {doc_id} удален из базы знаний")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления документа {doc_id}: {e}")
            return False
    
    def clear_collection(self) -> bool:
        """
        Очищает всю коллекцию.
        
        Returns:
            True если коллекция очищена успешно
        """
        try:
            # Удаляем коллекцию и создаем новую
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("База знаний очищена")
            return True
        except Exception as e:
            logger.error(f"Ошибка очистки базы знаний: {e}")
            return False

# Глобальный экземпляр для использования в других модулях
_knowledge_base = None

def get_knowledge_base() -> KnowledgeBase:
    """Возвращает глобальный экземпляр базы знаний."""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base

# Удобные функции для использования в других модулях
def add_document(doc_id: str, document_text: str, metadata: Dict[str, Any] = None) -> bool:
    """Добавляет документ в базу знаний."""
    return get_knowledge_base().add_document(doc_id, document_text, metadata)

def search_relevant_docs(query_text: str, n_results: int = 3) -> List[str]:
    """Ищет релевантные документы."""
    return get_knowledge_base().search_relevant_docs(query_text, n_results) 