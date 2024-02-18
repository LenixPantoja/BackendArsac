from django.urls import path,re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="ARSAC API",
      default_version='v1',
      description="Welcome to API documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="aldair.pantoja.velasquez@gmail.com"),
      license=openapi.License(name="Licenced to INTES"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Crea un token 
    path('api/crearHorario/', AppAsist_API_CrearHorario.as_view(), name = 'createSchedule'),
    path('api/crearMateria/', AppAsist_Api_CrearMateria.as_view(), name = 'crearMateria'),
    path('api/crearPeriodo/', AppAsist_API_CrearPeriodoAcadem.as_view(), name='crearPeriodo'),
    path('api/crearCurso/', AppAsist_API_Curso.as_view(), name='crearCurso'),
    path('api/AsistenciaEstudiante/', AppAsist_API_AsistenciaEst.as_view(), name= "AsistenciaEstudiante"),
    path('api/AsistenciaParticipante/', AppAsist_API_AsistenciaPart.as_view(), name = "AsistenciaParticipante"),
    path('api/ObservacionesEstudiante/', AppAsist_API_ObservacionesEstudiante.as_view(), name = "ObservacionEstudiante"),
    path('api/ObservacionesParticipante/', AppAsist_API_ObservacionesParticipante.as_view(), name = "ObservacionParticipante"),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)