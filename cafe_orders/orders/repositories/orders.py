from typing import Protocol

from django.db import transaction

from orders.entities.dto import OrderDTO, OrderUpdateDTO
from orders.models import Orders


class OrdersRepositoryProtocol(Protocol):

    def add(self, create_objects: OrderDTO):
        ...

    def get(self, order_id: int):
        ...

    def get_by_id_table(self, table_id: int | None, status: str | None) -> OrderDTO:
        ...

    def get_list(self):
        ...

    def update(self, order_id: int, update_objects: OrderUpdateDTO):
        ...

    def delete(self, delete_objects: int):
        ...


class OrdersRepositoryImpl:
    """ Реализация репозитория для работы с заказами """

    def __init__(self):
        self.model = Orders

    def add(self, create_objects: OrderDTO):
        """ Добавляет новый заказ в базу данных """
        order = self.model.objects.create(table_number=create_objects.table_number,
                                          items=create_objects.items,
                                          status=create_objects.status,
                                          total_price=create_objects.total_price)
        return order

    def get(self, order_id: int):
        """ Возвращает заказ по его ID """
        return self.model.objects.get(id=order_id)

    def get_by_id_table(self, table_id=None, status=None) -> OrderDTO:
        """ Возвращает заказы по номеру стола и/или статусу
        return: QuerySet[Orders]: Список заказов, соответствующих критериям"""
        if table_id and status:
            return self.model.objects.filter(table_number=table_id, status=status)
        if table_id is not None:
            return self.model.objects.filter(table_number=table_id)
        if status:
            return self.model.objects.filter(status=status)

    def get_list(self):
        """ Возвращает список всех заказов """
        return list(self.model.objects.all())

    @transaction.atomic
    def update(self, order_id: int, update_objects: OrderUpdateDTO):
        """ Обновляет существующий заказ """
        order = self.model.objects.get(pk=order_id)
        order.items = update_objects.items
        order.status = update_objects.status
        if hasattr(update_objects, 'table_number'):
            order.table_number = update_objects.table_number
        if hasattr(update_objects, 'total_price'):
            order.total_price = update_objects.total_price
        order.save()
        return order

    @transaction.atomic
    def delete(self, delete_objects: int):
        """ Удаляет заказ по его ID """
        order = self.model.objects.get(id=delete_objects)
        order.delete()
