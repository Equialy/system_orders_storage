from django.http import HttpResponseBadRequest, HttpResponseNotFound

from orders.exceptions import InvalidOrderData, OrderNotFound, InvalidOrderTableData, InvalidOrderItemsData


class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, InvalidOrderData):
            return HttpResponseBadRequest(str(exception), status=400)
        elif isinstance(exception, OrderNotFound):
            return HttpResponseNotFound(str(exception))
        elif isinstance(exception, InvalidOrderTableData):
            return HttpResponseNotFound(str(exception))
        elif isinstance(exception, InvalidOrderItemsData):
            return HttpResponseNotFound(str(exception))


        return None