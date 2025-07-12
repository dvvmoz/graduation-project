#!/usr/bin/env python3
"""
Тест полного анализа по всем пунктам методологии.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.knowledge_base import get_knowledge_base
from modules.llm_service import get_llm_service

def test_full_analysis():
    """Тестирует полный анализ по всем пунктам методологии."""
    
    # Инициализируем сервисы
    kb = get_knowledge_base()
    llm = get_llm_service()
    
    # Тестовый вопрос
    question = "Какие документы нужны для регистрации ООО в Беларуси?"
    
    print(f"🔍 Вопрос: {question}")
    print("\n" + "="*70)
    
    # Получаем контекст из базы знаний
    context_docs = kb.search(question)
    print(f"📚 Найдено документов: {len(context_docs)}")
    
    # Генерируем ответ
    print("\n🤖 Генерация ответа...")
    answer = llm.get_answer(question, context_docs)
    
    print("\n" + "="*70)
    print("📝 ОТВЕТ:")
    print("="*70)
    print(answer)
    print("="*70)
    
    # Анализируем, выполнены ли все пункты
    print("\n🔍 АНАЛИЗ ВЫПОЛНЕНИЯ МЕТОДОЛОГИИ:")
    print("-" * 50)
    
    # Проверяем системный анализ
    has_legal_field = any(word in answer.lower() for word in ['отрасль', 'право', 'гражданск', 'хозяйственн', 'административн'])
    has_significance = any(word in answer.lower() for word in ['значимость', 'важность', 'необходимо'])
    has_user_level = any(word in answer.lower() for word in ['новичок', 'студент', 'профессионал', 'граждан', 'специалист'])
    
    print(f"✅ Системный анализ:")
    print(f"   - Отрасль права: {'✓' if has_legal_field else '✗'}")
    print(f"   - Юридическая значимость: {'✓' if has_significance else '✗'}")
    print(f"   - Уровень пользователя: {'✓' if has_user_level else '✗'}")
    
    # Проверяем многоуровневую экспертизу
    has_law_refs = any(word in answer.lower() for word in ['статья', 'кодекс', 'закон', 'ст.', 'гк', 'хк'])
    has_reliability = any(word in answer.lower() for word in ['100%', '80%', '60%', 'достоверность'])
    
    print(f"\n✅ Многоуровневая экспертиза:")
    print(f"   - Ссылки на нормы: {'✓' if has_law_refs else '✗'}")
    print(f"   - Шкала достоверности: {'✓' if has_reliability else '✗'}")
    
    # Проверяем адаптивный ответ
    has_conclusion = any(word in answer.lower() for word in ['вывод', 'итого', 'заключение'])
    has_checklist = any(word in answer.lower() for word in ['действия', 'шаги', 'порядок', 'необходимо'])
    
    print(f"\n✅ Адаптивный ответ:")
    print(f"   - Итоговый вывод: {'✓' if has_conclusion else '✗'}")
    print(f"   - Чек-лист действий: {'✓' if has_checklist else '✗'}")
    
    # Проверяем превентивную безопасность
    has_constitution = 'конституц' in answer.lower()
    has_risks = any(word in answer.lower() for word in ['риск', 'опасность', 'внимание', 'осторожно'])
    
    print(f"\n✅ Превентивная безопасность:")
    print(f"   - Соответствие Конституции: {'✓' if has_constitution else '✗'}")
    print(f"   - Указание рисков: {'✓' if has_risks else '✗'}")
    
    # Проверяем дисклеймер
    has_disclaimer = '⚖️' in answer and 'законодательству РБ' in answer
    
    print(f"\n✅ Дисклеймер:")
    print(f"   - Присутствует: {'✓' if has_disclaimer else '✗'}")
    
    # Общая статистика
    total_checks = 9
    passed_checks = sum([
        has_legal_field, has_significance, has_user_level,
        has_law_refs, has_reliability,
        has_conclusion, has_checklist,
        has_constitution, has_risks,
        has_disclaimer
    ])
    
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"   Выполнено пунктов: {passed_checks}/{total_checks} ({passed_checks/total_checks*100:.1f}%)")
    
    if passed_checks >= 7:
        print("   🎉 ОТЛИЧНО! Методология выполняется в полном объеме")
    elif passed_checks >= 5:
        print("   ⚠️  ХОРОШО! Большинство пунктов выполняется")
    else:
        print("   ❌ ТРЕБУЕТСЯ ДОРАБОТКА! Методология выполняется частично")

if __name__ == "__main__":
    test_full_analysis() 