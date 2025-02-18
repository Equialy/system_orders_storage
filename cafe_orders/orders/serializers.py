from rest_framework import serializers

from orders.models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ["table_number", "items", "total_price", "status"]

class OrdersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ["items",  "status"]

class ItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrdersOperationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    table_number = serializers.IntegerField()
    items = serializers.JSONField()
    status = serializers.CharField()
    total_price = serializers.FloatField(required=False)

