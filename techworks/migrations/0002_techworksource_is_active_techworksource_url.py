# Generated by Django 4.0.5 on 2022-06-07 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techworks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='techworksource',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='techworksource',
            name='url',
            field=models.CharField(default='', max_length=255),
        ),
    ]