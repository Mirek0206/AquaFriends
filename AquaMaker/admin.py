from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from AquaAdminPanel.admin import AquaAdminPanel
from .models import Aquarium, Filter, Heater, Light, Pump, Decorator

admin.site.register(Aquarium, SimpleHistoryAdmin)
admin.site.register(Pump)
admin.site.register(Light)
admin.site.register(Heater)
admin.site.register(Filter)
admin.site.register(Decorator)

AquaAdminPanel().register(Aquarium)
AquaAdminPanel().register(Pump)
AquaAdminPanel().register(Light)
AquaAdminPanel().register(Heater)
AquaAdminPanel().register(Filter)
AquaAdminPanel().register(Decorator)
