from django.db.models import Prefetch

from authentication.models import Customer
from orders.models import Order, OrderItem, Product


class OrderRepository:
    def create_order(self, customer_id: int, products: list[dict]):
        try:
            customer = Customer.objects.get(id=customer_id)
            order = Order.objects.create(customer=customer)
            for p in products:
                product = Product.objects.get(id=p["id"])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=p["quantity"],
                    total_price=product.price * p["quantity"],
                )
        except Customer.DoesNotExist:
            raise ValueError("O cliente informado não existe")
        except Product.DoesNotExist:
            raise ValueError("Um ou mais produtos informados não existem")
        except Exception as e:
            raise ValueError(f"Ocorreu um erro enquanto criávamos o pedido: {str(e)}")

        return order

    def list_orders(
        self, customer_id: int, size: int = 20, offset: int = 0, order_by: str = "id"
    ):
        orders = (
            Order.objects.filter(customer_id=customer_id)
            .order_by(order_by)
            .prefetch_related(Prefetch("items"))
            .select_related("customer")
        )

        return orders[offset : offset + size]

    def get_order(self, order_id: int):
        try:
            order = Order.objects.prefetch_related("items__product").get(id=order_id)
            return order
        except Order.DoesNotExist:
            raise ValueError("O pedido informado não existe")
