# Generated by Django 4.1.5 on 2023-06-13 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vintage', '0015_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
