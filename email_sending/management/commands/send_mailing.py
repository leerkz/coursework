from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import now
from email_sending.models import EmailRecipient, EmailManagement, MailingAttempt
from django.conf import settings


class Command(BaseCommand):
    help = "Send emails to recipients and log attempts"

    def handle(self, *args, **kwargs):
        emails = EmailManagement.objects.all()

        for email in emails:
            recipients = EmailRecipient.objects.all()

            for recipient in recipients:
                try:
                    # Отправка письма
                    send_mail(
                        subject=email.topic,
                        message=email.message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )

                    # Логируем успешную попытку
                    MailingAttempt.objects.create(
                        recipient=recipient,
                        email_management=email,
                        status='success',
                        response='Email sent successfully',
                        timestamp=now()
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully sent to {recipient.email}'))

                except Exception as e:
                    # Логируем неуспешную попытку
                    MailingAttempt.objects.create(
                        recipient=recipient,
                        email_management=email,
                        status='failed',
                        response=str(e),
                        timestamp=now()
                    )
                    self.stdout.write(self.style.ERROR(f'Failed to send to {recipient.email}: {e}'))
