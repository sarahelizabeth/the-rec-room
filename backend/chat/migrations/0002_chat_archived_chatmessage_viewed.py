# Generated by Django 4.2.2 on 2023-09-08 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
