from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
import datetime

# Importamos los serializadores de App Usuarios
from AppUsuarios.serializers import *
from AppAsistencia.serializers import *
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
            
            # Crear una lista de diccionarios con claves y valores.
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
                    'Profesion_docente': profesion.nombre_Profesion,
                    'Acceso': docente_info['docente_estado']
                })
            return Response(docentes_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppUser_Estudiante_ApiView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, estudiante_numero_Id=None, format=None):
        try:
            matricula = Matricula.objects.all()
            serializers = MatriculaSerializer(matricula, many=True)
            estudiantes_data = []
            for miMatricula in serializers.data:
                estudiante = Estudiante.objects.get(id = miMatricula['estudiante'])
                curso = Curso.objects.get(id = miMatricula['curso'])
                
                estudiantes_data.append({
                    'id':estudiante.id,
                    'Username_Login':estudiante.user.username,
                    'Nombre_Estudiante':estudiante.user.first_name + ' ' + estudiante.user.last_name,
                    'Identificacion_Estudiante':estudiante.estudiante_numero_Id,
                    'Acceso': estudiante.estudiante_estado,
                    'id_Curso_Estudiante':curso.id,
                    'Curso_Estudiante':curso.nombre_curso,
                    'Id_Materia_Estudiante':curso.materia.id,
                    'Materia_Estudiante':curso.materia.nombre_materia,
                    
                    })
            return Response(estudiantes_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppUser_EstudiantesCursoMateria(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):

        try:
            pMateria =  request.query_params.get("pMateria", None)
            pCurso = request.query_params.get("pCurso", None)

            if pMateria is None and  pCurso is None:
                return Response({'Error':"Los parámetros pMateria y pCurso son necesarios."})
            
            matricula = Matricula.objects.all()
            serializers = MatriculaSerializer(matricula, many=True)
            estudiantes_data = []
            for miMatricula in serializers.data:
                cursoMateria = CursoMateria.objects.get(pk = miMatricula['curso_Materia'])
                mi_estudiante = Estudiante.objects.get(pk = miMatricula['estudiante'])
                
                print(cursoMateria.curso.nombre_curso)
                miMateria = cursoMateria.materia.id
                miCurso =  cursoMateria.curso.id
                if miMateria == int(pMateria) and miCurso == int(pCurso):
                    estudiantes_data.append({
                        'id':miMatricula['id'],
                        'Username_Login': mi_estudiante.user.username,
                        'id_estudiante': mi_estudiante.id,
                        'Nombre_Estudiante': mi_estudiante.user.first_name + ' ' + mi_estudiante.user.last_name,
                        "Identificacion_Estudiante": mi_estudiante.estudiante_numero_Id,
                        "Acceso": mi_estudiante.estudiante_estado,
                        "id_Curso_Estudiante": cursoMateria.curso.id,
                        "Curso_Estudiante": cursoMateria.curso.nombre_curso,
                        "Id_Materia_Estudiante": cursoMateria.materia.id,
                        "Materia_Estudiante": cursoMateria.materia.nombre_materia,
                        })
                
            return Response(estudiantes_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class AppUser_InformacionDocente(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        pUser = request.query_params.get("pUser", None)
        dataMatricula = Matricula.objects.all()
        for miMatricula in dataMatricula:
            usuarioDocente = miMatricula.curso_Materia.materia.docente.user.username
            usuarioEstudiante = miMatricula.estudiante.user.username 
            if usuarioDocente == pUser:
                # Obtener la fecha de nacimiento del docente
                fecha_nac = miMatricula.curso_Materia.materia.docente.docente_fecha_nacim
                
                # Calcular la edad
                fecha_actual = datetime.now()
                edad = fecha_actual.year - fecha_nac.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nac.month, fecha_nac.day))
                
                response_data = [{
                    "Username": usuarioDocente,
                    "Perfil": "Docente | admin",
                    "Profesion": miMatricula.curso_Materia.materia.docente.docente_profesion.nombre_Profesion,
                    "Edad": edad,
                    "Identificacion": miMatricula.curso_Materia.materia.docente.docente_numero_Id
                }]
                return Response(response_data)
            
            elif usuarioEstudiante == pUser:
                # Obtener la fecha de nacimiento del docente
                fecha_nac = miMatricula.estudiante.estudiante_fecha_nac
                
                # Calcular la edad
                fecha_actual = datetime.now()
                edad = fecha_actual.year - fecha_nac.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nac.month, fecha_nac.day))
                
                response_data = [{
                    "Username": usuarioEstudiante,
                    "Perfil": "Estudiante",
                    "Edad": edad,
                    "Identificacion": miMatricula.estudiante.estudiante_numero_Id
                }]
                return Response(response_data)
        # Si no se encuentra ningún docente con el usuario proporcionado
        return Response({"error": "Usuario no encontrado"}, status=404)
