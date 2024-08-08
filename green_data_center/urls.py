from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('monitoring/', include('monitoring.urls')),  # Include monitoring URLs
    path('energy_prediction/', include('energy_prediction.urls')),  # Include energy_prediction URLs
    path('anomalies/', include('anomaly_detection.urls')),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
