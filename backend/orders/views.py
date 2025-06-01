from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.repositories import OrderRepository, ProductRepository
from orders.serializers import (
    CreateOrderSerializer,
    OrderOutputSerializer,
    ProductOutputSerializer,
)
from orders.services import OrderService, ProductService
from orders.tasks import import_products


class OrderListCreateView(APIView):
    def get(self, request):
        customer_id = request.query_params.get("customer_id")
        size = int(request.query_params.get("size", 20))
        offset = int(request.query_params.get("offset", 0))
        order_by = request.query_params.get("order_by", "id")

        if not customer_id:
            return Response(
                {"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        repository = OrderRepository()
        orders = OrderService(order_repository=repository).list_orders(
            customer_id=customer_id, size=size, offset=offset, order_by=order_by
        )

        output_serializer = OrderOutputSerializer(orders, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        customer_id = data["customer_id"]
        products = data["items"]

        repository = OrderRepository()
        try:
            order = OrderService(order_repository=repository).create_order(
                customer_id=customer_id, products=products
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        output_serializer = OrderOutputSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    def get(self, request, order_id):
        import_products()
        repository = OrderRepository()

        try:
            order = OrderService(order_repository=repository).get_order(order_id)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)

        output_serializer = OrderOutputSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class ProductListView(APIView):
    def get(self, request):
        size = int(request.query_params.get("size", 20))
        offset = int(request.query_params.get("offset", 0))
        order_by = request.query_params.get("order_by", "id")

        repository = ProductRepository()
        service = ProductService(repository=repository)
        products = service.list_products(size=size, offset=offset, order_by=order_by)

        output_serializer = ProductOutputSerializer(products, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        repository = ProductRepository()
        service = ProductService(repository=repository)

        try:
            product = service.get_product(product_id=product_id)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)

        output_serializer = ProductOutputSerializer(product)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
