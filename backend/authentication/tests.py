from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class LoginViewTests(APITestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "strongpassword123"
        self.user = User.objects.create_user(
            email=self.email, password=self.password, name="Test User"
        )
        self.url = reverse("login")  # Use the name of your route

    def test_login_success(self):
        """Test user can login with valid credentials."""
        response = self.client.post(
            self.url, {"email": self.email, "password": self.password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data["token"], token.key)

    def test_login_invalid_password(self):
        """Test login fails with wrong password."""
        response = self.client.post(
            self.url, {"email": self.email, "password": "wrongpassword"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "E-mail ou senha inválidos")

    def test_login_invalid_email(self):
        """Test login fails with wrong email."""
        response = self.client.post(
            self.url, {"email": "wrong@example.com", "password": self.password}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "E-mail ou senha inválidos")

    def test_login_missing_fields(self):
        """Test login fails if email or password is missing."""
        response = self.client.post(self.url, {"email": self.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, {"password": self.password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")  # Match your URL name
        self.valid_payload = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }

    def test_register_success(self):
        """Test that a user can register successfully."""
        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.valid_payload["email"])
        self.assertEqual(response.data["name"], self.valid_payload["name"])

        user = User.objects.get(email=self.valid_payload["email"])
        self.assertTrue(user.check_password(self.valid_payload["password"]))

    def test_register_missing_fields(self):
        """Test registration fails if required fields are missing."""
        payload = {
            "email": "missing@example.com",
            "password": "password123",
            # missing 'name'
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_register_invalid_email(self):
        """Test registration fails with invalid email format."""
        payload = {
            "email": "invalid-email",
            "password": "password123",
            "name": "Invalid Email",
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_duplicate_email(self):
        """Test registration fails if email is already taken."""
        User.objects.create_user(
            email=self.valid_payload["email"],
            password="AnotherPass123",
            name="Existing User",
        )

        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("duplicate key", response.data["error"])
