from django.contrib import admin

from AquaAccount.models import Profile
from AquaAdminPanel.admin import AquaAdminPanel

# Register your models here.

admin.site.register(Profile)
AquaAdminPanel().register(Profile)