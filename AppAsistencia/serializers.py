from rest_framework import serializers
from AppAsistencia.models import Curso, Horario, Periodo, Materia, Matricula, AsistenciaEstudiante, ObservacionesEstudiante


class CursoSerializer(serializers.ModelSerializer):
     class Meta:
          model = Curso
          fields = ('__all__')

class HorarioSerializer(serializers.ModelSerializer):
     class Meta:
          model = Horario
          fields = ('__all__')

class PeriodoSerializer(serializers.ModelSerializer):
     class Meta:
          model = Periodo
          fields = ('__all__')

class MateriaSerializer(serializers.ModelSerializer):
     class Meta:
          model = Materia
          fields = ('__all__')

class MatriculaSerializer(serializers.ModelSerializer):
     class Meta:
          model = Matricula
          fields = ('__all__')
     
class AsistenciaEstudianteSerializer(serializers.ModelSerializer):
     class Meta:
          model =AsistenciaEstudiante
          fields = ('__all__')

class ObservacionesEstSerializer(serializers.ModelSerializer):
     class Meta:
          model = ObservacionesEstudiante
          fields = ('__all__')

