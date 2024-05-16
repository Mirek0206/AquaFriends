from django.urls import path
from . import views

urlpatterns = [
    path('create_aquarium/', views.create_aquarium, name='create_aquarium'),
]
