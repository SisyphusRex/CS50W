from django.contrib import admin
from .models import User, Email

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active")


class EmailAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipients", "subject")


admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)
