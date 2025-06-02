from rest_framework import serializers

from authentication.serializers import CustomerSerializer


class OrderProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    def get_name(self, obj):
        return obj.product.name if hasattr(obj, "product") else obj.get("name", "")


class CreateOrderSerializer(serializers.Serializer):
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


class ProductOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=240, read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    description = serializers.CharField(read_only=True, allow_blank=True)
    image = serializers.URLField(read_only=True, allow_blank=True)
    available_quantity = serializers.IntegerField(read_only=True)
