import datetime

from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Customer
from authentication.serializers import CustomerSerializer, RegisterCustomerSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data["email"].lower()
        password = request.data["password"]

        customer = authenticate(request, email=email, password=password)

        if not customer:
            return Response({"error": "Invalid email or password"}, status=400)

        token = Token.objects.get_or_create(user=customer)
        customer.last_login = datetime.datetime.now(datetime.timezone.utc)
        customer.save()

        return Response({"token": token[0].key}, status=200)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterCustomerSerializer

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=400)

        try:
            customer = Customer.objects.create_user(
                email=serialized_data.validated_data["email"],
                username=serialized_data.validated_data["email"],
                password=serialized_data.validated_data["password"],
                name=serialized_data.validated_data["name"],
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        serialized_user = CustomerSerializer(customer)

        return Response(serialized_user.data, status=201)
