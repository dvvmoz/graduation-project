"""
Модуль для обработки текста и извлечения данных из PDF-файлов.
"""
import re
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Извлекает весь текст из PDF-файла.
    
    Args:
        pdf_path: Путь к PDF-файлу
        
    Returns:
        Извлеченный текст из всех страниц PDF
        
    Raises:
        FileNotFoundError: Если файл не найден
        Exception: При ошибке чтения PDF
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            full_text += page_text + "\n\n"
            
        doc.close()
        logger.info(f"Извлечено {len(full_text)} символов из файла {pdf_path}")
        return full_text.strip()
        
    except FileNotFoundError:
        logger.error(f"Файл не найден: {pdf_path}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при чтении PDF файла {pdf_path}: {e}")
        raise

def split_text_into_structure(text: str) -> list[str]:
    """
    Разделяет текст на абзацы, пункты и подпункты.
    
    Распознает следующие маркеры:
    - Нумерованные пункты: 1., 2., 10.
    - Многоуровневые пункты: 1.1., 1.2.3.
    - Буквенные пункты: а), б), в)
    - Маркированные списки: •, -, *
    
    Args:
        text: Исходный текст для разделения
        
    Returns:
        Список структурированных текстовых блоков
    """
    if not text or not text.strip():
        return []
    
    # Паттерн для поиска различных типов маркеров в начале строки
    pattern = r"(?m)^\s*(\d+\.[\d\.]*\s+|[а-яА-Я]\)\s+|[a-zA-Z]\)\s+|[•\-\*]\s+)"
    
    # Разделяем текст по маркерам, сохраняя маркеры
    parts = re.split(pattern, text)
    
    structured_blocks = []
    
    # Первый элемент - текст до первого маркера
    if parts[0].strip():
        # Разделяем на абзацы по двойным переводам строки
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', parts[0]) if p.strip()]
        structured_blocks.extend(paragraphs)
    
    # Обрабатываем остальные части (маркер + текст)
    i = 1
    while i < len(parts):
        if i + 1 < len(parts):
            marker = parts[i].strip()
            content = parts[i + 1].strip()
            
            if marker and content:
                # Очищаем текст от лишних переводов строк
                cleaned_content = re.sub(r'\n+', ' ', content)
                full_item = f"{marker} {cleaned_content}"
                structured_blocks.append(full_item)
            
            i += 2
        else:
            i += 1
    
    # Фильтруем пустые блоки и слишком короткие
    filtered_blocks = []
    for block in structured_blocks:
        clean_block = block.strip()
        if clean_block and len(clean_block) > 10:  # Минимальная длина блока
            filtered_blocks.append(clean_block)
    
    logger.info(f"Разделено на {len(filtered_blocks)} структурированных блоков")
    return filtered_blocks

def clean_text(text: str) -> str:
    """
    Очищает текст от лишних пробелов и символов.
    
    Args:
        text: Исходный текст
        
    Returns:
        Очищенный текст
    """
    if not text:
        return ""
    
    # Удаляем лишние пробелы и переводы строк
    cleaned = re.sub(r'\s+', ' ', text)
    
    # Удаляем пробелы в начале и конце
    cleaned = cleaned.strip()
    
    return cleaned 