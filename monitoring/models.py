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
        ('Data Center Statistics', 'Data Center Statistics')  # Added entry for the new table
    ], default='Table 2-4')
