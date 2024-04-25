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
from datetime import datetime

from AppAsistencia.models import *
from AppUsuarios.models import *
from AppAsistencia.serializers import *

# Create your views here.

class AppApiReportesPorEstudiante(APIView):
    def get(self, request, format=None):
        asistencia =  AsistenciaEstudiante.objects.all()
        observaciones = ObservacionesEstudiante.objects.all()
        serializer = AsistenciaEstudianteSerializer(asistencia, many=True)
        #Parametros para obtener el reporte filtrado.
        pNumeroDocumento = request.query_params.get("pNumeroDocumento", None)
        pMateria =  int(request.query_params.get("pMateria", None))
        pCurso = int(request.query_params.get("pCurso", None))
        pRango1 = request.query_params.get("pRango1", None)
        pRango2 = request.query_params.get("pRango2", None)
        

        dataReporte = []
        # Parametro de consulta
        if pNumeroDocumento is None or pMateria is None or pRango1 is None or pRango2 is None or pCurso is None:
            return Response(
                {"error": "Parametros incompletos(pNumeroDocumento, pMateria, pRango1, pRango2)"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Recorridos
        for dataAsistencia in serializer.data:
            matricula = Matricula.objects.get(id=dataAsistencia["matricula_estudiante"])
            estudiante = Estudiante.objects.get(id=matricula.estudiante.id)
            cedulaEst =  estudiante.estudiante_numero_Id
            curso = Curso.objects.get(id=matricula.curso_Materia.curso.id)
            idCurso = curso.id
            idMateria = matricula.curso_Materia.materia.id
            periodo = Periodo.objects.get(id=matricula.curso_Materia.materia.periodo.id)
            fecha_objeto = datetime.strptime(dataAsistencia["asistenciaEst_created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
            fecha_formateada = fecha_objeto.strftime('%Y-%m-%d')
            print(idCurso, idMateria)
            if (fecha_formateada >= pRango1 and 
                fecha_formateada <= pRango2 and 
                pNumeroDocumento == cedulaEst and 
                pMateria == idMateria and 
                idCurso == pCurso):
                observaciones = ObservacionesEstudiante.objects.all()
                lista_observaciones = []
                contador = 0
                for observ in observaciones:
                    if observ.asistenciaEst.id == dataAsistencia["id"]:
                        contador=contador + 1
                        lista_observaciones.append(f"Observación {contador}:{observ.observacionEst}")
                #Formateo de fechas
                hora_inicio = matricula.curso_Materia.materia.horario.hora_inicio
                hora_inicio_format = hora_inicio.strftime("%I:%M:%S %p")
                hora_fin = matricula.curso_Materia.materia.horario.hora_fin
                hora_fin_format = hora_fin.strftime("%I:%M:%S %p")
                print()
                dataReporte.append({
                    "id": dataAsistencia["id"],
                    "Tipo_asistencia": dataAsistencia["tipo_asistencia"],
                    "Descripcion": dataAsistencia["descripcion"],
                    "Hora_llegada": dataAsistencia["hora_llegada"],
                    "FechaCreacion": dataAsistencia["asistenciaEst_created_at"],
                    "Nombre_estudiante":estudiante.user.first_name + " " + estudiante.user.last_name,
                    "Curso_matriculado": curso.nombre_curso,
                    "Periodo": periodo.nombre_periodo,
                    "Materia": matricula.curso_Materia.materia.nombre_materia,
                    "Horario": f"{hora_inicio_format} a {hora_fin_format}",
                    "Docente": matricula.curso_Materia.materia.docente.user.first_name + " " + matricula.curso_Materia.materia.docente.user.last_name,
                    "Lista_Observaciones": lista_observaciones
                })
        return Response(dataReporte)
    
class AppApiReporteDiario(APIView):
    def get(self, request, format = None):
        asistencia =  AsistenciaEstudiante.objects.all()
        observaciones = ObservacionesEstudiante.objects.all()
        serializer = AsistenciaEstudianteSerializer(asistencia, many=True)
        pRango1 = request.query_params.get("pRango1", None)
        pRango2 = request.query_params.get("pRango2", None)
        dataReporte = []

        if pRango1 is None or pRango2 is None:
            return Response(
                {"error": "Parametros incompletos(pRango1, pRango2)"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        for dataAsistencia in serializer.data:
            
            matricula = Matricula.objects.get(id=dataAsistencia["matricula_estudiante"])
            estudiante = Estudiante.objects.get(id=matricula.estudiante.id)
            cedulaEst =  estudiante.estudiante_numero_Id
            curso = Curso.objects.get(id=matricula.curso_Materia.curso.id)
            periodo = Periodo.objects.get(id=matricula.curso_Materia.materia.periodo.id)
            fecha_objeto = datetime.strptime(dataAsistencia["asistenciaEst_created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
            observaciones = ObservacionesEstudiante.objects.all()
            fecha_formateada = fecha_objeto.strftime('%Y-%m-%d')
            if (fecha_formateada >= pRango1 and 
                fecha_formateada <= pRango2 ):

                cant_observaciones = len(observaciones)
                
                lista_observaciones = []
                contador = 0
                for observ in observaciones:
                    print("jaasdfasd")
                    
                    if observ.asistenciaEst.id == dataAsistencia["id"]:
                        print("paso chavalito")
                        contador=contador + 1
                        lista_observaciones.append(f"Observación {contador}:{observ.observacionEst}")
                    #Formateo de fechas
                        hora_inicio = matricula.curso_Materia.materia.horario.hora_inicio
                        hora_inicio_format = hora_inicio.strftime("%I:%M:%S %p")
                        hora_fin = matricula.curso_Materia.materia.horario.hora_fin
                        hora_fin_format = hora_fin.strftime("%I:%M:%S %p")
                        print()
                        dataReporte.append({
                            "id": dataAsistencia["id"],
                            "Tipo_asistencia": dataAsistencia["tipo_asistencia"],
                            "Descripcion": dataAsistencia["descripcion"],
                            "Hora_llegada": dataAsistencia["hora_llegada"],
                            "FechaCreacion": dataAsistencia["asistenciaEst_created_at"],
                            "Nombre_estudiante":estudiante.user.first_name + " " + estudiante.user.last_name,
                            "Cc_estudiante":cedulaEst,
                            "Curso_matriculado": curso.nombre_curso,
                            "Periodo": periodo.nombre_periodo,
                            "Materia": matricula.curso_Materia.materia.nombre_materia,
                            "Horario": f"{hora_inicio_format} a {hora_fin_format}",
                            "Docente": matricula.curso_Materia.materia.docente.user.first_name + " " + matricula.curso_Materia.materia.docente.user.last_name,
                            "Lista_Observaciones": lista_observaciones
                    })
        return Response(dataReporte)
    
class AppApiReportePorCurso(APIView):
    def get(self, request, format=None):
        asistencia =  AsistenciaEstudiante.objects.all()
        observaciones = ObservacionesEstudiante.objects.all()
        serializer = AsistenciaEstudianteSerializer(asistencia, many=True)
        #Parametros para obtener el reporte filtrado.
        pMateria =  int(request.query_params.get("pMateria", None))
        pCurso = int(request.query_params.get("pCurso", None))
        pRango1 = request.query_params.get("pRango1", None)
        pRango2 = request.query_params.get("pRango2", None)
        

        dataReporte = []
        # Parametro de consulta
        if pMateria is None or pRango1 is None or pRango2 is None or pCurso is None:
            return Response(
                {"error": "Parametros incompletos(pCurso, pMateria, pRango1, pRango2)"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Recorridos
        for dataAsistencia in serializer.data:
            print(dataAsistencia)
            matricula = Matricula.objects.get(id=dataAsistencia["matricula_estudiante"])
            estudiante = Estudiante.objects.get(id=matricula.estudiante.id)
            cedulaEst =  estudiante.estudiante_numero_Id
            curso = Curso.objects.get(id=matricula.curso_Materia.curso.id)
            idCurso = curso.id
            idMateria = matricula.curso_Materia.materia.id
            periodo = Periodo.objects.get(id=matricula.curso_Materia.materia.periodo.id)
            fecha_objeto = datetime.strptime(dataAsistencia["asistenciaEst_created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
            fecha_formateada = fecha_objeto.strftime('%Y-%m-%d')

            if (fecha_formateada >= pRango1 and 
                fecha_formateada <= pRango2 and
                pMateria == idMateria and 
                idCurso == pCurso):
                print("pasa por aqui chaval")
                observaciones = ObservacionesEstudiante.objects.all()
                lista_observaciones = []
                contador = 0
                for observ in observaciones:
                    if observ.asistenciaEst.id == dataAsistencia["id"]:
                        contador=contador + 1
                        lista_observaciones.append(f"Observación {contador}:{observ.observacionEst}")
                #Formateo de fechas
                hora_inicio = matricula.curso_Materia.materia.horario.hora_inicio
                hora_inicio_format = hora_inicio.strftime("%I:%M:%S %p")
                hora_fin = matricula.curso_Materia.materia.horario.hora_fin
                hora_fin_format = hora_fin.strftime("%I:%M:%S %p")
                print()
                dataReporte.append({
                    "id": dataAsistencia["id"],
                    "Tipo_asistencia": dataAsistencia["tipo_asistencia"],
                    "Descripcion": dataAsistencia["descripcion"],
                    "Hora_llegada": dataAsistencia["hora_llegada"],
                    "FechaCreacion": dataAsistencia["asistenciaEst_created_at"],
                    "Nombre_estudiante":estudiante.user.first_name + " " + estudiante.user.last_name,
                    "Cc_estudiante": cedulaEst,
                    "Curso_matriculado": curso.nombre_curso,
                    "Periodo": periodo.nombre_periodo,
                    "Materia": matricula.curso_Materia.materia.nombre_materia,
                    "Horario": f"{hora_inicio_format} a {hora_fin_format}",
                    "Docente": matricula.curso_Materia.materia.docente.user.first_name + " " + matricula.curso_Materia.materia.docente.user.last_name,
                    "Lista_Observaciones": lista_observaciones
                })
        return Response(dataReporte)


