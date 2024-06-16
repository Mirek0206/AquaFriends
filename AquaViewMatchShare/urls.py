from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.lobby, name="chat-lobby"),

    path('find_best_match/', views.findBestMatch, name='find_best_match'),
    path('accept/<int:user_id>/', views.acceptMatch, name='accept'),
    path('reject/<int:user_id>/', views.rejectMatch, name='reject'),

    path('get_oldest_like/', views.getOldestLike, name='get_oldest_like'),
    path('accept_like/<int:user_id>/', views.acceptLike, name='accept_like'),
    path('reject_like/<int:user_id>/', views.rejectLike, name='reject_like'),
]
