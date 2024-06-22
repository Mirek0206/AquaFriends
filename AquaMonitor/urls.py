from django.urls import path
from . import views

app_name = 'AquaMonitor'

urlpatterns = [
    path('aquarium/<int:aquarium_id>/parameters/', views.user_aquariums_and_parameters, name='user_aquariums_and_parameters'),
    path('aquarium/', views.user_aquariums_and_parameters, name='user_aquariums_and_parameters'),
    path('aquarium/<int:aquarium_id>/add_parameter/', views.add_water_parameter, name='add_water_parameter'),
    path('aquarium/<int:aquarium_id>/add_exceptional_situation/', views.add_exceptional_situation, name='add_exceptional_situation'),
]
