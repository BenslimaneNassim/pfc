# Generated by Django 4.1.5 on 2023-06-11 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vintage', '0013_profile_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nb_ratings',
            field=models.IntegerField(default=0),
        ),
    ]