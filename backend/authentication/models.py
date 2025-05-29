import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomerManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = Customer(email=email, **extra_fields)
        user.password = make_password(password)
        user.date_joined = datetime.datetime.now(datetime.timezone.utc)
        user.save(using=self._db)

        return user


class Customer(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(max_length=100, unique=True, verbose_name="E-mail")
    password = models.CharField(max_length=100, verbose_name="Senha")

    REQUIRED_FIELDS = ["first_name", "password"]
    USERNAME_FIELD = "email"

    objects = CustomerManager()

    def __str__(self):
        return self.email
