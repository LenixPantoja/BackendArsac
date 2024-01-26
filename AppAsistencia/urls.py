from django.urls import path
from .views import *
urlpatterns = [
    # Crea un token 
    path('api/crearHorario/', AppAsist_API_CrearHorario.as_view(), name = 'createSchedule'),
    path('api/crearMateria/', AppAsist_Api_CrearMateria.as_view(), name = 'crearMateria'),
    path('api/crearPeriodo/', AppAsist_API_CrearPeriodoAcadem.as_view(), name='crearPeriodo'),
    path('api/crearCurso/', AppAsist_API_CrearCurso.as_view(), name='crearCurso'),
    path('api/AsistenciaEstudiante/', AppAsist_API_AsistenciaEst.as_view(), name= "crearAsistenciaEst"),
    path('api/AsistenciaParticipante/', AppAsist_API_AsistenciaPart.as_view(), name = "AsistenciaParticipante")
]