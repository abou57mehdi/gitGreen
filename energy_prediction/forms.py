from django import forms

class PredictionForm(forms.Form):
    voltaje = forms.FloatField(
        required=True,
        label="Voltage (V)",
        min_value=0,
        max_value=300,
        help_text="Enter voltage in volts. Typical range: 0-300 volts."
    )
    corriente = forms.FloatField(
        required=True,
        label="Current (A)",
        min_value=0,
        max_value=50,
        help_text="Enter current in amperes. Typical range: 0-50 amperes."
    )
    frecuencia = forms.FloatField(
        required=True,
        label="Frequency (Hz)",
        min_value=0,
        max_value=60,
        help_text="Enter frequency in Hertz. Typical range: 0-60 Hertz."
    )
    temperatura_esp32 = forms.FloatField(
        required=True,
        label="ESP32 Temperature (°C)",
        min_value=-40,
        max_value=125,
        help_text="Enter temperature in Celsius. Typical range: -40 to 125°C."
    )
