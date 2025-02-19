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
    """ Сервис для обработки запросов  """

    def __init__(self, orders_repository_factory: OrdersRepositoryProtocol):
        self.orders_repository_factory = orders_repository_factory

    def _calculate_total_price(self, order_dto: OrderDTO | OrderUpdateDTO):
        """ Подсчет общей суммы заказов """
        if not order_dto.items:
            raise InvalidOrderData()

        return sum(item["price"] * item["quantity"] for item in order_dto.items)

    def create_order(self, order_dto: OrderDTO) -> OrderDTO:
        """ Создание заказа
        OrderDTO : DTO заказа, содержащее данные для создания
        InvalidOrderTableData: Если номер стола меньше 1.
        InvalidOrderItemsData: Если цена какого-либо блюда отрицательная.
        InvalidOrderData: Если данные заказа некорректны"""
        if int(order_dto.table_number) < 1:
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
        """ Возвращает заказ по его ID
         OrderNotFound: Если заказ с указанным ID не найден"""
        return self.orders_repository_factory.get(order_id=order_id)

    def get_by_table(self, table_number: int | None, status: str | None) -> OrderDTO:
        """ table_number (int | None): Номер стола. Если None, фильтр по номеру стола не применяется. """
        table_number = int(table_number) if table_number.isdigit() else None
        return self.orders_repository_factory.get_by_id_table(table_id=table_number, status=status)

    def list_orders(self) -> OrderDTO:
        """ Возвращает список всех заказов """
        return self.orders_repository_factory.get_list()

    def update_orders(self, order_id: int, order_dto: OrderUpdateDTO):
        """ Обновляет существующий заказ
        InvalidOrderItemsData: Если цена какого-либо блюда отрицательная.
        OrderNotFound: Если заказ с указанным ID не найден.
        InvalidOrderData: Если данные заказа некорректны."""
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
        """ Удаляет заказ по его ID """
        try:
            return self.orders_repository_factory.delete(order_id)
        except:
            raise OrderNotFound()
