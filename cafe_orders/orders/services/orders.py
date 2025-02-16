from typing import Protocol

from orders.entities.dto import OrderDTO, OrderUpdateDTO
from orders.exceptions import InvalidOrderDishes

from orders.repositories.orders import OrdersRepositoryProtocol


class OrdersServiceProtocol(Protocol):

    def calculate_total_price(self, create_objects: OrderDTO):
        ...

    def create_order(self, create_objects: OrderDTO):
        ...

    def get_order(self, order_id: int) -> OrderDTO:
        ...

    def list_orders(self) -> OrderDTO:
        ...

    def update_orders(self,order_id:int, order_dto: OrderDTO):
        ...

    def delete_order(self, order_dto: OrderDTO):
        ...


class OrdersServiceImpl:
    def __init__(self, orders_repository_factory: OrdersRepositoryProtocol):
        self.orders_repository_factory = orders_repository_factory

    def _calculate_total_price(self, order_dto: OrderDTO | OrderUpdateDTO):
        if not order_dto.items:
            raise InvalidOrderDishes("Заказ должен содержать хотя бы одно блюдо")
        if not order_dto.items:
            raise InvalidOrderDishes("Заказ должен содержать хотя бы одно блюдо.")
        return sum(item["price"] * item["quantity"] for item in order_dto.items)

    def create_order(self, order_dto: OrderDTO) -> OrderDTO:
        order_dto.total_price = self._calculate_total_price(order_dto)

        return self.orders_repository_factory.add(order_dto)

    def get_order(self, order_id: int) -> OrderDTO:
        return self.orders_repository_factory.get(order_id=order_id)

    def list_orders(self) -> OrderDTO:
        return self.orders_repository_factory.get_list()

    def update_orders(self,order_id:int,  order_dto: OrderUpdateDTO):
        order_dto.total_price = self._calculate_total_price(order_dto)
        return self.orders_repository_factory.update(update_objects=order_dto, order_id=order_id)

    def delete_order(self, order_id: int):
        return self.orders_repository_factory.delete(order_id)
