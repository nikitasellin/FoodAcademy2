from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = 'title', 'full_name', 'status'
    ordering = '-received_time',
