from django.contrib import admin

from AquaMonitor.models import ExceptionalSituation, WaterParameter

admin.site.register(WaterParameter)
admin.site.register(ExceptionalSituation)