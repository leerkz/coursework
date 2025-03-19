from django.contrib import admin
from .models import EmailRecipient, EmailManagement, Sending

@admin.register(EmailRecipient)
class EmailRecipientAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'full_name',
        'comment',
    )
    list_filter = ('email', 'full_name')

@admin.register(EmailManagement)
class EmailManagementAdmin(admin.ModelAdmin):
    list_display = (
        'topic',
        'body',
    )
    list_filter = ('topic',)

@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = (
        'datetime_start',
        'datetime_end',
        'status',
        'get_recipients',  # Используем метод вместо ManyToMany
        'message',
    )
    list_filter = ('status', 'datetime_start', 'datetime_end')
    search_fields = ('message__topic', 'recipients__email')  # Поправил поиск

    def get_recipients(self, obj):
        return ', '.join([recipient.email for recipient in obj.recipients.all()])  # Метод для отображения получателей

    get_recipients.short_description = 'Получатели'  # Название столбца в админке
