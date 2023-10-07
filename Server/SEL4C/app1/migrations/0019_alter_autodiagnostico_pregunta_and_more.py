# Generated by Django 4.2.4 on 2023-10-05 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0018_alter_pregunta_tipo_pregunta"),
    ]

    operations = [
        migrations.AlterField(
            model_name="autodiagnostico",
            name="pregunta",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app1.pregunta",
            ),
        ),
        migrations.AlterField(
            model_name="autodiagnostico",
            name="respuesta",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app1.respuesta",
            ),
        ),
        migrations.AlterField(
            model_name="autodiagnostico",
            name="usuario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app1.usuario",
            ),
        ),
    ]
