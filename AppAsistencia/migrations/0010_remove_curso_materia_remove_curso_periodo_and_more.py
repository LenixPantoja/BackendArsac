# Generated by Django 4.2.6 on 2024-04-17 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppAsistencia', '0009_alter_horario_dia_semana'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='materia',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='periodo',
        ),
        migrations.AddField(
            model_name='materia',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.periodo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='horario',
            name='dia_semana',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='CursoMateria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.curso')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.materia')),
            ],
        ),
    ]
