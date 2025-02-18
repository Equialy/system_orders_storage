from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.di import OrdersService
from orders.entities.dto import OrderDTO, OrderUpdateDTO
from orders.serializers import OrdersSerializer, OrdersOperationSerializer, OrdersUpdateSerializer


@extend_schema(
    tags=['Orders'],
    description='Список заказов',
    request=OrdersSerializer,
)
class OrderListAPIView(APIView):
    serializer_class = OrdersSerializer

    def get(self, request):
        orders = OrdersService.list_orders()
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Orders'],
    description='Создание заказов',
    request=OrdersSerializer,
)
class OrderCreateAPIView(APIView):
    serializer_class = OrdersOperationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_data = OrderDTO(
                table_number=serializer.validated_data['table_number'],
                items=serializer.validated_data['items'],
                status=serializer.validated_data['status']
            )
            orders = OrdersService.create_order(order_dto=order_data)
            response = self.serializer_class(orders)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Orders'],
    description='Обновление заказов',
    request=OrdersUpdateSerializer,
)
class OrderUpdateAPIView(APIView):
    serializer_class = OrdersUpdateSerializer

    def put(self, request, order_id: int):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_data = OrderUpdateDTO(
                items=serializer.validated_data['items'],
                status=serializer.validated_data['status']
            )
            orders = OrdersService.update_orders(order_id=order_id, order_dto=order_data)
            response = self.serializer_class(orders)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Orders'],
    description='Удаление заказов',
    request=OrdersSerializer,
)
class OrderDeleteAPIView(APIView):
    serializer_class = OrdersOperationSerializer

    def delete(self, request, order_id):
        OrdersService.delete_order(order_id=order_id)
        return Response(status=status.HTTP_200_OK)
