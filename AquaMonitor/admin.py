from django.contrib import admin
from AquaAdminPanel.admin import AquaAdminPanel
from AquaMonitor.models import ExceptionalSituation, SituationType, WaterParameter

admin.site.register(WaterParameter)
admin.site.register(ExceptionalSituation)
admin.site.register(SituationType)

AquaAdminPanel().register(WaterParameter)
AquaAdminPanel().register(ExceptionalSituation)
AquaAdminPanel().register(SituationType)