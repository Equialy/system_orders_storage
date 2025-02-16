from typing import Protocol

from django.db import transaction

from orders.entities.dto import OrderDTO, OrderUpdateDTO
from orders.models import Orders


class OrdersRepositoryProtocol(Protocol):

    def add(self, create_objects: OrderDTO):
        ...

    def get(self, order_id: int):
        ...

    def get_by_id_table(self, table_id: int):
        ...

    def get_list(self):
        ...

    def update(self,order_id: int, update_objects: OrderUpdateDTO):
        ...

    def delete(self, delete_objects: int):
        ...

class OrdersRepositoryImpl:
    def __init__(self):
        self.model = Orders

    def add(self, create_objects: OrderDTO):
        order = self.model.objects.create(table_number=create_objects.table_number,
                                            items=create_objects.items,
                                            status=create_objects.status,
                                            total_price=create_objects.total_price)
        return order

    def get(self, order_id: int):
        return self.model.objects.get(id=order_id)

    def get_by_id_table(self, table_id: int):
        return

    def get_list(self):
        return list(self.model.objects.all())

    def update(self,order_id:int, update_objects: OrderUpdateDTO):
        order = self.model.objects.get(pk=order_id)
        order.items = update_objects.items
        order.status = update_objects.status
        if hasattr(update_objects, 'table_number'):
            order.table_number = update_objects.table_number
        if hasattr(update_objects, 'total_price'):
            order.total_price = update_objects.total_price
        order.save()
        return order

    def delete(self, delete_objects: int):
        self.model.objects.filter(pk=delete_objects).delete()



