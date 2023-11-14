from django.contrib import admin
from AppAsistencia.models import Curso ,Horario, Materia, Periodo, ObservacionesEstudiante, ObservacionParticipantes, AsistenciaEstudiante, AsistenciaParticipante
# Register your models here.
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('tipoHorario', 'hora_inicio', 'hora_fin')
    search_fields = ('tipoHorario',)

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_materia', 'docente', 'horario')
    search_fields = ('nombre_materia', 'docente__usuario__username')  

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('nombre_periodo',)
    search_fields = ('nombre_periodo',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre_curso', 'materia', 'periodo', 'curso_created_at', 'curso_updated_at')
    list_filter = ('periodo', 'materia')
    search_fields = ('nombre_curso', 'materia__nombre_materia')


@admin.register(AsistenciaEstudiante)
class AsistenciaEstudianteAdmin(admin.ModelAdmin):
    list_display = ('tipo_asistencia', 'estudiante', 'curso', 'hora_llegada', 'asistenciaEst_created_at')
    list_filter = ('curso', 'tipo_asistencia')
    search_fields = ('estudiante__usuario__username', 'curso__nombre_curso')
    date_hierarchy = 'asistenciaEst_created_at'


@admin.register(AsistenciaParticipante)
class AsistenciaParticipanteAdmin(admin.ModelAdmin):
    list_display = ('tipo_asistencia', 'participante', 'curso', 'hora_llegada', 'asistenciaPart_created_at')
    list_filter = ('curso', 'tipo_asistencia')
    search_fields = ('participante__usuario__username', 'curso__nombre_curso')
    date_hierarchy = 'asistenciaPart_created_at'

@admin.register(ObservacionesEstudiante)
class ObservacionesEstudianteAdmin(admin.ModelAdmin):
    list_display = ('observacionEst', 'asistenciaEst', 'observacion_created_at', 'observacion_updated_at')
    search_fields = ('observacionEst', 'asistenciaEst__descripcion')  

@admin.register(ObservacionParticipantes)
class ObservacionParticipantesAdmin(admin.ModelAdmin):
    list_display = ('observacionPart', 'asistenciaPart', 'observacion_created_at', 'observacion_updated_at')
    search_fields = ('observacionPart', 'asistenciaPart__descripcion')