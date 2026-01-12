from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "Votre Nom",
            }),
            "email": forms.EmailInput(attrs={
                "class": "contact-input",
                "placeholder": "Votre Email",
            }),
            "subject": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "Sujet de votre message",
            }),
            "message": forms.Textarea(attrs={
                "class": "contact-textarea",
                "placeholder": "Votre Message",
                "rows": 5,
            }),
        }

    def send_email(self, instance: ContactMessage):
        subject = instance.subject or "Nouveau message de contact"
        full_message = (
            f"De: {instance.name} <{instance.email}>\n\n"
            f"Message:\n{instance.message}\n\n"
            f"Reçu le: {instance.created_at}"
        )
        send_mail(
            subject=subject,
            message=full_message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", instance.email),
            recipient_list=[getattr(settings, "CONTACT_RECIPIENT_EMAIL", "admin@example.com")],
            fail_silently=False,
        )
