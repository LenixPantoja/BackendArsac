from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets

# Importamos los serializadores de App Usuarios
from AppUsuarios.serializers import *

# Importamos los views de App Usuarios
from AppUsuarios.models import *
#Importamos los views de App Asistencia
from AppAsistencia.models import *
# Librerias para JWT
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


class AppUser_Login_ApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:
            # Obtenemos el usuario autenticado
            user = request.user

            # Serializamos el usuario para obtener el nombre de usuario y el nombre completo
            serializer = UserSerializer(user)

            # Devolvemos la información del usuario como respuesta
            return Response(serializer.data)
        else:
            return Response({"detail": "El usuario no está autenticado"}, status=401)


""" 
    Funcion que permite saber si el JWT fue aceptado
"""


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_post(request):
    return JsonResponse({"msg": "todo funcionando"})


"""
    @Class AppUser_ApiView
    y el método POST que permitirá guardar registros en la base de datos.
    metodo GET que permitirá obtener la lista de docentes de la base de datos. 
"""
class AppUser_Docente_ApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # Serializar los datos del usuario
        user_data = request.data["docente"]
        user_serializer = UsuariosSerializers(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            # Asignar el usuario al docente
            docente_data = {
                "user": user.id,
                "docente_profesion": request.data["docente_profesion"],
                "docente_tipo_Id": request.data["docente_tipo_Id"],
                "docente_estado": request.data["docente_estado"],
                "docente_numero_Id": request.data["docente_numero_Id"],
                "docente_fecha_nacim": request.data["docente_fecha_nacim"],
            }
            docente_serializer = DocenteSerializers(data=docente_data)
            if docente_serializer.is_valid():
                docente_serializer.save()
                return Response(docente_serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                docente_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Metodo get que permite 
    def get(self, request, format=None):
        try:
             # Obtener la lista de todos los docentes
            docentes = Docente.objects.all()
            serializer = DocenteSerializers(docentes, many=True)
            
            # Crear una lista de diccionarios con claves y valores
            docentes_data = []
            for data_dict in serializer.data:
                docente_info = {f"{key}": value for key, value in data_dict.items()}
                user = User.objects.get(id=docente_info['user'])
                profesion = Profesion.objects.get(id=docente_info['docente_profesion'])
                docentes_data.append({
                    'id': docente_info['id'],
                    'UsernameLogin': user.username,
                    'Nombre_docente': user.first_name + " " + user.last_name,
                    'Cedula_docente': docente_info['docente_numero_Id'],
                    'Profesion_docente': profesion.nombre_Profesion
                })
            return Response(docentes_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppUser_Estudiante_ApiView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, estudiante_numero_Id=None, format=None):
        try:
            if estudiante_numero_Id:
                estudiante = Estudiante.objects.get(estudiante_numero_Id=estudiante_numero_Id)
                serializer = EstudianteSerializers(estudiante)
                estudiante_data = serializer.data
                user = User.objects.get(id=estudiante_data['user'])
                curso = Curso.objects.get(id=estudiante_data['curso'])
                response_data = {
                    'id': estudiante_data['id'],
                    'UsernameLogin': user.username,
                    'Nombre_estudiante': user.first_name + " " + user.last_name,
                    'Identificacion_estudiante': estudiante_data['estudiante_numero_Id'],
                    'Curso': curso.nombre_curso
                }
                return Response(response_data)
            else:
                estudiantes = Estudiante.objects.all()
                serializer = EstudianteSerializers(estudiantes, many=True)
                estudiantes_data = []
                for data_dict in serializer.data:
                    estudiante_info = {f"{key}": value for key, value in data_dict.items()}
                    user = User.objects.get(id=estudiante_info['user'])
                    curso = Curso.objects.get(id=estudiante_info['curso'])
                    estudiantes_data.append({
                        'id': estudiante_info['id'],
                        'UsernameLogin': user.username,
                        'Nombre_estudiante': user.first_name + " " + user.last_name,
                        'Identificacion_estudiante': estudiante_info['estudiante_numero_Id'],
                        'Curso': curso.nombre_curso
                    })
                return Response(estudiantes_data)    
        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AppUser_Participante_ApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # Obtiene la lista de todos los estudiantes
    def get(self, request, format=None):

        try:
            participante = Participante.objects.all()
            serializer = ParticipanteSerializers(participante, many=True)
            participante_data = []
            for data_dict in serializer.data:
                participante_info = {f"{key}": value for key, value in data_dict.items()}
                user = User.objects.get(id = participante_info['user'])
                curso = Curso.objects.get(id = participante_info['curso'])
                participante_data.append({
                    'id': participante_info['id'],
                    'Username_Login': user.username,
                    'Nombre_estudiante': user.first_name + " " + user.last_name,
                    'Identificacion': participante_info['participante_numero_Id'],
                    'Curso': curso.nombre_curso
                })
            return Response(participante_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
          