# Generated by Django 5.0.6 on 2024-07-29 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0004_remove_article_created_at_article_table_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCenterStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('data_center_count', models.IntegerField()),
                ('additional_info', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
