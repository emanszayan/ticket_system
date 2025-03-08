from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    list_display = ('title', 'customer','priority','assigned_to')