from django.db import models

from authentication.models import Customer
from orders.choices import STATUS_CHOICES


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=240, verbose_name="Nome")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    image = models.URLField(blank=True, null=True, verbose_name="Imagem")
    available_quantity = models.PositiveIntegerField(
        default=0, verbose_name="Quantidade Disponível"
    )

    def __str__(self):
        return f"{self.name} - {self.price}"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Cliente",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING", verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return f"Pedido #{self.id} para {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Itens do Pedido",
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço Total"
    )

    def __str__(self):
        return f"Pedido #{self.order.id}: {self.product.name} ({self.quantity})"
