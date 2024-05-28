from django.urls import path
from .views import delete_fish, edit_aquarium

app_name = 'AquaLife'

urlpatterns = [
    path('aquarium/edit/<int:pk>/', edit_aquarium, name='edit_aquarium'),
    path('fish/delete/<int:pk>/', delete_fish, name='delete_fish'),
]