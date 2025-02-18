class OrderNotFound(Exception):
    def __init__(self):
        self.message = "Заказ не найден"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidOrderData(Exception):
    def __init__(self):
        self.message = "Заказ должен содержать хотя бы одно блюдо"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidOrderTableData(Exception):
    def __init__(self):
        self.message = "Номер стола должен быть больше нуля"
        super().__init__(self.message)

    def __str__(self):
        return self.message

class InvalidOrderItemsData(Exception):
    def __init__(self):
        self.message = "Введенные данные заказа некорректны"
        super().__init__(self.message)

    def __str__(self):
        return self.message

