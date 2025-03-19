from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from email_sending.models import EmailRecipient


class EmailRecipientCreateView(CreateView):
    model = EmailRecipient
    #form_class = EmailRecipientForm
    template_name = 'email_sending/recipient_form.html'
    success_url = reverse_lazy('email_sending:home')

class HomePageView(ListView):
    model = EmailRecipient
    template_name = 'email_sending/home.html'
