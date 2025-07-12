"""
Модуль для веб-скрапинга юридических сайтов и пополнения базы знаний
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import logging
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set, Optional
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import json
import os

from .text_processing import TextProcessor
from .knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)


class WebScraper:
    """Класс для скрапинга юридических сайтов"""
    
    def __init__(self, knowledge_base: KnowledgeBase, text_processor: TextProcessor):
        self.knowledge_base = knowledge_base
        self.text_processor = text_processor
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls: Set[str] = set()
        self.max_pages = 50  # Максимальное количество страниц для скрапинга
        self.delay = 1  # Задержка между запросами в секундах
        
    def scrape_single_page(self, url: str) -> Optional[Dict]:
        """
        Скрапинг одной страницы
        
        Args:
            url: URL страницы для скрапинга
            
        Returns:
            Словарь с данными страницы или None при ошибке
        """
        try:
            logger.info(f"Скрапинг страницы: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Удаляем ненужные элементы
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Извлекаем заголовок
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Без заголовка"
            
            # Извлекаем основной контент
            content = ""
            
            # Ищем основной контент в различных тегах
            main_content_selectors = [
                'main', 'article', '.content', '.main-content', 
                '.post-content', '.entry-content', '#content', '#main'
            ]
            
            for selector in main_content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(separator=' ', strip=True)
                    break
            
            # Если не нашли основной контент, берем весь body
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(separator=' ', strip=True)
            
            # Очищаем текст
            content = self._clean_text(content)
            
            if len(content) < 100:  # Слишком короткий контент
                return None
            
            return {
                'url': url,
                'title': title_text,
                'content': content,
                'domain': urlparse(url).netloc
            }
            
        except Exception as e:
            logger.error(f"Ошибка при скрапинге {url}: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """
        Очистка текста от лишних символов
        
        Args:
            text: Исходный текст
            
        Returns:
            Очищенный текст
        """
        # Удаляем множественные пробелы и переносы строк
        text = re.sub(r'\s+', ' ', text)
        
        # Удаляем специальные символы
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]]', '', text)
        
        # Удаляем лишние пробелы в начале и конце
        text = text.strip()
        
        return text
    
    def get_legal_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Извлечение ссылок на юридические страницы
        
        Args:
            soup: BeautifulSoup объект страницы
            base_url: Базовый URL
            
        Returns:
            Список URL для дальнейшего скрапинга
        """
        links = []
        domain = urlparse(base_url).netloc
        
        # Ключевые слова для юридических страниц (РБ + РФ)
        legal_keywords = [
            # Общие правовые термины
            'закон', 'кодекс', 'постановление', 'указ', 'приказ',
            'регламент', 'положение', 'инструкция', 'методика',
            'право', 'юридический', 'правовой', 'законодательство',
            'суд', 'адвокат', 'нотариус', 'договор', 'иск',
            'заявление', 'жалоба', 'апелляция', 'кассация',
            
            # Специфика для Беларуси
            'республика беларусь', 'беларусь', 'белорусский',
            'совет министров', 'национальное собрание', 'парламент',
            'конституционный суд', 'верховный суд', 'хозяйственный суд',
            'прокуратура', 'министерство юстиции', 'нотариат',
            'исполнительный комитет', 'облисполком', 'горисполком',
            'трудовой кодекс', 'гражданский кодекс', 'уголовный кодекс',
            'административный кодекс', 'процессуальный кодекс',
            'декрет', 'распоряжение', 'решение', 'определение'
        ]
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            link_text = link.get_text().lower()
            
            # Проверяем, что ссылка ведет на тот же домен
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc != domain:
                continue
            
            # Проверяем ключевые слова в тексте ссылки
            if any(keyword in link_text for keyword in legal_keywords):
                links.append(full_url)
            
            # Проверяем ключевые слова в URL
            if any(keyword in href.lower() for keyword in legal_keywords):
                links.append(full_url)
        
        return list(set(links))  # Убираем дубликаты
    
    def scrape_website(self, start_url: str, max_pages: int = None) -> List[Dict]:
        """
        Скрапинг всего сайта начиная с указанного URL
        
        Args:
            start_url: Начальный URL для скрапинга
            max_pages: Максимальное количество страниц
            
        Returns:
            Список словарей с данными страниц
        """
        if max_pages is None:
            max_pages = self.max_pages
            
        pages_data = []
        urls_to_visit = [start_url]
        self.visited_urls.clear()
        
        page_count = 0
        
        while urls_to_visit and page_count < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
                
            self.visited_urls.add(current_url)
            
            # Скрапим текущую страницу
            page_data = self.scrape_single_page(current_url)
            
            if page_data:
                pages_data.append(page_data)
                page_count += 1
                
                # Получаем новые ссылки для посещения
                try:
                    response = self.session.get(current_url, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    new_links = self.get_legal_links(soup, current_url)
                    
                    # Добавляем новые ссылки в очередь
                    for link in new_links:
                        if link not in self.visited_urls and link not in urls_to_visit:
                            urls_to_visit.append(link)
                            
                except Exception as e:
                    logger.error(f"Ошибка при получении ссылок с {current_url}: {e}")
            
            # Задержка между запросами
            time.sleep(self.delay)
        
        logger.info(f"Скрапинг завершен. Обработано страниц: {len(pages_data)}")
        return pages_data
    
    async def scrape_website_async(self, start_url: str, max_pages: int = None) -> List[Dict]:
        """
        Асинхронный скрапинг сайта
        
        Args:
            start_url: Начальный URL для скрапинга
            max_pages: Максимальное количество страниц
            
        Returns:
            Список словарей с данными страниц
        """
        if max_pages is None:
            max_pages = self.max_pages
            
        pages_data = []
        urls_to_visit = [start_url]
        self.visited_urls.clear()
        
        async with aiohttp.ClientSession() as session:
            page_count = 0
            
            while urls_to_visit and page_count < max_pages:
                current_url = urls_to_visit.pop(0)
                
                if current_url in self.visited_urls:
                    continue
                    
                self.visited_urls.add(current_url)
                
                # Асинхронный скрапинг страницы
                page_data = await self._scrape_page_async(session, current_url)
                
                if page_data:
                    pages_data.append(page_data)
                    page_count += 1
                    
                    # Получаем новые ссылки
                    new_links = await self._get_links_async(session, current_url)
                    
                    for link in new_links:
                        if link not in self.visited_urls and link not in urls_to_visit:
                            urls_to_visit.append(link)
                
                await asyncio.sleep(self.delay)
        
        logger.info(f"Асинхронный скрапинг завершен. Обработано страниц: {len(pages_data)}")
        return pages_data
    
    async def _scrape_page_async(self, session: aiohttp.ClientSession, url: str) -> Optional[Dict]:
        """Асинхронный скрапинг одной страницы"""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                    
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Удаляем ненужные элементы
                for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                    element.decompose()
                
                title = soup.find('title')
                title_text = title.get_text().strip() if title else "Без заголовка"
                
                content_text = soup.get_text(separator=' ', strip=True)
                content_text = self._clean_text(content_text)
                
                if len(content_text) < 100:
                    return None
                
                return {
                    'url': url,
                    'title': title_text,
                    'content': content_text,
                    'domain': urlparse(url).netloc
                }
                
        except Exception as e:
            logger.error(f"Ошибка при асинхронном скрапинге {url}: {e}")
            return None
    
    async def _get_links_async(self, session: aiohttp.ClientSession, url: str) -> List[str]:
        """Асинхронное получение ссылок со страницы"""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                    
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                return self.get_legal_links(soup, url)
                
        except Exception as e:
            logger.error(f"Ошибка при получении ссылок с {url}: {e}")
            return []
    
    def add_to_knowledge_base(self, pages_data: List[Dict]) -> int:
        """
        Добавление данных в базу знаний
        
        Args:
            pages_data: Список словарей с данными страниц
            
        Returns:
            Количество добавленных документов
        """
        added_count = 0
        
        for page_data in pages_data:
            try:
                # Разбиваем контент на чанки
                chunks = self.text_processor.split_text(page_data['content'])
                
                for i, chunk in enumerate(chunks):
                    # Создаем метаданные для чанка
                    metadata = {
                        'source': 'web_scraper',
                        'url': page_data['url'],
                        'title': page_data['title'],
                        'domain': page_data['domain'],
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        'content_type': 'legal_website'
                    }
                    
                    # Добавляем в базу знаний
                    self.knowledge_base.add_document(chunk, metadata)
                    added_count += 1
                    
            except Exception as e:
                logger.error(f"Ошибка при добавлении страницы {page_data['url']}: {e}")
        
        logger.info(f"Добавлено в базу знаний: {added_count} чанков")
        return added_count
    
    def scrape_and_add(self, start_url: str, max_pages: int = None) -> Dict:
        """
        Скрапинг сайта и добавление в базу знаний
        
        Args:
            start_url: Начальный URL для скрапинга
            max_pages: Максимальное количество страниц
            
        Returns:
            Словарь с результатами операции
        """
        logger.info(f"Начинаем скрапинг сайта: {start_url}")
        
        # Скрапим сайт
        pages_data = self.scrape_website(start_url, max_pages)
        
        if not pages_data:
            return {
                'success': False,
                'message': 'Не удалось получить данные с сайта',
                'pages_scraped': 0,
                'chunks_added': 0
            }
        
        # Добавляем в базу знаний
        chunks_added = self.add_to_knowledge_base(pages_data)
        
        # Обновляем информацию о парсинге
        try:
            from .scraping_tracker import update_scraping_info
            update_scraping_info(start_url, len(pages_data), chunks_added)
        except Exception as e:
            logger.error(f"Ошибка обновления информации о парсинге: {e}")
        
        return {
            'success': True,
            'message': f'Успешно обработано {len(pages_data)} страниц',
            'pages_scraped': len(pages_data),
            'chunks_added': chunks_added,
            'start_url': start_url
        }


def create_scraper_from_config() -> WebScraper:
    """
    Создание экземпляра WebScraper с настройками из конфигурации
    
    Returns:
        Экземпляр WebScraper
    """
    from .knowledge_base import KnowledgeBase
    from .text_processing import TextProcessor
    
    knowledge_base = KnowledgeBase()
    text_processor = TextProcessor()
    
    return WebScraper(knowledge_base, text_processor)


if __name__ == "__main__":
    # Пример использования
    scraper = create_scraper_from_config()
    
    # Скрапинг юридического сайта
    result = scraper.scrape_and_add(
        start_url="https://www.garant.ru/",
        max_pages=10
    )
    
    print(f"Результат скрапинга: {result}") 