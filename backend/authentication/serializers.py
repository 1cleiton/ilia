from rest_framework import serializers


class RegisterCustomerSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )

    def validate_password_confirm(self, value):
        if self.initial_data["password"] != value:
            raise serializers.ValidationError("Passwords does not match!")
        return value


class CustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
