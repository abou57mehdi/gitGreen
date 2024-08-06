from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('monitoring/', include('monitoring.urls')),  # Include monitoring URLs
    path('energy_prediction/', include('energy_prediction.urls')),  # Include energy_prediction URLs
    path('anomalies/', include('anomaly_detection.urls')),


]
