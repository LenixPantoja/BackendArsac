from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profesion(models.Model):
    nombre_Profesion = models.CharField(max_length=255)
    profesion_created_at = models.DateTimeField(auto_now_add=True)
    profesion_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profesion"
        verbose_name_plural = "Profesiones"

    def __str__(self):
        return str(self.nombre_Profesion)


class Docente(models.Model):
    user = models.OneToOneField(
        User, verbose_name="UsuarioDocente", on_delete=models.CASCADE
    )
    docente_profesion = models.ForeignKey(
        Profesion, verbose_name="Profesion", on_delete=models.CASCADE
    )
    docente_tipo_Id = models.CharField(max_length=10)
    docente_estado = models.BooleanField()
    docente_numero_Id = models.CharField(max_length=50)
    docente_fecha_nacim = models.DateField()
    docente_created_at = models.DateTimeField(auto_now_add=True)
    docente_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)


class Estudiante(models.Model):
    user = models.OneToOneField(
        User, verbose_name="UsuarioEstudiante", on_delete=models.CASCADE
    )
    estudiante_fecha_matricula = models.DateField()
    estudiante_estado = models.BooleanField()
    estudiante_tipo_Id = models.CharField(max_length=10)
    estudiante_numero_Id = models.CharField(max_length=50)
    estudiante_fecha_nac = models.DateField()
    curso = models.CharField(max_length=50)
    estudiante_created_at = models.DateTimeField(auto_now_add=True)
    estudiante_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Esudiantes"

    def __str__(self):
        return str(self.user.first_name)


class Participante(models.Model):
    user = models.OneToOneField(
        User, verbose_name="UsuarioParticipante", on_delete=models.CASCADE
    )
    # participante_fecha_matricula = models.DateField()
    participante_estado = models.BooleanField()
    participante_tipo_Id = models.CharField(max_length=10)
    participante_numero_Id = models.CharField(max_length=50)
    curso = models.CharField(max_length=50)
    participante_created_at = models.DateTimeField(auto_now_add=True)
    participante_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)

    # 24 +1 estuco
