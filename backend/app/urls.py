from django.urls import path
from rest_framework.routers import SimpleRouter

from authentication import views as auth_views

router = SimpleRouter()

urlpatterns = [
    path("api/v1/auth/login/", auth_views.LoginView.as_view(), name="login"),
    path("api/v1/auth/register/", auth_views.RegisterView.as_view(), name="register"),
]

urlpatterns += router.urls
