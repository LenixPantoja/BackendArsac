from django.db import models
from AppUsuarios.models import Docente, Estudiante

# Create your models here.
import os
from django.db import models

class Horario(models.Model):
    dia_semana = models.CharField(max_length = 100)
    tipoHorario = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return str(f"{self.dia_semana} - {self.tipoHorario} - {self.hora_inicio} - {self.hora_fin}")

class Periodo(models.Model):
    nombre_periodo = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self):
        return str(self.nombre_periodo)

class Materia(models.Model):
    nombre_materia = models.CharField(max_length=100)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"

    def __str__(self):
        return str(self.nombre_materia)


class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    curso_created_at = models.DateTimeField(auto_now_add=True)
    curso_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return str(self.nombre_curso)
class CursoMateria(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Curso Materia"
        verbose_name_plural = "Cursos Materias"

    def __str__(self):
        return str(str(self.curso.id) + '-' + self.curso.nombre_curso + '-' + str(self.materia.id) + '-' + self.materia.nombre_materia)

    
class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso_Materia = models.ForeignKey(CursoMateria, on_delete=models.CASCADE)
    matricula_created_at = models.DateTimeField(auto_now_add=True)
    matricula_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MatriculaEstudiante"
        verbose_name_plural = "MatriculasEstudiante"

    def __str__(self):
        return str(self.estudiante.user.first_name +" "+self.estudiante.user.last_name + " | " + self.curso_Materia.materia.nombre_materia)

""" 
class AsistenciaEstudiante(models.Model):
    tipo_asistencia = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, default="Sin registro")
    hora_llegada = models.DateTimeField()
    soporte = models.ImageField(
        upload_to="imageSoportes/", null=True, default="Sin registro"
    )
    matricula_estudiante = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    asistenciaEst_created_at = models.DateTimeField(auto_now_add=True)
    asistenciaEst_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AsistenciaEstudiante"
        verbose_name_plural = "AsistenciaEstudiantes"

    def __str__(self):
        return str(self.tipo_asistencia + " | "+ self.matricula_estudiante.curso_Materia.curso.nombre_curso + " | "+ self.matricula_estudiante.estudiante.user.first_name + " "+ self.matricula_estudiante.estudiante.user.last_name)
 """
def soporte_file_path(instance, filename):
    # Retorna la ruta del archivo para la imagen de soporte
    return os.path.join('imageSoportes', filename)

class AsistenciaEstudiante(models.Model):
    tipo_asistencia = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, default="Sin registro")
    hora_llegada = models.DateTimeField()
    soporte = models.ImageField(upload_to=soporte_file_path, null=True)  # Campo para almacenar la imagen
    matricula_estudiante = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    asistenciaEst_created_at = models.DateTimeField(auto_now_add=True)
    asistenciaEst_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AsistenciaEstudiante"
        verbose_name_plural = "AsistenciaEstudiantes"
class ObservacionesEstudiante(models.Model):
    asistenciaEst = models.ForeignKey(AsistenciaEstudiante, on_delete=models.CASCADE)
    observacionEst = models.TextField()
    observacion_created_at = models.DateTimeField(auto_now_add=True)
    observacion_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ObservacionEstudiante"
        verbose_name_plural = "ObservacionesEstudiantes"

    def __str__(self):
        return str(self.observacionEst)


