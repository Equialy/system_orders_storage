
from django.urls import path

from orders import views

urlpatterns = [
    path('orders/form', views.OrderFormView.as_view(), name='order_form'),
    path('orders/create', views.OrderCreateView.as_view(), name='order_create'),
    path('', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:order_id>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:order_id>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
]
