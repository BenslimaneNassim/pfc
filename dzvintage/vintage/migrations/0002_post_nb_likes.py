# Generated by Django 4.1.5 on 2023-06-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vintage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='nb_likes',
            field=models.IntegerField(default=0),
        ),
    ]
