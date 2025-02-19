import json

from django.shortcuts import render, redirect
from django.views import View

from .di import OrdersService
from .entities.dto import OrderDTO, OrderUpdateDTO


class OrderListView(View):
    """ Представление для выдачи всех существующих заказов """

    def get(self, request):
        order_list = OrdersService.list_orders()
        return render(request, 'order_list.html', {'orders': order_list})


class OrderFormView(View):
    """ Представление для выдачи формы создания заказов """

    def get(self, request):
        return render(request, 'order_form.html')


class OrderSearchView(View):
    """ Представление для поиска заказов """

    def get(self, request):
        order = OrdersService.get_by_table(table_number=request.GET["table_number"],
                                           status=request.GET["status"])
        return render(request, "order_search.html", {'orders': order})


class OrderCreateView(View):
    """ Представление для создания заказов """

    def post(self, request):
        table_number = int(request.POST["table_number"])
        status = request.POST["status"]
        items_json = request.POST.get("items")
        items = json.loads(items_json)
        order_data = OrderDTO(table_number=table_number, items=items, status=status)
        OrdersService.create_order(order_data)
        return redirect('orders:order_list')


class OrderUpdateView(View):
    """ Представление для обновления заказов """

    def get(self, request, order_id):
        """ Выдает заказ по ID """
        order = OrdersService.get_order(order_id)
        return render(request, 'order_edit.html', {'order': order})

    def post(self, request, order_id):
        """ Представление для отправки озмененных данных о заказе """
        items_json = request.POST.get("items")
        items = json.loads(items_json)
        order_update = OrderUpdateDTO(items=items, status=request.POST["status"])
        OrdersService.update_orders(order_id, order_update)
        return redirect('orders:order_list')


class OrderDeleteView(View):
    """ Представление для удаления заказов """

    def post(self, request, order_id):
        OrdersService.delete_order(order_id)
        return redirect('orders:order_list')
