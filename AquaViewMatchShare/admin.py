from django.contrib import admin
from AquaAccount.models import Message
from AquaAdminPanel.admin import AquaAdminPanel

# Register your models here.
admin.site.register(Message)
AquaAdminPanel().register(Message)