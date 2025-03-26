from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from .forms import CustomUserCreationForm


class RecipientRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class RecipientLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("email_sending:home")


class RecipientLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")
