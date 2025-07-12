"""
Тесты для модуля config.py
"""
import os
import pytest
from unittest.mock import patch

# Импортируем конфигурацию
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import load_config, TELEGRAM_TOKEN, OPENAI_API_KEY, CHROMA_DB_PATH

class TestConfig:
    """Тесты для конфигурации проекта."""
    
    def test_load_config_success(self):
        """Тест успешной загрузки конфигурации."""
        # Мокаем переменные окружения
        with patch.dict(os.environ, {
            'TELEGRAM_TOKEN': '123456789:test_token',
            'OPENAI_API_KEY': 'sk-test_key_123'
        }):
            # Не должно вызвать исключение
            load_config()
    
    def test_load_config_missing_telegram_token(self):
        """Тест с отсутствующим токеном Telegram."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'sk-test_key_123'
        }, clear=True):
            with pytest.raises(ValueError, match="TELEGRAM_TOKEN"):
                load_config()
    
    def test_load_config_missing_openai_key(self):
        """Тест с отсутствующим ключом OpenAI."""
        with patch.dict(os.environ, {
            'TELEGRAM_TOKEN': '123456789:test_token'
        }, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                load_config()
    
    def test_default_chroma_db_path(self):
        """Тест значения по умолчанию для пути к базе данных."""
        with patch.dict(os.environ, {}, clear=True):
            # Импортируем заново для получения значения по умолчанию
            from config import CHROMA_DB_PATH
            assert CHROMA_DB_PATH == "db/chroma"
    
    def test_custom_chroma_db_path(self):
        """Тест кастомного пути к базе данных."""
        custom_path = "custom/db/path"
        with patch.dict(os.environ, {
            'CHROMA_DB_PATH': custom_path
        }):
            # Обновляем переменную
            import importlib
            import config
            importlib.reload(config)
            assert config.CHROMA_DB_PATH == custom_path

class TestConfigConstants:
    """Тесты для констант конфигурации."""
    
    def test_default_model_is_set(self):
        """Проверяем, что модель по умолчанию задана."""
        from config import DEFAULT_MODEL
        assert DEFAULT_MODEL is not None
        assert isinstance(DEFAULT_MODEL, str)
        assert len(DEFAULT_MODEL) > 0
    
    def test_max_results_is_positive(self):
        """Проверяем, что максимальное количество результатов положительное."""
        from config import MAX_RESULTS
        assert isinstance(MAX_RESULTS, int)
        assert MAX_RESULTS > 0
    
    def test_max_tokens_is_positive(self):
        """Проверяем, что максимальное количество токенов положительное."""
        from config import MAX_TOKENS
        assert isinstance(MAX_TOKENS, int)
        assert MAX_TOKENS > 0 