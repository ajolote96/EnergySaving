# Generated by Django 2.2 on 2020-05-07 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_autonomoconfig_activado'),
    ]

    operations = [
        migrations.AddField(
            model_name='autonomoconfig',
            name='promedio',
            field=models.FloatField(default=1.0, verbose_name='Promedio'),
            preserve_default=False,
        ),
    ]