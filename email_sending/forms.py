from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm

from email_sending.models import EmailManagement, EmailRecipient, Sending


class StyleFormMixin:
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class EmailManagementForm(StyleFormMixin, ModelForm):
    class Meta:
        model = EmailManagement
        fields = "__all__"

        def init(self, *args, **kwargs):
            self.user = kwargs.pop("user", None)  # Получаем текущего получателя
            super().init(*args, **kwargs)


class EmailRecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = EmailRecipient
        fields = "__all__"


class SendingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Sending
        fields = "__all__"

        def init(self, *args, **kwargs):
            self.user = kwargs.pop("user", None)  # Получаем текущего получателя
            super().init(*args, **kwargs)
