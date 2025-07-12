#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API админ-панели.
"""
import requests
import json
import time
import os

def test_admin_api():
    """Тестирует API админ-панели."""
    base_url = "http://127.0.0.1:5000"
    
    # Создаем сессию для сохранения cookies
    session = requests.Session()
    
    # Отключаем прокси для локальных подключений
    session.proxies = {
        'http': None,
        'https': None
    }
    
    # Отключаем прокси в переменных окружения
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    
    print("1. Проверка доступности админ-панели...")
    print(f"   URL: {base_url}")
    try:
        response = session.get(f"{base_url}/", timeout=10)
        print(f"   Статус: {response.status_code}")
        if response.status_code in [200, 302]:  # 302 - редирект на login
            print("   ✅ Админ-панель доступна")
        else:
            print("   ❌ Админ-панель недоступна")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Ошибка подключения: {e}")
        return False
    
    print("\n2. Аутентификация...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = session.post(
            f"{base_url}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Статус ответа: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Аутентификация успешна")
            else:
                print("   ❌ Аутентификация не удалась")
                print(f"   Ответ: {result}")
                return False
        else:
            print(f"   ❌ Ошибка аутентификации: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Ошибка аутентификации: {e}")
        return False
    
    print("\n3. Запуск команды test_demo...")
    try:
        command_data = {
            "command": "test_demo"
        }
        
        response = session.post(
            f"{base_url}/api/execute",
            json=command_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Статус ответа: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                process_id = result.get('process_id')
                print(f"   ✅ Команда запущена успешно. Process ID: {process_id}")
                
                # Ждем некоторое время для выполнения
                print("   ⏳ Ожидание выполнения...")
                time.sleep(8)  # Увеличиваем время ожидания
                
                # Проверяем статус процесса
                status_response = session.get(f"{base_url}/api/processes/{process_id}", timeout=10)
                if status_response.status_code == 200:
                    status_result = status_response.json()
                    print(f"   📊 Статус процесса: {status_result.get('status')}")
                    
                    if status_result.get('stdout'):
                        print("   📝 Вывод команды:")
                        print(status_result.get('stdout')[:500] + "..." if len(status_result.get('stdout')) > 500 else status_result.get('stdout'))
                    
                    if status_result.get('stderr'):
                        print("   ⚠️ Ошибки:")
                        print(status_result.get('stderr'))
                        
                    return status_result.get('status') == 'completed' and status_result.get('returncode') == 0
                else:
                    print(f"   ❌ Ошибка получения статуса: {status_response.status_code}")
                    return False
            else:
                print(f"   ❌ Ошибка запуска команды: {result.get('error')}")
                return False
        else:
            print(f"   ❌ Ошибка API: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Ошибка выполнения команды: {e}")
        return False

if __name__ == "__main__":
    print("🧪 ТЕСТИРОВАНИЕ API АДМИН-ПАНЕЛИ")
    print("=" * 50)
    
    success = test_admin_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ТЕСТ УСПЕШНО ПРОЙДЕН!")
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!") 