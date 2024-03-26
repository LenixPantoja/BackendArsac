# Generated by Django 4.2.6 on 2024-03-26 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAsistencia', '0005_matricula_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matricula',
            options={'verbose_name': 'MatriculaEstudiante', 'verbose_name_plural': 'MatriculasEstudiante'},
        ),
        migrations.AddField(
            model_name='matricula',
            name='matricula_created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matricula',
            name='matricula_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
