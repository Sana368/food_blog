from django.contrib import admin
from.models import ContactMessage
admin.site.register(ContactMessage)

# Register your models here.
from .models import Product
admin.site.register(Product)