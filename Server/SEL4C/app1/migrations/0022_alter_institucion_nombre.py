# Generated by Django 4.2.6 on 2023-10-08 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_remove_actividad_entrega_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institucion',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Institución'),
        ),
    ]
