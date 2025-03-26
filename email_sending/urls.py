from django.urls import path

from email_sending.views import HomePageView, EmailRecipientCreateView, EmailRecipientDetailView, \
    EmailRecipientUpdateView, EmailRecipientDeleteView

app_name = "email_sending"


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("email_create", EmailRecipientCreateView.as_view(), name="email_form"),
    path("email/<int:pk>/", EmailRecipientDetailView.as_view(), name="email_detail"),
    path("email/<int:pk>/update/", EmailRecipientUpdateView.as_view(), name="email_update"),
    path("email/<int:pk>/delete/", EmailRecipientDeleteView.as_view(), name="email_delete"),
]
