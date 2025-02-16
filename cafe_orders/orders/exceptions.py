class OrderNotFound(Exception):
    """Исключение, выбрасываемое, когда заказ не найден."""
    pass

class InvalidOrderData(Exception):
    def __init__(self, message:str):
        """Исключение для некорректных данных заказа."""
        self.message = message

class DishNotFound(Exception):
    """Исключение, выбрасываемое, когда блюдо не найдено."""
    pass


class InvalidOrderDishes(Exception):
    def __init__(self, message:str):
        """Исключение для некорректных данных заказа."""
        self.message = message