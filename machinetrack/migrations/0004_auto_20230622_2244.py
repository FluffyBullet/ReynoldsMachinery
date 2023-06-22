# Generated by Django 3.2.16 on 2023-06-22 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machinetrack', '0003_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='site_address',
        ),
        migrations.AlterField(
            model_name='company',
            name='phone_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
