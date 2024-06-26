import base64
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
from datetime import datetime


from dateutil.parser import isoparse

from AppAsistencia.models import *
from AppAsistencia.serializers import *

# Create your views here.


class AppAsist_API_CrearHorario(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            horario = Horario(
                dia_semana=request.data.get("dia_semana"),
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
            miCursoMateria = CursoMateria.objects.all()
            data_curso = []
            for dataCursoMateria in miCursoMateria:
                hora_inicio = dataCursoMateria.materia.horario.hora_inicio
                hora_inicio_format = hora_inicio.strftime("%I:%M:%S %p")
                hora_fin = dataCursoMateria.materia.horario.hora_fin
                hora_fin_format = hora_fin.strftime("%I:%M:%S %p")

                usernameDocente = dataCursoMateria.materia.docente.user.username
                if usernameDocente == pUserDocente:
                    data_curso.append({
                        'id': dataCursoMateria.curso.id,
                        'nombre_curso': dataCursoMateria.curso.nombre_curso,
                        'materia': dataCursoMateria.materia.nombre_materia,
                        'Hora_Inicio_Clase': hora_inicio_format,
                        'Hora_Fin_Clase': hora_fin_format,
                        'Dia': dataCursoMateria.materia.horario.dia_semana,
                        'tipo_horario': dataCursoMateria.materia.horario.tipoHorario,
                        'periodo': dataCursoMateria.materia.periodo.nombre_periodo,
                        'Docente': dataCursoMateria.materia.docente.user.username
                    })
            
            return Response(data_curso)
class AppAsist_API_AsistenciaEst(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        try:
            matricula = Matricula.objects.get(id=request.data["matricula_estudiante"])


            tipo_asistencia = request.data.get("tipo_asistencia")
            descripcion = request.data.get("descripcion")
            hora_llegada = request.data.get("hora_llegada")
            soporte_base64 = request.data.get("soporte")
            matricula_estudiante = matricula


            asistencia_estudiante = AsistenciaEstudiante(
                tipo_asistencia=tipo_asistencia,
                descripcion=descripcion,
                hora_llegada=hora_llegada,
                matricula_estudiante = matricula
            )
            if soporte_base64:
                filename = f"soporte_{asistencia_estudiante.id}.jpg"
                file_path = os.path.join(settings.MEDIA_ROOT, 'imageSoportes', filename)
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(soporte_base64))
                asistencia_estudiante.soporte = file_path

            # Aquí puedes realizar otras operaciones o validaciones necesarias

            asistencia_estudiante.save()
            return Response(
                        {
                            "msg": "Se ha creado la asistencia",
                            "NombreEstudiante": matricula.estudiante.user.first_name + " " + matricula.estudiante.user.last_name
                        },status=status.HTTP_201_CREATED
                    )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        pIdEstudiante = request.query_params.get("pIdEstudiante")
        pIdMateria =  request.query_params.get("pIdMateria")
        pIdCurso = request.query_params.get("pIdCurso")
        

        if pIdEstudiante:
            asistencia = AsistenciaEstudiante.objects.all()
            lista_asistencia = []
            asistencia = asistencia.order_by('-id')

            for dataAsistencia in asistencia:
                id_estudiante = dataAsistencia.matricula_estudiante.estudiante.id
                id_materia = dataAsistencia.matricula_estudiante.curso_Materia.materia.id
                id_curso =  dataAsistencia.matricula_estudiante.curso_Materia.curso.id
                soporte_url = None
                if dataAsistencia.soporte:
                    # Verificar si el campo soporte es un FileField o ImageField
                    if hasattr(dataAsistencia.soporte, 'url'):
                        soporte_url = request.build_absolute_uri(dataAsistencia.soporte.url)
                    else:
                        # Si no es un campo de tipo FileField o ImageField, asumimos que es la ruta de la imagen
                        soporte_url = dataAsistencia.soporte
    
                if (id_estudiante == int(pIdEstudiante) and
                    id_materia == int(pIdMateria) and
                    id_curso == int(pIdCurso)):
                    lista_asistencia.append({
                        "id": dataAsistencia.id,
                        "Tipo_asistencia": dataAsistencia.tipo_asistencia,
                        "Descripcion_asistencia": dataAsistencia.descripcion,
                        "Hora_llegada": dataAsistencia.hora_llegada,
                        "Soporte": soporte_url,
                        "id_estudiante": dataAsistencia.matricula_estudiante.estudiante.id,
                        "Estudiante": dataAsistencia.matricula_estudiante.estudiante.user.first_name + ' ' + dataAsistencia.matricula_estudiante.estudiante.user.last_name,
                        "id_curso":dataAsistencia.matricula_estudiante.curso_Materia.curso.id,
                        "Curso": dataAsistencia.matricula_estudiante.curso_Materia.curso.nombre_curso,
                        "id_materia": dataAsistencia.matricula_estudiante.curso_Materia.materia.id,
                        "Materia": dataAsistencia.matricula_estudiante.curso_Materia.materia.nombre_materia
                    })
                    print(lista_asistencia)
            return Response(lista_asistencia)
        else:
        

            pUser = request.query_params.get("pUser")

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
                usuarioDocente =  dataAsistencia.matricula_estudiante.curso_Materia.materia.docente.user.username
                if usuarioDocente == pUser:
                    lista_asistencia.append({
                        'id': dataAsistencia.id,
                        'Tipo_asistencia': dataAsistencia.tipo_asistencia,
                        'Descripcion_asistencia': dataAsistencia.descripcion,
                        'Hora_llegada' : dataAsistencia.hora_llegada,
                        'Soporte': soporte_url,
                        'id_estudiante': dataAsistencia.matricula_estudiante.estudiante.id,
                        'Estudiante': dataAsistencia.matricula_estudiante.estudiante.user.first_name + ' ' + dataAsistencia.matricula_estudiante.estudiante.user.last_name,
                        'id_curso':dataAsistencia.matricula_estudiante.curso_Materia.curso.id,
                        'Curso': dataAsistencia.matricula_estudiante.curso_Materia.curso.nombre_curso,
                        'id_materia': dataAsistencia.matricula_estudiante.curso_Materia.materia.id,
                        'Materia': dataAsistencia.matricula_estudiante.curso_Materia.materia.nombre_materia
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
                id_materia = observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.id
                id_curso = observacion.asistenciaEst.matricula_estudiante.curso_Materia.curso.id

                # VALIDACIONES
                if id_estudiante == int(pIdEstudiante) and id_materia == int(pIdMateria) and id_curso == int(pIdCurso): 
                    lista_observaciones.append({
                        'id': observacion.id,
                        'id_asistencia' : observacion.asistenciaEst.id,
                        'Descripcion': observacion.observacionEst,
                        'Curso': observacion.asistenciaEst.matricula_estudiante.curso_Materia.curso.nombre_curso,
                        'Periodo': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.periodo.nombre_periodo,
                        'Estudiante': observacion.asistenciaEst.matricula_estudiante.estudiante.user.first_name + " "+ observacion.asistenciaEst.matricula_estudiante.estudiante.user.last_name,
                        'Materia': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.nombre_materia,
                        'Docente': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.docente.user.first_name + " " + observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.docente.user.last_name,
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
                        'Curso': observacion.asistenciaEst.matricula_estudiante.curso_Materia.curso.nombre_curso,
                        'Periodo': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.periodo.nombre_periodo,
                        'Estudiante': observacion.asistenciaEst.matricula_estudiante.estudiante.user.first_name + " "+ observacion.asistenciaEst.matricula_estudiante.estudiante.user.last_name,
                        'Materia': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.nombre_materia,
                        'Docente': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.docente.user.first_name + " " + observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.docente.user.last_name,
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
            cursoMateria = CursoMateria.objects.all()
            serializer = MateriaSerializer(cursoMateria, many = True)
            horarioDocente = []
            
            pUser = request.query_params.get("pUser", None)
                # Parametro de consulta
            if pUser is None:
                return Response(
                    {"error": "El parámetro pUser es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            
            for dataCursoMateria in cursoMateria:
                pass
                miDocente = Docente.objects.get(id = dataCursoMateria.materia.docente.id)
                miHorario =  Horario.objects.get(id = dataCursoMateria.materia.horario.id)
                # Valida el usuario ingresado
                if pUser == str(miDocente.user.username):
                    horarioDocente.append({
                    "Docente": miDocente.user.first_name + " " + miDocente.user.last_name,
                    "Materia": dataCursoMateria.materia.nombre_materia,
                    "Curso": dataCursoMateria.curso.nombre_curso,
                    "Dia": miHorario.dia_semana,
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
                if pUser == str(miDocente.user.username):
                    horarioDocente.append({
                    "id" : dataMateria["id"],
                    "Materia": dataMateria["nombre_materia"]
                    })
                    print(horarioDocente)
            return Response(horarioDocente)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AppAsist_API_HorarioEstudiante(APIView):
    def get(self, request, format=None):
        try:
            matricula = Matricula.objects.all()
            horarioEstudiante = []
            pUser = request.query_params.get("pUser", None)
                # Parametro de consulta
            if pUser is None:
                return Response(
                    {"error": "El parámetro pUser es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            for dataMatricula in matricula:
                pass
                miDocente = Docente.objects.get(id = dataMatricula.curso_Materia.materia.docente.id)
                # Valida el usuario ingresado
                userEstudiante = dataMatricula.estudiante.user.username
                if userEstudiante == pUser:
                    horarioEstudiante.append({
                        "Docente": miDocente.user.first_name + " " + miDocente.user.last_name,
                        "Materia": dataMatricula.curso_Materia.materia.nombre_materia,
                        "Curso": dataMatricula.curso_Materia.curso.nombre_curso,
                        "Dia": dataMatricula.curso_Materia.materia.horario.dia_semana,
                        "Hora_inicio": dataMatricula.curso_Materia.materia.horario.hora_inicio,
                        "Hora_fin": dataMatricula.curso_Materia.materia.horario.hora_fin,
                        })                
            return Response(horarioEstudiante)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AppAsist_API_Materias_Estudiante(APIView):
    def get(self, request, format=None):
        try:
            matricula = Matricula.objects.all()
            horarioEstudiante = []
            
            pUser = request.query_params.get("pUser", None)
                # Parametro de consulta
            if pUser is None:
                return Response(
                    {"error": "El parámetro pUser es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            
            for dataMateria in matricula:
                pass
                userEstudiante = dataMateria.estudiante.user.username
                if pUser == userEstudiante:
                    horarioEstudiante.append({
                    "id" : dataMateria.id,
                    "Materia": dataMateria.curso_Materia.materia.nombre_materia
                    })
                    print(horarioEstudiante)
            return Response(horarioEstudiante)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AppAsist_ConsultarObs_Estudiante(APIView):
    def get(self, request, format=None):        
        pUser = request.query_params.get("pUser")
        pRango1 = request.query_params.get("pRango1")
        pRango2 = request.query_params.get("pRango2")
        pIdMateria =  request.query_params.get("pIdMateria")
        pIdCurso = request.query_params.get("pIdCurso")
        
        if pUser and pIdMateria and pIdCurso:
            observacionesEstudiante = ObservacionesEstudiante.objects.all()
            lista_observaciones = []

            for observacion in observacionesEstudiante:
                usurioEstudiante = observacion.asistenciaEst.matricula_estudiante.estudiante.user.username
                id_materia = observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.id
                id_curso = observacion.asistenciaEst.matricula_estudiante.curso_Materia.curso.id
                fecha_creacion = observacion.observacion_created_at
                fecha_formateada = fecha_creacion.strftime('%Y-%m-%d')
                # VALIDACIONES
                if (usurioEstudiante == pUser and 
                    id_materia == int(pIdMateria) and 
                    id_curso == int(pIdCurso) and 
                    fecha_formateada >= pRango1 and
                    fecha_formateada <= pRango2):
                    print(fecha_formateada)
                    lista_observaciones.append({
                        'id': observacion.id,
                        'id_asistencia' : observacion.asistenciaEst.id,
                        'Fecha_creacion_obs': fecha_formateada,
                        'Descripcion': observacion.observacionEst,
                        'Curso': observacion.asistenciaEst.matricula_estudiante.curso_Materia.curso.nombre_curso,
                        'Periodo': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.periodo.nombre_periodo,
                        'Estudiante': observacion.asistenciaEst.matricula_estudiante.estudiante.user.first_name + " "+ observacion.asistenciaEst.matricula_estudiante.estudiante.user.last_name,
                        'Materia': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.nombre_materia,
                        'Docente': observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.docente.user.first_name + " " + observacion.asistenciaEst.matricula_estudiante.curso_Materia.materia.docente.user.last_name,
                    })
            return Response(lista_observaciones)
        
class AppAsist_ConsultarAsist_Estudiante(APIView):
    
    def get(self, request, format=None):
        pUser = request.query_params.get("pUser")
        pRango1 = request.query_params.get("pRango1")
        pRango2 = request.query_params.get("pRango2")
        pIdMateria =  request.query_params.get("pIdMateria")
        pIdCurso = request.query_params.get("pIdCurso")
        

        if pUser:
            asistencia = AsistenciaEstudiante.objects.all()
            lista_asistencia = []
            asistencia = asistencia.order_by('-id')

            for dataAsistencia in asistencia:
                usuarioEstudiante = dataAsistencia.matricula_estudiante.estudiante.user.username
                id_materia = dataAsistencia.matricula_estudiante.curso_Materia.materia.id
                id_curso =  dataAsistencia.matricula_estudiante.curso_Materia.curso.id
                fecha_creacion = dataAsistencia.asistenciaEst_created_at
                fecha_formateada = fecha_creacion.strftime('%Y-%m-%d')

                soporte_url = None
                if dataAsistencia.soporte:
                    # Verificar si el campo soporte es un FileField o ImageField
                    if hasattr(dataAsistencia.soporte, 'url'):
                        soporte_url = request.build_absolute_uri(dataAsistencia.soporte.url)
                    else:
                        # Si no es un campo de tipo FileField o ImageField, asumimos que es la ruta de la imagen
                        soporte_url = dataAsistencia.soporte
    
                if (usuarioEstudiante == pUser and
                    id_materia == int(pIdMateria) and
                    id_curso == int(pIdCurso) and
                    fecha_formateada >= pRango1 and
                    fecha_formateada <= pRango2):
                    lista_asistencia.append({
                        "id": dataAsistencia.id,
                        "Tipo_asistencia": dataAsistencia.tipo_asistencia,
                        'Fecha_creacion_asist': fecha_formateada,
                        "Descripcion_asistencia": dataAsistencia.descripcion,
                        "Hora_llegada": dataAsistencia.hora_llegada,
                        "Soporte": soporte_url,
                        "id_estudiante": dataAsistencia.matricula_estudiante.estudiante.id,
                        "Estudiante": dataAsistencia.matricula_estudiante.estudiante.user.first_name + ' ' + dataAsistencia.matricula_estudiante.estudiante.user.last_name,
                        "id_curso":dataAsistencia.matricula_estudiante.curso_Materia.curso.id,
                        "Curso": dataAsistencia.matricula_estudiante.curso_Materia.curso.nombre_curso,
                        "id_materia": dataAsistencia.matricula_estudiante.curso_Materia.materia.id,
                        "Materia": dataAsistencia.matricula_estudiante.curso_Materia.materia.nombre_materia
                    })
                    print(lista_asistencia)
            return Response(lista_asistencia)
        
class AppAsist_API_Curso_Estudiante(APIView):
    
    def get(self, request, format=None):
        pUserEstudiante = request.query_params.get("pUser", None)
        
        if pUserEstudiante is not None:
            matricula = Matricula.objects.all()
            data_curso = []
            for dataCursoMateria in matricula:
                hora_inicio = dataCursoMateria.curso_Materia.materia.horario.hora_inicio
                hora_inicio_format = hora_inicio.strftime("%I:%M:%S %p")
                hora_fin = dataCursoMateria.curso_Materia.materia.horario.hora_fin
                hora_fin_format = hora_fin.strftime("%I:%M:%S %p")

                usernameEstudiante = dataCursoMateria.estudiante.user.username
                if usernameEstudiante == pUserEstudiante:
                    data_curso.append({
                        'id': dataCursoMateria.curso_Materia.curso.id,
                        'nombre_curso': dataCursoMateria.curso_Materia.curso.nombre_curso,
                        'materia': dataCursoMateria.curso_Materia.materia.nombre_materia,
                        'Hora_Inicio_Clase': hora_inicio_format,
                        'Hora_Fin_Clase': hora_fin_format,
                        'Dia': dataCursoMateria.curso_Materia.materia.horario.dia_semana,
                        'tipo_horario': dataCursoMateria.curso_Materia.materia.horario.tipoHorario,
                        'periodo': dataCursoMateria.curso_Materia.materia.periodo.nombre_periodo,
                        'Docente': dataCursoMateria.curso_Materia.materia.docente.user.username
                    })
            
            return Response(data_curso)

