### Ситема управления заказами
REST API для управления заказами в ресторане. Проект реализован на Django с использованием DRF (Django REST Framework).

## Установка

### Требования
- Python 3.8+
- PostgreSQL
- Django 4.2
- Виртуальное окружение (опционально)

### Клонирование репозитория
```
git clone https://github.com/Equialy/system_orders_storage.git
cd system_orders_storage
```
- Создать файл .env . Содержимое по аналогии файла .env.example


### Локальное развертывание
Настройка окружения
1. Создайте виртуальное окружение:
```
python -m venv venv
source venv/bin/activate  # В Windows: venv\Scripts\activate
```

2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Применение миграций базы данных:
```
python manage.py migrate
```
4. Запуск сервера:
```
python manage.py runserver
```

## API для приложения

```http://127.0.0.1:8000/api/docs/```

## Примеры заказов

POST /api/orders/create
Content-Type: application/json
```
{
    "table_number": "5",
    "items": [
        {"name": "Стейк Рибай", "price": 2500, "quantity": 1},
        {"name": "Красное вино", "price": 900, "quantity": 2}
    ],
    "status": "В ожидании"
}
```