# Generated by Django 4.2.4 on 2024-04-23 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0009_remove_booking_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
