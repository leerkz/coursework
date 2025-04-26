from django.urls import path

from email_sending.views import (
    HomePageView,
    EmailRecipientCreateView,
    EmailRecipientDetailView,
    EmailRecipientUpdateView,
    EmailRecipientDeleteView,
    EmailManagementCreateView,
    EmailManagementDetailView,
    EmailManagementUpdateView,
    EmailManagementDeleteView,
    SendingCreateView,
    SendingDetailView,
    SendingUpdateView,
    SendingDeleteView,
    EmailRecipientListView,
    EmailManagementListView,
    SendingListView,
    SendMailingView,
    MailingAttemptListView,
)

app_name = "email_sending"


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("email_create", EmailManagementCreateView.as_view(), name="email_form"),
    path("email/<int:pk>/", EmailManagementDetailView.as_view(), name="email_detail"),
    path(
        "email/<int:pk>/update/",
        EmailManagementUpdateView.as_view(),
        name="email_update",
    ),
    path(
        "email/<int:pk>/delete/",
        EmailManagementDeleteView.as_view(),
        name="email_delete",
    ),
    path("recipient_create", EmailRecipientCreateView.as_view(), name="recipient_form"),
    path(
        "recipient/<int:pk>/",
        EmailRecipientDetailView.as_view(),
        name="recipient_detail",
    ),
    path(
        "recipient/<int:pk>/update/",
        EmailRecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete/",
        EmailRecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("sending_create", SendingCreateView.as_view(), name="sending_form"),
    path("sending/<int:pk>/", SendingDetailView.as_view(), name="sending_detail"),
    path(
        "sending/<int:pk>/update/", SendingUpdateView.as_view(), name="sending_update"
    ),
    path(
        "sending/<int:pk>/delete/", SendingDeleteView.as_view(), name="sending_delete"
    ),
    path("recipients/", EmailRecipientListView.as_view(), name="recipient_list"),
    path("emails/", EmailManagementListView.as_view(), name="email_list"),
    path("sending_list/", SendingListView.as_view(), name="sending_list"),
    path("send_mailing/<int:pk>/", SendMailingView.as_view(), name="send_mailing"),
    path("attempts/", MailingAttemptListView.as_view(), name="mailing_attempt_list"),
]
