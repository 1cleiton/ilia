from orders.repositories import OrderRepository, ProductRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def create_order(self, customer_id: int, products: list[dict]):
        order = self.order_repository.create_order(
            customer_id=customer_id, products=products
        )
        return order

    def get_order(self, order_id, customer_id):
        order = self.order_repository.get_order(order_id)

        if order.customer_id != customer_id:
            raise ValueError("Pedido não pertence ao cliente informado")

        return order

    def list_orders(
        self, customer_id: int, size: int = 20, offset: int = 0, order_by: str = "id"
    ):
        orders = self.order_repository.list_orders(
            customer_id=customer_id, size=size, offset=offset, order_by=order_by
        )
        return orders


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product(self, product_id: int):
        return self.repository.get_product(product_id)

    def list_products(self, size: int = 20, offset: int = 0, order_by: str = "id"):
        return self.repository.list_products(
            size=size, offset=offset, order_by=order_by
        )
