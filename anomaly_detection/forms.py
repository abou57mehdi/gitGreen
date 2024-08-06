from django import forms

class AnomalyDetectionForm(forms.Form):
    data_file = forms.FileField(label='Upload CSV File')
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Upload CSV File')