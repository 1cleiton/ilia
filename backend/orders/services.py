from orders.repositories import OrderRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def create_order(self, customer_id: int, products: list[dict]):
        order = self.order_repository.create_order(
            customer_id=customer_id, products=products
        )
        return order

    def get_order(self, order_id):
        order = self.order_repository.get_order(order_id)
        return order

    def list_orders(
        self, customer_id: int, size: int = 20, offset: int = 0, order_by: str = "id"
    ):
        orders = self.order_repository.list_orders(
            customer_id=customer_id, size=size, offset=offset, order_by=order_by
        )
        return orders
