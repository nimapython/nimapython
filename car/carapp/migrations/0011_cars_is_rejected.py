# Generated by Django 4.2.4 on 2024-04-23 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0010_cars_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
