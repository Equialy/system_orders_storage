from django.contrib import admin

from orders.models import Orders


# Register your models here.
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    fields = ["table_number", "items", "total_price", "status"]

