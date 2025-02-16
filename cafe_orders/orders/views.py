import json

from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View

from .di import OrdersService
from .entities.dto import OrderDTO, OrderUpdateDTO


class OrderListView(View):
    def get(self, request):
        order_list = OrdersService.list_orders()
        return render(request, 'order_list.html', {'orders': order_list})


class OrderFormView(View):
    def get(self, request):
        return render(request, 'order_form.html')


class OrderCreateView(View):
    def post(self, request):
        table_number = int(request.POST["table_number"])
        status = request.POST["status"]
        items_json = request.POST.get("items")
        if not items_json:
            return HttpResponseBadRequest("Список блюд не передан")
        try:
            items = json.loads(items_json)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Некорректный формат списка блюд")
        if not items:
            return HttpResponseBadRequest("Необходимо добавить хотя бы одно блюдо")

        order_data = OrderDTO(
            table_number=table_number,
            items=items,
            status=status
        )
        OrdersService.create_order(order_data)
        return redirect('order_list')


class OrderUpdateView(View):
    def get(self, request, order_id):
        order = OrdersService.get_order(order_id)
        return render(request, 'order_edit.html', {'order': order})

    def post(self, request, order_id):
        items_json = request.POST.get("items")
        print(order_id)
        try:
            items = json.loads(items_json)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Некорректный формат списка блюд")
        order_update = OrderUpdateDTO(items=items,
                                      status=request.POST["status"]
                                      )
        OrdersService.update_orders(order_id, order_update)
        return redirect('order_list')


class OrderDeleteView(View):
    def post(self, request, order_id):
        OrdersService.delete_order(order_id)
        return redirect('order_list')
