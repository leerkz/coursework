from django.db import models


# Create your models here.
class EmailRecipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name='ф.и.о')
    comment = models.TextField(verbose_name='комментарий')

    class Meta:
        verbose_name = 'получатель расслылки'
        verbose_name_plural = 'получатели рассылок'
        ordering = ['email', 'full_name']

    def __str__(self):
        return self.email

class EmailManagement(models.Model):
    topic = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    class Meta:
        verbose_name = 'управление сообщением'
        verbose_name_plural = 'управление сообщениями'
        ordering = ['topic']

    def __str__(self):
        return self.topic

class Sending(models.Model):
    SENDING_STATUS = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('ended', 'Завершена')
    ]
    datetime_start = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата и время начало отправки")
    datetime_end = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=18, choices=SENDING_STATUS, default='created', verbose_name='статус рассылки')
    recipients = models.ManyToManyField(EmailRecipient, verbose_name='получатели')
    message = models.ForeignKey(EmailManagement, on_delete=models.CASCADE, verbose_name='Сообщения')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['message']

class EmailingTry(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    TRY_STATUS = [
        ('successful', 'успешно'),
        ('failed', 'не успешно')
    ]
    status = models.CharField(max_length=18, choices=TRY_STATUS, verbose_name='статус рассылки')
    email_answer = models.TextField(verbose_name='Ответ почтового сераера', blank=True, null=True)
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, verbose_name='попытка рассылки')

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытка рассылок'
        ordering = ['-datetime']

    def __str__(self):
        return f'Попытка рассылки {self.id}'
