from django.contrib import admin
from AppUsuarios.models import Docente, Estudiante, Participante, Profesion
# Register your models here.

@admin.register(Profesion)
class ProfesionAdmin(admin.ModelAdmin):
    list_display = ('nombre_Profesion', 'profesion_created_at', 'profesion_updated_at')
    search_fields = ('nombre_Profesion',)

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'docente_profesion', 'docente_tipo_Id', 'docente_estado', 'docente_numero_Id', 'docente_fecha_nacim', 'docente_created_at', 'docente_updated_at')
    list_filter = ('docente_estado', 'docente_profesion')
    search_fields = ('user__username', 'user__email', 'docente_numero_Id')

    def save_model(self, request, obj, form ,change):
        if not obj.user_id:
            obj.user_id = request.user.id
        obj.save()

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('user', 'estudiante_fecha_matricula', 'estudiante_estado', 'estudiante_tipo_Id', 'estudiante_numero_Id', 'estudiante_fecha_nac', 'estudiante_created_at', 'estudiante_updated_at')
    list_filter = ('estudiante_estado',)
    search_fields = ('user__username', 'user__email', 'estudiante_numero_Id')


    def save_model(self, request, obj, form ,change):
        if not obj.user_id:
            obj.user_id = request.user.id
        obj.save()

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('user', 'participante_estado', 'participante_tipo_Id', 'participante_numero_Id', 'participante_created_at', 'participante_updated_at')
    list_filter = ('participante_estado',)
    search_fields = ('user__username', 'user__email', 'participante_numero_Id')

    def save_model(self, request, obj, form ,change):
        if not obj.user_id:
            obj.user_id = request.user.id
        obj.save()