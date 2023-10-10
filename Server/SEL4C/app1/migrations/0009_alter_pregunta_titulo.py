# Generated by Django 4.2.4 on 2023-09-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0008_remove_autodiagnostico_pregunta_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pregunta",
            name="titulo",
            field=models.CharField(
                blank=True,
                max_length=300,
                null=True,
                unique=True,
                verbose_name="Pregunta",
            ),
        ),
    ]