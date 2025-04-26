from django.urls import path
from .views import RecipientRegisterView, RecipientLoginView, RecipientLogoutView

app_name = "users"

urlpatterns = [
    path("register/", RecipientRegisterView.as_view(), name="register"),
    path("login/", RecipientLoginView.as_view(), name="login"),
    path("logout/", RecipientLogoutView.as_view(), name="logout"),
]
