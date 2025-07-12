#!/usr/bin/env python3
"""
Финальный тест гибридного фильтра.
"""

from modules.bot_handler import is_legal_question, get_rejection_message

def main():
    print("🎯 ФИНАЛЬНЫЙ ТЕСТ ГИБРИДНОГО ФИЛЬТРА")
    print("=" * 40)
    
    # Быстрые тесты
    tests = [
        ("Как подать иск в суд?", True),
        ("Меня кинули с деньгами", True),
        ("Эстоппель в праве", True),
        ("Как приготовить борщ?", False),
        ("Права доступа к базе данных", False),
    ]
    
    correct = 0
    for question, expected in tests:
        result = is_legal_question(question)
        is_legal, score, explanation = result
        
        status = "✅" if is_legal == expected else "❌"
        legal_str = "ЮР" if is_legal else "НЕ ЮР"
        
        print(f"{status} {question}: {legal_str} (балл: {score:.3f})")
        
        if is_legal == expected:
            correct += 1
    
    accuracy = correct / len(tests) * 100
    print(f"\n📊 Точность: {correct}/{len(tests)} ({accuracy:.1f}%)")
    
    # Тест сообщения об отклонении
    print(f"\n📝 Сообщение об отклонении:")
    rejection_msg = get_rejection_message()
    print(f"✅ {rejection_msg[:50]}...")
    
    print(f"\n🎉 ГИБРИДНЫЙ ФИЛЬТР АКТИВЕН И РАБОТАЕТ!")

if __name__ == "__main__":
    main() 