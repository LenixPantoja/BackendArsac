from django.urls import path
from .views import *
urlpatterns = [
    # Crea un token 
    path('api/crearHorario/', AppAsist_API_CrearHorario.as_view(), name = 'createSchedule'),
    path('api/crearMateria/', AppAsist_Api_CrearMateria.as_view(), name = 'crearMateria'),
    path('api/crearPeriodo/', AppAsist_API_CrearPeriodoAcadem.as_view(), name='crearPeriodo'),
    path('api/crearCurso/', AppAsist_API_CrearCurso.as_view(), name='crearCurso'),
    path('api/crearAsistenciaEst/', AppAsist_API_CrearAsistenciaEst.as_view(), name= "crearAsistenciaEst"),
    path('api/crearAsistenciaPart/', AppAsist_API_CrearAsistenciaPart.as_view(), name = "crearAsistenciaPart")
]