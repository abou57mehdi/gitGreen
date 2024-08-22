from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Upload CSV File')
    chart_type = forms.ChoiceField(
        choices=[('line', 'Line'), ('scatter', 'Scatter'), ('bar', 'Bar'), ('pie', 'Pie')],
        label='Chart Type'
    )
    x_axis = forms.IntegerField(label='X-Axis Column Number')
    y_axis = forms.CharField(label='Y-Axis Column Numbers (comma-separated)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
        self.fields['chart_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['x_axis'].widget.attrs.update({'class': 'form-control'})
        self.fields['y_axis'].widget.attrs.update({'class': 'form-control'})






from django import forms

class DataSourceForm(forms.Form):
    SOURCE_CHOICES = [
        ('ftp', 'FTP'),
        ('sql', 'SQL'),
    ]
    
    chart_type = forms.ChoiceField(
        choices=[('line', 'Line'), ('scatter', 'Scatter'), ('bar', 'Bar'), ('pie', 'Pie')],
        label='Chart Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    x_axis = forms.CharField(
        label='X-Axis Column',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    y_axis = forms.CharField(
        label='Y-Axis Columns (comma-separated)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # FTP-specific fields
    ftp_server = forms.CharField(
        required=False,
        label='FTP Server',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    ftp_user = forms.CharField(
        required=False,
        label='FTP User',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    ftp_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='FTP Password'
    )
    ftp_file_path = forms.CharField(
        required=False,
        label='FTP File Path',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # SQL-specific fields
    sql_host = forms.CharField(
        required=False,
        label='SQL Host',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    sql_user = forms.CharField(
        required=False,
        label='SQL User',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    sql_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='SQL Password'
    )
    sql_database = forms.CharField(
        required=False,
        label='SQL Database',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    sql_query = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
        label='SQL Query'
    )
    db_type = forms.ChoiceField(
        choices=[('postgresql', 'PostgreSQL'), ('mysql', 'MySQL')],
        required=False,
        label='Database Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    source_type = forms.ChoiceField(
        choices=[('ftp', 'FTP'), ('sql', 'SQL')],
        label='Data Source',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
