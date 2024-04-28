from django.urls import path,re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from AppReportes.views import *
from AppUsuarios.views import *

urlpatterns = [
   # Api para generar reporte de asistencia de estudiantes
   path("api/reporteEstudiante",AppApiReportesPorEstudiante.as_view(), name = "ReportePorEstudiante"),
   path("api/reporteEstudiantePDF",AppApiReportesPorEstudiantePDF.as_view(), name = "ReportePorEstudiantePDF"),
   path("api/reporteEstudianteXLSX",AppApiReportesPorEstudianteXLSX.as_view(), name = "ReportePorEstudianteXLSX"),
   path("api/reportePorDiario", AppApiReporteDiario.as_view(), name = "ReporteDiario"),
   path("api/reportePorDiarioPDF", AppApiReporteDiarioPDF.as_view(), name = "ReporteDiarioPDF"),
   path("api/reportePorDiarioXLSX", AppApiReporteDiarioXLSX.as_view(), name = "ReporteDiarioXLSX"),
   path("api/reportePorCurso", AppApiReportePorCurso.as_view(), name = "ReportePorCurso"),
   path("api/reportePorCursoPDF", AppApiReportePorCursoPDF.as_view(), name = "ReportePorCursoPDF"),
   path("api/reportePorCursoXLSX", AppApiReportePorCursoXLSX.as_view(), name = "ReportePorCursoXLSX"),
   path('notify/notifications/', NotificationListAPIView.as_view(), name='notification-list'),
   path('notify/notifications/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification-detail'),



]