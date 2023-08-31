# Generated by Django 2.2.28 on 2023-04-26 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20230426_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='player',
        ),
        migrations.RemoveField(
            model_name='session',
            name='session_id',
        ),
        migrations.AddField(
            model_name='player',
            name='history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Session'),
        ),
        migrations.AddField(
            model_name='session',
            name='num_session',
            field=models.IntegerField(default=0),
        ),
    ]
