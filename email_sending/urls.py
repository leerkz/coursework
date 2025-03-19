from django.urls import path

from email_sending.views import HomePageView

app_name = 'email_sending'


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    ]


