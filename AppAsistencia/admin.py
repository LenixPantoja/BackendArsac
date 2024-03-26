from django.contrib import admin
from AppAsistencia.models import Curso ,Horario, Materia, Matricula, Periodo, ObservacionesEstudiante, AsistenciaEstudiante
# Register your models here.
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_filter = ('tipoHorario', 'hora_inicio', 'hora_fin',)
    list_display = ('tipoHorario', 'hora_inicio', 'hora_fin',)
    search_fields = ('tipoHorario', 'hora_inicio', 'hora_fin',)
    ordering = ('tipoHorario',)
    
@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_filter = ('nombre_materia', 'docente', 'horario',)
    list_display = ('nombre_materia', 'docente', 'horario',)
    search_fields = ('nombre_materia', 'docente__usuario__username',) 
    ordering = ('nombre_materia',) 

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_filter = ('nombre_periodo',)
    list_display = ('nombre_periodo',)
    search_fields = ('nombre_periodo',)
    ordering = ('nombre_periodo',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre_curso', 'materia', 'periodo', 'curso_created_at', 'curso_updated_at')
    list_filter = ('periodo', 'materia')
    search_fields = ('nombre_curso', 'materia__nombre_materia')


@admin.register(AsistenciaEstudiante)
class AsistenciaEstudianteAdmin(admin.ModelAdmin):
    list_display = ('tipo_asistencia', 'matricula_estudiante', 'hora_llegada', 'asistenciaEst_created_at')
    list_filter = ('matricula_estudiante', 'tipo_asistencia')
    search_fields = ('estudiante__usuario__username', 'matricula_estudiante')
    date_hierarchy = 'asistenciaEst_created_at'

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso')
    search_fields = ('estudiante__nombre', 'curso__nombre_curso')
    list_filter = ('curso',)

@admin.register(ObservacionesEstudiante)
class ObservacionesEstudianteAdmin(admin.ModelAdmin):
    list_display = ('observacionEst', 'asistenciaEst', 'observacion_created_at', 'observacion_updated_at')
    search_fields = ('observacionEst', 'asistenciaEst__descripcion')  