# Generated by Django 4.0.6 on 2022-11-05 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_jobs_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='currency',
            field=models.CharField(default='RUR', max_length=100),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='url',
            field=models.CharField(default='', max_length=500),
        ),
    ]
