from django.contrib import admin

from AquaMonitor.models import ExceptionalSituation, SituationType, WaterParameter

admin.site.register(WaterParameter)
admin.site.register(ExceptionalSituation)
admin.site.register(SituationType)