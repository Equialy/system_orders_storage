from django.urls import path

from api.orders_api import views

app_name = "api_orders"

urlpatterns = [
    path('orders/list',views.OrderListAPIView.as_view(),name='order_list'),
    path('orders/create',views.OrderCreateAPIView.as_view(),name='order_create'),
    path('orders/update/<int:order_id>',views.OrderUpdateAPIView.as_view(),name='order_update'),
    path('orders/delete/<int:order_id>',views.OrderDeleteAPIView.as_view(),name='order_delete'),
    ]
