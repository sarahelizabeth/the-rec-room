# Generated by Django 4.2.2 on 2023-08-19 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_report_type_of_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='body',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
