# Generated by Django 4.2.6 on 2023-10-19 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppAsistencia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservacionesEstudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacionEst', models.TextField()),
                ('observacion_created_at', models.DateTimeField(auto_now_add=True)),
                ('observacion_updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ObservacionEstudiante',
                'verbose_name_plural': 'ObservacionesEstudiantes',
            },
        ),
        migrations.CreateModel(
            name='ObservacionParticipantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacionPart', models.TextField()),
                ('observacion_created_at', models.DateTimeField(auto_now_add=True)),
                ('observacion_updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ObservacionEstudiante',
                'verbose_name_plural': 'ObservacionesEstudiantes',
            },
        ),
        migrations.AlterModelOptions(
            name='asistenciaestudiante',
            options={'verbose_name': 'AsistenciaEstudiante', 'verbose_name_plural': 'AsistenciaEstudiantes'},
        ),
        migrations.AlterModelOptions(
            name='asistenciaparticipante',
            options={'verbose_name': 'AsistenciaParticipante', 'verbose_name_plural': 'AsistenciaParticipantes'},
        ),
        migrations.AlterModelOptions(
            name='curso',
            options={'verbose_name': 'Curso', 'verbose_name_plural': 'Cursos'},
        ),
        migrations.AlterModelOptions(
            name='horario',
            options={'verbose_name': 'Horario', 'verbose_name_plural': 'Horarios'},
        ),
        migrations.AlterModelOptions(
            name='materia',
            options={'verbose_name': 'Materia', 'verbose_name_plural': 'Materias'},
        ),
        migrations.AlterModelOptions(
            name='periodo',
            options={'verbose_name': 'Periodo', 'verbose_name_plural': 'Periodos'},
        ),
        migrations.DeleteModel(
            name='Observaciones',
        ),
        migrations.AddField(
            model_name='observacionparticipantes',
            name='asistenciaPart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppAsistencia.asistenciaparticipante'),
        ),
        migrations.AddField(
            model_name='observacionesestudiante',
            name='asistenciaEst',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppAsistencia.asistenciaestudiante'),
        ),
    ]
