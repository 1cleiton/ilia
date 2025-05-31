from rest_framework import serializers

from authentication.serializers import CustomerSerializer


class OrderProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )


class CreateOrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    items = OrderProductSerializer(many=True)

    def validate_products(self, value):
        if not value:
            raise serializers.ValidationError("Products list cannot be empty.")
        return value


class OrderOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    customer = CustomerSerializer(read_only=True)
    items = OrderProductSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        read_only=True, method_name="get_total_price"
    )
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def get_total_price(self, obj):
        return sum(item["total_price"] for item in obj.items.values("total_price"))
