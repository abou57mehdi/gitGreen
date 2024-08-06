from django.shortcuts import render
from .forms import UploadFileForm, AnomalyDetectionForm
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from django.conf import settings

model = joblib.load('anomaly_detection/anomaly_model.pkl')
scaler = joblib.load('anomaly_detection/anomaly_scaler.pkl')


def detect_anomalies(request):
    form = AnomalyDetectionForm(request.POST or None)
    anomalies = None
    if request.method == 'POST':
        if form.is_valid():
            # Extract data from form and process
            data_file = form.cleaned_data['data_file']
            data = pd.read_csv(data_file)
            
            # Preprocess data
            features = data[['energia', 'WORKSTATION_CPU_POWER', 'WORKSTATION_GPU_POWER']]
            features = features.fillna(features.mean())
            scaled_features = scaler.transform(features)
            
            # Apply Isolation Forest
            predictions = model.predict(scaled_features)
            anomalies = predictions == -1
            
            data['Anomaly'] = anomalies
            anomaly_data = data[anomalies]
            
            return render(request, 'anomaly_detection/results.html', {'data': data.to_dict(orient='records'), 'anomalies': anomaly_data.to_dict(orient='records')})

    return render(request, 'anomaly_detection/detect.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                df = pd.read_csv(file)
                print(df.head())  # Debugging: Print the first few rows of the DataFrame
            except Exception as e:
                print(f"Error reading CSV: {e}")

                
            # Identify categorical columns
            categorical_columns = ['MAC', 'weekday', 'fecha_servidor', 'fecha_esp32']

            # Exclude categorical columns
            numerical_columns = [col for col in df.columns if col not in categorical_columns]
            if all(col in df.columns for col in numerical_columns):
                X = df[numerical_columns]
                X_scaled = scaler.transform(X)

                # Predict anomalies
                predictions = model.predict(X_scaled)
                df['Anomaly'] = ['Yes' if p == -1 else 'No' for p in predictions]

                # Save or display the results
                df.to_csv('small_file_with_anomalies.csv', index=False)

                return render(request, 'anomaly_detection/results.html', {'data': df.to_dict(orient='records')})
            else:
                return render(request, 'anomaly_detection/upload.html', {'form': form, 'error': 'CSV does not contain required columns.'})
    else:
        form = UploadFileForm()
    
    return render(request, 'anomaly_detection/upload.html', {'form': form})
