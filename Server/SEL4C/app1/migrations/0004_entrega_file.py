# Generated by Django 4.2.4 on 2023-08-31 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_file_entrega_file_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrega',
            name='file',
            field=models.CharField(default='', max_length=50),
        ),
    ]