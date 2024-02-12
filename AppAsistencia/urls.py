from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Crea un token 
    path('api/crearHorario/', AppAsist_API_CrearHorario.as_view(), name = 'createSchedule'),
    path('api/crearMateria/', AppAsist_Api_CrearMateria.as_view(), name = 'crearMateria'),
    path('api/crearPeriodo/', AppAsist_API_CrearPeriodoAcadem.as_view(), name='crearPeriodo'),
    path('api/crearCurso/', AppAsist_API_Curso.as_view(), name='crearCurso'),
    path('api/AsistenciaEstudiante/', AppAsist_API_AsistenciaEst.as_view(), name= "AsistenciaEstudiante"),
    path('api/AsistenciaParticipante/', AppAsist_API_AsistenciaPart.as_view(), name = "AsistenciaParticipante"),
    path('api/ObservacionesEstudiante/', AppAsist_API_ObservacionesEstudiante.as_view(), name = "ObservacionEstudiante")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)