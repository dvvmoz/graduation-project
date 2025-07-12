#!/usr/bin/env python3
"""
Простой тест демо-версии системы.
"""
# Отключаем телеметрию ChromaDB в первую очередь
import disable_telemetry

import os
import sys
from pathlib import Path

# Отключаем телеметрию ChromaDB для предотвращения ошибок
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from demo_bot import DemoLegalAssistant

def main():
    """Главная функция для тестирования демо-бота."""
    print("[ТЕСТ] НАЧАЛО ТЕСТИРОВАНИЯ СИСТЕМЫ")
    print("=" * 60)
    
    try:
        # Инициализируем демо-ассистента
        print("1. Инициализация ассистента...")
        demo = DemoLegalAssistant()
        print("   [OK] Ассистент успешно инициализирован.")
        
        # Получение статистики
        stats = demo.knowledge_base.get_collection_stats()
        doc_count = stats.get('total_documents', 0)
        print(f"   [INFO] База знаний содержит: {doc_count} документов")

        if doc_count == 0:
            print("\\n[ОШИБКА] ВНИМАНИЕ: База знаний пуста. Тестирование не может быть продолжено.")
            print("   [РЕШЕНИЕ] Запустите команду 'Обновить БД' в админ-панели.")
            return

        # Тестовые вопросы
        test_questions = [
            "налоговые ставки",
            "права потребителя", 
            "документы для регистрации",
            "административные штрафы",
            "несуществующий запрос для проверки"
        ]
        
        print(f"\\n2. Выполнение {len(test_questions)} тестовых запросов...")
        
        all_tests_passed = True
        for i, question in enumerate(test_questions, 1):
            print(f"\\n---> ТЕСТ {i}: '{question}'")
            try:
                answer = demo.get_demo_answer(question)
                
                if "НАЙДЕНО В БАЗЕ ЗНАНИЙ" in answer or "не найдена в базе знаний" in answer:
                    print(f"   [OK] Тест '{question}' пройден успешно.")
                    # print("\n" + answer.strip() + "\n") # Раскомментируйте для полного вывода
                else:
                    print(f"   [ОШИБКА] Тест '{question}' провален. Ответ не содержит ожидаемой информации.")
                    all_tests_passed = False
                
                print("-" * 40)
            except Exception as e:
                print(f"   [КРИТИЧЕСКАЯ ОШИБКА] в тесте '{question}': {e}")
                all_tests_passed = False

        print("\\n" + "=" * 60)
        if all_tests_passed:
            print("[УСПЕХ] ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
        else:
            print("[ОШИБКА] ОБНАРУЖЕНЫ ОШИБКИ. Проверьте вывод выше.")
            
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] при запуске теста: {e}")

if __name__ == "__main__":
    main() 