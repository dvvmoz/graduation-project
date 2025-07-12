"""
Тесты для модуля веб-скрапинга
"""

import pytest
import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь
sys.path.append(str(Path(__file__).parent.parent))

from modules.web_scraper import WebScraper
from modules.knowledge_base import KnowledgeBase
from modules.text_processing import TextProcessor


class TestWebScraper:
    """Тесты для класса WebScraper"""
    
    @pytest.fixture
    def scraper(self):
        """Создает экземпляр WebScraper для тестов"""
        knowledge_base = KnowledgeBase()
        text_processor = TextProcessor()
        return WebScraper(knowledge_base, text_processor)
    
    def test_clean_text(self, scraper):
        """Тест очистки текста"""
        dirty_text = "  Это   тестовый   текст  \n\n  с лишними  пробелами  "
        clean_text = scraper._clean_text(dirty_text)
        
        assert clean_text == "Это тестовый текст с лишними пробелами"
        assert "  " not in clean_text  # Нет двойных пробелов
        assert "\n" not in clean_text  # Нет переносов строк
    
    def test_clean_text_with_special_chars(self, scraper):
        """Тест очистки текста со специальными символами"""
        text_with_chars = "Текст с @#$%^&*() символами и <script>alert('test')</script>"
        clean_text = scraper._clean_text(text_with_chars)
        
        # Проверяем, что специальные символы удалены
        assert "@" not in clean_text
        assert "#" not in clean_text
        assert "<script>" not in clean_text
    
    def test_get_legal_links(self, scraper):
        """Тест извлечения юридических ссылок"""
        from bs4 import BeautifulSoup
        
        # Создаем HTML с юридическими ссылками
        html = """
        <html>
        <body>
            <a href="/law/article1">Закон о правах</a>
            <a href="/code/civil">Гражданский кодекс</a>
            <a href="/news/weather">Погода</a>
            <a href="/legal/contract">Договор купли-продажи</a>
            <a href="https://external.com">Внешняя ссылка</a>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = "https://example.com"
        
        links = scraper.get_legal_links(soup, base_url)
        
        # Проверяем, что найдены юридические ссылки
        assert len(links) >= 3  # Должно найти минимум 3 юридические ссылки
        assert any("law" in link for link in links)
        assert any("code" in link for link in links)
        assert any("legal" in link for link in links)
        
        # Проверяем, что внешние ссылки не включены
        assert not any("external.com" in link for link in links)
    
    def test_scraper_initialization(self, scraper):
        """Тест инициализации скрапера"""
        assert scraper.knowledge_base is not None
        assert scraper.text_processor is not None
        assert scraper.session is not None
        assert scraper.max_pages == 50
        assert scraper.delay == 1
    
    def test_create_scraper_from_config(self):
        """Тест создания скрапера из конфигурации"""
        from modules.web_scraper import create_scraper_from_config
        
        scraper = create_scraper_from_config()
        
        assert isinstance(scraper, WebScraper)
        assert scraper.knowledge_base is not None
        assert scraper.text_processor is not None


class TestWebScraperIntegration:
    """Интеграционные тесты для веб-скрапера"""
    
    @pytest.fixture
    def mock_knowledge_base(self):
        """Создает мок базы знаний"""
        class MockKnowledgeBase:
            def __init__(self):
                self.documents = []
            
            def add_document(self, text, metadata):
                self.documents.append({
                    'text': text,
                    'metadata': metadata
                })
            
            def get_collection_stats(self):
                return {
                    'total_documents': len(self.documents),
                    'collection_name': 'test_collection',
                    'db_path': '/test/path'
                }
        
        return MockKnowledgeBase()
    
    @pytest.fixture
    def mock_text_processor(self):
        """Создает мок обработчика текста"""
        class MockTextProcessor:
            def split_text(self, text):
                # Простое разделение на чанки по 100 символов
                chunks = []
                for i in range(0, len(text), 100):
                    chunks.append(text[i:i+100])
                return chunks
        
        return MockTextProcessor()
    
    def test_add_to_knowledge_base(self, mock_knowledge_base, mock_text_processor):
        """Тест добавления данных в базу знаний"""
        scraper = WebScraper(mock_knowledge_base, mock_text_processor)
        
        # Тестовые данные страниц
        pages_data = [
            {
                'url': 'https://example.com/page1',
                'title': 'Тестовая страница 1',
                'content': 'Это тестовый контент первой страницы с юридической информацией о правах и обязанностях граждан в соответствии с законодательством Российской Федерации.',
                'domain': 'example.com'
            },
            {
                'url': 'https://example.com/page2',
                'title': 'Тестовая страница 2',
                'content': 'Вторая тестовая страница содержит информацию о договорах и их заключении согласно гражданскому кодексу.',
                'domain': 'example.com'
            }
        ]
        
        # Добавляем в базу знаний
        chunks_added = scraper.add_to_knowledge_base(pages_data)
        
        # Проверяем результаты
        assert chunks_added > 0
        assert len(mock_knowledge_base.documents) == chunks_added
        
        # Проверяем структуру добавленных документов
        for doc in mock_knowledge_base.documents:
            assert 'text' in doc
            assert 'metadata' in doc
            assert doc['metadata']['source'] == 'web_scraper'
            assert doc['metadata']['content_type'] == 'legal_website'
            assert 'url' in doc['metadata']
            assert 'title' in doc['metadata']
            assert 'domain' in doc['metadata']


def test_scraper_error_handling():
    """Тест обработки ошибок скрапера"""
    knowledge_base = KnowledgeBase()
    text_processor = TextProcessor()
    scraper = WebScraper(knowledge_base, text_processor)
    
    # Тест с невалидным URL
    result = scraper.scrape_single_page("https://invalid-url-that-does-not-exist.com")
    assert result is None
    
    # Тест с пустым URL
    result = scraper.scrape_single_page("")
    assert result is None


if __name__ == "__main__":
    pytest.main([__file__]) 