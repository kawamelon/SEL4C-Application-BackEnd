# Generated by Django 2.2.28 on 2023-04-16 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20230416_0519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='player_id',
        ),
    ]
