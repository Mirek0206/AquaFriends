from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AquaAccount.urls')),
    path('', include('AquaMaker.urls')),
    path('', include('AquaLife.urls')),
    path('', include('AquaAdminPanel.urls')),
    path('', include('AquaViewMatchShare.urls')),
    path('', include('AquaMonitor.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)