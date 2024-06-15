from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Aquarium, Filter, Heater, Light, Pump

admin.site.register(Aquarium, SimpleHistoryAdmin)
admin.site.register(Pump)
admin.site.register(Light)
admin.site.register(Heater)
admin.site.register(Filter)
