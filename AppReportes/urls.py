from django.urls import path,re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from AppReportes.views import *

urlpatterns = [
   # Api para generar reporte de asistencia de estudiantes
   path("api/reporteEstudiante",AppApiReportesPorEstudiante.as_view(), name = "ReportePorEstudiante"),
   path("api/reportePorDiarioPDF", AppApiReporteDiarioPDF.as_view(), name = "ReporteDiarioPDF"),
   path("api/reportePorDiarioXLSX", AppApiReporteDiarioXLSX.as_view(), name = "ReporteDiarioXLSX"),
   path("api/reportePorCurso", AppApiReportePorCurso.as_view(), name = "ReportePorCurso")
]