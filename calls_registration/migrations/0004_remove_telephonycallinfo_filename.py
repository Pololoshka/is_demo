# Generated by Django 4.2.13 on 2024-06-06 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calls_registration', '0003_remove_telephonycallinfo_messages_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telephonycallinfo',
            name='filename',
        ),
    ]