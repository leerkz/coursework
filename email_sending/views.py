from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from email_sending.models import EmailRecipient, EmailManagement


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


class EmailManagementUpdateView(UpdateView):
    model = EmailManagement
    template_name = "email_sending/email_form.html"
    fields = [
        "topic",
    ]
    success_url = reverse_lazy("email_sending:email_update")


class EmailManagementDeleteView(DeleteView):
    model = EmailManagement
    template_name = "email_sending/email_delete.html"
    success_url = reverse_lazy("email_sending:home")
