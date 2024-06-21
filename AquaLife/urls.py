from django.urls import path
from .views import check_species_conflicts, delete_aquarium, delete_fish, edit_aquarium

app_name = 'AquaLife'

urlpatterns = [
    path('aquarium/edit/<int:pk>/', edit_aquarium, name='edit_aquarium'),
    path('fish/delete/<int:pk>/', delete_fish, name='delete_fish'),
    path('aquarium/delete/<int:pk>/', delete_aquarium, name='delete_aquarium'),
    path("check_species_conflicts/", check_species_conflicts, name="check_species_conflicts"),
]