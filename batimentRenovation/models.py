from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'          # ← ICI
    REQUIRED_FIELDS = ['username']    # username reste demandé pour createsuperuser
    
    USER = 'USER'
    ADMIN = 'ADMIN'

    ROLES_CHOICES = (
        (USER, "Utilisateur"),
        (ADMIN, "Administrateur"),
    )

    role = models.CharField(max_length=30, choices=ROLES_CHOICES, verbose_name='Rôle')

class ContactMessage(models.Model):
    name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email")
    subject = models.CharField("Sujet", max_length=150, blank=True)
    message = models.TextField("Message")
    created_at = models.DateTimeField("Reçu le", auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'Sans sujet'}"
