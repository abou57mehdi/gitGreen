from django.urls import path
from . import views

app_name = 'energy_prediction'  

urlpatterns = [
    path('predict/', views.predict, name='predict_form'),  # Ensure this name matches the one used in the HTML
]
