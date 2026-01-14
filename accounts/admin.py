from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'date_envoi')
    list_filter = ('date_envoi',)
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('date_envoi',)