from rest_framework import serializers
from AppAsistencia.models import Curso, Horario, Periodo, Materia, AsistenciaEstudiante, AsistenciaParticipante, ObservacionesEstudiante, ObservacionParticipantes


class CursoSerializer(serializers.Serializer):
     class Meta:
          model = Curso
          fields = ('__all__')

class HorarioSerializer(serializers.Serializer):
     class Meta:
          model = Horario
          fields = ('__all__')

class PeriodoSerializer(serializers.Serializer):
     class Meta:
          model = Periodo
          fields = ('__all__')

class MateriaSerializer(serializers.Serializer):
     class Meta:
          model = Materia
          fields = ('__all__')
     
class AsistenciaEstudianteSerializer(serializers.Serializer):
     class Meta:
          model =AsistenciaEstudiante
          fields = ('__all__')

class AsistenciaParticipanteSerializer(serializers.Serializer):
     class Meta:
          model = AsistenciaParticipante
          fields = ('__all__')

class ObservacionesEstSerializer(serializers.Serializer):
     class Meta:
          model = ObservacionesEstudiante
          fields = ('__all__')

class ObservacionesPartSerializer(serializers.Serializer):
     class Meta:
          model = ObservacionParticipantes
          fields = ('__all__')