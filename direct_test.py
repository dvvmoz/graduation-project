#!/usr/bin/env python3
"""
Прямое тестирование функциональности админ-панели.
"""
import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from admin_panel import AdminPanel

def test_admin_panel_directly():
    """Тестирует админ-панель напрямую."""
    print("🧪 ПРЯМОЕ ТЕСТИРОВАНИЕ АДМИН-ПАНЕЛИ")
    print("=" * 50)
    
    try:
        # Создаем экземпляр админ-панели
        print("1. Инициализация админ-панели...")
        admin = AdminPanel()
        print("   ✅ Админ-панель инициализирована")
        
        # Тестируем команду test_demo
        print("\n2. Тестирование команды test_demo...")
        result = admin.execute_command('test_demo')
        
        if result.get('success'):
            process_id = result.get('process_id')
            print(f"   ✅ Команда запущена успешно. Process ID: {process_id}")
            print(f"   📝 Сообщение: {result.get('message')}")
            
            # Ждем выполнения
            print("   ⏳ Ожидание выполнения...")
            import time
            time.sleep(8)
            
            # Проверяем статус
            status = admin.get_process_status(process_id)
            print(f"   📊 Статус: {status.get('status')}")
            
            if status.get('stdout'):
                print("   📝 Вывод команды:")
                stdout = status.get('stdout')
                if len(stdout) > 500:
                    print(stdout[:500] + "...")
                else:
                    print(stdout)
            
            if status.get('stderr'):
                print("   ⚠️ Ошибки:")
                print(status.get('stderr'))
            
            return status.get('status') == 'completed' and status.get('returncode') == 0
        else:
            print(f"   ❌ Ошибка запуска: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Критическая ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_admin_panel_directly()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ТЕСТ УСПЕШНО ПРОЙДЕН!")
        print("\n✅ Кнопка 'Тест системы' работает корректно!")
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
        print("\n❌ Есть проблемы с кнопкой 'Тест системы'.") 