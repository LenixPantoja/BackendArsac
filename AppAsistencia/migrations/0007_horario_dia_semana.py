# Generated by Django 4.2.6 on 2024-04-15 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAsistencia', '0006_alter_matricula_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='dia_semana',
            field=models.TextField(default="LUNES", max_length=100),
            preserve_default=False,
        ),
    ]
