from django.urls import path
from rest_framework.routers import SimpleRouter

from authentication import views as auth_views
from orders import views as order_views

router = SimpleRouter()

urlpatterns = [
    path("api/v1/auth/login/", auth_views.LoginView.as_view(), name="login"),
    path("api/v1/auth/register/", auth_views.RegisterView.as_view(), name="register"),
    path(
        "api/v1/orders/",
        order_views.OrderListCreateView.as_view(),
        name="order-list-create",
    ),
    path(
        "api/v1/orders/<int:order_id>/",
        order_views.OrderDetailView.as_view(),
        name="order-detail",
    ),
]

urlpatterns += router.urls
