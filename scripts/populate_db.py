#!/usr/bin/env python3
"""
Скрипт для наполнения базы знаний из PDF файлов.
"""
import os
import sys
import logging
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import load_config
from modules.text_processing import extract_text_from_pdf, split_text_into_structure
from modules.knowledge_base import add_document, get_knowledge_base

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_pdf_file(pdf_path: str, source_folder: str = "data") -> int:
    """
    Обрабатывает один PDF файл и добавляет его содержимое в базу знаний.
    
    Args:
        pdf_path: Путь к PDF файлу
        source_folder: Папка-источник для метаданных
        
    Returns:
        Количество добавленных документов
    """
    try:
        filename = os.path.basename(pdf_path)
        logger.info(f"📄 Обрабатываю файл: {filename}")
        
        # Извлекаем текст из PDF
        full_text = extract_text_from_pdf(pdf_path)
        
        if not full_text.strip():
            logger.warning(f"❌ Файл {filename} пуст или не содержит текста")
            return 0
        
        # Разделяем текст на структурированные блоки
        text_blocks = split_text_into_structure(full_text)
        
        if not text_blocks:
            logger.warning(f"❌ Не удалось разделить текст из файла {filename}")
            return 0
        
        # Добавляем каждый блок в базу знаний
        added_count = 0
        base_name = os.path.splitext(filename)[0]
        
        for i, block in enumerate(text_blocks):
            # Создаем уникальный ID для каждого блока
            doc_id = f"{base_name}_block_{i:03d}"
            
            # Метаданные для блока
            metadata = {
                "source_file": filename,
                "source_folder": source_folder,
                "block_index": i,
                "total_blocks": len(text_blocks),
                "block_length": len(block)
            }
            
            # Добавляем блок в базу знаний
            if add_document(doc_id, block, metadata):
                added_count += 1
            else:
                logger.warning(f"❌ Не удалось добавить блок {i} из файла {filename}")
        
        logger.info(f"✅ Добавлено {added_count} блоков из файла {filename}")
        return added_count
        
    except Exception as e:
        logger.error(f"❌ Ошибка обработки файла {pdf_path}: {e}")
        return 0

def populate_from_directory(data_dir: str = "data") -> dict:
    """
    Наполняет базу знаний из всех PDF файлов в указанной директории.
    
    Args:
        data_dir: Путь к директории с PDF файлами
        
    Returns:
        Статистика обработки
    """
    stats = {
        "total_files": 0,
        "processed_files": 0,
        "total_blocks": 0,
        "failed_files": []
    }
    
    # Проверяем существование директории
    if not os.path.exists(data_dir):
        logger.error(f"❌ Директория {data_dir} не найдена")
        return stats
    
    # Получаем список PDF файлов
    pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logger.warning(f"❌ PDF файлы в директории {data_dir} не найдены")
        return stats
    
    stats["total_files"] = len(pdf_files)
    logger.info(f"📚 Найдено {len(pdf_files)} PDF файлов для обработки")
    
    # Обрабатываем каждый файл
    for filename in pdf_files:
        pdf_path = os.path.join(data_dir, filename)
        
        blocks_added = process_pdf_file(pdf_path, data_dir)
        
        if blocks_added > 0:
            stats["processed_files"] += 1
            stats["total_blocks"] += blocks_added
        else:
            stats["failed_files"].append(filename)
    
    return stats

def show_statistics(stats: dict):
    """
    Отображает статистику обработки.
    
    Args:
        stats: Словарь со статистикой
    """
    logger.info("📊 Статистика обработки:")
    logger.info(f"  📄 Всего файлов: {stats['total_files']}")
    logger.info(f"  ✅ Обработано успешно: {stats['processed_files']}")
    logger.info(f"  📝 Добавлено блоков: {stats['total_blocks']}")
    
    if stats['failed_files']:
        logger.warning(f"  ❌ Файлы с ошибками: {len(stats['failed_files'])}")
        for filename in stats['failed_files']:
            logger.warning(f"    - {filename}")
    
    # Получаем статистику базы знаний
    kb = get_knowledge_base()
    kb_stats = kb.get_collection_stats()
    logger.info(f"  🗂️ Всего документов в базе: {kb_stats.get('total_documents', 0)}")

def main():
    """Основная функция скрипта."""
    logger.info("🚀 Запуск скрипта наполнения базы знаний")
    
    try:
        # Загружаем конфигурацию
        load_config()
        
        # Проверяем наличие папки data
        data_dir = "data"
        if not os.path.exists(data_dir):
            logger.info(f"📁 Создаю директорию {data_dir}")
            os.makedirs(data_dir)
            logger.info(f"📁 Директория {data_dir} создана. Добавьте PDF файлы и запустите скрипт снова.")
            return
        
        # Наполняем базу знаний
        stats = populate_from_directory(data_dir)
        
        # Показываем статистику
        show_statistics(stats)
        
        if stats["processed_files"] > 0:
            logger.info("✅ Наполнение базы знаний завершено успешно!")
        else:
            logger.warning("❌ Не удалось обработать ни одного файла")
            
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 