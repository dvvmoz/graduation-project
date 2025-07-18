# 🧠 ML-аналитика в админ-панели

## 📋 Обзор функциональности

Новая секция "ML-аналитика" в админ-панели позволяет администраторам полноценно мониторить и управлять системой ML-фильтра юридических вопросов.

## 🎯 Возможности

### 1. 📊 Общая статистика
- **Всего вопросов** - общее количество обработанных вопросов
- **Принято** - количество и процент принятых вопросов
- **Отклонено** - количество и процент отклоненных вопросов
- **Точность** - процент правильно классифицированных вопросов

### 2. 📈 Детальная аналитика
- **Средняя уверенность** принятых и отклоненных вопросов
- **Высокая уверенность** (>0.9) - количество вопросов с высокой уверенностью
- **Низкая уверенность** (<0.7) - количество вопросов требующих проверки
- **Динамические поиски** - количество обращений к pravo.by

### 3. 🔍 Интерактивные инструменты

#### Вопросы с низкой уверенностью
- Настраиваемый **порог уверенности** (слайдер 0.1-0.9)
- Список последних вопросов с уверенностью ниже порога
- Цветовая индикация: красный (<0.5), желтый (0.5-0.7)

#### Распределение по категориям
- Визуализация популярных категорий вопросов
- Прогресс-бары с процентами
- Количество вопросов по категориям

### 4. 💾 Экспорт данных

#### Настройки экспорта
- **Минимальная уверенность** для экспорта (0.5-1.0)
- **Период данных**: 7/30/90 дней или все время
- Экспорт в CSV формате для дообучения модели

#### Автоматическая генерация файлов
- Файлы с меткой времени: `ml_training_data_20241213_143052.csv`
- Уведомления об успешном экспорте
- Обработка ошибок с детальными сообщениями

## 🔧 Технические особенности

### API Endpoints
```
GET /api/ml-analytics/summary       - Текстовая сводка статистики
GET /api/ml-analytics/stats         - Детальная статистика (JSON)
GET /api/ml-analytics/low-confidence - Вопросы с низкой уверенностью
GET /api/ml-analytics/export        - Экспорт данных в CSV
GET /api/ml-analytics/categories    - Распределение по категориям
```

### Параметры запросов
- `days` - период анализа (по умолчанию 30)
- `threshold` - порог уверенности (по умолчанию 0.7)
- `limit` - лимит результатов (по умолчанию 50)
- `min_confidence` - минимальная уверенность для экспорта (по умолчанию 0.8)

### Автоматическое обновление
- Данные обновляются при переключении на вкладку
- Интерактивные элементы обновляют данные в реальном времени
- Кнопка "Обновить" для принудительного обновления

## 📱 Интерфейс

### Навигация
```
🧠 ML-аналитика - новая секция в боковом меню
```

### Структура страницы
1. **Заголовок** с кнопкой обновления
2. **Общая статистика** - текстовая сводка
3. **Карточки метрик** - ключевые показатели
4. **Графики и детали** - категории и проблемные вопросы
5. **Экспорт и управление** - инструменты для дообучения

## 🚀 Использование

### Ежедневный мониторинг
1. Откройте админ-панель: `http://127.0.0.1:5000`
2. Перейдите в раздел "ML-аналитика"
3. Проверьте общую статистику и точность
4. Просмотрите вопросы с низкой уверенностью

### Дообучение модели
1. Настройте минимальную уверенность (рекомендуется 0.8)
2. Выберите период данных (30 дней для регулярного обновления)
3. Нажмите "Экспорт CSV"
4. Используйте полученный файл для дообучения

### Анализ проблем
1. Снизьте порог уверенности для поиска проблемных вопросов
2. Проанализируйте распределение по категориям
3. Выявите категории с низкой производительностью
4. Настройте фильтр для улучшения точности

## ⚙️ Настройки

### Пороги уверенности
- **Высокая уверенность**: > 0.9 (отличная классификация)
- **Средняя уверенность**: 0.7-0.9 (хорошая классификация)
- **Низкая уверенность**: < 0.7 (требует проверки)

### Рекомендуемые настройки
- **Мониторинг**: порог 0.7, период 30 дней
- **Экспорт**: минимальная уверенность 0.8
- **Анализ проблем**: порог 0.5, лимит 50

## 🔐 Безопасность

- Доступ только для авторизованных администраторов
- Все данные обрабатываются локально
- Экспорт файлов в безопасную папку проекта
- Логирование всех операций

## 📊 Пример использования

### Сценарий 1: Еженедельный мониторинг
```
1. Откройте ML-аналитику
2. Проверьте точность (цель: >85%)
3. Просмотрите вопросы с низкой уверенностью
4. Если точность падает - экспортируйте данные для дообучения
```

### Сценарий 2: Подготовка к дообучению
```
1. Установите период: 30 дней
2. Минимальная уверенность: 0.8
3. Экспорт CSV
4. Проанализируйте категории для улучшения
```

### Сценарий 3: Отладка проблем
```
1. Порог уверенности: 0.5
2. Изучите проблемные вопросы
3. Выявите паттерны ошибок
4. Корректируйте логику фильтра
```

## 🎯 Метрики успеха

- **Точность классификации**: >85%
- **Вопросы с высокой уверенностью**: >60%
- **Вопросы с низкой уверенностью**: <10%
- **Регулярность экспорта**: еженедельно
- **Время отклика интерфейса**: <2 сек

---

**Система готова для профессионального мониторинга и управления ML-фильтром!** 🚀 