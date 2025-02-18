### Ситема управления заказами

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
alembic upgrade head
```
4. Запуск сервера:
```
uvicorn src.main:app --reload
```

