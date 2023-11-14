# Generated by Django 4.2.6 on 2023-10-17 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AppUsuarios', '0003_participante'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaEstudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_asistencia', models.CharField(max_length=100)),
                ('descripcion', models.TextField(default='Sin registro', null=True)),
                ('hora_llegada', models.DateTimeField()),
                ('soporte', models.ImageField(default='Sin registro', null=True, upload_to='imagenes/')),
                ('asistenciaEst_created_at', models.DateTimeField(auto_now_add=True)),
                ('asistenciaEst_updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AsistenciaParticipante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_asistencia', models.CharField(max_length=100)),
                ('descripcion', models.TextField(default='Sin registro', null=True)),
                ('hora_llegada', models.DateTimeField()),
                ('soporte', models.ImageField(default='Sin registro', null=True, upload_to='imagenes/')),
                ('asistenciaPart_created_at', models.DateTimeField(auto_now_add=True)),
                ('asistenciaPart_updated_at', models.DateTimeField(auto_now=True)),
                ('Participante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppUsuarios.participante')),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoHorario', models.CharField(max_length=100)),
                ('hora_inicio', models.DateTimeField()),
                ('hora_fin', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_periodo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Observaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField()),
                ('observacion_created_at', models.DateTimeField(auto_now_add=True)),
                ('observacion_updated_at', models.DateTimeField(auto_now=True)),
                ('asistenciaEst', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppAsistencia.asistenciaestudiante')),
                ('asistenciaPart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppAsistencia.asistenciaparticipante')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_materia', models.CharField(max_length=100)),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppUsuarios.docente')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.horario')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_curso', models.CharField(max_length=50)),
                ('curso_created_at', models.DateTimeField(auto_now_add=True)),
                ('curso_updated_at', models.DateTimeField(auto_now=True)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.materia')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.periodo')),
            ],
        ),
        migrations.AddField(
            model_name='asistenciaparticipante',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.curso'),
        ),
        migrations.AddField(
            model_name='asistenciaestudiante',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAsistencia.curso'),
        ),
        migrations.AddField(
            model_name='asistenciaestudiante',
            name='estudiante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppUsuarios.estudiante'),
        ),
    ]
