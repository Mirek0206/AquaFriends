from django.contrib import admin
from AquaViewMatchShare.models import Message
from AquaAdminPanel.admin import AquaAdminPanel

# Register your models here.
admin.site.register(Message)
AquaAdminPanel().register(Message)