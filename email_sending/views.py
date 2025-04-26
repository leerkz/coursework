from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from email_sending.models import (
    EmailRecipient,
    EmailManagement,
    Sending,
    MailingAttempt,
)
from users.models import CustomUser


# Главная страница
class HomePageView(LoginRequiredMixin, ListView):
    model = EmailRecipient
    template_name = "email_sending/home.html"
    context_object_name = "recipients"

    def get_queryset(self):
        cached_data = cache.get("home_recipients")
        if not cached_data:
            cached_data = EmailRecipient.objects.all()
            cache.set(
                "home_recipients", cached_data, timeout=60 * 5
            )  # Кешируем на 5 минут
        return cached_data


# Контроллеры для клиентов (EmailRecipient)
class EmailRecipientCreateView(LoginRequiredMixin, CreateView):
    model = EmailRecipient
    template_name = "email_sending/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("email_sending:home")


class EmailRecipientDetailView(LoginRequiredMixin, DetailView):
    model = EmailRecipient
    template_name = "email_sending/recipient_detail.html"
    context_object_name = "recipient"

    def get_object(self, queryset=None):
        recipient_id = self.kwargs["pk"]
        cached_recipient = cache.get(f"recipient_{recipient_id}")

        if not cached_recipient:
            cached_recipient = super().get_object(queryset)
            cache.set(
                f"recipient_{recipient_id}", cached_recipient, timeout=60 * 10
            )  # Кешируем на 10 минут

        return cached_recipient


class EmailRecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmailRecipient
    template_name = "email_sending/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("email_sending:home")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.user or self.request.user.is_superuser


class EmailRecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmailRecipient
    template_name = "email_sending/recipient_delete.html"
    success_url = reverse_lazy("email_sending:home")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.user or self.request.user.is_superuser


# Контроллеры для EmailManagement
class EmailManagementCreateView(LoginRequiredMixin, CreateView):
    model = EmailManagement
    template_name = "email_sending/email_form.html"
    fields = ["topic"]
    success_url = reverse_lazy("email_sending:home")


class EmailManagementDetailView(LoginRequiredMixin, DetailView):
    model = EmailManagement
    template_name = "email_sending/email_detail.html"
    context_object_name = "email"


class EmailManagementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmailManagement
    template_name = "email_sending/email_form.html"
    fields = ["topic"]

    def get_success_url(self):
        return reverse("email_sending:email_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        email = self.get_object()
        return self.request.user == email.user or self.request.user.is_superuser


class EmailManagementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmailManagement
    template_name = "email_sending/email_delete.html"
    success_url = reverse_lazy("email_sending:home")

    def test_func(self):
        email = self.get_object()
        return self.request.user == email.user or self.request.user.is_superuser


# Контроллеры для рассылок (Sending)
class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    template_name = "email_sending/sending_form.html"
    fields = ["message"]
    success_url = reverse_lazy("email_sending:home")


class SendingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Sending
    template_name = "email_sending/sending_detail.html"
    context_object_name = "sending"

    def test_func(self):
        sending = self.get_object()
        return self.request.user == sending.user or self.request.user.is_superuser


class SendingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sending
    template_name = "email_sending/sending_form.html"
    fields = ["message"]
    success_url = reverse_lazy("email_sending:home")

    def test_func(self):
        sending = self.get_object()
        return self.request.user == sending.user or self.request.user.is_superuser


class SendingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Sending
    template_name = "email_sending/sending_delete.html"
    success_url = reverse_lazy("email_sending:home")

    def test_func(self):
        sending = self.get_object()
        return self.request.user == sending.user or self.request.user.is_superuser


# Контроллер для списка получателей
class EmailRecipientListView(LoginRequiredMixin, ListView):
    model = EmailRecipient
    template_name = "email_sending/recipient_list.html"
    context_object_name = "recipients"


# Контроллер для списка сообщений
class EmailManagementListView(LoginRequiredMixin, ListView):
    model = EmailManagement
    template_name = "email_sending/email_list.html"
    context_object_name = "emails"


# Контроллер для списка рассылок
class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = "email_sending/sending_list.html"
    context_object_name = "sendings"

    def get_queryset(self):
        user = self.request.user
        cache_key = f"sending_list_{user.id}"

        cached_sendings = cache.get(cache_key)
        if not cached_sendings:
            if user.is_superuser:
                cached_sendings = Sending.objects.all()
            else:
                cached_sendings = Sending.objects.filter(user=user)
            cache.set(cache_key, cached_sendings, timeout=60 * 5)  # Кеш на 5 минут

        return cached_sendings


# Контроллер для отправки рассылки
class SendMailingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "email_sending.can_send_newsletter"

    def get(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)

        if not self.request.user.is_superuser and self.request.user != sending.user:
            messages.error(request, "Вы можете управлять только своими рассылками.")
            return redirect(reverse_lazy("email_sending:sending_list"))

        recipients = sending.recipients.all()
        subject = sending.message.topic
        body = sending.message.body
        recipient_list = [recipient.email for recipient in recipients]

        if recipient_list:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            sending.status = "ended"
            sending.save()
            cache.delete(
                f"sending_list_{request.user.id}"
            )  # Очистка кеша списка рассылок
            messages.success(request, "Рассылка успешно отправлена!")
        else:
            messages.error(request, "Нет доступных получателей.")

        return redirect(reverse_lazy("email_sending:sending_list"))


# Контроллер для попыток отправки
class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "email_sending/mailing_attempt_list.html"
    context_object_name = "attempts"
    ordering = ["-timestamp"]


# Контроллер блокировки пользователей (только админ или менеджер)
class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    permission_required = "email_sending.can_block_user"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.has_perm(
            "email_sending.can_block_user"
        )

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs.get("pk"))

        if user.is_superuser:
            messages.error(request, "Вы не можете заблокировать администратора.")
            return redirect("email_sending:admin_user_list")

        user.is_active = False
        user.save()
        messages.success(request, f"Пользователь {user.email} заблокирован.")
        return redirect("email_sending:admin_user_list")
