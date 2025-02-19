import json

import pytest
from django.db import transaction
from django.urls import reverse

from orders.di import OrdersService
from orders.entities.dto import OrderDTO, OrderUpdateDTO
from orders.exceptions import InvalidOrderItemsData
from orders.repositories.orders import OrdersRepositoryImpl
from orders.services.orders import OrdersServiceImpl


@pytest.fixture
def order():
    order_data = OrderDTO(table_number=1, items=[{"name": "Стейк Рибай", "price": 2500, "quantity": 1}], status="В ожидании")
    return OrdersService.create_order(order_data)


@pytest.mark.django_db
def test_order_list_view(client, order):
    url = reverse('orders:order_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'order_list.html' in [t.name for t in response.templates]
    assert order in response.context['orders']


@pytest.mark.django_db
def test_order_form_view(client):
    url = reverse('orders:order_form')
    response = client.get(url)

    assert response.status_code == 200
    assert 'order_form.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_order_search_view(client, order):
    url = reverse('orders:order_search')
    params = {
        'table_number': order.table_number,
        'status': order.status
    }
    response = client.get(url, params)

    assert response.status_code == 200
    assert 'order_search.html' in [t.name for t in response.templates]
    assert order in response.context['orders']


@pytest.mark.django_db
def test_order_create_view(client):
    url = reverse('orders:order_create')
    data = {
        'table_number': 2,
        'status': 'completed',
        'items': json.dumps([{"name": "Бургер с беконом", "price": 1300, "quantity": 1}])
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('orders:order_list')

    orders = OrdersService.list_orders()
    assert len(orders) == 1
    assert orders[0].table_number == 2


@pytest.mark.django_db
def test_order_update_view_get(client, order):
    url = reverse('orders:order_update', args=[order.id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'order_edit.html' in [t.name for t in response.templates]
    assert response.context['order'] == order


@pytest.mark.django_db
def test_order_update_view_post(client, order):
    url = reverse('orders:order_update', args=[order.id])
    data = {
        'status': 'completed',
        'items': json.dumps([{"name": "Бургер с беконом", "price": 1300, "quantity": 1}])
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('orders:order_list')

    updated_order = OrdersService.get_order(order.id)
    assert updated_order.status == 'completed'
    assert updated_order.items == [{"name": "Бургер с беконом", "price": 1300, "quantity": 1}]


@pytest.mark.django_db
def test_order_delete_view(client, order):
    url = reverse('orders:order_delete', args=[order.id])
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('orders:order_list')


# ----- Проверка атомарности ----


@pytest.fixture
def orders_repo():
    return OrdersRepositoryImpl()


@pytest.fixture
def orders_service(orders_repo):
    return OrdersServiceImpl(orders_repo)


@pytest.mark.django_db
def test_atomic_update_on_failure(orders_service, orders_repo):
    order = orders_repo.add(OrderDTO(
        table_number=1,
        items=[{"name": "Бургер с беконом", "price": 1300, "quantity": 1}],
        status="pending",
        total_price=10.0
    ))

    original_items = order.items
    original_status = order.status
    invalid_update = OrderUpdateDTO(
        items=[{"name": "Бургер с беконом", "price": -3.0, "quantity": 1}],  # Отрицательная цена
        status="processing"
    )
    with pytest.raises(InvalidOrderItemsData):
        with transaction.atomic():
            orders_service.update_orders(order.id, invalid_update)

    updated_order = orders_repo.get(order.id)
    assert updated_order.items == original_items
    assert updated_order.status == original_status


@pytest.mark.django_db
def test_transaction_multiple_operations(orders_service, orders_repo):
    valid_order = OrderDTO(
        table_number=1,
        items=[{"name": "Бургер с беконом", "price": 1300, "quantity": 1}],
        status="pending",
        total_price=10.0
    )
    invalid_order = OrderDTO(
        table_number=2,
        items=[{"name": "Бургер с беконом", "price": -3.0, "quantity": 1}],  # Отрицательная цена
        status="pending"
    )

    try:
        with transaction.atomic():
            orders_service.create_order(valid_order)
            orders_service.create_order(invalid_order)
    except InvalidOrderItemsData:
        pass
    assert len(orders_repo.get_list()) == 0
