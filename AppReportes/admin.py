from django.contrib import admin
from AppReportes.models import Notification
# Register your models here.

@admin.register(Notification)
class NotificacionAdmin(admin.ModelAdmin):
    list_filter = ('message', 'created_at', 'updated_at',)
    list_display = ('message', 'created_at', 'updated_at',)
    search_fields = ('message', 'created_at', 'updated_at',)
    ordering = ('message',)