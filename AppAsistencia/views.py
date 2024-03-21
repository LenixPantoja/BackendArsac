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
        # Obtener todos los horarios y serializarlos
        try:
            pUserDocente = request.query_params.get("pDocente", None)
            # Parametro de consulta @pUserDocente es el usuario decente
            if pUserDocente is not None:
                cursos = Curso.objects.all()
                serializer = CursoSerializer(cursos, many=True)
                
                curso_data = []
                for miCurso in serializer.data:
                    curso_info = {f"{key}": value for key, value in miCurso.items()}
                    id_materia = curso_info['materia']
                    id_perido = curso_info['periodo']
                    materia = Materia.objects.filter(id=id_materia)
                    periodo = Periodo.objects.filter(id=id_perido)

                    for miMateria in materia:
                        print('')
                    
                    for miPeriodo in periodo:
                        print('')  
                    hora_inicio = miMateria.horario.hora_inicio
                    hora_inicio_format = hora_inicio.strftime("%I:%M:%S %p")
                    hora_fin = miMateria.horario.hora_fin
                    hora_fin_format = hora_fin.strftime("%I:%M:%S %p")

                    user_docente = miMateria.docente.user.username
                    if pUserDocente == user_docente:
                        curso_data.append({
                            'id': curso_info['id'],
                            'nombre_curso': curso_info['nombre_curso'],
                            'materia':miMateria.nombre_materia,
                            'Hora_Inicio_Clase':hora_inicio_format,
                            'Hora_Fin_Clase':hora_fin_format,
                            'tipo_horario': miMateria.horario.tipoHorario,
                            'periodo': miPeriodo.nombre_periodo,
                            'Docente': miMateria.docente.user.first_name
                        })
                return Response(curso_data)
            else:
                return Response(
                    {"error": "El parámetro p es necesario."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": "Hubo un problema al obtener los cursos y las materias"},
                status=status.HTTP_204_NO_CONTENT,
            )

class AppAsist_API_AsistenciaEst(APIView):
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
                QuerySetCurso1 = Curso.objects.filter(id=CursoEstudinte)
                nombreCurso1 = ""
                # Obtenemos el nombre del curso del estudiante que esta en la lista
                for i in QuerySetCurso1:
                    nombreCurso1 = i
                
                idCurso = request.data.get("curso")
                QuerySetCurso2 = Curso.objects.filter(id= idCurso)
                nombreCurso2= ""
                for j in QuerySetCurso2:
                    nombreCurso2 = j
                
                print(existing_estudiante.estudiante_numero_Id)
                print(type(nombreCurso1))
                print(type(nombreCurso2))
                # Verifica si el estudiante fue encontrado y si esta en el curso correcto.
                if existing_estudiante and str(nombreCurso1) == str(nombreCurso2):
                #if existing_estudiante and CursoEstudinte == request.data.get("curso"):
                
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
                            "NombreEstudiante": estudiante.user.first_name + " " + estudiante.user.last_name
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
            querySetEstudiante = Estudiante.objects.filter(id = asistencia_info['estudiante'])
            for miEstudiante in querySetEstudiante:
                pass
            curso = Curso.objects.get( id = asistencia_info['curso'])
            print(curso.materia.nombre_materia)
            asistencia_data.append({
                'id': asistencia_info['id'],
                'Tipo_asistencia':asistencia_info['tipo_asistencia'],
                'Descripcion_asistencia': asistencia_info['descripcion'],
                'Hora_llegada': asistencia_info['hora_llegada'],
                'Soporte_imagen': asistencia_info['soporte'],
                'Estudiante': miEstudiante.user.first_name + " " + miEstudiante.user.last_name,
                'Curso': curso.nombre_curso,
                'Materia': curso.materia.nombre_materia
            })
        return Response(asistencia_data)


class AppAsist_API_AsistenciaPart(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = AsistenciaParticipanteSerializer(data=request.data)
            if serializer.is_valid():
                #Solicita el numero de documento como parametro de consulta.
                pNumeroDocumento = request.query_params.get("pNumeroDocumento", None)
                # Parametro de consulta
                if pNumeroDocumento is None:
                    return Response(
                        {"error": "El parámetro pNumeroDocumento es necesario."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Verifica si el estudiante exite en la base de datos.
                existing_participante = Participante.objects.filter(
                    participante_numero_Id=pNumeroDocumento
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

                    asistenciaParticipante = AsistenciaParticipante(
                        tipo_asistencia=dataParticipante["tipo_asistencia"],
                        descripcion=dataParticipante["descripcion"],
                        hora_llegada=dataParticipante["hora_llegada"],
                        soporte=dataParticipante["soporte"],
                        participante=participante,
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # Obtener todas las asistencias y serializarlos
        asistenciaPart = AsistenciaParticipante.objects.all()
        serializer = AsistenciaParticipanteSerializer(asistenciaPart, many=True)
        asistencia_data = []
        for data_dict in serializer.data:
            asistencia_info = {f"{key}": value for key, value in data_dict.items()}
            querySetParticipante = Participante.objects.filter(id = asistencia_info['participante'])
            for miParticipante in querySetParticipante:
                pass
            curso = Curso.objects.get( id = asistencia_info['curso'])
            print(curso.materia.nombre_materia)
            asistencia_data.append({
                'id': asistencia_info['id'],
                'Tipo_asistencia':asistencia_info['tipo_asistencia'],
                'Descripcion_asistencia': asistencia_info['descripcion'],
                'Hora_llegada': asistencia_info['hora_llegada'],
                'Soporte_imagen': asistencia_info['soporte'],
                'Participante': miParticipante.user.first_name + " " + miParticipante.user.last_name,
                'Curso': curso.nombre_curso,
                'Materia': curso.materia.nombre_materia
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
                nombre_estudiante = id_asistencia_estudiante.estudiante.user.first_name + " " + id_asistencia_estudiante.estudiante.user.last_name
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
        observacionesEstudiante = ObservacionesEstudiante.objects.all()
        serializer =  ObservacionesEstSerializer(observacionesEstudiante, many =  True)

        return Response(serializer.data)
    
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
                nombre_estudiante = id_asistencia_estudiante.estudiante.user.first_name + " " + id_asistencia_estudiante.estudiante.user.last_name
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
                "Curso": data_Asistencia.curso.nombre_curso,
                "Periodo": data_Asistencia.curso.periodo.nombre_periodo,
                "Estudiante": data_Asistencia.estudiante.user.first_name + " " + data_Asistencia.estudiante.user.last_name,
                "Materia": data_Asistencia.curso.materia.nombre_materia,
                "Docente": data_Asistencia.curso.materia.docente.user.first_name + " " + data_Asistencia.curso.materia.docente.user.last_name
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

class AppAsist_API_ObservacionesParticipante(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        try:
            serializer = ObservacionesPartSerializer(data=request.data)
            if serializer.is_valid():
                data_observaciones = request.data
                # Obtener la instancia de AsistenciaParticipante utilizando el ID proporcionado
                asistencia_participante = data_observaciones.get("asistenciaPart")
                # Guardamos el ID de la asistencia
                id_asistencia_participante = AsistenciaParticipante.objects.get(pk=asistencia_participante)
                # Guardamos en la variable el nombre del participante
                nombre_participante = id_asistencia_participante.participante.user.first_name + " " + id_asistencia_participante.participante.user.last_name
                # Creamos un objeto de tipo ObservacionEstudiante
                obervacion_participante = ObservacionParticipantes(
                    asistenciaPart = id_asistencia_participante,
                    observacionPart = data_observaciones["observacionPart"]
                )
                obervacion_participante.save()
                return Response(
                        {
                            "msg": f"Se creo la observación del participante: {nombre_participante}"
                        }
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        lista_observaciones = []
        observacionesParticipante = ObservacionParticipantes.objects.all()
        serializer =  ObservacionesPartSerializer(observacionesParticipante, many=True)
        data_observaciones = request.data
        id_asistencia =  data_observaciones.get("asistenciaPart")
        query_Set_Asistencia = AsistenciaParticipante.objects.filter(id = id_asistencia)

        for data_dict in serializer.data:
            observacion_info = {f"{key}": value for key, value in data_dict.items()}
            for data_Asistencia in query_Set_Asistencia:
                pass
            lista_observaciones.append({
                "id": observacion_info["id"],
                "id_asistencia": id_asistencia,
                "Descripcion": observacion_info["observacionPart"],
                "Curso": data_Asistencia.curso.nombre_curso,
                "Periodo": data_Asistencia.curso.periodo.nombre_periodo,
                "Participante": data_Asistencia.participante.user.first_name + " " + 
                                data_Asistencia.participante.user.last_name,
                "Materia": data_Asistencia.curso.materia.nombre_materia,
                "Docente": data_Asistencia.curso.materia.docente.user.first_name + " " + 
                           data_Asistencia.curso.materia.docente.user.last_name
                })
        return Response(lista_observaciones)
    
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
