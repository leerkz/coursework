from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from email_sending.models import EmailRecipient, EmailManagement, Sending

from email_sending.models import MailingAttempt


class HomePageView(ListView):
    model = EmailRecipient
    template_name = "email_sending/home.html"
    context_object_name = "recipients"


class EmailRecipientCreateView(CreateView):
    model = EmailRecipient
    template_name = "email_sending/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("email_sending:home")


class EmailRecipientDetailView(DetailView):
    model = EmailRecipient
    template_name = "email_sending/recipient_detail.html"
    context_object_name = "recipient"


class EmailRecipientUpdateView(UpdateView):
    model = EmailRecipient
    template_name = "email_sending/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("email_sending:home")


class EmailRecipientDeleteView(DeleteView):
    model = EmailRecipient
    template_name = "email_sending/recipient_delete.html"
    success_url = reverse_lazy("email_sending:home")


class EmailManagementCreateView(CreateView):
    model = EmailManagement
    template_name = "email_sending/email_form.html"
    fields = [
        "topic",
    ]
    success_url = reverse_lazy("email_sending:home")


class EmailManagementDetailView(DetailView):
    model = EmailManagement
    template_name = "email_sending/email_detail.html"
    context_object_name = "email"


from django.urls import reverse

class EmailManagementUpdateView(UpdateView):
    model = EmailManagement
    template_name = "email_sending/email_form.html"
    fields = ["topic"]

    # Указываем success_url с передачей pk текущего объекта
    def get_success_url(self):
        return reverse('email_sending:email_detail', kwargs={'pk': self.object.pk})



class EmailManagementDeleteView(DeleteView):
    model = EmailManagement
    template_name = "email_sending/email_delete.html"
    success_url = reverse_lazy("email_sending:home")


class SendingCreateView(CreateView):
    model = Sending
    template_name = "email_sending/sending_form.html"
    fields = [
        "message",
    ]
    success_url = reverse_lazy("email_sending:home")


class SendingDetailView(DetailView):
    model = Sending
    template_name = "email_sending/sending_detail.html"
    context_object_name = "sending"


class SendingUpdateView(UpdateView):
    model = Sending
    template_name = "email_sending/sending_form.html"
    fields = [
        "message",
    ]
    success_url = reverse_lazy("email_sending:sending_update")


class SendingDeleteView(DeleteView):
    model = Sending
    template_name = "email_sending/sending_delete.html"
    success_url = reverse_lazy("email_sending:home")


# Контроллер для списка получателей
class EmailRecipientListView(ListView):
    model = EmailRecipient
    template_name = "email_sending/recipient_list.html"
    context_object_name = "recipients"


# Контроллер для списка сообщений
class EmailManagementListView(ListView):
    model = EmailManagement
    template_name = "email_sending/email_list.html"
    context_object_name = "emails"


# Контроллер для списка рассылок
class SendingListView(ListView):
    model = Sending
    template_name = "email_sending/sending_list.html"
    context_object_name = "sendings"

    def get_queryset(self):
        # Убедитесь, что у текущего пользователя есть доступ к данным
        return Sending.objects.filter(user=self.request.user)




class SendMailingView(View):
    def get(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)

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
            sending.status = 'ended'
            sending.save()
            messages.success(request, 'Рассылка успешно отправлена!')
        else:
            messages.error(request, 'Нет доступных получателей.')

        return redirect(reverse_lazy('email_sending:sending_list'))





class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = 'email_sending/mailing_attempt_list.html'
    context_object_name = 'attempts'
    ordering = ['-timestamp']

