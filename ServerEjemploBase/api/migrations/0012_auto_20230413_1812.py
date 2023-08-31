# Generated by Django 2.2.28 on 2023-04-13 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20230412_0616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='complete_l1',
        ),
        migrations.RemoveField(
            model_name='record',
            name='complete_l2',
        ),
        migrations.RemoveField(
            model_name='record',
            name='complete_l3',
        ),
        migrations.RemoveField(
            model_name='record',
            name='time_l1',
        ),
        migrations.RemoveField(
            model_name='record',
            name='time_l2',
        ),
        migrations.RemoveField(
            model_name='record',
            name='time_l3',
        ),
        migrations.RemoveField(
            model_name='record',
            name='total_mistakes_l1',
        ),
        migrations.RemoveField(
            model_name='record',
            name='total_mistakes_l2',
        ),
        migrations.RemoveField(
            model_name='record',
            name='total_mistakes_l3',
        ),
        migrations.AddField(
            model_name='record',
            name='max_levelpoints',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='MAX Points'),
        ),
        migrations.AddField(
            model_name='record',
            name='num_level',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Level'),
        ),
        migrations.AddField(
            model_name='record',
            name='player_points',
            field=models.IntegerField(blank=True, null=True, verbose_name='Player Points'),
        ),
        migrations.AddField(
            model_name='record',
            name='time',
            field=models.DurationField(blank=True, null=True, verbose_name='Time to finish'),
        ),
        migrations.AddField(
            model_name='record',
            name='total_mistakes',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total Mistakes'),
        ),
        migrations.AddField(
            model_name='record',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Updated at'),
        ),
    ]
