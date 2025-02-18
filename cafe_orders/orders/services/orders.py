from typing import Protocol

from django.core.exceptions import ObjectDoesNotExist

from orders.entities.dto import OrderDTO, OrderUpdateDTO
from orders.exceptions import InvalidOrderData, OrderNotFound, InvalidOrderTableData, InvalidOrderItemsData
from orders.repositories.orders import OrdersRepositoryProtocol


class OrdersServiceProtocol(Protocol):

    def calculate_total_price(self, create_objects: OrderDTO):
        ...

    def create_order(self, order_dto: OrderDTO):
        ...

    def get_order(self, order_id: int) -> OrderDTO:
        ...

    def get_by_table(self, table_number: int) -> OrderDTO:
        ...

    def list_orders(self) -> OrderDTO:
        ...

    def update_orders(self, order_id: int, order_dto: OrderDTO):
        ...

    def delete_order(self, order_id: int):
        ...


class OrdersServiceImpl:
    def __init__(self, orders_repository_factory: OrdersRepositoryProtocol):
        self.orders_repository_factory = orders_repository_factory

    def _calculate_total_price(self, order_dto: OrderDTO | OrderUpdateDTO):
        if not order_dto.items:
            raise InvalidOrderData()

        return sum(item["price"] * item["quantity"] for item in order_dto.items)

    def create_order(self, order_dto: OrderDTO) -> OrderDTO:
        if order_dto.table_number < 1:
            raise InvalidOrderTableData()
        for item in order_dto.items:
            if item["price"] < 0:
                raise InvalidOrderItemsData()
        try:
            order_dto.total_price = self._calculate_total_price(order_dto)
            return self.orders_repository_factory.add(order_dto)
        except TypeError as e:
            raise InvalidOrderData()

    def get_order(self, order_id: int) -> OrderDTO:
        return self.orders_repository_factory.get(order_id=order_id)

    def get_by_table(self, table_number: str | None, status: str | None) -> OrderDTO:
        if len(table_number) == 0:
            table_number = None
        return self.orders_repository_factory.get_by_id_table(table_id=table_number, status=status)

    def list_orders(self) -> OrderDTO:
        return self.orders_repository_factory.get_list()

    def update_orders(self, order_id: int, order_dto: OrderUpdateDTO):
        for item in order_dto.items:
            if item["price"] < 0:
                raise InvalidOrderItemsData()
        try:
            order_dto.total_price = self._calculate_total_price(order_dto)
            return self.orders_repository_factory.update(update_objects=order_dto, order_id=order_id)
        except ObjectDoesNotExist:
            raise OrderNotFound()
        except TypeError:
            raise InvalidOrderData()

    def delete_order(self, order_id: int):
        try:
            return self.orders_repository_factory.delete(order_id)
        except:
            raise OrderNotFound()
