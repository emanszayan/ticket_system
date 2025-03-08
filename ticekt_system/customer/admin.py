from django.contrib import admin
from .models import Customer
# Register your models here.
# admin.site.register(Customer)

@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'mobile','phone','email','address')