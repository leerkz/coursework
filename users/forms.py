from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    country = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "password1",
            "password2",
            "phone_number",
            "country",
            "avatar",
        )
