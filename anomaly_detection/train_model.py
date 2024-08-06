import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Load your dataset (replace 'your_dataset.csv' with your actual file)
df = pd.read_csv('cleaned_data.csv')

# Identify categorical columns
categorical_columns = ['MAC', 'weekday', 'fecha_servidor', 'fecha_esp32']  # Adjust if needed

# Exclude categorical columns
numerical_columns = [col for col in df.columns if col not in categorical_columns]
X = df[numerical_columns]

# Preprocess the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the Isolation Forest model
model = IsolationForest(contamination=0.05)  # Adjust the contamination parameter as needed
model.fit(X_scaled)

# Save the model and scaler
joblib.dump(model, 'anomaly_model.pkl')
joblib.dump(scaler, 'anomaly_scaler.pkl')
