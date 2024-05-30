from django.urls import path
from .views import admin_login, admin_panel

urlpatterns = [
    path('aap/login', admin_login, name='admin_login'),
    path('aap/panel', admin_panel, name='admin_panel'),
]