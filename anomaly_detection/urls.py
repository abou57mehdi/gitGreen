from django.urls import path
from .views import upload_file, detect_anomalies
app_name = 'anomaly_detection'


urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('detect/', detect_anomalies, name='detect_anomalies'),
]
