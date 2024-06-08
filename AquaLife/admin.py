from django.contrib import admin

from AquaAdminPanel.admin import AquaAdminPanel
from AquaLife.models import Fish, Species

admin.site.register(Species)
admin.site.register(Fish)

AquaAdminPanel().register(Species)
AquaAdminPanel().register(Fish)
