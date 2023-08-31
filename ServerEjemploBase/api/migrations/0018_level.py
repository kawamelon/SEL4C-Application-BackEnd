# Generated by Django 2.2.28 on 2023-04-20 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20230419_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_level', models.PositiveIntegerField(blank=True, null=True, verbose_name='Level')),
                ('max_score', models.PositiveIntegerField(blank=True, null=True, verbose_name='MAX Score')),
            ],
        ),
    ]
