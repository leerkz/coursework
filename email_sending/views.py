from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from email_sending.models import EmailRecipient


class EmailRecipientCreateView(CreateView):
    model = EmailRecipient
    template_name = 'email_sending/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('email_sending:home')

class EmailRecipientDetailView(DetailView):
    model = EmailRecipient
    template_name = 'email_sending/recipient_detail.html'
    context_object_name = 'recipient'

class EmailRecipientUpdateView(UpdateView):
    model = EmailRecipient
    template_name = 'email_sending/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('email_sending:home')

class EmailRecipientDeleteView(DeleteView):
    model = EmailRecipient
    template_name = 'email_sending/recipient_delete.html'
    success_url = reverse_lazy('email_sending:home')
