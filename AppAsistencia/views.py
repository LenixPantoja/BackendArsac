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
        asistencia_data = []
        for data_dict in serializer.data:
            asistencia_info = {f"{key}": value for key, value in data_dict.items()}
            matricula = Matricula.objects.get( id = asistencia_info['matricula_estudiante'])
            print(matricula.curso.materia.nombre_materia)
            asistencia_data.append({
                'id': asistencia_info['id'],
                'Tipo_asistencia':asistencia_info['tipo_asistencia'],
                'Descripcion_asistencia': asistencia_info['descripcion'],
                'Hora_llegada': asistencia_info['hora_llegada'],
                'Soporte_imagen': asistencia_info['soporte'],
                'Estudiante': matricula.estudiante.user.first_name + " " + matricula.estudiante.user.last_name,
                'Curso': matricula.curso.nombre_curso,
                'Materia': matricula.curso.materia.nombre_materia
            })
        return Response(asistencia_data)
    
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
        lista_observaciones = []
        observacionesEstudiante = ObservacionesEstudiante.objects.all()
        serializer =  ObservacionesEstSerializer(observacionesEstudiante, many =  True)
        data_observaciones = request.data
        id_asistencia =  data_observaciones.get("asistenciaEst")
        query_Set_Asistencia = AsistenciaEstudiante.objects.filter(id = id_asistencia)

        for data_dict in serializer.data:
            observacion_info = {f"{key}": value for key, value in data_dict.items()}
            for data_Asistencia in query_Set_Asistencia:
                pass
            lista_observaciones.append({
                "id": observacion_info["id"],
                "id_asistencia": id_asistencia,
                "Descripcion": observacion_info["observacionEst"],
                "Curso": data_Asistencia.matricula_estudiante.curso.nombre_curso,
                "Periodo": data_Asistencia.matricula_estudiante.curso.periodo.nombre_periodo,
                "Estudiante": data_Asistencia.matricula_estudiante.estudiante.user.first_name + " " + data_Asistencia.matricula_estudiante.estudiante.user.last_name,
                "Materia": data_Asistencia.matricula_estudiante.curso.materia.nombre_materia,
                "Docente": data_Asistencia.matricula_estudiante.curso.materia.docente.user.first_name + " " + data_Asistencia.matricula_estudiante.curso.materia.docente.user.last_name
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
