# Generated by Django 4.2.13 on 2024-06-04 08:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('robot_currency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyrobot',
            name='dt_add',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
