# Generated by Django 2.2.28 on 2023-04-27 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20230427_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='time',
            field=models.IntegerField(default=0.0),
        ),
    ]
