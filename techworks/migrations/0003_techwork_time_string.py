# Generated by Django 4.0.5 on 2022-06-16 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techworks', '0002_techworksource_is_active_techworksource_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='techwork',
            name='time_string',
            field=models.CharField(max_length=300, null=True, verbose_name='Дата публикации'),
        ),
    ]
