from django.shortcuts import render
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
                    tipoHorario=request.data.get('tipoHorario'),
                    hora_inicio=request.data.get('hora_inicio'),
                    hora_fin=request.data.get('hora_fin'),
               )
               horario.save()

               return Response({'msg': 'Se ha creado el horario'})
          except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppAsist_Api_CrearMateria(APIView):
     permission_classes = (permissions.IsAuthenticated,)
     def post(self, request, format = None):
          try: 
               serializer = MateriaSerializer(data = request.data)
               if(serializer.is_valid()):
                    dataMateria = request.data
                    docente = Docente.objects.get(id=dataMateria["docente"])
                    horario = Horario.objects.get(id=dataMateria["horario"])

                    materia = Materia(
                         nombre_materia = dataMateria["nombre_materia"],
                         docente = docente,
                         horario = horario
                    )
                    materia.save()

                    return Response({'msg': 'Se ha creado la materia'})
          except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
          
class AppAsist_API_CrearPeriodoAcadem(APIView):
     permission_classes = (permissions.IsAuthenticated,)
     def post(self, request, format =  None):
          try:
               serializer = PeriodoSerializer(data = request.data)
               if(serializer.is_valid()):
                    dataPeriodo = request.data

                    periodo = Periodo(
                         nombre_periodo = dataPeriodo["nombre_periodo"]
                    )
                    periodo.save()

                    return Response({'msg': 'Se ha creado la el periodo'})
          except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppAsist_API_CrearCurso(APIView):

     permission_classes = (permissions.IsAuthenticated,)
     def post(self, request, format = None):
          try:
               serializer = CursoSerializer(data = request.data)
               if(serializer.is_valid()):
                    dataCurso = request.data
                    materia = Materia.objects.get(id=dataCurso["materia"])
                    periodo = Periodo.objects.get(id=dataCurso["periodo"])

                    curso = Curso(
                         nombre_curso = dataCurso["nombre_curso"],
                         materia = materia,
                         periodo = periodo
                    )
                    curso.save()

                    return Response({'msg': 'Se ha creado la el curso'})
          except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
     
class AppAsist_API_CrearAsistenciaEst(APIView):
     permission_classes =(permissions.IsAuthenticated,)
     def post(self, request, format =  None):
          try:
               serializer = AsistenciaEstudianteSerializer(data = request.data)
               if(serializer.is_valid()):
                    dataAsisEstudiante = request.data
                    estudiante = Estudiante.objects.get(id=dataAsisEstudiante["estudiante"])
                    curso =  Curso.objects.get(id=dataAsisEstudiante["curso"])

               asistenciaEstudiante= AsistenciaEstudiante(
                    tipo_asistencia = dataAsisEstudiante["tipo_asistencia"],
                    descripcion = dataAsisEstudiante["descripcion"],
                    hora_llegada = dataAsisEstudiante["hora_llegada"],
                    soporte = dataAsisEstudiante["soporte"],
                    estudiante = estudiante,
                    curso = curso
               )
               asistenciaEstudiante.save()
               return Response({'msg': 'Se ha creado la asistencia'})
          except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppAsist_API_CrearAsistenciaEst(APIView):
     permission_classes =(permissions.IsAuthenticated,)
     def post(self, request, format =  None):
          try:
               serializer = AsistenciaEstudianteSerializer(data = request.data)
               if(serializer.is_valid()):
                    dataAsisEstudiante = request.data
                    estudiante = Estudiante.objects.get(id=dataAsisEstudiante["estudiante"])
                    curso =  Curso.objects.get(id=dataAsisEstudiante["curso"])

               asistenciaEstudiante= AsistenciaEstudiante(
                    tipo_asistencia = dataAsisEstudiante["tipo_asistencia"],
                    descripcion = dataAsisEstudiante["descripcion"],
                    hora_llegada = dataAsisEstudiante["hora_llegada"],
                    soporte = dataAsisEstudiante["soporte"],
                    estudiante = estudiante,
                    curso = curso
               )
               asistenciaEstudiante.save()
               return Response({'msg': 'Asistencia del estudiante creada'})
          except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AppAsist_API_CrearAsistenciaPart(APIView):
     permission_classes =(permissions.IsAuthenticated,)
     def post(self, request, format =  None):
          try:
               serializer = AsistenciaParticipanteSerializer(data = request.data)
               if(serializer.is_valid()):
                    dataAsisParticipante= request.data
                    participante = Participante.objects.get(id=dataAsisParticipante["participante"])
                    curso =  Curso.objects.get(id=dataAsisParticipante["curso"])

                    asistenciaParticipante= AsistenciaParticipante(
                         tipo_asistencia = dataAsisParticipante["tipo_asistencia"],
                         descripcion = dataAsisParticipante["descripcion"],
                         hora_llegada = dataAsisParticipante["hora_llegada"],
                         soporte = dataAsisParticipante["soporte"],
                         participante = participante,
                         curso = curso
                    )
                    asistenciaParticipante.save()
                    return Response({'msg': 'Asistencia del participante creada'})
          except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)