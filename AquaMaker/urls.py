from django.urls import path

from . import views

app_name = 'AquaMaker'

urlpatterns = [
    path("create_aquarium/", views.create_aquarium, name="create_aquarium"),
    path("get_min_power_devices/", views.get_min_power_devices, name="get_min_power_devices"),
    path(
        "history_aquarium/<int:pk>/",
        views.aquarium_history,
        name="history_aquarium",
    ),
]
