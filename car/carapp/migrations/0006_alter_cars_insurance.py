# Generated by Django 4.2.4 on 2024-04-19 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0005_alter_cars_registration_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='insurance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
