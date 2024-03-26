from django.db import models
from AppUsuarios.models import Docente, Estudiante

# Create your models here.


class Horario(models.Model):
    tipoHorario = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return str(f"{self.tipoHorario} - {self.hora_inicio} - {self.hora_fin}")


class Materia(models.Model):
    nombre_materia = models.CharField(max_length=100)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"

    def __str__(self):
        return str(self.nombre_materia)


class Periodo(models.Model):
    nombre_periodo = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self):
        return str(self.nombre_periodo)


class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    curso_created_at = models.DateTimeField(auto_now_add=True)
    curso_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return str(self.nombre_curso + " | " + self.materia.nombre_materia)

class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    matricula_created_at = models.DateTimeField(auto_now_add=True)
    matricula_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MatriculaEstudiante"
        verbose_name_plural = "MatriculasEstudiante"

    def __str__(self):
        return str(self.estudiante.user.first_name +" "+self.estudiante.user.last_name + " | " + self.curso.materia.nombre_materia)


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
        return str(self.tipo_asistencia)


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


