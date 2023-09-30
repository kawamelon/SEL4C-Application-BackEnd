# Generated by Django 4.2.4 on 2023-09-26 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0010_rename_titulo_pregunta_pregunta"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="autodiagnostico",
            name="titulo",
        ),
        migrations.RemoveField(
            model_name="pregunta",
            name="autodiagnostico",
        ),
        migrations.AddField(
            model_name="autodiagnostico",
            name="index",
            field=models.PositiveIntegerField(default=0, verbose_name="Index"),
        ),
        migrations.AddField(
            model_name="autodiagnostico",
            name="num_auto",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Número de Autodiagnóstico"
            ),
        ),
        migrations.AddField(
            model_name="autodiagnostico",
            name="pregunta",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app1.pregunta",
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="autodiagnostico",
            name="usuario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app1.usuario",
                unique=True,
            ),
        ),
        migrations.DeleteModel(
            name="Respuesta",
        ),
    ]