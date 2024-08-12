from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    chart_type = forms.ChoiceField(choices=[
        ('line', 'Line Chart'),
        ('scatter', 'Scatter Plot'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart')
    ])
    x_axis = forms.IntegerField(min_value=1, label='X-Axis Column Number')
    y_axis = forms.CharField(max_length=255, label='Y-Axis Column Numbers (comma-separated)')
