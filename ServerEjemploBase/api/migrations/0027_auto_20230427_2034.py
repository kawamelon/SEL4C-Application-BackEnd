# Generated by Django 2.2.28 on 2023-04-27 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20230427_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]
