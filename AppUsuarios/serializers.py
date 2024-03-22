from rest_framework import serializers
from .models import Docente, Profesion, Estudiante, Participante
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'full_name']

""" Clase serializable de Profesion """
class ProfesionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profesion
        fields = '__all__'

""" Clase serializable de Docente """
class DocenteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'   

""" Clase serializable de Estudiante"""
class EstudianteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'   

""" Clase serializable de Participante"""
class ParticipanteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'   

""" Clase serializable de usuarios """
class UsuariosSerializers(serializers.ModelSerializer):
    docente = DocenteSerializers()
    class Meta:
        model = User
        fields = '__all__'

