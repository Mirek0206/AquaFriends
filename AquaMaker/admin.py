from django.contrib import admin
from .models import Aquarium, Pump, Light, Heater, Filter

admin.site.register(Aquarium)
admin.site.register(Pump)
admin.site.register(Light)
admin.site.register(Heater)
admin.site.register(Filter)
