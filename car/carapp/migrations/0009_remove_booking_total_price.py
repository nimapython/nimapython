# Generated by Django 4.2.4 on 2024-04-22 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0008_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='total_price',
        ),
    ]
