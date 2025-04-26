from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser
from email_sending.models import Sending, EmailRecipient


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if sender.name == "users":  # Проверяем, что миграция выполняется в users
        # Создаём группы
        user_group, created = Group.objects.get_or_create(name="Пользователь")
        manager_group, created = Group.objects.get_or_create(name="Менеджер")

        # Получаем модели, для которых нужны разрешения
        sending_ct = ContentType.objects.get_for_model(Sending)
        recipient_ct = ContentType.objects.get_for_model(EmailRecipient)
        user_ct = ContentType.objects.get_for_model(CustomUser)

        # Разрешения для Пользователя
        user_permissions = Permission.objects.filter(
            content_type__in=[sending_ct, recipient_ct],
            codename__in=[
                "add_sending",
                "change_sending",
                "delete_sending",
                "view_sending",
            ],
        )
        user_group.permissions.set(user_permissions)

        # Разрешения для Менеджера
        manager_permissions = Permission.objects.filter(
            content_type__in=[sending_ct, recipient_ct, user_ct]
        )
        manager_group.permissions.set(manager_permissions)
