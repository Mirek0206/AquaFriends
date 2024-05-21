from django.urls import path
from .views import edit_aquarium

app_name = 'AquaMaker'

urlpatterns = [
    path('aquarium/edit/<int:pk>/', edit_aquarium, name='edit_aquarium'),
]