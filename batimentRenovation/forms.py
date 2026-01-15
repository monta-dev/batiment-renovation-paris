from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
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

class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=150,
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'auth-input',
            'placeholder': 'votre@email.com'
        })
    )
    password = forms.CharField(
        max_length=63,
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'auth-input',
            'placeholder': '••••••••'
        })
    )

User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=150,
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'auth-input',
            'placeholder': 'votre@email.com'
        })
    )

    class Meta:
        model = User
        fields = ['email']  # Seulement email (password1/2 auto UserCreationForm)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter la classe CSS aux champs de mot de passe générés automatiquement
        self.fields['password1'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': '••••••••'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': '••••••••'
        })
        # Optionnel : personnaliser les labels
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        if not user.username:
            user.username = email  # on aligne username sur email
        # Rôle "User" par défaut (pas de champ role dans Meta)
        if hasattr(user, 'role'):
            user.role = 'User'
        if commit:
            user.save()
        return user