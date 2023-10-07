# Generated by Django 4.2.4 on 2023-09-26 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0006_alter_administrador_correo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pregunta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "titulo",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="Pregunta",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="actividad",
            name="tokens",
        ),
        migrations.AddField(
            model_name="entrega",
            name="filename",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Título"
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="correo",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Correo"
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="genero",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Género"
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="nombre",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                unique=True,
                verbose_name="Nombre Completo",
            ),
        ),
        migrations.AlterField(
            model_name="entrega",
            name="file",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Archivo"
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="password",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                unique=True,
                verbose_name="Contraseña",
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="username",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Nombre de Usuario"
            ),
        ),
        migrations.CreateModel(
            name="Respuesta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tokens", models.PositiveIntegerField(default=0)),
                (
                    "pregunta",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app1.pregunta",
                        unique=True,
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app1.usuario",
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Autodiagnostico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "titulo",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="Nombre",
                    ),
                ),
                (
                    "pregunta",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app1.pregunta",
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="progreso",
            name="autodiagnostico",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app1.autodiagnostico",
                unique=True,
            ),
        ),
    ]