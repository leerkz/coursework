from users.models import CustomUser
from django.contrib import admin


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ("email", "phone_number", "avatar")
    list_filter = ("email",)
