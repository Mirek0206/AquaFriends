from django.contrib import admin

from AquaAdminPanel.admin import AquaAdminPanel

from .models import Aquarium, Filter, Heater, Light, Pump

admin.site.register(Aquarium)
admin.site.register(Pump)
admin.site.register(Light)
admin.site.register(Heater)
admin.site.register(Filter)

AquaAdminPanel().register(Aquarium)
AquaAdminPanel().register(Pump)
AquaAdminPanel().register(Light)
AquaAdminPanel().register(Heater)
AquaAdminPanel().register(Filter)
