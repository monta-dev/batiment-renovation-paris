from django.contrib import admin
from .models import ContactMessage, User

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")