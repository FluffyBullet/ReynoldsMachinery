# Generated by Django 3.2.16 on 2023-07-05 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machinetrack', '0019_auto_20230704_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineprofile',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='machinetrack.machinemodel', to_field='model_name'),
        ),
    ]
