from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import joblib
import numpy as np
from .forms import PredictionForm
import os
from django.conf import settings

# Define file paths relative to the current file
def get_model_path(filename):
    return os.path.join(settings.BASE_DIR, 'energy_prediction', filename)

# Load the model, scaler, and encoder
model_path = get_model_path('model.joblib')
scaler_path = get_model_path('scaler.joblib')
encoder_path = get_model_path('encoder.joblib')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
encoder = joblib.load(encoder_path)

def predict(request):
    prediction = None
    form = PredictionForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                # Retrieve form data
                voltaje = form.cleaned_data.get('voltaje')
                corriente = form.cleaned_data.get('corriente')
                frecuencia = form.cleaned_data.get('frecuencia')
                temperatura_esp32 = form.cleaned_data.get('temperatura_esp32')
                
                # Debugging: Print the cleaned data
                print(f"voltaje: {voltaje}, corriente: {corriente}, frecuencia: {frecuencia}, temperatura_esp32: {temperatura_esp32}")

                if None in [voltaje, corriente, frecuencia, temperatura_esp32]:
                    raise ValueError("One or more form fields have invalid values.")

                # Prepare the data for prediction
                data = np.array([[voltaje, corriente, frecuencia, temperatura_esp32]])

                # Scale the data
                scaled_data = scaler.transform(data)

                # Make prediction
                prediction = model.predict(scaled_data)[0]

            except Exception as e:
                return render(request, 'energy_prediction/predict_form.html', {
                    'form': form,
                    'error': f"An error occurred: {e}"
                })
        else:
            return render(request, 'energy_prediction/predict_form.html', {
                'form': form,
                'error': 'Form validation failed. Please check your input values.'
            })

    return render(request, 'energy_prediction/predict_form.html', {'form': form, 'prediction': prediction})
