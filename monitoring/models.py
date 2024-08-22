from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    table_name = models.CharField(max_length=200, choices=[
        ('Table 2-4', 'Table 2-4'),
        ('Table 2-6', 'Table 2-6'),
        ('Table 2-7', 'Table 2-7'),
        ('Table 3-2', 'Table 3-2'),
        ('Table 3-10', 'Table 3-10'),
        ('Table 6-5', 'Table 6-5'),
        ('Data Center Statistics', 'Data Center Statistics')
    ], default='Table 2-4')
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # New image field


class DataSource(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # e.g., 'SQL', 'FTP'
    connection_info = models.TextField()  # JSON or plain text with connection details

    def __str__(self):
        return self.name