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


class AppAsist_API_CrearCurso(APIView):
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

    def get(self, request, format=None):
        # Obtener todos los horarios y serializarlos
        cursos = Curso.objects.all()
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)


class AppAsist_API_CrearAsistenciaEst(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = AsistenciaEstudianteSerializer(data=request.data)
            if serializer.is_valid():
                pNumeroDocumento = request.query_params.get("pNumeroDocumento", None)
                # Parametro de consulta
                if pNumeroDocumento is None:
                    return Response(
                        {"error": "El parámetro pNumeroDocumento es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Verifica si el estudiante exite en la base de datos.
                existing_estudiante = Estudiante.objects.filter(
                    estudiante_numero_Id=pNumeroDocumento
                ).first()
                # Obtiene el curso de estudiante encontrado.
                CursoEstudinte = existing_estudiante.curso
                # Veriica si el estudiante fue encontrado y si esta en el curso correcto.

                if existing_estudiante and CursoEstudinte == request.data.get("curso"):
                    dataAsisEstudiante = request.data
                    # Obtiene el nombre del estudiante quien marcó la asistencia.
                    nombreEstudiante = (
                        existing_estudiante.user.first_name
                        + " "
                        + existing_estudiante.user.last_name
                    )
                    estudiante = Estudiante.objects.get(
                        id=dataAsisEstudiante["estudiante"]
                    )
                    curso = Curso.objects.get(id=dataAsisEstudiante["curso"])

                    asistenciaEstudiante = AsistenciaEstudiante(
                        tipo_asistencia=dataAsisEstudiante["tipo_asistencia"],
                        descripcion=dataAsisEstudiante["descripcion"],
                        hora_llegada=dataAsisEstudiante["hora_llegada"],
                        soporte=dataAsisEstudiante["soporte"],
                        estudiante=estudiante,
                        curso=curso,
                    )
                    asistenciaEstudiante.save()
                    return Response(
                        {
                            "msg": "Se ha creado la asistencia",
                            "NombreEstudiante": nombreEstudiante,
                        }
                    )
                else:
                    return Response(
                        {
                            "msg": "No se encontró el estudiante o el estudiante no pertenece a al curso seleccionado."
                        }
                    )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # Obtener todas las asistencias y serializarlos
        asistenciaEst = AsistenciaEstudiante.objects.all()
        serializer = AsistenciaEstudianteSerializer(asistenciaEst, many=True)
        return Response(serializer.data)


class AppAsist_API_CrearAsistenciaPart(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = AsistenciaParticipanteSerializer(data=request.data)
            if serializer.is_valid():
                pNumeroDocumento = request.query_params.get("pNumeroDocumento", None)
                # Parametro de consulta
                if pNumeroDocumento is None:
                    return Response(
                        {"error": "El parámetro pNumeroDocumento es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Verifica si el estudiante exite en la base de datos.
                existing_participante = Participante.objects.filter(
                    estudiante_numero_Id=pNumeroDocumento
                ).first()
                # Obtiene el curso de estudiante encontrado.
                CursoParticipante = existing_participante.curso
                # Veriica si el estudiante fue encontrado y si esta en el curso correcto.

                if CursoParticipante and CursoParticipante == request.data.get("curso"):
                    dataParticipante = request.data
                    # Obtiene el nombre del estudiante quien marcó la asistencia.
                    nombreParticipante = (
                        existing_participante.user.first_name
                        + " "
                        + existing_participante.user.last_name
                    )
                    participante = Participante.objects.get(
                        id=dataParticipante["participante"]
                    )
                    curso = Curso.objects.get(id=dataParticipante["curso"])

                    asistenciaParticipante = AsistenciaEstudiante(
                        tipo_asistencia=dataParticipante["tipo_asistencia"],
                        descripcion=dataParticipante["descripcion"],
                        hora_llegada=dataParticipante["hora_llegada"],
                        soporte=dataParticipante["soporte"],
                        estudiante=participante,
                        curso=curso,
                    )
                    asistenciaParticipante.save()
                    return Response(
                        {
                            "msg": "Se ha creado la asistencia",
                            "NombreEstudiante": nombreParticipante,
                        }
                    )
                else:
                    return Response(
                        {
                            "msg": "No se encontró el estudiante o el estudiante no pertenece a al curso seleccionado."
                        }
                    )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # Obtener todos los horarios y serializarlos
        asistenciaPart = AsistenciaParticipante.objects.all()
        serializer = AsistenciaParticipanteSerializer(asistenciaPart, many=True)
        return Response(serializer.data)
