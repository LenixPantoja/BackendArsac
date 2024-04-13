from urllib import request
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings

from dateutil.parser import isoparse

from AppAsistencia.models import *
from AppAsistencia.serializers import *

# Create your views here.


class AppAsist_API_CrearHorario(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            horario = Horario(
                tipoHorario=request.data.get("tipoHorario"),
                hora_inicio=request.data.get("hora_inicio"),
                hora_fin=request.data.get("hora_fin"),
            )
            horario.save()

            return Response({"msg": "Se ha creado el horario"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # Obtener todos los horarios y serializarlos
        horarios = Horario.objects.all()
        serializer = HorarioSerializer(horarios, many=True)
        return Response(serializer.data)


class AppAsist_Api_CrearMateria(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = MateriaSerializer(data=request.data)
            if serializer.is_valid():
                dataMateria = request.data
                docente = Docente.objects.get(id=dataMateria["docente"])
                horario = Horario.objects.get(id=dataMateria["horario"])

                materia = Materia(
                    nombre_materia=dataMateria["nombre_materia"],
                    docente=docente,
                    horario=horario,
                )
                materia.save()

                return Response({"msg": "Se ha creado la materia"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # Obtener todos los horarios y serializarlos
        materias = Materia.objects.all()
        serializer = MateriaSerializer(materias, many=True)
        return Response(serializer.data)


class AppAsist_API_CrearPeriodoAcadem(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = PeriodoSerializer(data=request.data)
            if serializer.is_valid():
                dataPeriodo = request.data

                periodo = Periodo(nombre_periodo=dataPeriodo["nombre_periodo"])
                periodo.save()

                return Response({"msg": "Se ha creado la el periodo"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # Obtener todos los horarios y serializarlos
        periodos = Periodo.objects.all()
        serializer = PeriodoSerializer(periodos, many=True)
        return Response(serializer.data)


class AppAsist_API_Curso(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = CursoSerializer(data=request.data)
            if serializer.is_valid():
                dataCurso = request.data
                materia = get_object_or_404(Materia, id=dataCurso["materia"])
                periodo = get_object_or_404(Periodo, id=dataCurso["periodo"])

                curso = Curso(
                    nombre_curso=dataCurso["nombre_curso"],
                    materia=materia,
                    periodo=periodo,
                )
                curso.save()

                return Response({"msg": "Se ha creado la el curso"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Obtiene la lista de cursos dado el docente
    def get(self, request, format=None):
        pUserDocente = request.query_params.get("pDocente", None)
        
        if pUserDocente is not None:
            cursos = Curso.objects.all()
            serializer = CursoSerializer(cursos, many=True)
            
            curso_data = []
            cursos_procesados = set()  # Usar un conjunto para evitar duplicados
            nombre_docente = ""
            for miCurso in serializer.data:
                curso_info = {f"{key}": value for key, value in miCurso.items()}
                
                # Verificar si las claves necesarias están presentes en curso_info
                if 'nombre_curso' not in curso_info or 'materia' not in curso_info or 'periodo' not in curso_info:
                    continue  # Omitir este curso si falta alguna clave requerida
                
                id_materia = curso_info['materia']
                id_perido = curso_info['periodo']
                materia = Materia.objects.filter(id=id_materia)
                periodo = Periodo.objects.filter(id=id_perido)
                
                for miMateria in materia:
                    pass  # No necesitas hacer nada aquí
                
                for miPeriodo in periodo:
                    pass  # Tampoco necesitas hacer nada aquí
                
                hora_inicio = miMateria.horario.hora_inicio
                hora_inicio_format = hora_inicio.strftime("%I:%M:%S %p")
                hora_fin = miMateria.horario.hora_fin
                hora_fin_format = hora_fin.strftime("%I:%M:%S %p")
                user_docente = miMateria.docente.user.username
                nombre_docente = user_docente
                # Verificar si el docente coincide y si el curso ya se ha procesado
                curso_key = (curso_info['nombre_curso'], curso_info.get('Docente', ''))  # Utiliza get para manejar la falta de la clave 'Docente'
                if user_docente == pUserDocente and curso_key not in cursos_procesados:
                    cursos_procesados.add(curso_key)
                    curso_data.append({
                        'id': curso_info['id'],
                        'nombre_curso': curso_info['nombre_curso'],
                        'materia': miMateria.nombre_materia,
                        'Hora_Inicio_Clase': hora_inicio_format,
                        'Hora_Fin_Clase': hora_fin_format,
                        'tipo_horario': miMateria.horario.tipoHorario,
                        'periodo': miPeriodo.nombre_periodo,
                        'Docente': nombre_docente  # Utiliza get para manejar la falta de la clave 'Docente'
                    })
            
            return Response(curso_data)
        else:
            return Response(
                {"error": "El parámetro pDocente es necesario."},
                status=status.HTTP_400_BAD_REQUEST,
            )

class AppAsist_API_AsistenciaEst(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = AsistenciaEstudianteSerializer(data=request.data)
            if serializer.is_valid():
                
                
                    dataAsisEstudiante = request.data
                    
                    matricula = Matricula.objects.get(id=dataAsisEstudiante["matricula_estudiante"])

                    asistenciaEstudiante = AsistenciaEstudiante(
                        tipo_asistencia=dataAsisEstudiante["tipo_asistencia"],
                        descripcion=dataAsisEstudiante["descripcion"],
                        hora_llegada=dataAsisEstudiante["hora_llegada"],
                        soporte=dataAsisEstudiante["soporte"],
                        matricula_estudiante = matricula
                    )
                    asistenciaEstudiante.save()
                    return Response(
                        {
                            "msg": "Se ha creado la asistencia",
                            "NombreEstudiante": matricula.estudiante.user.first_name + " " + matricula.estudiante.user.last_name
                        }
                    )
            else:
                return Response({"Error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        pIdEstudiante = request.query_params.get("pIdEstudiante")

        if(pIdEstudiante is None):
            return Response({"Error": "El parametro pIdEstudiante es necesario"})

        if pIdEstudiante:
            asistencia = AsistenciaEstudiante.objects.all()
            lista_asistencia = []

            for dataAsistencia in asistencia:
                id_estudiante = dataAsistencia.matricula_estudiante.estudiante.id
                soporte_url = None
                if dataAsistencia.soporte:
                    # Verificar si el campo soporte es un FileField o ImageField
                    if hasattr(dataAsistencia.soporte, 'url'):
                        soporte_url = request.build_absolute_uri(dataAsistencia.soporte.url)
                    else:
                        # Si no es un campo de tipo FileField o ImageField, asumimos que es la ruta de la imagen
                        soporte_url = dataAsistencia.soporte
                if id_estudiante == int(pIdEstudiante):
                    lista_asistencia.append({
                        'id': dataAsistencia.id,
                        'Tipo_asistencia': dataAsistencia.tipo_asistencia,
                        'Descripcion_asistencia': dataAsistencia.descripcion,
                        'Hora_llegada' : dataAsistencia.hora_llegada,
                        'Soporte_imagen': soporte_url,
                        'Estudiante': dataAsistencia.matricula_estudiante.estudiante.user.first_name + ' ' + dataAsistencia.matricula_estudiante.estudiante.user.last_name,
                        'Curso': dataAsistencia.matricula_estudiante.curso.nombre_curso,
                        'Materia': dataAsistencia.matricula_estudiante.curso.materia.nombre_materia
                    })
            return Response(lista_asistencia)
        else:
            asistencia = AsistenciaEstudiante.objects.all()
            lista_asistencia = []

            for dataAsistencia in asistencia:
                soporte_url = None
                if dataAsistencia.soporte:
                    # Verificar si el campo soporte es un FileField o ImageField
                    if hasattr(dataAsistencia.soporte, 'url'):
                        soporte_url = request.build_absolute_uri(dataAsistencia.soporte.url)
                    else:
                        # Si no es un campo de tipo FileField o ImageField, asumimos que es la ruta de la imagen
                        soporte_url = dataAsistencia.soporte
                
                lista_asistencia.append({
                    'id': dataAsistencia.id,
                    'Tipo_asistencia': dataAsistencia.tipo_asistencia,
                    'Descripcion_asistencia': dataAsistencia.descripcion,
                    'Hora_llegada' : dataAsistencia.hora_llegada,
                    'Soporte_imagen': soporte_url,
                    'Estudiante': dataAsistencia.matricula_estudiante.estudiante.user.first_name + ' ' + dataAsistencia.matricula_estudiante.estudiante.user.last_name,
                    'Curso': dataAsistencia.matricula_estudiante.curso.nombre_curso,
                    'Materia': dataAsistencia.matricula_estudiante.curso.materia.nombre_materia
                })
            return Response(lista_asistencia)
            
class AppAsist_API_ObservacionesEstudiante(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        try:
            serializer = ObservacionesEstSerializer(data=request.data)
            if serializer.is_valid():
                data_observaciones = request.data
                # Obtener la instancia de AsistenciaEstudiante utilizando el ID proporcionado
                asistencia_estudiante_id = data_observaciones.get("asistenciaEst")
                # Guardamos el ID de la asistencia
                id_asistencia_estudiante = AsistenciaEstudiante.objects.get(pk=asistencia_estudiante_id)
                nombre_estudiante = id_asistencia_estudiante.matricula_estudiante.estudiante.user.first_name + " " + id_asistencia_estudiante.matricula_estudiante.estudiante.user.last_name
                # Creamos un objeto de tipo ObservacionEstudiante
                obervacion_estudiante = ObservacionesEstudiante(
                    asistenciaEst = id_asistencia_estudiante,
                    observacionEst = data_observaciones["observacionEst"]
                )
                obervacion_estudiante.save()
                return Response(
                        {
                            "msg": f"Se creo la observación del estudiante: {nombre_estudiante}"
                        }
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, format=None):        
        pIdEstudiante = request.query_params.get("pIdEstudiante")
        pIdMateria =  request.query_params.get("pIdMateria")
        pIdCurso = request.query_params.get("pIdCurso")
        
        if pIdEstudiante and pIdMateria and pIdCurso:
            observacionesEstudiante = ObservacionesEstudiante.objects.all()
            lista_observaciones = []

            for observacion in observacionesEstudiante:
                id_estudiante = observacion.asistenciaEst.matricula_estudiante.estudiante.id
                id_materia = observacion.asistenciaEst.matricula_estudiante.curso.materia.id
                id_curso = observacion.asistenciaEst.matricula_estudiante.curso.id

                if id_estudiante == int(pIdEstudiante) and id_materia == int(pIdMateria) and id_curso == int(pIdCurso): 
                    lista_observaciones.append({
                        'id': observacion.id,
                        'id_asistencia' : observacion.asistenciaEst.id,
                        'Descripcion': observacion.observacionEst,
                        'Curso': observacion.asistenciaEst.matricula_estudiante.curso.nombre_curso,
                        'Periodo': observacion.asistenciaEst.matricula_estudiante.curso.periodo.nombre_periodo,
                        'Estudiante': observacion.asistenciaEst.matricula_estudiante.estudiante.user.first_name + " "+ observacion.asistenciaEst.matricula_estudiante.estudiante.user.last_name,
                        'Materia': observacion.asistenciaEst.matricula_estudiante.curso.materia.nombre_materia,
                        'Docente': observacion.asistenciaEst.matricula_estudiante.curso.materia.docente.user.first_name + " " + observacion.asistenciaEst.matricula_estudiante.curso.materia.docente.user.last_name,
                    })
            return Response(lista_observaciones)
        else:
            observacionesEstudiante = ObservacionesEstudiante.objects.all()
            lista_observaciones = []
            for observacion in observacionesEstudiante:                 
                lista_observaciones.append({
                    'id': observacion.id,
                    'id_asistencia' : observacion.asistenciaEst.id,
                    'Descripcion': observacion.observacionEst,
                    'Curso': observacion.asistenciaEst.matricula_estudiante.curso.nombre_curso,
                    'Periodo': observacion.asistenciaEst.matricula_estudiante.curso.periodo.nombre_periodo,
                    'Estudiante': observacion.asistenciaEst.matricula_estudiante.estudiante.user.first_name + " "+ observacion.asistenciaEst.matricula_estudiante.estudiante.user.last_name,
                    'Materia': observacion.asistenciaEst.matricula_estudiante.curso.materia.nombre_materia,
                    'Docente': observacion.asistenciaEst.matricula_estudiante.curso.materia.docente.user.first_name + " " + observacion.asistenciaEst.matricula_estudiante.curso.materia.docente.user.last_name,
                })
            return Response(lista_observaciones)

    def delete(self, request, pk, format=None):
        try:
            observacion_estudiante = ObservacionesEstudiante.objects.get(pk=pk)
            observacion_estudiante.delete()
            return Response({"msg": "Observación eliminada correctamente"})
        except ObservacionesEstudiante.DoesNotExist:
            return Response({"error": "La observación no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            observacion_estudiante = ObservacionesEstudiante.objects.get(pk=pk)
            serializer = ObservacionesEstSerializer(observacion_estudiante, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObservacionesEstudiante.DoesNotExist:
            return Response({"error": "La observación no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class AppAsist_API_HorarioDocente(APIView):
    def get(self, request, format=None):
        try:
            materia = Materia.objects.all()
            serializer = MateriaSerializer(materia, many = True)
            horarioDocente = []
            
            pUser = request.query_params.get("pUser", None)
                # Parametro de consulta
            if pUser is None:
                return Response(
                    {"error": "El parámetro pUser es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            
            for dataMateria in serializer.data:
                pass
                miDocente = Docente.objects.get(id = dataMateria["docente"])
                miHorario =  Horario.objects.get(id = dataMateria["horario"])
                
                if pUser == str(miDocente.user.username):
                    horarioDocente.append({
                    "Docente": miDocente.user.first_name + " " + miDocente.user.last_name,
                    "Materia": dataMateria["nombre_materia"],
                    "Hora_inicio": miHorario.hora_inicio,
                    "Hora_fin": miHorario.hora_fin
                    })
                    print(horarioDocente)
            return Response(horarioDocente)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppAsist_API_Materias_Docente(APIView):
    def get(self, request, format=None):
        try:
            materia = Materia.objects.all()
            serializer = MateriaSerializer(materia, many = True)
            horarioDocente = []
            
            pUser = request.query_params.get("pUser", None)
                # Parametro de consulta
            if pUser is None:
                return Response(
                    {"error": "El parámetro pUser es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            
            for dataMateria in serializer.data:
                pass
                miDocente = Docente.objects.get(id = dataMateria["docente"])
                miHorario =  Horario.objects.get(id = dataMateria["horario"])
                
                if pUser == str(miDocente.user.username):
                    horarioDocente.append({
                    "id" : dataMateria["id"],
                    "Materia": dataMateria["nombre_materia"]
                    })
                    print(horarioDocente)
            return Response(horarioDocente)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
