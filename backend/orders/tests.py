from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authentication.models import Customer
from orders.models import Order, OrderItem, Product
from orders.tasks import import_products

User = get_user_model()


class OrderTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            email="customer@example.com",
            password="Testpass123!",
            name="Test Customer",
        )
        self.token = Token.objects.create(user=self.customer)

        self.auth_header = {"Authorization": f"Token {self.token.key}"}

        self.product1 = Product.objects.create(name="Product 1", price=10.0)
        self.product2 = Product.objects.create(name="Product 2", price=20.0)

        self.list_create_url = reverse("order-list-create")

        self.order = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=2,
            total_price=self.product1.price * 2,
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            quantity=2,
            total_price=self.product1.price * 2,
        )

    def test_list_orders_success(self):
        response = self.client.get(
            self.list_create_url,
            {"customer_id": self.customer.id},
            headers=self.auth_header,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.order.id)

    def test_list_orders_missing_customer(self):
        response = self.client.get(self.list_create_url, headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_create_order_success(self):
        payload = {
            "items": [
                {"id": self.product1.id, "quantity": 2},
                {"id": self.product2.id, "quantity": 2},
            ],
        }
        response = self.client.post(
            self.list_create_url,
            payload,
            format="json",
            headers=self.auth_header,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(len(response.data["items"]), 2)

    def test_create_order_invalid_product(self):
        payload = {
            "items": [{"id": 9999, "quantity": 1}],
        }
        response = self.client.post(
            self.list_create_url,
            payload,
            format="json",
            headers=self.auth_header,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_create_order_missing_fields(self):
        payload = {}
        response = self.client.post(
            self.list_create_url,
            payload,
            format="json",
            headers=self.auth_header,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("items", response.data)


class OrderDetailTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create_user(
            email="test@example.com", name="Test User", password="testpass"
        )
        self.token = Token.objects.create(user=self.customer)
        self.auth_header = {"Authorization": f"Token {self.token.key}"}

        self.product = Product.objects.create(
            name="Product 1",
            description="Test product",
            price=100,
            available_quantity=10,
        )

        self.order = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            total_price=self.product.price,
            quantity=1,
        )

        self.detail_url = reverse("order-detail", kwargs={"order_id": self.order.id})

    def test_retrieve_order_success(self):
        response = self.client.get(self.detail_url, headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["id"], self.order.id)
        self.assertEqual(response.data["total_price"], self.product.price)
        self.assertGreaterEqual(len(response.data["items"]), 1)

    def test_retrieve_order_not_found(self):
        url = reverse("order-detail", kwargs={"order_id": 9999})
        response = self.client.get(url, headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "O pedido informado não existe")

    def test_retrieve_order_unauthorized(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_order_from_other_customer(self):
        other_customer = Customer.objects.create_user(
            email="other@example.com", name="Other User", password="otherpass"
        )
        other_token = Token.objects.create(user=other_customer)
        other_auth_header = {"Authorization": f"Token {other_token.key}"}

        response = self.client.get(self.detail_url, headers=other_auth_header)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Pedido não pertence ao cliente informado"
        )


class ProductTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create_user(
            email="customer@example.com", name="Customer", password="testpass"
        )
        self.token = Token.objects.create(user=self.customer)
        self.auth_header = {"Authorization": f"Token {self.token.key}"}

        self.product1 = Product.objects.create(
            name="Product 1", price=10.0, available_quantity=100
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=20.0, available_quantity=50
        )

    def test_list_products(self):
        url = reverse("product-list")
        response = self.client.get(url, headers=self.auth_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        product_names = [product["name"] for product in response.data]
        self.assertIn("Product 1", product_names)
        self.assertIn("Product 2", product_names)

    def test_list_products_with_pagination(self):
        url = reverse("product-list") + "?size=1&offset=1"
        response = self.client.get(url, headers=self.auth_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Product 2")

    def test_retrieve_product_success(self):
        url = reverse("product-detail", args=[self.product1.id])
        response = self.client.get(url, headers=self.auth_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.product1.name)
        self.assertEqual(response.data["id"], self.product1.id)

    def test_retrieve_product_not_found(self):
        url = reverse("product-detail", args=[9999])
        response = self.client.get(url, headers=self.auth_header)

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.data)

    def test_list_products_unauthenticated(self):
        url = reverse("product-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_retrieve_product_unauthenticated(self):
        url = reverse("product-detail", args=[self.product1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)


class ImportProductsTestCase(TestCase):
    @patch("orders.tasks.requests.get")
    def test_import_products_success(self, mock_get):
        mock_products = [
            {
                "id": 1,
                "name": "Product 1",
                "description": "Description 1",
                "price": 10.0,
                "available_quantity": 100,
                "image": "http://example.com/image1.png",
            },
            {
                "id": 2,
                "name": "Product 2",
                "description": "Description 2",
                "price": 20.0,
                "available_quantity": 200,
                "image": "http://example.com/image2.png",
            },
        ]

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_products

        imported_count = import_products()

        self.assertEqual(imported_count, 2)
        self.assertEqual(Product.objects.count(), 2)

        product = Product.objects.get(id=1)
        self.assertEqual(product.name, "Product 1")
        self.assertEqual(product.price, 10.0)

    @patch("orders.tasks.requests.get")
    def test_import_products_api_failure(self, mock_get):
        mock_get.return_value.status_code = 500

        imported_count = import_products()

        self.assertEqual(imported_count, 0)
        self.assertEqual(Product.objects.count(), 0)

    @patch("orders.tasks.requests.get")
    def test_import_products_with_existing_product(self, mock_get):
        Product.objects.create(
            id=1,
            name="Existing Product",
            description="Existing Description",
            price=9.99,
            available_quantity=50,
            image="http://example.com/existing.png",
        )

        mock_products = [
            {
                "id": 1,
                "name": "Product 1",
                "description": "Description 1",
                "price": 10.0,
                "available_quantity": 100,
                "image": "http://example.com/image1.png",
            },
            {
                "id": 2,
                "name": "Product 2",
                "description": "Description 2",
                "price": 20.0,
                "available_quantity": 200,
                "image": "http://example.com/image2.png",
            },
        ]

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_products

        imported_count = import_products()

        self.assertEqual(imported_count, 1)
        self.assertEqual(Product.objects.count(), 2)

    @patch("orders.tasks.requests.get")
    def test_import_products_no_url_set(self, mock_get):
        with patch.dict("os.environ", {}, clear=True):
            imported_count = import_products()
            self.assertEqual(imported_count, 0)
            self.assertEqual(Product.objects.count(), 0)
