# Generated by Django 5.0.6 on 2024-07-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0003_article_delete_energydata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='created_at',
        ),
        migrations.AddField(
            model_name='article',
            name='table_name',
            field=models.CharField(choices=[('Table 2-4', 'Table 2-4'), ('Table 2-6', 'Table 2-6'), ('Table 2-7', 'Table 2-7'), ('Table 3-2', 'Table 3-2'), ('Table 3-10', 'Table 3-10'), ('Table 6-5', 'Table 6-5')], default='Table 2-4', max_length=200),
        ),
    ]
