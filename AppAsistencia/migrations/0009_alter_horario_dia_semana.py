# Generated by Django 4.2.6 on 2024-04-15 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAsistencia', '0008_alter_horario_dia_semana'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='dia_semana',
            field=models.CharField(max_length=99),
        ),
    ]