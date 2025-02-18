
from django.urls import path


from orders import views

app_name = "orders"

urlpatterns = [
    path('orders/form', views.OrderFormView.as_view(), name='order_form'),
    path('orders/create', views.OrderCreateView.as_view(), name='order_create'),
    path('', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:order_id>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/search/', views.OrderSearchView.as_view(), name='order_search'),
    path('orders/<int:order_id>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
]
