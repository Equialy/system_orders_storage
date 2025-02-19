import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from orders.entities.dto import OrderDTO, OrderUpdateDTO
from orders.di import OrdersService
from orders.models import Orders
from orders.serializers import OrdersSerializer, OrdersOperationSerializer, OrdersUpdateSerializer


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def order():
    order_data = OrderDTO(
        table_number=1,
        items=[{"name": "Шоколадный мусс", "price": 500, "quantity": 1}],
        status="В ожидании",
        total_price=10.0
    )
    return OrdersService.create_order(order_data)


@pytest.mark.django_db
class TestOrderAPI:

    def test_list_orders(self, client, order):
        url = reverse('api_orders:order_list')
        response = client.get(url)
        print(response.data)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['table_number'] == order.table_number
        assert response.data[0]['status'] == order.status

    def test_create_order_success(self, client):
        url = reverse('api_orders:order_create')
        data = {
            "table_number": 2,
            "items": [{"name": "Стейк Рибай", "price": 2500, "quantity": 1}],
            "status": "Готово"
        }

        response = client.post(url, data, format='json')

        assert response.status_code == 201
        assert Orders.objects.count() == 1
        assert response.data['table_number'] == 2

    def test_create_order_invalid_data(self, client):
        url = reverse('api_orders:order_create')
        invalid_data = {
            "table_number": -1,
            "items": [{"name": "Стейк Рибай", "price": -3.0, "quantity": 1}],
            "status": "invalid_status"
        }

        response = client.post(url, invalid_data, format='json')

        assert response.status_code == 400


    def test_update_order_success(self, client, order):
        url = reverse('api_orders:order_update', args=[order.id])
        data = {
            "items": [{"name": "Красное вино", "price": 900, "quantity": 2}],
            "status": "В ожидании"
        }

        response = client.put(url, data, format='json')

        assert response.status_code == 201
        updated_order = Orders.objects.get(id=order.id)
        assert updated_order.status == "В ожидании"
        assert updated_order.total_price == 1800.0

    def test_update_order_not_found(self, client):
        url = reverse('api_orders:order_update', args=[999])
        data = {
            "items": [{"name": "Красное вино", "price": 900, "quantity": 2}],
            "status": "В ожидании"
        }

        response = client.put(url, data, format='json')

        assert response.status_code == 404

    def test_delete_order_success(self, client, order):
        url = reverse('api_orders:order_delete', args=[order.id])

        response = client.delete(url)

        assert response.status_code == 200
        assert Orders.objects.count() == 0

    def test_delete_order_not_found(self, client):
        url = reverse('api_orders:order_delete', args=[999])

        response = client.delete(url)

        assert response.status_code == 404

    def test_serialization(self, order):
        serializer = OrdersSerializer(instance=order)
        data = serializer.data

        assert data['table_number'] == order.table_number
        assert data['status'] == order.status
        assert len(data['items']) == 1

    def test_operation_serializer_validation(self):
        valid_data = {
            "table_number": 3,
            "items": [{"name": "Бургер с беконом", "price": 1300, "quantity": 1}],
            "status": "В ожидании"
        }
        serializer = OrdersOperationSerializer(data=valid_data)

        assert serializer.is_valid()

    def test_update_serializer_validation(self):
        valid_data = {
            "items": [{"name": "Бургер с беконом", "price": 1300, "quantity": 1}],
            "status": "Оплачено"
        }
        serializer = OrdersUpdateSerializer(data=valid_data)

        assert serializer.is_valid()