# Generated by Django 4.2.4 on 2024-04-19 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0003_cars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cars',
            name='petrol',
        ),
        migrations.AddField(
            model_name='cars',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
